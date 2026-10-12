"""
Módulo de Simulación de Transitorios Hidráulicos y Golpe de Ariete.
Implementa el cálculo de celeridad de onda elástica, sobrepresión por fórmulas
de Allievi y Joukowsky, envolvente de presiones y espesor de pared de acero ASTM A36.
"""

import os
import math
from typing import Dict, Any, Optional
import numpy as np
import matplotlib.pyplot as plt


def calcular_celeridad(D: float, e: float) -> float:
    """
    Calcula la celeridad (velocidad de propagación) de la onda de presión en la tubería forzada.

    Fórmula de Allievi: a = sqrt( K / (rho * (1 + (K / E) * (D / e))) )

    Args:
        D: Diámetro interior de la tubería en metros (ej. 0.250 m).
        e: Espesor de la pared de la tubería en metros (ej. 0.005 m).

    Returns:
        Celeridad de onda 'a' en m/s.
    """
    if D <= 0 or e <= 0:
        raise ValueError("El diámetro y el espesor deben ser mayores a cero.")

    k_agua = 2.19e9    # Módulo de elasticidad volumétrica del agua (Pa)
    e_acero = 2.06e11  # Módulo de elasticidad de Young para acero ASTM A36 (Pa)
    rho_agua = 1000.0  # Densidad del agua (kg/m³)

    termino_deformacion = 1.0 + (k_agua / e_acero) * (D / e)
    a = math.sqrt(k_agua / (rho_agua * termino_deformacion))
    return float(round(a, 2))


def calcular_sobrepresion(
    L: float,
    v: float,
    tc: float,
    Hb: float = 115.0,
    D: float = 0.250,
    e: float = 0.005
) -> Dict[str, Any]:
    """
    Calcula el tiempo crítico de reflexión y la sobrepresión máxima por golpe de ariete.

    Args:
        L: Longitud de la tubería forzada en metros.
        v: Velocidad del agua en régimen permanente en m/s.
        tc: Tiempo de maniobra o cierre de las toberas/válvula en segundos.
        Hb: Salto bruto estático en metros.
        D: Diámetro interior de la tubería en metros.
        e: Espesor nominal de pared en metros.

    Returns:
        Diccionario con celeridad, tiempo crítico, tipo de maniobra, sobrepresión (delta_H) y presión máxima (H_max).
    """
    if L <= 0 or v <= 0 or tc <= 0:
        raise ValueError("L, v y tc deben ser estrictamente positivos.")

    g = 9.81
    a = calcular_celeridad(D, e)
    tc_critico = (2.0 * L) / a

    if tc > tc_critico:
        # Cierre lento: Fórmula de Allievi lineal
        tipo_maniobra = "CIERRE LENTO (Allievi)"
        delta_h = (2.0 * L * v) / (g * tc)
    else:
        # Cierre rápido: Fórmula de Joukowsky
        tipo_maniobra = "CIERRE RÁPIDO (Joukowsky)"
        delta_h = (a * v) / g

    h_max = Hb + delta_h

    return {
        "celeridad_m_s": a,
        "tiempo_critico_reflexion_s": round(tc_critico, 4),
        "tiempo_cierre_maniobra_s": round(tc, 2),
        "relacion_tiempo_cierre": round(tc / tc_critico, 2),
        "tipo_maniobra": tipo_maniobra,
        "sobrepresion_delta_H_m": round(delta_h, 2),
        "sobrepresion_porcentaje_salto": round((delta_h / Hb) * 100.0, 2),
        "presion_maxima_H_max_m": round(h_max, 2),
        "presion_maxima_bar": round(h_max / 10.197, 2)
    }


def espesor_requerido(H_max: float, D: float, sigma_adm: float = 125.0e6) -> float:
    """
    Calcula el espesor mínimo requerido de chapa de acero bajo presión máxima interna
    según la fórmula de calderería con sobreespesor por corrosión de 1.5 mm.

    Fórmula: e = (H_max * gamma_agua * D) / (2 * sigma_adm) + e_corrosion

    Args:
        H_max: Presión máxima estática más golpe de ariete en metros de columna de agua.
        D: Diámetro interior en metros.
        sigma_adm: Esfuerzo admisible del acero en Pascales (ASTM A36: Fy/2 = 250 MPa / 2 = 125 MPa).

    Returns:
        Espesor total requerido en milímetros (mm).
    """
    gamma_agua = 9810.0  # N/m³
    e_corrosion = 0.0015  # 1.5 mm margen de corrosión
    e_calc_m = (H_max * gamma_agua * D) / (2.0 * sigma_adm) + e_corrosion
    return float(round(e_calc_m * 1000.0, 2))


