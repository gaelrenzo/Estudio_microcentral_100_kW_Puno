"""Rutinas hidráulicas preliminares para revisar datos de campo de la MCH.

No convierte cotas de terreno en niveles de agua ni reemplaza el cálculo firmado.
La distancia entre dos extremos es solo la cuerda; la longitud de tubería se
obtiene sumando puntos ordenados sobre el eje levantado.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from io import StringIO

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


class EvaluadorHidraulicoMCH:
    def __init__(
        self,
        densidad_kg_m3: float = 1000.0,
        gravedad_m_s2: float = 9.80665,
        viscosidad_cinematica_m2_s: float = 1.004e-6,
    ) -> None:
        """Los valores predeterminados del agua son aproximados (~20 °C)."""
        self.rho = densidad_kg_m3
        self.g = gravedad_m_s2
        self.nu = viscosidad_cinematica_m2_s

    @staticmethod
    def _positivo(nombre: str, valor: float, permitir_cero: bool = False) -> None:
        if not np.isfinite(valor) or valor < 0 or (not permitir_cero and valor == 0):
            raise ValueError(f"{nombre} debe ser finito y {'no negativo' if permitir_cero else 'positivo'}.")

    @staticmethod
    def calcular_geometria_3d(
        este1: float,
        norte1: float,
        cota1: float,
        este2: float,
        norte2: float,
        cota2: float,
    ) -> dict[str, float]:
        """Devuelve la distancia entre extremos; no es la longitud desarrollada."""
        vals = np.asarray([este1, norte1, cota1, este2, norte2, cota2], dtype=float)
        if not np.isfinite(vals).all():
            raise ValueError("Las coordenadas y cotas deben ser finitas y usar unidades compatibles.")
        dx, dy, dz = este2 - este1, norte2 - norte1, cota2 - cota1
        planar = float(np.hypot(dx, dy))
        if planar == 0:
            raise ValueError("La distancia planar debe ser positiva para calcular la pendiente.")
        return {
            "dist_planar_m": planar,
            "desnivel_firmado_m": float(dz),
            "cuerda_3d_minima_m": float(np.sqrt(dx * dx + dy * dy + dz * dz)),
            "pendiente_firmada_pct": float(100 * dz / planar),
        }

    @staticmethod
    def longitud_trazado_3d(puntos: pd.DataFrame) -> float:
        """Suma la polilínea del eje; requiere progresivas crecientes y cota del eje."""
        columnas = {"Progresiva_m", "Este_m", "Norte_m", "Cota_m"}
        faltantes = columnas - set(puntos.columns)
        if faltantes:
            raise ValueError(f"Faltan columnas del eje: {', '.join(sorted(faltantes))}")
        p = puntos.sort_values("Progresiva_m")
        xyz = p[["Este_m", "Norte_m", "Cota_m"]].to_numpy(dtype=float)
        prog = p["Progresiva_m"].to_numpy(dtype=float)
        if len(xyz) < 2 or not np.isfinite(xyz).all() or not np.isfinite(prog).all():
            raise ValueError("Se requieren al menos dos puntos finitos del eje.")
        if np.any(np.diff(prog) <= 0):
            raise ValueError("Las progresivas deben ser estrictamente crecientes y únicas.")
        return float(np.linalg.norm(np.diff(xyz, axis=0), axis=1).sum())

    def calcular_perdidas_darcy(
        self,
        Q_m3_s: float,
        D_interior_m: float,
        L_eje_m: float,
        rugosidad_absoluta_m: float,
        K_total: float,
    ) -> dict[str, float | str]:
        """Darcy-Weisbach; K_total debe ser la suma documentada de pérdidas locales."""
        for n, v in (
            ("Q", Q_m3_s),
            ("D interior", D_interior_m),
            ("L de eje", L_eje_m),
            ("viscosidad cinemática", self.nu),
            ("densidad", self.rho),
            ("gravedad", self.g),
        ):
            self._positivo(n, v)
        self._positivo("rugosidad", rugosidad_absoluta_m, permitir_cero=True)
        self._positivo("K_total", K_total, permitir_cero=True)

        area = np.pi * D_interior_m**2 / 4
        velocidad = Q_m3_s / area
        reynolds = velocidad * D_interior_m / self.nu
        rel_rugosidad = rugosidad_absoluta_m / D_interior_m
        if reynolds < 2300:
            factor = 64 / reynolds
            metodo = "laminar"
        elif reynolds > 5000:
            if rel_rugosidad >= 0.05:
                raise ValueError("Rugosidad relativa fuera del rango de Swamee-Jain; revisar método.")
            factor = 0.25 / np.log10(rel_rugosidad / 3.7 + 5.74 / reynolds**0.9) ** 2
            metodo = "Swamee-Jain"
        else:
            raise ValueError("Régimen transicional (2300≤Re≤5000): no adoptar factor automático.")

        carga_velocidad = velocidad**2 / (2 * self.g)
        hf = factor * (L_eje_m / D_interior_m) * carga_velocidad
        hk = K_total * carga_velocidad
        return {
            "velocidad_m_s": float(velocidad),
            "reynolds": float(reynolds),
            "factor_darcy": float(factor),
            "metodo_factor": metodo,
            "hf_m": float(hf),
            "hk_m": float(hk),
            "h_perdidas_m": float(hf + hk),
        }

    def calcular_potencia(
        self,
        Q_disponible_m3_s: float,
        nivel_aguas_arriba_m: float,
        nivel_aguas_abajo_m: float,
        h_perdidas_m: float,
        eta_turbina: float,
        eta_generador: float,
        eta_transformador: float = 1.0,
    ) -> dict[str, float]:
        """Usa niveles de agua compatibles y eficiencias declaradas para el punto de cálculo."""
        self._positivo("Q disponible", Q_disponible_m3_s)
        self._positivo("pérdidas", h_perdidas_m, permitir_cero=True)
        etas = (eta_turbina, eta_generador, eta_transformador)
        if any(not np.isfinite(e) or not 0 < e <= 1 for e in etas):
            raise ValueError("Cada eficiencia debe estar en el intervalo (0, 1].")
        h_bruto = nivel_aguas_arriba_m - nivel_aguas_abajo_m
        if not np.isfinite(h_bruto) or h_bruto <= 0:
            raise ValueError("El nivel aguas arriba debe superar al nivel aguas abajo.")
        h_neto = h_bruto - h_perdidas_m
        if h_neto <= 0:
            raise ValueError("Las pérdidas igualan o superan el salto bruto.")
        eta = eta_turbina * eta_generador * eta_transformador
        p_kw = self.rho * self.g * Q_disponible_m3_s * h_neto * eta / 1000
        return {
            "salto_bruto_m": float(h_bruto),
            "salto_neto_m": float(h_neto),
            "eta_global": float(eta),
            "potencia_electrica_kw": float(p_kw),
        }

    @staticmethod
    def calcular_aforo(subsecciones: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
        """Integra Q=Σ(Aᵢvᵢ); Aᵢ y vᵢ deben representar cada subsección medida."""
        req = {"area_parcial_m2", "velocidad_media_m_s"}
        faltantes = req - set(subsecciones.columns)
        if faltantes:
            raise ValueError(f"Faltan columnas: {', '.join(sorted(faltantes))}")
        df = subsecciones.copy()
        vals = df[list(req)].to_numpy(dtype=float)
        if not np.isfinite(vals).all() or (df["area_parcial_m2"] <= 0).any() or (df["velocidad_media_m_s"] < 0).any():
            raise ValueError("Áreas y velocidades deben ser finitas; área > 0 y velocidad ≥ 0.")
        df["caudal_parcial_m3_s"] = df["area_parcial_m2"] * df["velocidad_media_m_s"]
        area = float(df["area_parcial_m2"].sum())
        q = float(df["caudal_parcial_m3_s"].sum())
        return df, {"Q_m3_s": q, "area_total_m2": area, "velocidad_media_m_s": q / area}

    @staticmethod
    def _curva_potencia(h: np.ndarray, a: float, b: float, h0: float) -> np.ndarray:
        return a * np.power(h - h0, b)

    def ajustar_curva_gasto(
        self,
        niveles_h_m: np.ndarray,
        caudales_q_m3_s: np.ndarray,
        h0_bounds_m: tuple[float, float],
        h0_inicial_m: float,
        sigma_q_m3_s: np.ndarray | None = None,
    ) -> dict[str, object]:
        """Ajusta una ley de potencia de un solo control."""
        # shortcut: ajuste de un solo control; segmentar cuando haya aforos y evidencia hidráulica suficientes.
        h = np.asarray(niveles_h_m, dtype=float)
        q = np.asarray(caudales_q_m3_s, dtype=float)
        if h.ndim != 1 or q.ndim != 1 or len(h) != len(q) or len(h) < 4:
            raise ValueError("Se requieren al menos cuatro pares h-Q unidimensionales.")
        if not np.isfinite(h).all() or not np.isfinite(q).all() or np.any(q <= 0):
            raise ValueError("Niveles y caudales deben ser finitos; Q debe ser positivo.")
        h0_min, h0_max = h0_bounds_m
        if (
            not np.isfinite([h0_min, h0_max, h0_inicial_m]).all()
            or np.unique(h).size < 3
            or np.ptp(q) == 0
            or not h0_min < h0_inicial_m < h0_max < float(h.min())
        ):
            raise ValueError(
                "Requiere ≥3 niveles distintos, Q variable y límites finitos "
                "con h0_min < h0_inicial < h0_max < nivel mínimo medido."
            )
        ajuste_kwargs: dict[str, object] = {}
        if sigma_q_m3_s is not None:
            sigma = np.asarray(sigma_q_m3_s, dtype=float)
            if sigma.shape != q.shape or not np.isfinite(sigma).all() or np.any(sigma <= 0):
                raise ValueError("sigma_Q debe tener la misma longitud que Q y contener incertidumbres positivas.")
            ajuste_kwargs = {"sigma": sigma, "absolute_sigma": True}
        b0, log_a0 = np.polyfit(np.log(h - h0_inicial_m), np.log(q), 1)
        a0 = max(float(np.exp(log_a0)), 1e-12)
        popt, pcov = curve_fit(
            self._curva_potencia,
            h,
            q,
            p0=[a0, max(float(b0), 0.1), h0_inicial_m],
            bounds=([1e-12, 1e-8, h0_min], [np.inf, np.inf, h0_max]),
            maxfev=20000,
            **ajuste_kwargs,
        )
        pred = self._curva_potencia(h, *popt)
        resid = q - pred
        ss_tot = float(np.sum((q - q.mean()) ** 2))
        r2 = float(1 - np.sum(resid**2) / ss_tot) if ss_tot > 0 else float("nan")
        stderr = np.sqrt(np.maximum(np.diag(pcov), 0))
        stderr_list = [float(v) if np.isfinite(v) else None for v in stderr]
        return {
            "a": float(popt[0]),
            "b": float(popt[1]),
            "h0_m": float(popt[2]),
            "rmse_m3_s": float(np.sqrt(np.mean(resid**2))),
            "r2": r2,
            "error_estandar_parametros": stderr_list,
        }


def leer_csv_topografia(ruta: str | Path) -> tuple[dict[str, str], pd.DataFrame]:
    """Lee comentarios '# METADATOS: clave=valor' y luego la tabla CSV."""
    ruta = Path(ruta)
    lineas = ruta.read_text(encoding="utf-8-sig").splitlines()
    metadatos: dict[str, str] = {}
    for linea in lineas:
        if not linea.lstrip().startswith("#"):
            continue
        contenido = re.sub(r"^\s*#\s*METADATOS\s*:\s*", "", linea.strip(), flags=re.I)
        for item in contenido.split(","):
            if "=" in item:
                k, v = item.split("=", 1)
                metadatos[k.strip()] = v.strip()
    df = pd.read_csv(StringIO("\n".join(linea for linea in lineas if not linea.lstrip().startswith("#"))))
    requeridas = {"ID", "Punto", "Este_m", "Norte_m", "Cota_m", "Tipo_Cota", "Incertidumbre_m", "Progresiva_m"}
    faltantes = requeridas - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas topográficas: {', '.join(sorted(faltantes))}")
    return metadatos, df


class AuditorCalidadCSV:
    """Revisa estructura, metadatos y coherencia geométrica básica del CSV."""

    DATUMS_VERTICALES_VALIDOS = {"IGN_PERU", "EGM96", "NAVD88"}
    ZONAS_UTM_PERU = {"17S", "18S", "19S"}

    @classmethod
    def auditar_csv_topografia(
        cls,
        path_csv: str | Path,
        pendiente_max_pct: float = 150.0,
        bounds_este: tuple[float, float] = (300000, 500000),
        bounds_norte: tuple[float, float] = (8000000, 8500000),
    ) -> dict[str, object]:
        reporte: dict[str, object] = {
            "valido": True,
            "observaciones": [],
            "metadatos": {},
            "filas_totales": 0,
        }
        observaciones: list[str] = reporte["observaciones"]  # type: ignore[assignment]
        ruta = Path(path_csv)
        if not ruta.is_file():
            reporte["valido"] = False
            observaciones.append(f"El archivo no existe: {ruta}")
            return reporte

        try:
            lineas = ruta.read_text(encoding="utf-8-sig").splitlines()
            metadatos: dict[str, str] = {}
            for linea in lineas:
                if linea.lstrip().upper().startswith("# METADATOS:"):
                    for item in linea.split(":", 1)[1].split(","):
                        if "=" in item:
                            clave, valor = item.split("=", 1)
                            metadatos[clave.strip()] = valor.strip()
                    break
            reporte["metadatos"] = metadatos

            for campo in ("Datum", "Zona", "Datum_Vertical", "Metodo"):
                if not metadatos.get(campo):
                    reporte["valido"] = False
                    observaciones.append(f"Falta el metadato obligatorio: {campo}")
            if metadatos.get("Datum_Vertical") and metadatos["Datum_Vertical"] not in cls.DATUMS_VERTICALES_VALIDOS:
                observaciones.append(f"Datum vertical no estándar: {metadatos['Datum_Vertical']}")
            if metadatos.get("Zona") and metadatos["Zona"] not in cls.ZONAS_UTM_PERU:
                observaciones.append(f"Zona UTM fuera del ámbito nacional esperado: {metadatos['Zona']}")

            df = pd.read_csv(StringIO("\n".join(linea for linea in lineas if not linea.lstrip().startswith("#"))))
        except (OSError, UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
            reporte["valido"] = False
            observaciones.append(f"Error al leer el CSV: {exc}")
            return reporte

        reporte["filas_totales"] = len(df)
        columnas = ["Este_m", "Norte_m", "Cota_m", "Tipo_Cota"]
        faltantes = [col for col in columnas if col not in df.columns]
        for columna in faltantes:
            reporte["valido"] = False
            observaciones.append(f"Columna faltante en CSV: {columna}")
        if faltantes:
            return reporte
        if df.empty:
            reporte["valido"] = False
            observaciones.append("El CSV no contiene filas de datos.")
            return reporte

        for columna in ("Este_m", "Norte_m", "Cota_m"):
            df[columna] = pd.to_numeric(df[columna], errors="coerce")
        nulos = int(df[columnas].isna().sum().sum())
        coords_finitas = np.isfinite(df[["Este_m", "Norte_m", "Cota_m"]].to_numpy(dtype=float)).all(axis=1)
        no_finitos = int((~coords_finitas & ~df[["Este_m", "Norte_m", "Cota_m"]].isna().any(axis=1)).sum())
        if nulos or no_finitos:
            reporte["valido"] = False
            observaciones.append(
                f"Se encontraron {nulos} valores nulos y {no_finitos} filas con coordenadas no finitas en columnas críticas."
            )

        finitos = coords_finitas
        duplicados = int(df.loc[finitos].duplicated(subset=["Este_m", "Norte_m", "Cota_m"]).sum())
        if duplicados:
            observaciones.append(f"Advertencia: Se encontraron {duplicados} coordenadas 3D duplicadas.")

        if finitos.any():
            coords = df.loc[finitos]
            fuera = (
                ~coords["Este_m"].between(*bounds_este)
                | ~coords["Norte_m"].between(*bounds_norte)
            )
            if fuera.any():
                observaciones.append("Advertencia: Hay coordenadas fuera del Bounding Box geográfico esperado para la zona.")

            if "Progresiva_m" in df.columns:
                df["Progresiva_m"] = pd.to_numeric(df["Progresiva_m"], errors="coerce")
                orden = df.sort_values("Progresiva_m", kind="stable")
            else:
                orden = df
            for i in range(len(orden) - 1):
                p1, p2 = orden.iloc[i], orden.iloc[i + 1]
                if not np.isfinite(p1[["Este_m", "Norte_m", "Cota_m"]].to_numpy(dtype=float)).all() or not np.isfinite(p2[["Este_m", "Norte_m", "Cota_m"]].to_numpy(dtype=float)).all():
                    continue
                dist = float(np.hypot(p2["Este_m"] - p1["Este_m"], p2["Norte_m"] - p1["Norte_m"]))
                dh = float(abs(p2["Cota_m"] - p1["Cota_m"]))
                if dist == 0 and dh > 0:
                    reporte["valido"] = False
                    observaciones.append(f"Inconsistencia grave en fila {i + 2}: Mismas coordenadas planar X/Y pero con distinta cota.")
                elif dist > 0 and dh / dist * 100 > pendiente_max_pct:
                    observaciones.append(
                        f"Salto de cota anómalo entre fila {i + 1} y {i + 2}: Pendiente = {dh / dist * 100:.1f}% "
                        f"(Dist = {dist:.2f} m, dH = {dh:.2f} m)."
                    )
        return reporte


def main() -> None:
    parser = argparse.ArgumentParser(description="Cálculos hidráulicos preliminares para la MCH.")
    sub = parser.add_subparsers(dest="accion", required=True)

    p_geo = sub.add_parser("cuerda", help="Calcula distancia planar y cuerda 3D entre dos puntos.")
    p_geo.add_argument("csv")
    p_geo.add_argument("--inicio", required=True, help="Valor de la columna Punto.")
    p_geo.add_argument("--fin", required=True, help="Valor de la columna Punto.")
    p_linea = sub.add_parser("trazado", help="Suma distancias 3D de puntos levantados del eje.")
    p_linea.add_argument("csv")
    p_linea.add_argument("--tipo-cota", required=True, help="Valor de Tipo_Cota para puntos del eje.")
    p_perd = sub.add_parser("perdidas", help="Calcula Darcy-Weisbach y pérdidas locales con K_total.")
    p_perd.add_argument("--q", type=float, required=True, help="Caudal m3/s.")
    p_perd.add_argument("--d", type=float, required=True, help="Diámetro interior m.")
    p_perd.add_argument("--l", type=float, required=True, help="Longitud desarrollada medida m.")
    p_perd.add_argument("--rugosidad", type=float, required=True, help="Rugosidad absoluta m.")
    p_perd.add_argument("--k-total", type=float, required=True, help="Suma documentada de coeficientes K (0 solo si no hay accesorios).")
    p_perd.add_argument("--nu", type=float, default=1.004e-6, help="Viscosidad cinemática m2/s.")
    p_aforo = sub.add_parser("aforo", help="Integra Q=sum(A_parcial*v_media).")
    p_aforo.add_argument("csv")
    p_curva = sub.add_parser("curva", help="Ajusta un tramo de curva Q=a(h-h0)^b.")
    p_curva.add_argument("csv")
    p_curva.add_argument("--h-col", default="nivel_m")
    p_curva.add_argument("--q-col", default="caudal_m3_s")
    p_curva.add_argument("--h0-min", type=float, required=True)
    p_curva.add_argument("--h0-max", type=float, required=True)
    p_curva.add_argument("--h0-inicial", type=float, required=True)
    p_curva.add_argument("--sigma-col", help="Columna opcional de incertidumbre de Q (m3/s).")

    args = parser.parse_args()
    evaluador = EvaluadorHidraulicoMCH(
        viscosidad_cinematica_m2_s=getattr(args, "nu", 1.004e-6)
    )
    try:
        if args.accion in {"cuerda", "trazado"}:
            _, puntos = leer_csv_topografia(args.csv)
            if args.accion == "cuerda":
                def punto(nombre: str) -> pd.Series:
                    encontrados = puntos.loc[puntos["Punto"] == nombre]
                    if len(encontrados) != 1:
                        raise ValueError(f"El punto {nombre!r} debe aparecer exactamente una vez.")
                    return encontrados.iloc[0]

                a, b = punto(args.inicio), punto(args.fin)
                resultado = evaluador.calcular_geometria_3d(
                    a["Este_m"], a["Norte_m"], a["Cota_m"],
                    b["Este_m"], b["Norte_m"], b["Cota_m"],
                )
            else:
                eje = puntos.loc[puntos["Tipo_Cota"].str.casefold() == args.tipo_cota.casefold()]
                resultado = {
                    "longitud_desarrollada_3d_m": evaluador.longitud_trazado_3d(eje)
                }
        elif args.accion == "perdidas":
            resultado = evaluador.calcular_perdidas_darcy(
                args.q, args.d, args.l, args.rugosidad, args.k_total
            )
        elif args.accion == "aforo":
            datos = pd.read_csv(args.csv, comment="#")
            _, resultado = evaluador.calcular_aforo(datos)
        else:
            datos = pd.read_csv(args.csv, comment="#")
            resultado = evaluador.ajustar_curva_gasto(
                datos[args.h_col].to_numpy(),
                datos[args.q_col].to_numpy(),
                (args.h0_min, args.h0_max),
                args.h0_inicial,
                datos[args.sigma_col].to_numpy() if args.sigma_col else None,
            )
    except (OSError, KeyError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    print(json.dumps(resultado, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
