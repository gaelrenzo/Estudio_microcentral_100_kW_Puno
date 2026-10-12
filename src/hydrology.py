"""
Módulo de Análisis Hidrológico y Curva de Duración de Caudales (CDC).
Permite la carga, validación, cálculo estadístico y graficación de series históricas de caudal.
"""

import os
from typing import Dict, Tuple, Any
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def cargar_caudales(ruta_csv: str) -> pd.DataFrame:
    """
    Carga un archivo CSV con series de caudales diarios.

    Args:
        ruta_csv: Ruta absoluta o relativa al archivo CSV.

    Returns:
        pd.DataFrame con los datos leídos.

    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta proporcionada.
    """
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"No se encontró el archivo de caudales: {ruta_csv}")
    
    df = pd.read_csv(ruta_csv)
    return df


def validar_datos(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Valida la coherencia e integridad de los datos hidrológicos cargados.

    Args:
        df: DataFrame que contiene al menos la columna 'Caudal_Rio_m3s'.

    Returns:
        Diccionario con métricas de validación y estado de integridad.
    """
    columna_caudal = "Caudal_Rio_m3s"
    tiene_columna = columna_caudal in df.columns
    total_filas = len(df)
    nulos = int(df[columna_caudal].isna().sum()) if tiene_columna else 0
    negativos = int((df[columna_caudal] < 0).sum()) if tiene_columna else 0

    rango_fechas = None
    if "Fecha" in df.columns and total_filas > 0:
        rango_fechas = (str(df["Fecha"].iloc[0]), str(df["Fecha"].iloc[-1]))

    valido = tiene_columna and total_filas > 0 and nulos == 0 and negativos == 0

    return {
        "valido": valido,
        "total_registros": total_filas,
        "valores_nulos": nulos,
        "valores_negativos": negativos,
        "columna_principal": columna_caudal,
        "rango_fechas": rango_fechas
    }


def estadisticas_caudales(caudales: np.ndarray) -> Dict[str, Any]:
    """
    Calcula estadísticos descriptivos y percentiles clave de persistencia de caudales.

    Args:
        caudales: Array unidimensional con registros de caudal en m³/s.

    Returns:
        Diccionario con media, valores extremos, desviación y percentiles de excedencia.
    """
    if len(caudales) == 0:
        raise ValueError("El arreglo de caudales está vacío.")

    p_targets = [10, 25, 50, 75, 78, 85, 90, 95]
    percentiles = {p: float(np.percentile(caudales, 100 - p)) for p in p_targets}

    return {
        "total_observaciones": int(len(caudales)),
        "caudal_medio": float(np.mean(caudales)),
        "caudal_maximo": float(np.max(caudales)),
        "caudal_minimo": float(np.min(caudales)),
        "desviacion_estandar": float(np.std(caudales)),
        "percentiles": percentiles
    }


def curva_duracion(caudales: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Construye la Curva de Duración de Caudales (CDC) empleando la fórmula de Weibull.

    Args:
        caudales: Array unidimensional con registros de caudal en m³/s.

    Returns:
        Tupla (p_weibull, q_ordenados) con probabilidades de excedencia en % y caudales ordenados.
    """
    n = len(caudales)
    if n == 0:
        raise ValueError("El arreglo de caudales está vacío.")

    q_ordenados = np.sort(caudales)[::-1]
    p_weibull = (np.arange(1, n + 1) / (n + 1)) * 100.0

    return p_weibull, q_ordenados


def graficar_cdc(
    caudales: np.ndarray,
    ruta_salida: str,
    q_diseno: float = 0.125,
    q_eco: float = 0.030
) -> str:
    """
    Genera y guarda en disco la gráfica de la Curva de Duración de Caudales.

    Args:
        caudales: Array unidimensional con registros de caudal en m³/s.
        ruta_salida: Ruta completa donde se guardará la imagen PNG generada.
        q_diseno: Caudal nominal de diseño en m³/s.
        q_eco: Caudal ecológico de reserva en m³/s.

    Returns:
        Ruta del archivo de imagen generado.
    """
    p_weibull, q_sorted = curva_duracion(caudales)

    directorio = os.path.dirname(ruta_salida)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)

    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(p_weibull, q_sorted, color="#1F4E79", lw=2, label="Curva de Duración de Caudales (CDC)")
    plt.axhline(q_diseno, color="crimson", linestyle="--", lw=1.5, label=f"Caudal de Diseño Qd = {q_diseno*1000:.0f} L/s")
    plt.axhline(q_eco, color="forestgreen", linestyle=":", lw=1.5, label=f"Caudal Ecológico Qeco = {q_eco*1000:.0f} L/s")
    plt.axhline(q_diseno + q_eco, color="darkorange", linestyle="-.", lw=1.2, label=f"Requerimiento Captación = {(q_diseno+q_eco)*1000:.0f} L/s")

    plt.title(
        "Curva de Duración de Caudales (CDC) - Microcuenca Río Blanco (Puno)\nSerie Histórica 2014 - 2023 (10 Años)",
        fontsize=12,
        fontweight="bold"
    )
    plt.xlabel("Probabilidad de Excedencia / Persistencia (%)", fontsize=11)
    plt.ylabel("Caudal Medio Diario (m³/s)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.xlim(0, 100)
    plt.ylim(0, max(1.5, float(np.percentile(caudales, 98))))
    plt.legend(frameon=True, facecolor="#F9FBFD", edgecolor="#BFBFBF")
    plt.tight_layout()

    plt.savefig(ruta_salida)
    plt.close()

    return ruta_salida