def perfil_presiones(
    L: float,
    D: float,
    Hb: float,
    terreno: Optional[np.ndarray] = None,
    delta_h: Optional[float] = None,
    tc: float = 4.0,
    cota_camara: float = 2417.8
) -> Dict[str, Any]:
    """
    Genera los vectores de elevación del terreno y piezométricas estáticas y dinámicas.

    Args:
        L: Longitud de tubería en metros.
        D: Diámetro interior en metros.
        Hb: Salto bruto en metros.
        terreno: Vector opcional de cotas del terreno. Si es None, se calcula perfil topográfico cóncavo real.
        delta_h: Sobrepresión máxima en tobera. Si es None, se calcula con tc=4.0 s.
        tc: Tiempo de cierre en segundos.
        cota_camara: Cota topográfica de la cámara de carga en m.s.n.m.

    Returns:
        Diccionario con progresivas x, z_terreno, piezometrica estática y envolvente dinámica máxima.
    """
    puntos = 100
    x = np.linspace(0, L, puntos)

    if terreno is None:
        # Perfil parabólico-cóncavo característico de ladera andina
        z_terreno = cota_camara - (Hb * ((x / L) ** 1.2))
    else:
        z_terreno = terreno

    if delta_h is None:
        v0 = 0.125 / ((math.pi * (D ** 2)) / 4.0)
        ariete = calcular_sobrepresion(L, v0, tc, Hb=Hb, D=D)
        delta_h = ariete["sobrepresion_delta_H_m"]

    presion_estatica = cota_camara - z_terreno
    presion_dinamica_max = presion_estatica + delta_h * (x / L)
    cota_casa_maquinas = cota_camara - Hb

    return {
        "x_progresiva": x,
        "z_terreno": z_terreno,
        "presion_estatica": presion_estatica,
        "presion_dinamica_max": presion_dinamica_max,
        "linea_piezometrica_estatica": z_terreno + presion_estatica,
        "linea_piezometrica_dinamica": z_terreno + presion_dinamica_max,
        "delta_h_max": delta_h,
        "cota_camara": cota_camara,
        "cota_casa_maquinas": cota_casa_maquinas,
        "longitud": L,
        "salto_bruto": Hb
    }


def graficar_perfil(perfil: Dict[str, Any], ruta_salida: str) -> str:
    """
    Genera el gráfico del perfil longitudinal de la tubería forzada con la envolvente
    de sobrepresión por golpe de ariete.

    Args:
        perfil: Diccionario devuelto por perfil_presiones().
        ruta_salida: Ruta del archivo PNG donde guardar el gráfico.

    Returns:
        Ruta del archivo guardado.
    """
    x = perfil["x_progresiva"]
    z_terreno = perfil["z_terreno"]
    piezo_estatica = perfil["linea_piezometrica_estatica"]
    piezo_dinamica = perfil["linea_piezometrica_dinamica"]
    presion_dinamica = perfil["presion_dinamica_max"]
    h_max = float(np.max(presion_dinamica))

    directorio = os.path.dirname(ruta_salida)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)

    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(x, z_terreno, color="black", lw=2, label="Perfil Tubería Forzada (Terreno)")
    plt.plot(x, piezo_estatica, color="navy", linestyle="--", lw=1.5, label=f"Línea Piezométrica Estática (Hb = {perfil['salto_bruto']:.1f} m)")
    plt.plot(x, piezo_dinamica, color="crimson", lw=2, label=f"Línea de Presión Máxima con Ariete (Pmax = {h_max:.1f} m)")

    plt.fill_between(x, z_terreno, piezo_dinamica, color="#FFCCCC", alpha=0.35, label="Zona de Solicitación de Presión")

    plt.title("Perfil Longitudinal y Envolvente de Sobrepresión por Golpe de Ariete\nMCH Río Blanco 100 kW (Puno)", fontsize=12, fontweight="bold")
    plt.xlabel("Progresiva a lo largo de la Tubería Forzada (m)", fontsize=11)
    plt.ylabel("Elevación (m.s.n.m.)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(frameon=True, facecolor="#F9FBFD", edgecolor="#BFBFBF")
    plt.tight_layout()

    plt.savefig(ruta_salida)
    plt.close()

    return ruta_salida
