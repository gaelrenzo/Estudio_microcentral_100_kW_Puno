"""
Módulo de Ingeniería Eléctrica y Evaluación Energética.
Contiene el cálculo de transformadores, estimación de energía anual, factor de planta,
pérdidas de transmisión y selección de niveles de tensión según normativa.
"""

import math
from typing import Dict, Any, List
import numpy as np


def tensionConexion(P_kw: float) -> str:
    """
    Determina el nivel de tensión reglamentario para la interconexión al sistema eléctrico
    conforme a los criterios del Código Nacional de Electricidad (CNE) y normas DGE/MINEM.

    Args:
        P_kw: Potencia nominal neta de la central en kilovatios (kW).

    Returns:
        Cadena con la clasificación y rango de tensión recomendado.
    """
    if P_kw <= 0:
        raise ValueError("La potencia debe ser estrictamente positiva.")

    if P_kw <= 10.0:
        return "Baja Tensión Monofásica (220 V / 0.22 kV)"
    elif P_kw <= 50.0:
        return "Baja Tensión Trifásica (380/220 V / 0.38 kV)"
    elif P_kw <= 500.0:
        return "Media Tensión Rural/Urbana (10.0 kV / 13.2 kV / 22.9 kV)"
    elif P_kw <= 10000.0:
        return "Media Tensión (22.9 kV / 33.0 kV)"
    else:
        return "Alta Tensión (60 kV / 138 kV / 220 kV)"


def calcular_transformador(
    potencia_kw: float,
    tension_kv: float,
    cos_phi: float = 0.85,
    tension_baja_kv: float = 0.400
) -> Dict[str, Any]:
    """
    Calcula la potencia aparente requerida, adopta la capacidad comercial normalizada
    y calcula las corrientes nominales en alta y baja tensión.

    Args:
        potencia_kw: Potencia activa generada en kW.
        tension_kv: Tensión primaria / interconexión en kV (ej. 10.0 kV o 22.9 kV).
        cos_phi: Factor de potencia nominal del generador sincrónico (típico 0.85).
        tension_baja_kv: Tensión en bornes de generación en kV (típico 0.400 kV / 400 V).

    Returns:
        Diccionario con potencia en kVA comercial, tensiones y corrientes nominales.
    """
    if potencia_kw <= 0 or tension_kv <= 0:
        raise ValueError("La potencia y la tensión deben ser positivas.")

    potencia_aparente_calculada = potencia_kw / cos_phi

    # Capacidades comerciales estándar normalizadas (IEC / ITINTEC)
    capacidades_comerciales = [
        15, 25, 37.5, 50, 75, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250
    ]

    capacidad_adoptada = next(
        (cap for cap in capacidades_comerciales if cap >= potencia_aparente_calculada),
        math.ceil(potencia_aparente_calculada / 50.0) * 50.0
    )

    # Corrientes nominales trifásicas
    # I = S / (sqrt(3) * V)
    corriente_baja = (capacidad_adoptada) / (math.sqrt(3.0) * tension_baja_kv)
    corriente_alta = (capacidad_adoptada) / (math.sqrt(3.0) * tension_kv)

    return {
        "potencia_activa_kw": potencia_kw,
        "factor_potencia": cos_phi,
        "potencia_aparente_calculada_kva": round(potencia_aparente_calculada, 2),
        "potencia_nominal_transformador_kva": capacidad_adoptada,
        "tension_primaria_alta_kv": tension_kv,
        "tension_secundaria_baja_kv": tension_baja_kv,
        "corriente_nominal_baja_a": round(corriente_baja, 2),
        "corriente_nominal_alta_a": round(corriente_alta, 2),
        "frecuencia_hz": 60
    }


