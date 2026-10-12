#!/usr/bin/env python3
"""
Modelo de Evaluación Económica, Financiera y Análisis de Sensibilidad Multivariable
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Ollachea, Puno
Autor: Área de Gestión de Proyectos y Finanzas / UNAP FIME
"""
import numpy as np

def evaluacion_financiera_completa():
    # 1. Parámetros de Inversión (CAPEX)
    capex_total = 245800.0   # USD (2,458 USD/kW instalado)
    
    # Desglose del CAPEX:
    capex_items = {
        "Obras Civiles y Captación (Bocatoma, Desarenador, Canal)": 84500.0,
        "Cámara de Carga, Aliviadero y Dados de Anclaje": 26800.0,
        "Tubería Forzada Penstock de Acero ASTM A36 (380 m)": 43500.0,
        "Equipamiento Electromecánico (Pelton, Válvula, ELC)": 45000.0,
        "Generador Síncrono 125 kVA y Tableros": 16500.0,
        "Subestación 0.38/10 kV y Línea MT (3.2 km)": 14500.0,
        "Ingeniería de Detalle, Supervisión y Geodesia": 8500.0,
        "Plan de Manejo Ambiental, Social y Licencias": 6500.0
    }
    
    # 2. Costos de Operación y Mantenimiento (OPEX)
    # 3.0 % del CAPEX anual
    opex_anual = capex_total * 0.03 # 7,374.0 USD/año
    
    # 3. Parámetros Energéticos y Comerciales
    potencia_kw = 100.0
    horas_anio = 8760.0
    factor_planta = 0.768 # 76.8% (Caso Base Conservador P90)
    generacion_kwh_anual = potencia_kw * horas_anio * factor_planta # 672,768 kWh/año
    
    tarifa_base_usd_kwh = 0.075 # 75.0 USD/MWh (Tarifa RER OSINERGMIN / PPA Rural)
    ingreso_anual_base = generacion_kwh_anual * tarifa_base_usd_kwh # 50,457.60 USD/año
    
    flujo_operativo_neto = ingreso_anual_base - opex_anual # 43,083.60 USD/año
    
    # 4. Estructura de Financiamiento
    # 60% Deuda (Banca de Desarrollo / COFIDE a 7.5% anual, plazo 10 años)
    # 40% Capital Propio (Equity Comunitario / Subvención MINEM)
    pct_deuda = 0.60
    monto_deuda = capex_total * pct_deuda # 147,480.0 USD
    equity = capex_total * (1.0 - pct_deuda) # 98,320.0 USD
    tasa_interes_deuda = 0.075
    plazo_deuda_anios = 10
    # Cuota anual constante (Método Francés)
    cuota_deuda = monto_deuda * (tasa_interes_deuda * (1 + tasa_interes_deuda)**plazo_deuda_anios) / (((1 + tasa_interes_deuda)**plazo_deuda_anios) - 1)
    
    # 5. Evaluación a 25 y 30 años (Tasa Social de Descuento: 10%)
    tasa_descuento = 0.10
    horizonte = 25
    
    # Flujos del Proyecto (Económico Puro, sin deuda)
    flujos_econ = [-capex_total] + [flujo_operativo_neto] * horizonte
    
    # VAN Económico
    van_econ = sum(f / ((1.0 + tasa_descuento)**t) for t, f in enumerate(flujos_econ))
    
    # TIR Económica (Bisección)
    def calc_npv(flujos, rate):
        return sum(f / ((1.0 + rate)**t) for t, f in enumerate(flujos))
    
    r_low, r_high = 0.0, 1.0
    for _ in range(100):
        r_mid = (r_low + r_high) / 2.0
        if calc_npv(flujos_econ, r_mid) > 0:
            r_low = r_mid
        else:
            r_high = r_mid
    tir_econ = r_mid * 100.0
    
    # Payback Simple
    payback_simple = capex_total / flujo_operativo_neto
    
    # LCOE (Levelized Cost of Energy)
    costo_actualizado = capex_total + sum(opex_anual / ((1.0 + tasa_descuento)**t) for t in range(1, horizonte + 1))
    energia_actualizada = sum(generacion_kwh_anual / ((1.0 + tasa_descuento)**t) for t in range(1, horizonte + 1))
    lcoe_usd_kwh = costo_actualizado / energia_actualizada
    
    # Relación Beneficio / Costo (B/C)
    valor_actual_ingresos = sum(ingreso_anual_base / ((1.0 + tasa_descuento)**t) for t in range(1, horizonte + 1))
    valor_actual_costos = capex_total + sum(opex_anual / ((1.0 + tasa_descuento)**t) for t in range(1, horizonte + 1))
    b_c_ratio = valor_actual_ingresos / valor_actual_costos
    
    print("================================================================")
    print("EVALUACIÓN ECONÓMICA Y FINANCIERA (BASE 25 AÑOS, TASA 10%)")
    print("================================================================")
    print(f"CAPEX Total:                        ${capex_total:,.2f} USD ({capex_total/potencia_kw:,.1f} USD/kW)")
    print(f"OPEX Anual Estimado (3%):           ${opex_anual:,.2f} USD/año")
    print(f"Generación Neta Anual (P90):        {generacion_kwh_anual:,.0f} kWh/año ({generacion_kwh_anual/1000:.2f} MWh)")
    print(f"Tarifa de Venta / Valorizada:       ${tarifa_base_usd_kwh:.4f} USD/kWh (75.00 USD/MWh)")
    print(f"Ingresos Brutos Anuales:            ${ingreso_anual_base:,.2f} USD/año")
    print(f"Flujo de Caja Operativo Neto:       ${flujo_operativo_neto:,.2f} USD/año")
    print("----------------------------------------------------------------")
    print(f"Valor Actual Neto Económico (VAN):  ${van_econ:,.2f} USD")
    print(f"Tasa Interna de Retorno (TIR):      {tir_econ:.2f} %")
    print(f"Relación Beneficio / Costo (B/C):   {b_c_ratio:.2f}")
    print(f"Período de Recuperación (Payback):  {payback_simple:.2f} Años")
    print(f"Costo Nivelado de Energía (LCOE):   ${lcoe_usd_kwh:.4f} USD/kWh (${lcoe_usd_kwh*1000:.2f} USD/MWh)")
    print("----------------------------------------------------------------")
    print(f"Estructura Financiera: Deuda 60% (${monto_deuda:,.0f}) | Equity 40% (${equity:,.0f})")
    print(f"Servicio Anual de Deuda (Años 1-10): ${cuota_deuda:,.2f} USD/año (DSCR = {flujo_operativo_neto/cuota_deuda:.2f}x)")

    # 6. Análisis de Sensibilidad Multivariable
    print("\n================================================================")
    print("ANÁLISIS DE SENSIBILIDAD MULTIVARIABLE (VAN Y TIR)")
    print("================================================================")
    print(f"{'Escenario':<30} | {'VAN (USD)':<15} | {'TIR (%)':<10} | {'Viabilidad'}")
    print("-" * 70)
    
    escenarios = [
        ("Caso Base", 1.0, 1.0, 1.0),
        ("CAPEX +20%", 1.20, 1.0, 1.0),
        ("CAPEX -20%", 0.80, 1.0, 1.0),
        ("Tarifa +20% (90 USD/MWh)", 1.0, 1.20, 1.0),
        ("Tarifa -20% (60 USD/MWh)", 1.0, 0.80, 1.0),
        ("Hidrología Seca (-25% Caudal)", 1.0, 1.0, 0.75),
        ("Hidrología Húmeda (+15% Caudal)", 1.0, 1.0, 1.15),
        ("Pesimista Severo (CAPEX+20%, Tar-20%)", 1.20, 0.80, 0.80),
        ("Optimista Alto (CAPEX-10%, Tar+15%)", 0.90, 1.15, 1.10)
    ]
    
    for nom, f_cap, f_tar, f_hid in escenarios:
        c_mod = capex_total * f_cap
        op_mod = c_mod * 0.03
        gen_mod = min(100.0 * 8760.0, generacion_kwh_anual * f_hid)
        tar_mod = tarifa_base_usd_kwh * f_tar
        ing_mod = gen_mod * tar_mod
        flujo_mod = ing_mod - op_mod
        flujos_mod = [-c_mod] + [flujo_mod] * horizonte
        van_mod = sum(f / ((1.0 + tasa_descuento)**t) for t, f in enumerate(flujos_mod))
        
        # TIR
        r_l, r_h = 0.0, 1.0
        for _ in range(80):
            r_m = (r_l + r_h) / 2.0
            if calc_npv(flujos_mod, r_m) > 0:
                r_l = r_m
            else:
                r_h = r_m
        tir_mod = r_m * 100.0
        viab = "ALTA" if tir_mod >= 12.0 else ("MEDIA" if tir_mod >= 10.0 else "RIESGOSA")
        print(f"{nom:<30} | ${van_mod:>13,.2f} | {tir_mod:>8.2f} % | {viab}")

if __name__ == "__main__":
    evaluacion_financiera_completa()
