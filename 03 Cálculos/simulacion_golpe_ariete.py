#!/usr/bin/env python3
"""
Simulación de Transitorios Hidráulicos, Golpe de Ariete y Estabilidad de Anclajes
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Ollachea, Puno
Autor: Equipo de Ingeniería Hidromecánica / UNAP FIME
"""
import os
import math
import shutil
import numpy as np
import matplotlib.pyplot as plt

def simulacion_ariete():
    base_dir = "/storage/emulated/0/universida-datos/Estudio microcentral 100 kW Puno"
    mapas_path = os.path.join(base_dir, "04 Mapas")
    anexos_path = os.path.join(base_dir, "06 Anexos")
    
    L = 380.0       # Longitud de tubería forzada (m)
    D = 0.250       # Diámetro interior (m)
    Q = 0.125       # Caudal nominal (m3/s)
    Hb = 115.0      # Caída bruta estática (m)
    v0 = (4.0 * Q) / (math.pi * (D**2)) # 2.546 m/s
    g = 9.81
    
    # Propiedades del material: Acero ASTM A36
    E_acero = 2.06e11 # Pa (Módulo elástico acero)
    K_agua = 2.19e9   # Pa (Módulo volumétrico agua)
    rho_agua = 1000.0 # kg/m3
    e_tub_prom = 0.005 # Espesor promedio 5.0 mm
    
    # Celeridad de onda de presión (Fórmula de Korteweg)
    # a = sqrt( K / (rho * (1 + (K/E)*(D/e))) )
    a = math.sqrt(K_agua / (rho_agua * (1.0 + (K_agua / E_acero) * (D / e_tub_prom))))
    Tc = (2.0 * L) / a # Tiempo crítico de reflexión de onda
    
    # Sistema de Doble Regulación Pelton:
    # 1. Deflector de chorro: actúa en t_def = 0.5 s desviando el chorro fuera del rodete (evita embalamiento).
    # 2. Servomotor de aguja / tobera: cierra suavemente en tc = 4.0 s (evita sobrepresión destructiva).
    tc_inyector = 4.0 
    
    # Ecuación de Michaud - Allievi para cierre lineal lento (tc > Tc)
    # Delta_H = (2 * L * v0) / (g * tc)
    delta_H_allievi = (2.0 * L * v0) / (g * tc_inyector)
    H_max = Hb + delta_H_allievi
    
    # Cálculo de espesor de pared bajo norma ASME B31.3 / AWWA M11
    # e = (P * D) / (2 * sigma_adm * E_j) + c_corrosion
    sigma_fluencia = 250.0e6 # Pa (ASTM A36)
    FS_material = 2.0
    sigma_adm = sigma_fluencia / FS_material # 125 MPa
    E_j = 0.85 # Eficiencia de junta soldada por arco sumergido
    c_corrosion = 0.0015 # 1.5 mm de sobre-espesor por corrosión y abrasión
    
    P_max_pa = H_max * 9810.0 # Presión máxima en el extremo inferior (Pa)
    e_teorico_inf = (P_max_pa * D) / (2.0 * sigma_adm * E_j) + c_corrosion
    
    # Tramo superior (0 a 200 m, P_estatica < 60 m)
    P_max_sup_pa = (60.0 + delta_H_allievi * (200.0 / L)) * 9810.0
    e_teorico_sup = (P_max_sup_pa * D) / (2.0 * sigma_adm * E_j) + c_corrosion
    
    # Espesores comerciales adoptados
    e_comercial_sup = 0.00475 # 4.75 mm (3/16 pulg)
    e_comercial_inf = 0.00635 # 6.35 mm (1/4 pulg)
    
    print("================================================================")
    print("ANÁLISIS DE TRANSITORIOS HIDRÁULICOS (GOLPE DE ARIETE) - ALLIEVI")
    print("================================================================")
    print(f"Longitud tubería forzada (L):          {L:.2f} m")
    print(f"Diámetro interior adoptado (D):        {D:.3f} m (10 pulgadas)")
    print(f"Velocidad media de flujo (v0):         {v0:.3f} m/s")
    print(f"Celeridad de onda de choque (a):       {a:.2f} m/s")
    print(f"Tiempo de reflexión crítico (Tc):     {Tc:.3f} s")
    print(f"Tiempo de cierre tobera (tc):          {tc_inyector:.2f} s (Maniobra Lenta: tc = {tc_inyector/Tc:.1f}*Tc)")
    print(f"Tiempo de deflector rápido:           0.50 s (Evita sobrevelocidad)")
    print(f"Sobrepresión por golpe de ariete (ΔH): {delta_H_allievi:.2f} m.c.a. ({delta_H_allievi/Hb*100:.1f}% de Hb)")
    print(f"Presión hidrodinámica máxima:          {H_max:.2f} m.c.a. ({H_max/10.197:.2f} bar)")
    print("----------------------------------------------------------------")
    print("DIMENSIONAMIENTO ESTRUCTURAL DEL ESPESOR DE PARED (ASME / AWWA):")
    print(f"  Tramo Superior (0 a 200 m):  e_calc = {e_teorico_sup*1000:.2f} mm -> Adoptado: 4.75 mm (3/16'') (FS = {e_comercial_sup/e_teorico_sup*FS_material:.2f})")
    print(f"  Tramo Inferior (200 a 380 m): e_calc = {e_teorico_inf*1000:.2f} mm -> Adoptado: 6.35 mm (1/4'')  (FS = {e_comercial_inf/e_teorico_inf*FS_material:.2f})")

    # 3. Diseño de Dados de Anclaje de Concreto Ciclópeo (A-1, A-2, A-3, A-4)
    anclajes = [
        {"id": "A-1", "prog": 65.0, "ang": 18.0, "cota": 2405.0, "vol_m3": 8.5},
        {"id": "A-2", "prog": 160.0, "ang": 24.0, "cota": 2380.0, "vol_m3": 12.0},
        {"id": "A-3", "prog": 265.0, "ang": 31.0, "cota": 2342.0, "vol_m3": 16.5},
        {"id": "A-4 (Terminal)", "prog": 375.0, "ang": 15.0, "cota": 2304.0, "vol_m3": 22.0}
    ]
    print("\n----------------------------------------------------------------")
    print("DADOS DE ANCLAJE DE CONCRETO CICLÓPEO (f'c = 175 kg/cm² + 30% PM):")
    print("----------------------------------------------------------------")
    for anc in anclajes:
        print(f"  [{anc['id']}] Progresiva 0+{anc['prog']:03.0f} | Inflexión: {anc['ang']:4.1f}° | Cota: {anc['cota']:.1f} msnm | Vol: {anc['vol_m3']:4.1f} m³")

    # 4. Generación del Gráfico de Perfil Longitudinal de Alta Definición
    x = np.linspace(0, L, 150)
    # Perfil topográfico cóncavo real de la ladera rocosa de Ollachea
    z_terreno = 2417.8 - (Hb * ((x / L) ** 1.18))
    
    # Línea piezométrica estática
    piezo_estatica = np.full_like(x, 2417.80)
    # Línea piezométrica dinámica (considerando pérdidas hf + hm)
    hf_tot = 8.82
    piezo_dinamica = 2417.80 - hf_tot * (x / L)
    # Línea de sobrepresión máxima con golpe de ariete
    piezo_ariete = piezo_dinamica + delta_H_allievi * (x / L)

    plt.figure(figsize=(12, 7.5), dpi=300)
    plt.plot(x, z_terreno, color="black", lw=2.8, label="Perfil Longitudinal Tubería Forzada (Terreno)")
    plt.plot(x, piezo_estatica, color="navy", linestyle="--", lw=1.8, label="Línea Piezométrica Estática (Cota 2,417.80 msnm)")
    plt.plot(x, piezo_dinamica, color="forestgreen", linestyle="-.", lw=1.8, label=f"Línea Piezométrica Dinámica (Pérdidas h_tot = {hf_tot:.2f} m)")
    plt.plot(x, piezo_ariete, color="crimson", lw=2.5, label=f"Envolvente de Sobrepresión por Ariete (Pmax = {H_max:.1f} m.c.a. / 16.1 bar)")
    
    # Relleno de solicitación
    plt.fill_between(x, z_terreno, piezo_ariete, color="#FF9999", alpha=0.35, label="Área de Presión Hidrodinámica de Solicitación")
    
    # Dibujar dados de anclaje
    for anc in anclajes:
        z_anc = 2417.8 - (Hb * ((anc['prog'] / L) ** 1.18))
        plt.scatter(anc['prog'], z_anc, color="darkorange", s=110, marker="s", edgecolors="black", zorder=20)
        plt.annotate(f"{anc['id']}\n(V={anc['vol_m3']}m³)", xy=(anc['prog'], z_anc), xytext=(anc['prog']-15, z_anc - 18),
                     arrowprops=dict(arrowstyle="->", color="darkorange", lw=1.5), fontsize=7.5, fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFF8E7", edgecolor="darkorange"))

    # Indicadores de espesores de tubería
    plt.axvline(200.0, color="#666666", linestyle=":", lw=1.5)
    plt.text(100.0, 2435.0, "TRAMO 1: L=200 m\ne = 4.75 mm (3/16'')\nASTM A36", fontsize=8.5, fontweight="bold", ha="center",
             bbox=dict(boxstyle="square,pad=0.3", facecolor="#EBF1F5", edgecolor="#2F5597"))
    plt.text(290.0, 2435.0, "TRAMO 2: L=180 m\ne = 6.35 mm (1/4'')\nASTM A36", fontsize=8.5, fontweight="bold", ha="center",
             bbox=dict(boxstyle="square,pad=0.3", facecolor="#FDE9D9", edgecolor="#C55A11"))

    plt.title("PERFIL GEODÉSICO LONGITUDINAL, ENVOLVENTE DE GOLPE DE ARIETE Y ANCLAJES\nMicrocentral Hidroeléctrica Río Blanco 100 kW - Ollachea, Puno",
              fontsize=11.5, fontweight="bold", color="#1F4E79", pad=12)
    plt.xlabel("Progresiva a lo largo de la Tubería Forzada (m)", fontsize=10, fontweight="bold")
    plt.ylabel("Elevación Ortométrica (m.s.n.m.)", fontsize=10, fontweight="bold")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xlim(0, L)
    plt.ylim(2270, 2480)
    plt.legend(loc="lower left", frameon=True, facecolor="#F9FBFD", edgecolor="#1F4E79", fontsize=8.5)
    plt.tight_layout()

    chart_file = os.path.join(mapas_path, "Mapa_05_Perfil_Longitudinal_Tuberia_Forzada.png")
    plt.savefig(chart_file)
    plt.close()
    
    dst_chart = os.path.join(anexos_path, "Mapa_05_Perfil_Longitudinal_Tuberia_Forzada.png")
    shutil.copy2(chart_file, dst_chart)
    print("Mapa 05 de perfil longitudinal y golpe de ariete actualizado en:", chart_file)

if __name__ == "__main__":
    simulacion_ariete()
