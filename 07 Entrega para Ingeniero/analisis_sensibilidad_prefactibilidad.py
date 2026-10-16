"""Reproduce el estrés económico con la misma serie y supuestos de prefactibilidad."""

from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.economics import evaluacion_completa
from src.electrical import energia_anual
from src.hydrology import cargar_caudales


SERIE = ROOT / "data/series_caudales_diarios_historicos_2014_2023.csv"
OUT = Path(__file__).resolve().parent / "data/sensibilidad_extrema.csv"
Q_ECO = 0.030
ETA = 0.73
CAPEX = 245_800.0


def evaluar(nombre: str, caudales: np.ndarray, salto_m: float, q_diseno: float, capex: float) -> dict:
    energia = energia_anual(caudales, 100.0, q_diseno, Q_ECO, salto_m, ETA)
    finanzas = evaluacion_completa(
        capex, 0.03, 100.0, energia["factor_planta"], 0.075, 25, 0.10
    )
    return {
        "escenario": nombre,
        "salto_bruto_m": salto_m,
        "caudal_diseno_m3s": q_diseno,
        "capex_usd": capex,
        "energia_modelada_mwh_anio": energia["energia_anual_mwh"],
        "factor_planta_pct": energia["factor_planta_pct"],
        "van_usd": finanzas["van_usd"],
        "tir_pct": finanzas["tir_pct"],
        "bc": finanzas["relacion_beneficio_costo"],
        "payback_anios": finanzas["payback_anios"],
        "lcoe_usd_mwh": finanzas["lcoe_usd_mwh"],
    }


def main() -> None:
    q = cargar_caudales(str(SERIE))["Caudal_Rio_m3s"].to_numpy(dtype=float)
    escenarios = [
        evaluar("Base publicada", q, 115.0, 0.125, CAPEX),
        evaluar("Salto bruto 100 m", q, 100.0, 0.125, CAPEX),
        evaluar("Caudal de diseño 80 L/s", q, 115.0, 0.080, CAPEX),
        evaluar("CAPEX +30%", q, 115.0, 0.125, CAPEX * 1.30),
        evaluar("Combinado: 100 m, 80 L/s, CAPEX +30%", q, 100.0, 0.080, CAPEX * 1.30),
        # Interpretation B: total river flow is held at 80 L/s all year; 30 L/s remains in-stream.
        evaluar("Río 80 L/s todo el año; Qeco 30 L/s", np.full_like(q, 0.080), 115.0, 0.125, CAPEX),
        evaluar("Río 80 L/s todo el año + combinado", np.full_like(q, 0.080), 100.0, 0.125, CAPEX * 1.30),
    ]
    tabla = pd.DataFrame(escenarios)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(OUT, index=False)
    print(tabla.to_string(index=False))
    print(f"\nCSV: {OUT}")
    print("Nota: es sensibilidad del modelo de escenario, no una predicción hidrológica validada.")


if __name__ == "__main__":
    main()
