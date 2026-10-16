"""
Módulo de Selección y Análisis de Turbinas Hidráulicas.
Contiene tablas de clasificación por salto y caudal, cálculo de velocidad específica
y torque en el eje motriz.
"""

import math
from typing import Dict, Any


def velocidad_especifica(N: float, Q: float, H: float) -> float:
    """
    Calcula la velocidad específica dimensional (Ns en función del caudal) de una turbina.

    Fórmula: Ns = N * sqrt(Q) / (H^(3/4))

    Args:
        N: Velocidad de rotación en RPM.
        Q: Caudal volumétrico en m³/s.
        H: Salto neto o salto de diseño en metros.

    Returns:
        Velocidad específica Ns (rpm, m³/s, m).
    """
    if H <= 0 or Q <= 0 or N <= 0:
        raise ValueError("Los valores de N, Q y H deben ser estrictamente mayores a cero.")
    return float(N * math.sqrt(Q) / (H ** 0.75))


def kurier(N: float, P: float) -> float:
    """
    Calcula el torque o cupla motriz en el eje a partir de la potencia y la velocidad de rotación.

    Fórmula: T = (P * 1000) / omega = (P * 1000 * 60) / (2 * pi * N)

    Args:
        N: Velocidad de rotación en RPM.
        P: Potencia en el eje en kilovatios (kW).

    Returns:
        Torque en Newtons por metro (N·m).
    """
    if N <= 0:
        raise ValueError("La velocidad de rotación debe ser mayor a cero.")
    omega = (2.0 * math.pi * N) / 60.0
    torque = (P * 1000.0) / omega
    return float(round(torque, 2))


def seleccionar_turbina(caudal: float, salto: float) -> Dict[str, Any]:
    """
    Selecciona la tecnología de turbina óptima en base a la caída disponible y el caudal de diseño.

    Tabla de criterios técnicos:
      * Salto > 200m y Q < 2 m³/s (o microcentrales H >= 50m y Q <= 0.2 m³/s) → Pelton (Ns 10-35)
      * Salto 50-200m y Q 2-50 m³/s → Francis (Ns 60-300)
      * Salto < 50m y Q > 20 m³/s → Kaplan (Ns 300-1000)
      * Salto 100-500m y Q < 5 m³/s → Turgo (Ns 30-70)
      * Salto < 10m y Q > 10 m³/s → Tornillo de Arquímedes (Ns > 700)

    Args:
        caudal: Caudal de diseño nominal en m³/s.
        salto: Salto neto o bruto en metros.

    Returns:
        Diccionario con tipo de turbina, velocidad específica estimada,
        rangos de aplicación y eficiencia típica recomendada.
    """
    if caudal <= 0 or salto <= 0:
        raise ValueError("El caudal y el salto deben ser mayores a cero.")

    # Selección según rangos normativos e industriales
    if (salto > 200.0 and caudal < 2.0) or (salto >= 50.0 and caudal <= 0.20):
        tipo = "Pelton"
        ns_rango = "10 - 35"
        rango_caudales = "< 2.0 m³/s"
        rango_saltos = "> 50 m (típicamente > 150-200 m)"
        eficiencia_tipica = 0.88
        descripcion = "Turbina de acción/impulso ideal para altos saltos y caudales reducidos con inyectores variables."
    elif 100.0 <= salto <= 500.0 and caudal < 5.0:
        tipo = "Turgo"
        ns_rango = "30 - 70"
        rango_caudales = "< 5.0 m³/s"
        rango_saltos = "100 - 500 m"
        eficiencia_tipica = 0.86
        descripcion = "Turbina de acción de chorro inclinado, velocidad angular más elevada que Pelton."
    elif 50.0 <= salto <= 200.0 and 2.0 <= caudal <= 50.0:
        tipo = "Francis"
        ns_rango = "60 - 300"
        rango_caudales = "2 - 50 m³/s"
        rango_saltos = "50 - 200 m"
        eficiencia_tipica = 0.91
        descripcion = "Turbina de reacción de flujo mixto centrípeto, excelente rendimiento a plena carga."
    elif salto < 50.0 and caudal > 20.0:
        tipo = "Kaplan"
        ns_rango = "300 - 1000"
        rango_caudales = "> 20 m³/s"
        rango_saltos = "< 50 m"
        eficiencia_tipica = 0.92
        descripcion = "Turbina de reacción axial con álabes orientables para grandes caudales y bajo salto."
    elif salto < 10.0 and caudal > 10.0:
        tipo = "Tornillo de Arquímedes"
        ns_rango = "> 700"
        rango_caudales = "> 10 m³/s"
        rango_saltos = "< 10 m"
        eficiencia_tipica = 0.80
        descripcion = "Generación hidroeléctrica de muy baja caída, amigable con la fauna ictícola."
    elif salto < 50.0 and caudal <= 20.0:
        tipo = "Michell-Banki (Flujo Cruzado)"
        ns_rango = "40 - 200"
        rango_caudales = "0.05 - 5 m³/s"
        rango_saltos = "5 - 50 m"
        eficiencia_tipica = 0.82
        descripcion = "Turbina de flujo transversal simple de construir y mantener para microcentrales."
    else:
        # Asignación por umbral de salto general
        if salto >= 150.0:
            tipo = "Pelton"
            ns_rango = "10 - 35"
            rango_caudales = "< 2.0 m³/s"
            rango_saltos = "> 150 m"
            eficiencia_tipica = 0.88
            descripcion = "Turbina de acción seleccionada por predominancia de caída alta."
        elif salto >= 40.0:
            tipo = "Francis"
            ns_rango = "60 - 300"
            rango_caudales = "1 - 50 m³/s"
            rango_saltos = "40 - 200 m"
            eficiencia_tipica = 0.90
            descripcion = "Turbina de reacción seleccionada para salto medio."
        else:
            tipo = "Kaplan / Tubular"
            ns_rango = "300 - 1000"
            rango_caudales = "Variable"
            rango_saltos = "< 40 m"
            eficiencia_tipica = 0.89
            descripcion = "Turbina de baja caída para flujo axial."

    return {
        "tipo": tipo,
        "velocidad_especifica": ns_rango,
        "rango_caudales": rango_caudales,
        "rango_saltos": rango_saltos,
        "eficiencia_tipica": eficiencia_tipica,
        "descripcion": descripcion,
        "caudal_consultado_m3s": caudal,
        "salto_consultado_m": salto
    }