def factor_planta(energia_anual_mwh: float, potencia_nominal_kw: float) -> float:
    """
    Calcula el Factor de Planta anual (adimensional, entre 0 y 1).

    Fórmula: FP = (Energía_MWh * 1000) / (Potencia_kW * 8760 horas)

    Args:
        energia_anual_mwh: Generación neta anual en MWh.
        potencia_nominal_kw: Potencia nominal de placa instalada en kW.

    Returns:
        Factor de planta en valor decimal (ej. 0.768).
    """
    if potencia_nominal_kw <= 0:
        raise ValueError("La potencia nominal debe ser mayor a cero.")
    horas_anio = 8760.0
    return float(round((energia_anual_mwh * 1000.0) / (potencia_nominal_kw * horas_anio), 4))


def energia_anual(
    caudales: np.ndarray,
    potencia_nominal_kw: float,
    q_diseno: float = 0.125,
    q_eco: float = 0.030,
    hb: float = 115.0,
    eta_global: float = 0.73
) -> Dict[str, Any]:
    """
    Calcula la generación de energía anual simulando día a día a partir de la serie histórica
    restando el caudal ecológico y limitando al caudal de diseño.

    Args:
        caudales: Array de caudales diarios registrados en m³/s.
        potencia_nominal_kw: Potencia nominal instalada en kW (ej. 100 kW).
        q_diseno: Caudal máximo admisible por la turbina en m³/s.
        q_eco: Caudal ecológico reservado en el cauce en m³/s.
        hb: Salto bruto en metros.
        eta_global: Rendimiento total de conversión agua a red eléctrica.

    Returns:
        Diccionario con energía anual en MWh, kWh, factor de planta y horas equivalentes.
    """
    if len(caudales) == 0:
        raise ValueError("El arreglo de caudales no puede estar vacío.")

    # Caudal disponible para turbinar
    q_disponible = np.maximum(0.0, caudales - q_eco)
    q_turbinado = np.minimum(q_disponible, q_diseno)

    # Potencia diaria en kW: P = 9.81 * Q * H * eta
    p_diaria = np.minimum(potencia_nominal_kw, 9.81 * q_turbinado * hb * eta_global)
    energia_diaria_kwh = p_diaria * 24.0

    # Promedio anual equivalente
    total_dias = len(caudales)
    energia_total_kwh = float(np.sum(energia_diaria_kwh))
    energia_anual_kwh = (energia_total_kwh / total_dias) * 365.25
    energia_anual_mwh = energia_anual_kwh / 1000.0

    horas_equivalentes = energia_anual_kwh / potencia_nominal_kw
    fp = factor_planta(energia_anual_mwh, potencia_nominal_kw)

    return {
        "energia_anual_mwh": round(energia_anual_mwh, 2),
        "energia_anual_kwh": round(energia_anual_kwh, 2),
        "horas_equivalentes_plena_carga": round(horas_equivalentes, 1),
        "factor_planta": round(fp, 4),
        "factor_planta_pct": round(fp * 100.0, 2)
    }


def perdidas_electricas(
    potencia_kw: float,
    distancia_km: float,
    tension_kv: float,
    r_km: float = 0.54,
    cos_phi: float = 0.85
) -> float:
    """
    Estima las pérdidas de potencia por efecto Joule en la línea de media tensión.

    Args:
        potencia_kw: Potencia transmitida en kW.
        distancia_km: Longitud de la línea de evacuación en kilómetros.
        tension_kv: Nivel de tensión de transmisión entre fases en kV.
        r_km: Resistencia eléctrica del conductor en ohm/km (típico conductor AAAC 35 mm² ≈ 0.54 ohm/km).
        cos_phi: Factor de potencia de la carga.

    Returns:
        Pérdida de potencia en la línea en kW.
    """
    if tension_kv <= 0:
        raise ValueError("La tensión debe ser mayor a cero.")
    # Corriente de línea en Amperios: I = P_kW / (sqrt(3) * V_kV * cos_phi)
    corriente_a = potencia_kw / (math.sqrt(3.0) * tension_kv * cos_phi)
    resistencia_total = r_km * distancia_km
    # Pérdidas trifásicas Joule: P_perdidas = 3 * I^2 * R / 1000 (kW)
    perdidas_kw = 3.0 * (corriente_a ** 2) * resistencia_total / 1000.0
    return float(round(perdidas_kw, 3))
