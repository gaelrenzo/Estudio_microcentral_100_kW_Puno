"""Procesa un paquete único de topografía y aforo en data_campo/."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from scripts.procesamiento_hidraulico import (
    AuditorCalidadCSV,
    EvaluadorHidraulicoMCH,
    leer_csv_topografia,
)


def _leer_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, comment="#")


def _integrar_aforo(path: Path, evaluador: EvaluadorHidraulicoMCH) -> dict[str, float | str]:
    datos = _leer_csv(path)
    if {"area_parcial_m2", "velocidad_media_m_s"} <= set(datos.columns):
        _, resultado = evaluador.calcular_aforo(datos)
        resultado["metodo"] = "Áreas y velocidades por subsección entregadas en CSV"
        return resultado

    requeridas = {"Distancia_m", "Profundidad_m", "V_06_m_s"}
    if not requeridas <= set(datos.columns):
        raise ValueError(
            f"Aforo {path.name}: requiere area_parcial_m2/velocidad_media_m_s "
            "o Distancia_m/Profundidad_m/V_06_m_s."
        )
    datos = datos.sort_values("Distancia_m", kind="stable")
    x = datos["Distancia_m"].to_numpy(dtype=float)
    d = datos["Profundidad_m"].to_numpy(dtype=float)
    v = datos["V_06_m_s"].to_numpy(dtype=float)
    if len(x) < 2 or not np.isfinite([x, d, v]).all():
        raise ValueError(f"Aforo {path.name}: datos insuficientes o no finitos.")
    if np.any(np.diff(x) <= 0) or np.any(d < 0) or np.any(v < 0):
        raise ValueError(f"Aforo {path.name}: distancias deben crecer y profundidad/velocidad no ser negativas.")
    dx = np.diff(x)
    area = dx * (d[:-1] + d[1:]) / 2
    velocidad = (v[:-1] + v[1:]) / 2
    subsecciones = pd.DataFrame(
        {"area_parcial_m2": area, "velocidad_media_m_s": velocidad}
    )
    subsecciones = subsecciones.loc[subsecciones["area_parcial_m2"] > 0]
    if subsecciones.empty:
        raise ValueError(f"Aforo {path.name}: no hay subsecciones con área hidráulica positiva.")
    _, resultado = evaluador.calcular_aforo(subsecciones)
    resultado["metodo"] = "Integración trapezoidal por intervalos con V_06"
    return resultado


def procesar_paquete(
    data_dir: str | Path,
    report_path: str | Path,
    *,
    punto_aguas_arriba: str,
    punto_aguas_abajo: str,
    diametro_interior_m: float,
    rugosidad_m: float,
    k_total: float,
    eta_turbina: float,
    eta_generador: float,
    eta_transformador: float,
) -> dict[str, object]:
    data_dir, report_path = Path(data_dir), Path(report_path)
    data_dir.mkdir(parents=True, exist_ok=True)
    evaluador = EvaluadorHidraulicoMCH()
    topo_files: list[Path] = []
    aforo_files: list[Path] = []
    lines = ["# Reporte de procesamiento de datos de campo", "", f"Generado (UTC): {datetime.now(timezone.utc).isoformat()}", ""]
    for path in sorted(data_dir.glob("*.csv")):
        try:
            cols = set(_leer_csv(path).columns)
        except (OSError, UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
            lines.append(f"- **No procesado:** `{path.name}` — no se pudo leer: {exc}")
            continue
        if {"Este_m", "Norte_m", "Cota_m", "Tipo_Cota"} <= cols:
            topo_files.append(path)
        elif {"area_parcial_m2", "velocidad_media_m_s"} <= cols or {"Distancia_m", "Profundidad_m", "V_06_m_s"} <= cols:
            aforo_files.append(path)

    lines += ["## Auditoría topográfica", ""]
    topografias_validas: list[Path] = []
    for path in topo_files:
        auditoria = AuditorCalidadCSV.auditar_csv_topografia(path)
        if auditoria["valido"]:
            topografias_validas.append(path)
            lines.append(f"- `{path.name}`: **APROBADO** ({auditoria['filas_totales']} filas).")
            lines.extend(f"  - Aviso: {obs}" for obs in auditoria["observaciones"])
        else:
            lines.append(f"- `{path.name}`: **RECHAZADO**; cálculos omitidos para este archivo.")
            lines.extend(f"  - {obs}" for obs in auditoria["observaciones"])
    errors = []
    if len(topografias_validas) != 1:
        errors.append(f"Se requiere exactamente un CSV topográfico válido; encontrados: {len(topografias_validas)}.")
    if len(aforo_files) != 1:
        errors.append(f"Se requiere exactamente un CSV de aforo reconocido; encontrados: {len(aforo_files)}.")

    resultados: dict[str, object] = {}
    if not errors:
        topo_path = topografias_validas[0]
        try:
            _, puntos = leer_csv_topografia(topo_path)
            eje = puntos.loc[puntos["Tipo_Cota"].astype(str).str.casefold().str.replace(" ", "_") == "eje_tuberia"]
            longitud = evaluador.longitud_trazado_3d(eje)
            upstream = puntos.loc[puntos["Punto"].astype(str) == punto_aguas_arriba]
            downstream = puntos.loc[puntos["Punto"].astype(str) == punto_aguas_abajo]
            if len(upstream) != 1 or len(downstream) != 1:
                raise ValueError("Cada punto de nivel de agua debe existir exactamente una vez en la columna Punto.")
            q = _integrar_aforo(aforo_files[0], evaluador)
            pérdidas = evaluador.calcular_perdidas_darcy(
                Q_m3_s=float(q["Q_m3_s"]),
                D_interior_m=diametro_interior_m,
                L_eje_m=longitud,
                rugosidad_absoluta_m=rugosidad_m,
                K_total=k_total,
            )
            potencia = evaluador.calcular_potencia(
                Q_disponible_m3_s=float(q["Q_m3_s"]),
                nivel_aguas_arriba_m=float(upstream.iloc[0]["Cota_m"]),
                nivel_aguas_abajo_m=float(downstream.iloc[0]["Cota_m"]),
                h_perdidas_m=float(pérdidas["h_perdidas_m"]),
                eta_turbina=eta_turbina,
                eta_generador=eta_generador,
                eta_transformador=eta_transformador,
            )
            resultados = {"longitud_desarrollada_3d_m": longitud, "aforo": q, "perdidas": pérdidas, "potencia": potencia}
            lines += [
                "", "## Resultados", "",
                f"- Archivos fuente: topografía `{topo_path.name}`; aforo `{aforo_files[0].name}`.",
                f"- Puntos de nivel: aguas arriba `{punto_aguas_arriba}`; aguas abajo `{punto_aguas_abajo}`.",
                f"- Parámetros ingresados: diámetro interior {diametro_interior_m:g} m; rugosidad {rugosidad_m:g} m; K_total {k_total:g}; eficiencias turbina/generador/transformador {eta_turbina:g}/{eta_generador:g}/{eta_transformador:g}.",
                f"- Longitud desarrollada del eje: **{longitud:.3f} m**.",
                f"- Aforo integrado: **{float(q['Q_m3_s']):.6f} m³/s** ({float(q['Q_m3_s']) * 1000:.2f} L/s); método: {q['metodo']}.",
                f"- Pérdida continua Darcy–Weisbach: **{float(pérdidas['hf_m']):.3f} m**.",
                f"- Pérdidas locales con K_total={k_total:g}: **{float(pérdidas['hk_m']):.3f} m**.",
                f"- Salto bruto entre los puntos indicados: **{float(potencia['salto_bruto_m']):.3f} m**.",
                f"- Salto neto: **{float(potencia['salto_neto_m']):.3f} m**.",
                f"- Potencia eléctrica estimada usando el Q medido: **{float(potencia['potencia_electrica_kw']):.2f} kW**.",
            ]
        except (OSError, KeyError, TypeError, ValueError, RuntimeError) as exc:
            errors.append(str(exc))

    lines += ["", "## Estado", ""]
    if errors:
        lines.append("**INCOMPLETO:** no se generó un resultado hidráulico completo.")
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("**PROCESADO:** revisar datos fuente, supuestos y unidades antes de uso ingenieril.")
    lines += ["", "> Resultados preliminares. El caudal de un aforo aislado no establece caudal de diseño ni disponibilidad hídrica; verificar datum, niveles, incertidumbres, caudal ecológico, diámetro interior, K y eficiencias con evidencia de campo/fabricante.", ""]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return {"ok": not errors, "errors": errors, "results": resultados, "report": report_path}


def main(argv: list[str] | None = None) -> int:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Audita y procesa un paquete topográfico e hidráulico de campo.")
    parser.add_argument("--data-dir", type=Path, default=root / "data_campo")
    parser.add_argument("--report", type=Path, default=root / "07 Entrega para Ingeniero/REPORTE_PROCESAMIENTO_CAMPO.md")
    parser.add_argument("--punto-aguas-arriba", required=True, help="Nombre exacto en columna Punto (nivel de agua).")
    parser.add_argument("--punto-aguas-abajo", required=True, help="Nombre exacto en columna Punto (nivel de agua).")
    parser.add_argument("--diametro-interior-m", type=float, required=True)
    parser.add_argument("--rugosidad-m", type=float, required=True)
    parser.add_argument("--k-total", type=float, required=True)
    parser.add_argument("--eta-turbina", type=float, required=True)
    parser.add_argument("--eta-generador", type=float, required=True)
    parser.add_argument("--eta-transformador", type=float, required=True)
    args = parser.parse_args(argv)
    resultado = procesar_paquete(
        args.data_dir, args.report,
        punto_aguas_arriba=args.punto_aguas_arriba,
        punto_aguas_abajo=args.punto_aguas_abajo,
        diametro_interior_m=args.diametro_interior_m,
        rugosidad_m=args.rugosidad_m,
        k_total=args.k_total,
        eta_turbina=args.eta_turbina,
        eta_generador=args.eta_generador,
        eta_transformador=args.eta_transformador,
    )
    print(f"Reporte: {resultado['report']}")
    for error in resultado["errors"]:
        print(f"ERROR: {error}")
    for clave, valor in resultado["results"].items():
        print(f"{clave}: {valor}")
    return 0 if resultado["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
