"""
Módulo de Dimensionamiento Hidráulico y Electromecánico Integral.
Contiene funciones puras para el cálculo de canales, tuberías forzadas,
pérdidas de carga y grupos turbina-generador.
"""

import math
from typing import Dict, Any


def potencia_hidraulica(Q: float, Hn: float, eta: float) -> float:
    """
    Calcula la potencia hidráulica generada en kilovatios (kW).

    Args:
        Q: Caudal volumétrico en m³/s.
        Hn: Salto o caída neta en metros.
        eta: Rendimiento global o del componente analizado (fracción adimensional, 0-1).

    Returns:
        Potencia calculada en kW.
    """
    rho = 1000.0  # Densidad del agua (kg/m³)
    g = 9.81      # Aceleración gravitacional (m/s²)
    return (rho * g * Q * Hn * eta) / 1000.0


def salto_neto(Hb: float, hf: float, hm: float) -> float:
    """
    Calcula el salto neto restando las pérdidas por fricción y singulares del salto bruto.

    Args:
        Hb: Salto bruto estático en metros.
        hf: Pérdidas por fricción a lo largo de la tubería en metros.
        hm: Pérdidas menores o singulares (accesorios, codos, válvulas) en metros.

    Returns:
        Salto neto disponible Hn en metros.
    """
    return Hb - (hf + hm)


def velocidad_tubo(Q: float, D: float) -> float:
    """
    Calcula la velocidad media del flujo dentro de una conducción circular a presión.

    Args:
        Q: Caudal en m³/s.
        D: Diámetro interior de la tubería en metros.

    Returns:
        Velocidad media en m/s.
    """
    if D <= 0:
        raise ValueError("El diámetro de la tubería debe ser estrictamente positivo.")
    area = (math.pi * (D ** 2)) / 4.0
    return Q / area


def perdidas_darcy(Q: float, D: float, L: float, k_rug: float) -> float:
    """
    Calcula las pérdidas de carga continuas por fricción según Darcy-Weisbach y Swamee-Jain.

    Args:
        Q: Caudal en m³/s.
        D: Diámetro interior de la tubería en metros.
        L: Longitud total de la tubería en metros.
        k_rug: Rugosidad absoluta del material en metros (ej. 0.000045 m para acero).

    Returns:
        Pérdida de carga continua hf en metros de columna de agua.
    """
    g = 9.81
    nu = 1.23e-6  # Viscosidad cinemática del agua a aprox. 12 °C (m²/s)
    v = velocidad_tubo(Q, D)
    reynolds = (v * D) / nu

    # Fórmula explícita de Swamee-Jain para régimen turbulento
    f_darcy = 0.25 / (math.log10((k_rug / (3.7 * D)) + (5.74 / (reynolds ** 0.9)))) ** 2
    hf = f_darcy * (L / D) * ((v ** 2) / (2.0 * g))
    return hf


def dimensionamiento_canal(Q: float, n: float, S: float, b: float) -> Dict[str, Any]:
    """
    Dimensiona un canal de conducción rectangular mediante la ecuación de Manning
    resolviendo el tirante normal por método de Newton-Raphson.

    Args:
        Q: Caudal de diseño en m³/s.
        n: Coeficiente de rugosidad de Manning (adimensional, ej. 0.014 para concreto liso).
        S: Pendiente longitudinal de la solera del canal (m/m, ej. 0.0015).
        b: Ancho de la solera del canal en metros.

    Returns:
        Diccionario con tirante normal, velocidad, número de Froude, borde libre y régimen de flujo.
    """
    g = 9.81
    y = 0.1  # Valor semilla inicial

    for _ in range(100):
        area = b * y
        perimetro = b + 2.0 * y
        radio_hid = area / perimetro
        q_calc = (1.0 / n) * area * (radio_hid ** (2.0 / 3.0)) * math.sqrt(S)
        diff = q_calc - Q
        if abs(diff) < 1e-6:
            break
        y -= diff / 1.5

    velocidad = Q / (b * y)
    froude = velocidad / math.sqrt(g * y)
    regimen = "Subcrítico" if froude < 1.0 else ("Supercrítico" if froude > 1.0 else "Crítico")
    bordo_libre = max(0.20, round(0.30 * y + 0.15, 2))

    return {
        "ancho_solera_m": b,
        "tirante_normal_m": round(y, 4),
        "area_hidraulica_m2": round(b * y, 4),
        "perimetro_mojado_m": round(b + 2.0 * y, 4),
        "radio_hidraulico_m": round((b * y) / (b + 2.0 * y), 4),
        "velocidad_m_s": round(velocidad, 3),
        "numero_froude": round(froude, 3),
        "regimen_flujo": regimen,
        "bordo_libre_m": bordo_libre,
        "altura_total_canal_m": round(y + bordo_libre, 3)
    }


