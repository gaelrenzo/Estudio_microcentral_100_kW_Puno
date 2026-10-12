#!/usr/bin/env python3
"""
Módulo de Dimensionamiento Hidráulico y Electromecánico Integral
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Puno
"""
import math

def dimensionamiento():
    print("================================================================")
    print("DIMENSIONAMIENTO DE COMPONENTES HIDRÁULICOS Y ELECTROMECÁNICOS")
    print("================================================================")
    
    # 1. Datos iniciales
    Qd = 0.125  # m3/s
    Hb = 115.0  # m
    L_canal = 450.0 # m
    L_tub = 380.0   # m
    rho = 1000.0    # kg/m3
    g = 9.81        # m/s2
    
    # 2. Conducción (Canal Manning)
    n_manning = 0.014
    S_canal = 0.0015
    b_canal = 0.50
    # Iteración para tirante yn en canal rectangular
    # Qd = (1/n) * (b*y) * ((b*y)/(b+2*y))^(2/3) * S^(1/2)
    y = 0.1
    for _ in range(100):
        A = b_canal * y
        P = b_canal + 2 * y
        R = A / P
        Q_calc = (1.0 / n_manning) * A * (R ** (2.0 / 3.0)) * math.sqrt(S_canal)
        diff = Q_calc - Qd
        if abs(diff) < 1e-5:
            break
        # Newton derivative approx
        y -= diff / 1.5
    v_canal = Qd / (b_canal * y)
    Fr = v_canal / math.sqrt(g * y)
    
    print(f"[CANAL RECTANGULAR]")
    print(f"  Ancho b: {b_canal:.2f} m | Tirante yn: {y:.3f} m | Bordo libre: 0.28 m")
    print(f"  Velocidad media: {v_canal:.3f} m/s | Froude: {Fr:.3f} (Subcrítico)")
    
    # 3. Tubería Forzada
    # Diámetro económico Fahlbusch: D = 0.52 * Qd^0.43 * Hb^0.14
    D_fahl = 0.52 * (Qd ** 0.43) * (Hb ** 0.14)
    D_int = 0.250 # 250 mm comercial
    v_tub = (4.0 * Qd) / (math.pi * (D_int ** 2))
    
    # Pérdidas de carga (Darcy-Weisbach)
    k_rug = 0.000045 # m (acero)
    # Swamee-Jain para factor f
    Re = (v_tub * D_int) / 1.23e-6 # a 12 C
    f_darcy = 0.25 / (math.log10((k_rug / (3.7 * D_int)) + (5.74 / (Re ** 0.9)))) ** 2
    hf = f_darcy * (L_tub / D_int) * ((v_tub ** 2) / (2.0 * g))
    hm = 0.15 * hf # Pérdidas localizadas (codos, rejilla, válvula)
    htot = hf + hm
    Hn = Hb - htot
    
    print(f"\n[TUBERÍA FORZADA]")
    print(f"  Diámetro Fahlbusch: {D_fahl:.3f} m | Diámetro adoptado: {D_int:.3f} m (10 pulg)")
    print(f"  Velocidad: {v_tub:.3f} m/s | Reynolds: {Re:.0f} | Coef. fricción f: {f_darcy:.4f}")
    print(f"  Pérdida por fricción hf: {hf:.2f} m | Pérdidas acc. hm: {hm:.2f} m | Pérdida total: {htot:.2f} m ({htot/Hb*100:.1f}%)")
    print(f"  Caída neta Hn: {Hn:.2f} m")
    
    # 4. Turbina Pelton
    z_inyectores = 2
    q_iny = Qd / z_inyectores
    Cv = 0.97
    v_chorro = Cv * math.sqrt(2.0 * g * Hn)
    d_chorro = math.sqrt((4.0 * q_iny) / (math.pi * v_chorro))
    
    # Velocidad sincrónica generador 6 polos a 60 Hz = 1200 rpm
    N_rpm = 1200.0
    u_tangencial = 0.46 * v_chorro
    D_rodete = (60.0 * u_tangencial) / (math.pi * N_rpm)
    rel_D_d = D_rodete / d_chorro
    num_cucharas = int(round(D_rodete / (2.0 * d_chorro) + 15))
    
    eta_turb = 0.88
    eta_gen = 0.93
    eta_trans = 0.98
    eta_global = (Hn / Hb) * eta_turb * eta_gen * eta_trans
    
    P_mec = rho * g * Qd * Hn * eta_turb / 1000.0 # kW
    P_elec = P_mec * eta_gen # kW
    P_red = P_elec * eta_trans # kW
    
    print(f"\n[TURBINA PELTON & GENERADOR]")
    print(f"  Número de inyectores: {z_inyectores} | Caudal por inyector: {q_iny*1000:.1f} L/s")
    print(f"  Velocidad del chorro: {v_chorro:.2f} m/s | Diámetro de tobera d0: {d_chorro*1000:.1f} mm")
    print(f"  Velocidad sincrónica N: {N_rpm:.0f} RPM (6 polos, 60 Hz)")
    print(f"  Diámetro primitivo del rodete D1: {D_rodete*1000:.1f} mm | Relación D1/d0: {rel_D_d:.2f}")
    print(f"  Número de cucharas: {num_cucharas}")
    print(f"  Potencia mecánica en eje: {P_mec:.2f} kW")
    print(f"  Potencia eléctrica en bornes generador: {P_elec:.2f} kW")
    print(f"  Potencia neta entregada a red: {P_red:.2f} kW (~100 kW nominal)")
    print(f"  Rendimiento global agua-red: {eta_global*100:.2f}%")

if __name__ == "__main__":
    dimensionamiento()
