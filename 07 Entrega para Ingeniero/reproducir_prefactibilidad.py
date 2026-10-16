"""Reproduce solo los cálculos de prefactibilidad; no genera planos ni informes."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.electrical import energia_anual
from src.economics import evaluacion_completa
from src.hydraulics import calcular_grupo_turbina_generador, dimensionamiento_tuberia
from src.hydrology import cargar_caudales, estadisticas_caudales, validar_datos


data_path = ROOT / "data/series_caudales_diarios_historicos_2014_2023.csv"
df = cargar_caudales(str(data_path))
validacion = validar_datos(df)
if not validacion["valido"]:
    raise SystemExit(f"Serie no válida para el cálculo: {validacion}")

q = df["Caudal_Rio_m3s"].to_numpy()
hidro = estadisticas_caudales(q)
tuberia = dimensionamiento_tuberia(0.125, 115.0, 380.0, 0.000045, 0.250)
grupo = calcular_grupo_turbina_generador(
    0.125, tuberia["salto_neto_m"], 115.0, 2, 1200.0
)
energia = energia_anual(q, 100.0, 0.125, 0.030, 115.0)
economia = evaluacion_completa(
    245800.0, 0.03, 100.0, energia["factor_planta"],
    0.075, 25, 0.10
)

assert 0.0 < energia["factor_planta"] <= 1.0
assert grupo["potencia_neta_red_kw"] > 0.0

print("Prefactibilidad MCH Río Blanco — escenario computacional, 100 kW")
print(f"Registros: {validacion['total_registros']} | Qmedio: {hidro['caudal_medio']:.3f} m³/s | Q95: {hidro['percentiles'][95]:.3f} m³/s")
print(f"Qd adoptado: 0.125 m³/s | H bruto: 115.00 m | H neto calculado: {tuberia['salto_neto_m']:.2f} m")
print(f"Potencia calculada del conjunto: {grupo['potencia_neta_red_kw']:.2f} kW | Generador supuesto: 125 kVA, 100 kW a FP 0.8")
print(f"Energía modelada: {energia['energia_anual_mwh']:.2f} MWh/año | Factor de planta: {energia['factor_planta_pct']:.2f}%")
print(f"Economía: VAN USD {economia['van_usd']:,.2f} | TIR {economia['tir_pct']:.2f}% | Payback {economia['payback_anios']:.2f} años")
print(f"LCOE USD {economia['lcoe_usd_mwh']:.2f}/MWh | B/C {economia['relacion_beneficio_costo']:.2f}")
print("Aviso: la validación es estructural. La serie, los supuestos y la viabilidad requieren verificación profesional.")
