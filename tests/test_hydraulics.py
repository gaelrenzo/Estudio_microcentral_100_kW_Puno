"""
Pruebas unitarias para el módulo hidráulico y electromecánico (src/hydraulics.py, turbines.py, transient.py).
Validadas con los datos de diseño de la Microcentral Río Blanco - Puno (100 kW).
"""

import os
import sys
import math
import pytest

# Asegurar que la raíz del proyecto esté en el path de búsqueda
RUTA_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RUTA_RAIZ not in sys.path:
    sys.path.insert(0, RUTA_RAIZ)

from src.hydraulics import (
    potencia_hidraulica,
    salto_neto,
    velocidad_tubo,
    perdidas_darcy,
    dimensionamiento_canal,
    dimensionamiento_tuberia
)
from src.turbines import seleccionar_turbina, velocidad_especifica, kurier
from src.transient import calcular_celeridad, calcular_sobrepresion, espesor_requerido


def test_potencia_hidraulica():
    """
    Verifica el cálculo de la potencia hidráulica con los parámetros del proyecto Puno:
    Q = 0.125 m³/s, Hn = 101.67 m, eta = 0.88.
    """
    q = 0.125
    hn = 101.67
    eta = 0.88
    # P = 9.81 * 0.125 * 101.67 * 0.88 ≈ 109.72 kW
    potencia = potencia_hidraulica(q, hn, eta)
    assert isinstance(potencia, float)
    assert 105.0 < potencia < 115.0
    assert pytest.approx(potencia, rel=1e-2) == 109.72


def test_salto_neto():
    """
    Verifica el cálculo del salto neto a partir del salto bruto Hb=115 m
    y las pérdidas hf=11.59 m, hm=1.74 m.
    """
    hb = 115.0
    hf = 11.59
    hm = 1.74
    hn = salto_neto(hb, hf, hm)
    assert isinstance(hn, float)
    assert pytest.approx(hn, 0.01) == 101.67


def test_velocidad_tubo():
    """
    Verifica la velocidad del flujo en la tubería forzada de 10 pulgadas (D = 0.250 m)
    para el caudal de diseño Q = 0.125 m³/s.
    v = 4 * 0.125 / (pi * 0.25^2) ≈ 2.546 m/s
    """
    q = 0.125
    d = 0.250
    v = velocidad_tubo(q, d)
    assert isinstance(v, float)
    assert pytest.approx(v, abs=0.01) == 2.546


def test_seleccionar_turbina():
    """
    Verifica la selección de la turbina Pelton para el caso de estudio Puno
    (Salto = 115 m, Caudal = 0.125 m³/s) y para otros regímenes normativos.
    """
    # Caso Proyecto Puno (100 kW)
    seleccion_puno = seleccionar_turbina(caudal=0.125, salto=115.0)
    assert seleccion_puno["tipo"] == "Pelton"
    assert seleccion_puno["eficiencia_tipica"] == 0.88

    # Caso Salto alto convencional
    seleccion_pelton_alto = seleccionar_turbina(caudal=0.8, salto=300.0)
    assert seleccion_pelton_alto["tipo"] == "Pelton"

    # Caso Francis
    seleccion_francis = seleccionar_turbina(caudal=5.0, salto=120.0)
    assert seleccion_francis["tipo"] == "Francis"

    # Caso Kaplan
    seleccion_kaplan = seleccionar_turbina(caudal=25.0, salto=20.0)
    assert seleccion_kaplan["tipo"] == "Kaplan"

    # Verificación de velocidad específica Ns para Pelton
    ns = velocidad_especifica(N=1200.0, Q=0.125, H=115.0)
    assert 10.0 <= ns <= 35.0  # Rango catalogado para Pelton


def test_celeridad():
    """
    Verifica el cálculo de la celeridad de onda de presión elástica en tubería
    de acero ASTM A36 con D = 0.250 m y espesor e = 0.005 m (5 mm).
    Valor esperado: ~1175 m/s.
    """
    d = 0.250
    e = 0.005
    a = calcular_celeridad(d, e)
    assert isinstance(a, float)
    assert 1150.0 <= a <= 1200.0
    assert pytest.approx(a, rel=0.02) == 1175.74
