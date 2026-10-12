#!/usr/bin/env python3
"""
Módulo de Cálculo Eléctrico: Subestación Elevadora, Línea de Transmisión y Malla a Tierra
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Ollachea, Puno
Autor: Área de Sistemas Eléctricos de Potencia / UNAP FIME
"""
import math

def calculo_electrico():
    print("================================================================")
    print("CÁLCULOS ELÉCTRICOS DE EVACUACIÓN Y SUBESTACIÓN (MEM / IEEE)")
    print("================================================================")
    
    # 1. Transformador de Potencia Elevador
    S_gen = 125.0 # kVA
    V_bt = 0.380  # kV (380 V)
    V_mt = 10.0   # kV (10 kV red de distribución Electro Puno)
    
    # Corrientes nominales
    I_bt = (S_gen) / (math.sqrt(3.0) * V_bt) # 189.9 A
    I_mt = (S_gen) / (math.sqrt(3.0) * V_mt) # 7.22 A
    
    # Parámetros del transformador
    u_k = 0.045 # 4.5% tensión de cortocircuito
    P_cu = 1.85 # kW pérdidas en el cobre
    P_fe = 0.35 # kW pérdidas en el hierro (vacío)
    
    # Corriente de cortocircuito trifásica en bornes BT (IEC 60909)
    I_cc_bt = I_bt / u_k # 4,220 A (4.22 kA)
    # Potencia de cortocircuito BT
    S_cc_bt = (S_gen / u_k) / 1000.0 # 2.78 MVA
    
    # 2. Línea de Transmisión en Media Tensión 10 kV
    L_linea_km = 3.20 # km hasta punto de conexión Ollachea
    # Conductor de aleación de aluminio AAAC 35 mm² (Robin)
    R_cond = 0.985 # Ohm/km a 50°C
    X_cond = 0.365 # Ohm/km a 60 Hz
    cos_phi = 0.85
    sin_phi = math.sqrt(1.0 - cos_phi**2) # 0.527
    
    # Caída de tensión porcentual: Delta_V = (sqrt(3) * I * (R*cos_phi + X*sin_phi) * L) / V_mt * 100
    Delta_V_voltios = math.sqrt(3.0) * I_mt * (R_cond * cos_phi + X_cond * sin_phi) * L_linea_km
    Delta_V_pct = (Delta_V_voltios / (V_mt * 1000.0)) * 100.0
    
    # Pérdidas de potencia en la línea (Joule)
    P_perdidas_linea_kw = 3.0 * (I_mt ** 2) * (R_cond * L_linea_km) / 1000.0 # kW
    P_perdidas_pct = (P_perdidas_linea_kw / (S_gen * cos_phi)) * 100.0
    
    print(f"\n[TRANSFORMADOR ELEVADOR PRINCIPAL]")
    print(f"  Tipo:                             Trifásico en baño de aceite mineral, refrigeración ONAN")
    print(f"  Potencia nominal:                 125 kVA")
    print(f"  Relación de transformación:       0.380 / 10.0 kV ± 2x2.5% (Taps en vacío)")
    print(f"  Grupo de conexión:                Dyn5 (Neutro BT accesible y puesto a tierra)")
    print(f"  Corriente nominal BT (380 V):     {I_bt:.1f} A")
    print(f"  Corriente nominal MT (10 kV):     {I_mt:.2f} A")
    print(f"  Tensión de cortocircuito (uk):    {u_k*100:.1f} %")
    print(f"  Corriente de cortocircuito BT:    {I_cc_bt/1000:.2f} kA (Poder de corte mínimo: 10 kA)")

    print(f"\n[LÍNEA DE TRANSMISIÓN 10 kV (3.2 km)]")
    print(f"  Conductor seleccionado:           AAAC 35 mm² (Aleación Al-Mg-Si)")
    print(f"  Estructuras:                      Postes de concreto armado centrifugado (CAC) 12m/300daN")
    print(f"  Caída de tensión calculada:       {Delta_V_pct:.2f} % ({Delta_V_voltios:.1f} V) [Límite DGE = 5.0 % - CONFORME]")
    print(f"  Pérdidas Joule en línea:          {P_perdidas_linea_kw:.2f} kW ({P_perdidas_pct:.2f} % de la potencia)")

    # 3. Diseño de la Malla de Puesta a Tierra (IEEE Std 80-2013)
    # Suelo con tratamiento mejorador de sales conductivas y bentonita (rho_eq = 85 Ohm*m)
    rho_terreno = 85.0 # Ohm*m
    L_malla_x = 8.0 # m
    L_malla_y = 6.0 # m
    Area_malla = L_malla_x * L_malla_y # 48 m²
    n_electrodos = 8 # jabalinas de cobre 3/4" x 2.4 m en perímetro y centro
    L_conductor_total = (5 * 6.0) + (4 * 8.0) + (n_electrodos * 2.4) # 30 + 32 + 19.2 = 81.2 m
    
    # Resistencia de la malla según fórmula de Laurent & Nieman
    R_pat = rho_terreno * ((1.0 / L_conductor_total) + (1.0 / math.sqrt(20.0 * Area_malla)))
    
    print(f"\n[SISTEMA DE PUESTA A TIERRA (IEEE Std 80)]")
    print(f"  Resistividad equivalente suelo:   {rho_terreno:.1f} Ω·m (con dosis de bentonita sódica)")
    print(f"  Dimensiones de la malla:          {L_malla_x:.1f} m x {L_malla_y:.1f} m (Área = {Area_malla:.1f} m²)")
    print(f"  Conductor de malla:               Cobre desnudo de temple blando 50 mm²")
    print(f"  Electrodos verticales:            8 varillas Copperweld 3/4'' x 2.40 m")
    print(f"  Resistencia de puesta a tierra:   {R_pat:.2f} Ω [Límite Código Nacional de Electricidad = 5.0 Ω - CONFORME]")

if __name__ == "__main__":
    calculo_electrico()
