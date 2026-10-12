#!/usr/bin/env python3
"""
Simulación Horaria de Generación Hidroeléctrica (8,760 Horas / Año)
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Ollachea, Puno
Autor: Consultoría de Ingeniería Energética / UNAP FIME
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulacion_8760h():
    base_dir = "/storage/emulated/0/universida-datos/Estudio microcentral 100 kW Puno"
    data_path = os.path.join(base_dir, "02 Datos/series_caudales_diarios_historicos_2014_2023.csv")
    mapas_path = os.path.join(base_dir, "04 Mapas")
    
    df = pd.read_csv(data_path)
    caudales_diarios = df["Caudal_Rio_m3s"].values
    
    # Parámetros técnicos
    q_diseno = 0.125  # m³/s (125 L/s)
    q_min_op = 0.025  # m³/s (20% de carga nominal)
    q_eco = 0.030     # m³/s (30 L/s)
    Hn = 106.18       # m
    rho = 1000.0      # kg/m³
    g = 9.81          # m/s²
    disponibilidad = 0.965 # 96.5% de disponibilidad mecánica y eléctrica
    
    # Eficiencia combinada en función de la fracción de carga Q_turbinado / Q_diseno
    # Curva típica Pelton plana: se mantiene > 85% entre 30% y 100% de carga
    def calc_rendimiento_global(f_carga):
        if f_carga < 0.20:
            return 0.0
        # Polinomio cuadrático característico de turbina Pelton de 2 toberas
        return 0.74 * (0.80 + 0.35 * f_carga - 0.15 * (f_carga**2))

    # Simular para un año representativo (365 días x 24 horas = 8,760 horas)
    # Tomar el año hidrológico mediano
    n_anios = len(caudales_diarios) // 365
    anios_matrix = caudales_diarios[:n_anios*365].reshape(n_anios, 365)
    caudal_anio_medio = np.median(anios_matrix, axis=0) # 365 días representativos
    
    # Expandir a 8,760 horas con perfil de demanda y variación diurna ligera
    horas = 8760
    q_horario_rio = np.repeat(caudal_anio_medio, 24)
    # Factor aleatorio de modulación horaria leve (± 3%)
    np.random.seed(42)
    modulacion = 1.0 + np.random.uniform(-0.03, 0.03, horas)
    q_horario_rio = q_horario_rio * modulacion
    
    potencias_kw = []
    for q_rio in q_horario_rio:
        q_disponible = max(0.0, q_rio - q_eco)
        q_turb = min(q_diseno, q_disponible)
        f_carga = q_turb / q_diseno
        if f_carga >= 0.20:
            eta = calc_rendimiento_global(f_carga)
            # Potencia en bornes red
            p_kw = (rho * g * q_turb * Hn * eta / 1000.0) * disponibilidad
            potencias_kw.append(min(100.0, p_kw))
        else:
            potencias_kw.append(0.0)
            
    potencias_kw = np.array(potencias_kw)
    energia_anual_kwh = np.sum(potencias_kw) # Suma hora a hora (kW * 1h = kWh)
    energia_anual_mwh = energia_anual_kwh / 1000.0
    factor_planta = energia_anual_kwh / (100.0 * 8760.0) * 100.0
    
    # Desglose mensual
    meses_dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    nombres_meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Set", "Oct", "Nov", "Dic"]
    gen_mensual_mwh = []
    idx_inicio = 0
    for d in meses_dias:
        horas_mes = d * 24
        gen_m = np.sum(potencias_kw[idx_inicio:idx_inicio+horas_mes]) / 1000.0
        gen_mensual_mwh.append(gen_m)
        idx_inicio += horas_mes

    print("================================================================")
    print("SIMULACIÓN ENERGÉTICA HORARIA ANUAL (8,760 HORAS)")
    print("================================================================")
    print(f"Potencia activa neta nominal:     100.0 kW")
    print(f"Horas totales de simulación:      8,760 horas/año")
    print(f"Disponibilidad operativa:         {disponibilidad*100:.1f} %")
    print(f"Producción Neta Anual Simulada:   {energia_anual_kwh:,.1f} kWh/año ({energia_anual_mwh:.2f} MWh/año)")
    print(f"Factor de Planta Anual (FP):      {factor_planta:.2f} %")
    print("----------------------------------------------------------------")
    print("Desglose de Generación Mensual:")
    for mes, mwh in zip(nombres_meses, gen_mensual_mwh):
        print(f"  {mes}: {mwh:6.2f} MWh  (FP = {mwh*1000 / (100 * (len(potencias_kw)//12)):5.1f}%)")

if __name__ == "__main__":
    simulacion_8760h()
