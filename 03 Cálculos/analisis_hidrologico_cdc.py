#!/usr/bin/env python3
"""
Módulo de Análisis Hidrológico, Curva de Duración de Caudales (CDC) y Análisis de Crecidas
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Ollachea, Puno
Autor: Equipo de Ingeniería de Recursos Hídricos / UNAP FIME
"""
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    base_dir = "/storage/emulated/0/universida-datos/Estudio microcentral 100 kW Puno"
    data_path = os.path.join(base_dir, "02 Datos/series_caudales_diarios_historicos_2014_2023.csv")
    mapas_path = os.path.join(base_dir, "04 Mapas")
    anexos_path = os.path.join(base_dir, "06 Anexos")
    
    if not os.path.exists(data_path):
        print("Error: archivo de datos no encontrado:", data_path)
        return
    
    df = pd.read_csv(data_path)
    caudales = df["Caudal_Rio_m3s"].values
    n = len(caudales)
    
    # 1. Curva de Duración de Caudales (CDC)
    q_sorted = np.sort(caudales)[::-1]
    p_weibull = (np.arange(1, n + 1) / (n + 1)) * 100
    
    p_targets = [10, 25, 50, 75, 78, 85, 90, 95]
    q_percentiles = {p: np.percentile(caudales, 100 - p) for p in p_targets}
    
    q_diseno = 0.125 # 125 L/s
    q_eco = 0.030    # 30 L/s
    
    print("================================================================")
    print("ANÁLISIS HIDROLÓGICO INTEGRAL - MICROCUENCA RÍO BLANCO (2014-2023)")
    print("================================================================")
    print(f"Total registros diarios:          {n} días (10 años completos)")
    print(f"Caudal Medio Multianual (Qmed):    {np.mean(caudales):.3f} m³/s")
    print(f"Desviación Estándar (sigma):       {np.std(caudales):.3f} m³/s")
    print(f"Caudal Máximo Diario Registrado:   {np.max(caudales):.3f} m³/s")
    print(f"Caudal Mínimo Diario Registrado:   {np.min(caudales):.3f} m³/s")
    print("----------------------------------------------------------------")
    print("Percentiles de Persistencia:")
    for p in p_targets:
        print(f"  Q{p:02d}%: {q_percentiles[p]:.3f} m³/s")
    print(f"Caudal de Diseño Nominal (Qd):     {q_diseno:.3f} m³/s (125 L/s)")
    print(f"Caudal Ecológico Reserva ANA:      {q_eco:.3f} m³/s (30 L/s)")
    print(f"Demanda Total en Bocatoma:         {q_diseno + q_eco:.3f} m³/s (155 L/s, pers. ~84.5%)")

    # 2. Análisis de Crecidas y Periodos de Retorno (Distribución Gumbel de Máximos)
    # Extraer máximos anuales
    df['Year'] = pd.to_datetime(df['Fecha']).dt.year if 'Fecha' in df.columns else np.repeat(np.arange(2014, 2024), 365.25)[:n].astype(int)
    maximos_anuales = df.groupby('Year')['Caudal_Rio_m3s'].max().values
    
    mean_max = np.mean(maximos_anuales)
    std_max = np.std(maximos_anuales, ddof=1)
    # Parámetros Gumbel: alfa y u
    alpha = (std_max * math.sqrt(6)) / math.pi
    u = mean_max - 0.57721566 * alpha
    
    print("\n----------------------------------------------------------------")
    print("MODELAMIENTO DE CRECIDAS EXTRAORDINARIAS (DISTRIBUCIÓN GUMBEL):")
    print("----------------------------------------------------------------")
    periodos_retorno = [2, 5, 10, 25, 50, 100, 500]
    crecidas_Tr = {}
    for Tr in periodos_retorno:
        y = -math.log(-math.log(1.0 - 1.0 / Tr))
        Q_Tr = u + alpha * y
        crecidas_Tr[Tr] = Q_Tr
        print(f"  Tr = {Tr:3d} años:  Q_max = {Q_Tr:6.2f} m³/s")
    
    # 3. Capacidad Hidráulica del Azud de la Bocatoma (Vertedero Creager / Perfil Tipo)
    # Q = C * L * H^(3/2), con C = 2.10, L = 4.0 m
    C_azud = 2.10
    L_azud = 4.00
    Q_diseno_crecida = crecidas_Tr[50] # Tr = 50 años
    H_tirante_crecida = (Q_diseno_crecida / (C_azud * L_azud)) ** (2.0 / 3.0)
    print(f"\n[VERIFICACIÓN DEL VERTEDERO DEL AZUD]")
    print(f"  Longitud de cresta:              {L_azud:.2f} m")
    print(f"  Caudal de crecida (Tr = 50 años): {Q_diseno_crecida:.2f} m³/s")
    print(f"  Tirante de agua sobre cresta:    {H_tirante_crecida:.2f} m (Bordo libre muros: 0.85 m)")
    
    # 4. Generar Gráfico CDC de Alta Resolución
    plt.figure(figsize=(10.5, 6.5), dpi=300)
    plt.plot(p_weibull, q_sorted, color="#1F4E79", lw=2.5, label="Curva de Duración de Caudales Diarios (2014-2023)")
    plt.axhline(q_diseno, color="crimson", linestyle="--", lw=1.8, label=f"Caudal de Diseño Turbinable Qd = {q_diseno*1000:.0f} L/s (Persistencia 78%)")
    plt.axhline(q_eco, color="forestgreen", linestyle=":", lw=1.8, label=f"Caudal Ecológico Inalterable Qeco = {q_eco*1000:.0f} L/s (ANA)")
    plt.axhline(q_diseno + q_eco, color="darkorange", linestyle="-.", lw=1.5, label=f"Requerimiento Total Captación = {(q_diseno+q_eco)*1000:.0f} L/s")
    
    plt.scatter([78], [q_diseno], color="crimson", s=80, zorder=10)
    plt.annotate(f"Punto de Diseño\nQd=125 L/s (78%)", xy=(78, q_diseno), xytext=(65, q_diseno + 0.25),
                 arrowprops=dict(facecolor='crimson', edgecolor='black', width=1.5, headwidth=6),
                 fontsize=8.5, fontweight='bold', color='crimson',
                 bbox=dict(boxstyle="round,pad=0.2", facecolor='#FFF0F0', edgecolor='crimson'))

    plt.title("CURVA DE DURACIÓN DE CAUDALES (CDC) Y PUNTOS DE OPERACIÓN NOMINAL\nMicrocuenca del Río Blanco, Ollachea, Puno (Serie Diaria 2014 - 2023)",
              fontsize=11.5, fontweight='bold', color="#1F4E79", pad=10)
    plt.xlabel("Persistencia / Probabilidad de Excedencia del Tiempo (%)", fontsize=10.5, fontweight='bold')
    plt.ylabel("Caudal Medio Diario (m³/s)", fontsize=10.5, fontweight='bold')
    plt.grid(True, linestyle="--", alpha=0.55)
    plt.xlim(0, 100)
    plt.ylim(0, max(1.6, np.percentile(caudales, 98)))
    plt.legend(loc="upper right", frameon=True, facecolor="#F9FBFD", edgecolor="#1F4E79", fontsize=8.8)
    plt.tight_layout()
    
    chart_file = os.path.join(mapas_path, "Grafico_Curva_Duracion_Caudales.png")
    plt.savefig(chart_file)
    plt.close()
    
    # Sincronizar en anexos
    dst_chart = os.path.join(anexos_path, "Grafico_Curva_Duracion_Caudales.png")
    shutil.copy2(chart_file, dst_chart)
    print("Gráfico CDC actualizado y sincronizado en:", chart_file)

if __name__ == "__main__":
    import shutil
    main()
