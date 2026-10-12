#!/usr/bin/env python3
"""
Módulo de Diseño y Selección Electromecánica: Turbina Pelton y Generador Síncrono
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Ollachea, Puno
Autor: Equipo de Ingeniería Mecánica y Eléctrica / UNAP FIME
"""
import math

def diseno_electromecanico():
    print("================================================================")
    print("DISEÑO Y SELECCIÓN ELECTROMECÁNICA INTEGRAL (IEC 60193 / IEEE)")
    print("================================================================")
    
    # Parámetros hidráulicos de entrada
    Qd = 0.125       # m³/s (125 L/s)
    Hn = 106.18      # Salto neto (m)
    rho = 1000.0     # kg/m³
    g = 9.81         # m/s²
    
    # 1. Selección de Turbina Hidráulica
    # Velocidad específica aproximada: ns = (N * sqrt(P_mec)) / (Hn ** 1.25)
    # Para Hn = 106 m y Qd = 125 L/s, corresponde inequívocamente a Turbina Pelton
    z_inyectores = 2
    q_inyector = Qd / z_inyectores # 0.0625 m³/s (62.5 L/s)
    
    # Velocidad del chorro libre (Torricelli con coeficiente Cv)
    Cv = 0.97
    v_chorro = Cv * math.sqrt(2.0 * g * Hn) # 44.27 m/s
    
    # Diámetro de la tobera / chorro (d0)
    d_chorro = math.sqrt((4.0 * q_inyector) / (math.pi * v_chorro)) # 0.0424 m (42.4 mm)
    
    # Velocidad de giro del generador síncrono a f = 60 Hz
    # Polos p = 6 -> N = 120 * f / p = 120 * 60 / 6 = 1200 RPM
    N_rpm = 1200.0
    omega = (2.0 * math.pi * N_rpm) / 60.0 # 125.66 rad/s
    
    # Relación de velocidad periférica óptima Pelton: u = k_u * v_chorro (k_u = 0.46)
    k_u = 0.46
    u_tangencial = k_u * v_chorro # 20.36 m/s
    
    # Diámetro primitivo del rodete (D1): u = (pi * D1 * N) / 60
    D_rodete = (60.0 * u_tangencial) / (math.pi * N_rpm) # 0.3241 m (324.1 mm)
    rel_D_d = D_rodete / d_chorro # 7.65 (Rango óptimo: 7 a 14)
    
    # Número de cucharas (Fórmula de Taygun / Nechleba): Z = round(D / (2*d) + 15)
    num_cucharas = int(round((D_rodete / (2.0 * d_chorro)) + 15)) # 19 cucharas
    
    # Dimensiones de las cucharas Pelton
    ancho_B = 3.0 * d_chorro   # 127.2 mm
    largo_L = 2.6 * d_chorro   # 110.2 mm
    prof_T = 1.0 * d_chorro    # 42.4 mm
    ang_salida_beta2 = 165.0   # Grados (deja 15° para que el agua escape libremente sin chocar con la espalda de la siguiente)
    
    # Velocidad de embalamiento (Runaway Speed)
    N_embalamiento = 1.82 * N_rpm # 2,184 RPM
    
    # Potencias
    eta_turbina = 0.88
    eta_generador = 0.93
    eta_trafo_linea = 0.98
    
    P_hidraulica = (rho * g * Qd * Hn) / 1000.0 # kW
    P_mecanica = P_hidraulica * eta_turbina      # 114.57 kW
    P_electrica_bornes = P_mecanica * eta_generador # 106.55 kW
    P_red_neta = P_electrica_bornes * eta_trafo_linea # 104.42 kW
    
    # Momento torsor en el eje de la turbina
    Torque_nom = (P_mecanica * 1000.0) / omega # 911.75 N*m
    Torque_embalamiento = Torque_nom * 1.5
    
    # Dimensionamiento del eje por fatiga y torsión (Código ASME Shaft Design)
    # d_eje = ((16 / (pi * tau_adm)) * sqrt((Km * M)^2 + (Kt * T)^2))^(1/3)
    # Acero aleado AISI 4140 tratado térmicamente (Sy = 415 MPa, Sut = 655 MPa)
    tau_adm = 0.30 * 415.0e6 # 124.5 MPa
    d_eje_teorico = ((16.0 * Torque_nom) / (math.pi * tau_adm)) ** (1.0 / 3.0) # ~ 0.033 m
    d_eje_adoptado = 0.065 # 65 mm comercial para admitir chavetero, flexión y cojinetes
    
    print(f"\n[TURBINA HIDRÁULICA PELTON]")
    print(f"  Tipo:                             Pelton de eje horizontal, 2 inyectores a 90°")
    print(f"  Caudal por tobera:                {q_inyector*1000:.1f} L/s (Total = {Qd*1000:.1f} L/s)")
    print(f"  Velocidad del chorro (v0):        {v_chorro:.2f} m/s")
    print(f"  Diámetro de tobera / chorro (d0): {d_chorro*1000:.1f} mm")
    print(f"  Velocidad sincrónica nominal:     {N_rpm:.0f} RPM")
    print(f"  Velocidad de embalamiento (Nr):   {N_embalamiento:.0f} RPM")
    print(f"  Diámetro primitivo rodete (D1):   {D_rodete*1000:.1f} mm (Relación D1/d0 = {rel_D_d:.2f})")
    print(f"  Número de cucharas:               {num_cucharas} unidades monobloque")
    print(f"  Geometría cuchara:                Ancho B = {ancho_B*1000:.1f} mm | Largo L = {largo_L*1000:.1f} mm | Prof. T = {prof_T*1000:.1f} mm")
    print(f"  Material rodete:                  Acero inoxidable ASTM A743 Gr. CA6NM (13% Cr, 4% Ni)")
    print(f"  Rendimiento garantizado:          {eta_turbina*100:.1f} %")
    print(f"  Potencia mecánica al eje:         {P_mecanica:.2f} kW (Torque = {Torque_nom:.1f} N·m)")
    print(f"  Diámetro de eje adoptado:         {d_eje_adoptado*1000:.1f} mm (Acero AISI 4140)")

    # 2. Generador Síncrono Trifásico
    cos_phi = 0.85
    S_gen_requerida = P_electrica_bornes / cos_phi # 125.35 kVA -> 125 kVA estándar
    S_nominal = 125.0 # kVA
    V_nominal = 400.0 # V entre fases (400/230 V)
    I_nominal = (S_nominal * 1000.0) / (math.sqrt(3.0) * V_nominal) # 180.4 A
    
    print(f"\n[GENERADOR ELÉCTRICO SÍNCRONO]")
    print(f"  Potencia aparente nominal:        {S_nominal:.1f} kVA")
    print(f"  Potencia activa nominal:          {S_nominal * cos_phi:.1f} kW ({P_electrica_bornes:.2f} kW en operación)")
    print(f"  Factor de potencia nominal:       {cos_phi:.2f} inductivo")
    print(f"  Tensión nominal / Frecuencia:     400 / 230 V trifásico | 60 Hz")
    print(f"  Corriente nominal:                {I_nominal:.1f} A")
    print(f"  Número de polos:                  6 polos (1,200 RPM)")
    print(f"  Sistema de excitación:            Sin escobillas (Brushless) con imanes permanentes (PMG)")
    print(f"  Regulador de voltaje (AVR):       Digital de estado sólido, precisión ± 0.5%")
    print(f"  Clase de aislamiento:             Clase H (elevación de temperatura Clase F)")
    print(f"  Grado de protección / Enfriamiento: IP54 / IC01 (Auto-ventilado)")
    print(f"  Rendimiento a plena carga:        {eta_generador*100:.1f} %")

    # 3. Sistema de Regulación Electrónica de Carga (ELC)
    print(f"\n[SISTEMA DE REGULACIÓN Y CONTROL ELECTRÓNICO (ELC)]")
    print(f"  Principio de funcionamiento:      Modulación por ancho de pulsos (PWM) con transistores IGBT")
    print(f"  Capacidad del banco resistivo:    120 kW (120% de la potencia nominal)")
    print(f"  Estabilidad de frecuencia:        60.0 Hz ± 0.2 Hz ante variaciones escalón de carga de 0 a 100%")
    print(f"  Disipación de calor del balasto:  Refrigeración por agua en tanque secundario acoplado al canal de fuga")

if __name__ == "__main__":
    diseno_electromecanico()