def dimensionamiento_tuberia(
    Q: float,
    Hb: float,
    L: float = 380.0,
    k_rug: float = 0.000045,
    D_adoptado: float = 0.250
) -> Dict[str, Any]:
    """
    Dimensiona la tubería forzada calculando el diámetro económico (Fahlbusch),
    las pérdidas por fricción (Darcy-Weisbach) y singulares, y el salto neto resultante.

    Args:
        Q: Caudal en m³/s.
        Hb: Salto bruto estático en metros.
        L: Longitud de la tubería forzada en metros.
        k_rug: Rugosidad absoluta en metros (acero = 0.000045 m).
        D_adoptado: Diámetro interior comercial adoptado en metros (ej. 0.250 m / 10 pulg).

    Returns:
        Diccionario con diámetros, velocidades, pérdidas y salto neto.
    """
    g = 9.81
    nu = 1.23e-6

    # Diámetro económico según ecuación de Fahlbusch
    d_fahlbusch = 0.52 * (Q ** 0.43) * (Hb ** 0.14)
    v_tub = velocidad_tubo(Q, D_adoptado)
    reynolds = (v_tub * D_adoptado) / nu

    f_darcy = 0.25 / (math.log10((k_rug / (3.7 * D_adoptado)) + (5.74 / (reynolds ** 0.9)))) ** 2
    hf = f_darcy * (L / D_adoptado) * ((v_tub ** 2) / (2.0 * g))
    hm = 0.15 * hf  # Pérdidas menores por singularidades (codos, válvulas, transición)
    htot = hf + hm
    hn = salto_neto(Hb, hf, hm)

    return {
        "diametro_economico_fahlbusch_m": round(d_fahlbusch, 4),
        "diametro_adoptado_m": round(D_adoptado, 4),
        "velocidad_m_s": round(v_tub, 3),
        "numero_reynolds": round(reynolds, 0),
        "factor_friccion_darcy": round(f_darcy, 4),
        "perdidas_friccion_hf_m": round(hf, 2),
        "perdidas_singulares_hm_m": round(hm, 2),
        "perdidas_totales_m": round(htot, 2),
        "perdida_relativa_pct": round((htot / Hb) * 100.0, 2),
        "salto_neto_m": round(hn, 2),
        "longitud_tuberia_m": L
    }


def calcular_grupo_turbina_generador(
    Q: float,
    Hn: float,
    Hb: float = 115.0,
    z_inyectores: int = 2,
    N_rpm: float = 1200.0
) -> Dict[str, Any]:
    """
    Calcula los parámetros característicos y de desempeño del conjunto Turbina Pelton - Generador.

    Args:
        Q: Caudal nominal turbinado en m³/s.
        Hn: Salto neto en metros.
        Hb: Salto bruto en metros (para rendimiento global agua-red).
        z_inyectores: Número de toberas/inyectores de la turbina.
        N_rpm: Velocidad sincrónica de rotación en RPM.

    Returns:
        Diccionario con dimensiones de tobera, rodete, cucharas, eficiencias y potencias mecánicas/eléctricas.
    """
    rho = 1000.0
    g = 9.81
    cv = 0.97  # Coeficiente de velocidad de tobera

    q_inyector = Q / float(z_inyectores)
    v_chorro = cv * math.sqrt(2.0 * g * Hn)
    d_chorro = math.sqrt((4.0 * q_inyector) / (math.pi * v_chorro))

    # Velocidad periférica tangencial óptima (u ≈ 0.46 * c1)
    u_tangencial = 0.46 * v_chorro
    d_rodete = (60.0 * u_tangencial) / (math.pi * N_rpm)
    rel_d_d = d_rodete / d_chorro
    num_cucharas = int(round(d_rodete / (2.0 * d_chorro) + 15))

    eta_turb = 0.88
    eta_gen = 0.93
    eta_trans = 0.98
    eta_global = (Hn / Hb) * eta_turb * eta_gen * eta_trans

    p_hidraulica = (rho * g * Q * Hn) / 1000.0
    p_mecanica = p_hidraulica * eta_turb
    p_electrica = p_mecanica * eta_gen
    p_red = p_electrica * eta_trans

    return {
        "numero_inyectores": z_inyectores,
        "caudal_por_inyector_m3s": round(q_inyector, 4),
        "velocidad_chorro_m_s": round(v_chorro, 2),
        "diametro_chorro_m": round(d_chorro, 4),
        "velocidad_rotacion_rpm": N_rpm,
        "velocidad_tangencial_u_m_s": round(u_tangencial, 2),
        "diametro_primitivo_rodete_m": round(d_rodete, 4),
        "relacion_diametros_D_d": round(rel_d_d, 2),
        "numero_cucharas": num_cucharas,
        "eficiencia_turbina": eta_turb,
        "eficiencia_generador": eta_gen,
        "eficiencia_transformador": eta_trans,
        "eficiencia_global": round(eta_global, 4),
        "potencia_hidraulica_kw": round(p_hidraulica, 2),
        "potencia_mecanica_eje_kw": round(p_mecanica, 2),
        "potencia_electrica_bornes_kw": round(p_electrica, 2),
        "potencia_neta_red_kw": round(p_red, 2)
    }
