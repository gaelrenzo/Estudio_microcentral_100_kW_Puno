"""
MÓDULO DE PRUEBAS: tests/test_cad_integration.py
Validación y pruebas unitarias de la generación paramétrica de planos CAD (ezdxf)
y su integración modular con la ingeniería de la microcentral de 100 kW.
"""

import os
import tempfile
import pytest
import ezdxf

from src.cad_bridge.title_block import configurar_capas_estandar, dibujar_marco_y_cajetin
from src.cad_bridge.hydraulic_drawings import (
    generar_plano_01_ubicacion,
    generar_plano_02_planta_general,
    generar_plano_03_bocatoma_desarenador,
    generar_plano_04_perfil_tuberia,
    generar_plano_05_casa_maquinas
)
from src.cad_bridge.electromechanical_drawings import (
    generar_plano_06_grupo_pelton,
    generar_plano_07_diagrama_unifilar,
    generar_plano_08_subestacion_sab1
)
from src.cad_bridge.export_pipeline import exportar_todos_los_planos


def test_configuracion_capas_estandar():
    """Verifica que el archivo DXF cree las capas normalizadas con sus respectivos colores."""
    doc = ezdxf.new("R2010")
    configurar_capas_estandar(doc)

    capas_esperadas = [
        "0_MARCO_Y_BORDE", "0_CAJETIN", "0_TEXTOS_ROTULO",
        "COTAS_Y_NIVELES", "EJES_Y_CENTROS", "CIVIL_CONCRETO",
        "CIVIL_TERRENO", "HIDRAULICA_AGUA", "MECANICA_TUBERIA",
        "MECANICA_EQUIPOS", "ELECTRICA_LINEAS", "ELECTRICA_EQUIPOS"
    ]
    for c in capas_esperadas:
        assert c in doc.layers, f"Falta la capa normalizada: {c}"


def test_dibujo_cajetin_unap_fime():
    """Verifica la generación del cajetín A1 institucional y la rosa de los vientos."""
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    configurar_capas_estandar(doc)
    dibujar_marco_y_cajetin(
        msp,
        codigo_lamina="TEST-01",
        titulo_plano="PLANO DE PRUEBA DE INTEGRACIÓN",
        especialidad="ELECTROMECÁNICA",
        escala="1 : 100"
    )

    # Verificar existencia de entidades de texto y polilíneas
    textos = [e.dxf.text for e in msp.query("TEXT")]
    assert any("UNIVERSIDAD NACIONAL DEL ALTIPLANO PUNO" in t for t in textos)
    assert any("FACULTAD DE INGENIERÍA MECÁNICA ELÉCTRICA" in t for t in textos)
    assert any("TEST-01" in t for t in textos)
    assert any("N" == t for t in textos)  # Rosa de los vientos


def test_generacion_planos_individuales():
    """Verifica la creación exitosa de cada uno de los 8 planos en formato DXF."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        f_p1 = os.path.join(tmp_dir, "p1.dxf")
        generar_plano_01_ubicacion(f_p1)
        assert os.path.exists(f_p1) and os.path.getsize(f_p1) > 1000

        f_p2 = os.path.join(tmp_dir, "p2.dxf")
        generar_plano_02_planta_general(f_p2)
        assert os.path.exists(f_p2) and os.path.getsize(f_p2) > 1000

        f_p3 = os.path.join(tmp_dir, "p3.dxf")
        generar_plano_03_bocatoma_desarenador(f_p3)
        assert os.path.exists(f_p3) and os.path.getsize(f_p3) > 1000

        f_p4 = os.path.join(tmp_dir, "p4.dxf")
        generar_plano_04_perfil_tuberia(f_p4)
        assert os.path.exists(f_p4) and os.path.getsize(f_p4) > 1000

        f_p5 = os.path.join(tmp_dir, "p5.dxf")
        generar_plano_05_casa_maquinas(f_p5)
        assert os.path.exists(f_p5) and os.path.getsize(f_p5) > 1000

        f_p6 = os.path.join(tmp_dir, "p6.dxf")
        generar_plano_06_grupo_pelton(f_p6)
        assert os.path.exists(f_p6) and os.path.getsize(f_p6) > 1000

        f_p7 = os.path.join(tmp_dir, "p7.dxf")
        generar_plano_07_diagrama_unifilar(f_p7)
        assert os.path.exists(f_p7) and os.path.getsize(f_p7) > 1000

        f_p8 = os.path.join(tmp_dir, "p8.dxf")
        generar_plano_08_subestacion_sab1(f_p8)
        assert os.path.exists(f_p8) and os.path.getsize(f_p8) > 1000


def test_pipeline_completo_exportacion():
    """Verifica que el pipeline orquestador exporte todos los planos al directorio de destino."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        res = exportar_todos_los_planos(tmp_dir)
        assert res["total_planos"] == 8
        dxf_dir = os.path.join(tmp_dir, "planos", "dxf")
        archivos = os.listdir(dxf_dir)
        assert len(archivos) == 8
        assert all(f.endswith(".dxf") for f in archivos)
