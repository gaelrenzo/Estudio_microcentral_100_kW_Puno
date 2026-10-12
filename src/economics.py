"""
Módulo de Evaluación Económica y Financiera de Proyectos Hidroeléctricos.
Calcula indicadores de rentabilidad: VAN, TIR, Payback simple, LCOE (Levelized Cost of Energy)
y relación Beneficio/Costo.
"""

from typing import List, Dict, Any


def van(flujos: List[float], tasa: float) -> float:
    """
    Calcula el Valor Actual Neto (VAN / NPV) para una serie temporal de flujos de caja.

    Fórmula: VAN = sum( F_t / (1 + tasa)^t ) para t de 0 a N

    Args:
        flujos: Lista de flujos de efectivo. El elemento 0 es la inversión inicial negativa (-CAPEX).
        tasa: Tasa de descuento anual en valor decimal (ej. 0.10 para 10%).

    Returns:
        Valor Actual Neto en la moneda base (USD).
    """
    if tasa <= -1.0:
        raise ValueError("La tasa de descuento debe ser estrictamente mayor a -1.0.")
    valor_actual = sum(f / ((1.0 + tasa) ** t) for t, f in enumerate(flujos))
    return float(round(valor_actual, 2))


def tir(flujos: List[float]) -> float:
    """
    Calcula la Tasa Interna de Retorno (TIR / IRR) mediante el algoritmo de bisección.

    Args:
        flujos: Lista de flujos de efectivo con inversión inicial negativa en t=0.

    Returns:
        Tasa interna de retorno en porcentaje (ej. 16.24 para 16.24%).
    """
    if len(flujos) < 2 or flujos[0] >= 0:
        raise ValueError("Se requiere al menos una inversión inicial negativa en t=0.")

    def npv_rate(r: float) -> float:
        return sum(f / ((1.0 + r) ** t) for t, f in enumerate(flujos))

    # Búsqueda de intervalo con cambio de signo
    r_low = -0.50
    r_high = 2.00

    if npv_rate(r_low) * npv_rate(r_high) > 0:
        # Ampliar rango si es un proyecto de muy alta o baja rentabilidad
        r_high = 5.0

    for _ in range(120):
        r_mid = (r_low + r_high) / 2.0
        val_mid = npv_rate(r_mid)
        if abs(val_mid) < 1e-7:
            break
        if npv_rate(r_low) * val_mid <= 0:
            r_high = r_mid
        else:
            r_low = r_mid

    return float(round(r_mid * 100.0, 2))


def payback(capex: float, flujo_anual: float) -> float:
    """
    Calcula el período de recuperación simple de la inversión (Payback Period).

    Fórmula: Payback = CAPEX / Flujo_Neto_Anual

    Args:
        capex: Costo de capital inicial en USD (valor positivo).
        flujo_anual: Flujo neto de caja operativo anual promedio en USD.

    Returns:
        Tiempo de retorno en años.
    """
    if flujo_anual <= 0:
        return float("inf")
    return float(round(abs(capex) / flujo_anual, 2))


def lcoe(
    capex: float,
    opex_anual: float,
    energia_anual: float,
    horizonte: int,
    tasa: float
) -> float:
    """
    Calcula el Costo Nivelado de la Energía (LCOE - Levelized Cost of Energy).

    Fórmula: LCOE = (CAPEX + sum(OPEX_t / (1+r)^t)) / sum(Energía_t / (1+r)^t)

    Args:
        capex: Inversión inicial de capital en USD.
        opex_anual: Costo anual de operación y mantenimiento en USD.
        energia_anual: Energía eléctrica neta generada al año en kWh (o MWh según unidad deseada).
        horizonte: Vida útil del proyecto en años (ej. 25 o 30 años).
        tasa: Tasa de descuento anual en valor decimal (ej. 0.10).

    Returns:
        Costo nivelado por unidad de energía (USD/kWh).
    """
    if energia_anual <= 0 or horizonte <= 0:
        raise ValueError("La energía anual y el horizonte deben ser mayores a cero.")

    costo_actualizado = capex + sum(
        opex_anual / ((1.0 + tasa) ** t) for t in range(1, horizonte + 1)
    )
    energia_actualizada = sum(
        energia_anual / ((1.0 + tasa) ** t) for t in range(1, horizonte + 1)
    )

    return float(round(costo_actualizado / energia_actualizada, 4))


def evaluacion_completa(
    capex: float,
    opex_pct: float,
    potencia_kw: float,
    factor_planta: float,
    tarifa: float,
    horizonte: int,
    tasa_descuento: float = 0.10
) -> Dict[str, Any]:
    """
    Realiza la evaluación económica y financiera integral del proyecto hidroeléctrico.

    Args:
        capex: Inversión inicial total en USD (ej. 245,800 USD).
        opex_pct: Porcentaje anual de OPEX sobre el CAPEX (ej. 0.03 para 3%).
        potencia_kw: Potencia nominal de la central en kW (ej. 100 kW).
        factor_planta: Factor de planta esperado en decimal (ej. 0.768 para 76.8%).
        tarifa: Tarifa de venta de energía en USD/kWh (ej. 0.075 USD/kWh).
        horizonte: Horizonte temporal de evaluación en años (ej. 25 años).
        tasa_descuento: Tasa de descuento de costo de oportunidad de capital (ej. 0.10).

    Returns:
        Diccionario exhaustivo con todos los flujos e indicadores financieros:
        CAPEX, OPEX, Ingresos, Flujo Neto, VAN, TIR, Payback, LCOE y Relación B/C.
    """
    horas_anio = 8760.0
    opex_anual = capex * opex_pct
    generacion_kwh = potencia_kw * horas_anio * factor_planta
    generacion_mwh = generacion_kwh / 1000.0
    ingreso_anual = generacion_kwh * tarifa
    flujo_neto_anual = ingreso_anual - opex_anual

    flujos = [-capex] + [flujo_neto_anual] * horizonte

    van_proyecto = van(flujos, tasa_descuento)
    tir_proyecto = tir(flujos)
    payback_proyecto = payback(capex, flujo_neto_anual)
    lcoe_proyecto = lcoe(capex, opex_anual, generacion_kwh, horizonte, tasa_descuento)
    relacion_bc = round((van_proyecto + capex) / capex, 2)

    return {
        "capex_usd": round(capex, 2),
        "opex_anual_usd": round(opex_anual, 2),
        "opex_porcentaje": round(opex_pct * 100.0, 2),
        "potencia_instalada_kw": potencia_kw,
        "factor_planta": round(factor_planta, 4),
        "factor_planta_pct": round(factor_planta * 100.0, 2),
        "generacion_anual_kwh": round(generacion_kwh, 2),
        "generacion_anual_mwh": round(generacion_mwh, 2),
        "tarifa_venta_usd_kwh": tarifa,
        "tarifa_venta_usd_mwh": round(tarifa * 1000.0, 2),
        "ingreso_anual_usd": round(ingreso_anual, 2),
        "flujo_neto_anual_usd": round(flujo_neto_anual, 2),
        "horizonte_evaluacion_anios": horizonte,
        "tasa_descuento": tasa_descuento,
        "tasa_descuento_pct": round(tasa_descuento * 100.0, 2),
        "van_usd": van_proyecto,
        "tir_pct": tir_proyecto,
        "payback_anios": payback_proyecto,
        "lcoe_usd_kwh": lcoe_proyecto,
        "lcoe_usd_mwh": round(lcoe_proyecto * 1000.0, 2),
        "relacion_beneficio_costo": relacion_bc,
        "flujos_caja": flujos
    }
