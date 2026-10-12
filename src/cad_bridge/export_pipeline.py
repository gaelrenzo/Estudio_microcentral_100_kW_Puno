"""
MÓDULO: src/cad_bridge/export_pipeline.py
Pipeline maestro de orquestación, exportación y renderizado de los 8 Planos de Ingeniería
en formato CAD vectorial editable (.dxf) y vistas preliminares (.png).
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple, Any
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

from .hydraulic_drawings import (
    generar_plano_01_ubicacion,
    generar_plano_02_planta_general,
    generar_plano_03_bocatoma_desarenador,
    generar_plano_04_perfil_tuberia,
    generar_plano_05_casa_maquinas,
)
from .electromechanical_drawings import (
    generar_plano_06_grupo_pelton,
    generar_plano_07_diagrama_unifilar,
    generar_plano_08_subestacion_sab1,
)

PLANOS_INFO = [
    ("Plano_01_Ubicacion_Red_Geodesica.dxf", "U-01", generar_plano_01_ubicacion, "Ubicación y Red Geodésica REGGEN"),
    ("Plano_02_Planta_General_Obras_Hidraulicas.dxf", "GH-01", generar_plano_02_planta_general, "Planta General de Obras Hidráulicas"),
    ("Plano_03_Bocatoma_Tirolesa_Desarenador.dxf", "CH-01", generar_plano_03_bocatoma_desarenador, "Bocatoma Tirolesa y Desarenador 2 Naves"),
    ("Plano_04_Perfil_Longitudinal_Tuberia_Forzada.dxf", "TF-01", generar_plano_04_perfil_tuberia, "Perfil Longitudinal y Envolvente de Ariete"),
    ("Plano_05_Casa_Maquinas_Planta_Cortes.dxf", "CM-01", generar_plano_05_casa_maquinas, "Casa de Máquinas, Cortes y Fosa"),
    ("Plano_06_Disposicion_Electromecanica_Pelton.dxf", "EM-01", generar_plano_06_grupo_pelton, "Disposición Electromecánica Grupo Pelton"),
    ("Plano_07_Diagrama_Unifilar_Puesta_Tierra.dxf", "IE-01", generar_plano_07_diagrama_unifilar, "Diagrama Unifilar y Malla Puesta a Tierra"),
    ("Plano_08_Subestacion_Aerea_Biposte_SAB1.dxf", "SE-01", generar_plano_08_subestacion_sab1, "Subestación Aérea Biposte SAB-1 100 kVA"),
]


def renderizar_dxf_a_png(ruta_dxf: str, ruta_png: str, dpi: int = 200) -> None:
    """Renderiza un archivo DXF a imagen PNG de alta definición para revisión técnica."""
    try:
        doc = ezdxf.readfile(ruta_dxf)
        msp = doc.modelspace()
        fig = plt.figure(figsize=(16, 11), dpi=dpi)
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc)
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(msp, finalize=True)
        os.makedirs(os.path.dirname(ruta_png) or ".", exist_ok=True)
        fig.savefig(ruta_png, dpi=dpi, facecolor='white', bbox_inches='tight')
        plt.close(fig)
    except Exception as e:
        print(f"[Aviso] No se pudo renderizar preview PNG para {os.path.basename(ruta_dxf)}: {e}")


def exportar_todos_los_planos(directorio_base: str = None) -> Dict[str, Any]:
    """Genera la suite completa de los 8 planos DXF y sus vistas de previsualización."""
    if directorio_base is None:
        directorio_base = str(Path(__file__).resolve().parent.parent.parent)

    carpeta_dxf = os.path.join(directorio_base, "planos", "dxf")
    carpeta_preview = os.path.join(directorio_base, "planos", "preview")
    os.makedirs(carpeta_dxf, exist_ok=True)
    os.makedirs(carpeta_preview, exist_ok=True)

    resultados = []
    print("\n" + "=" * 70)
    print("   GENERANDO SUITE DE PLANOS DE INGENIERÍA EN CAD VECTORIAL (DXF)")
    print("=" * 70)

    for nombre_archivo, lamina, generador_func, descripcion in PLANOS_INFO:
        ruta_dxf = os.path.join(carpeta_dxf, nombre_archivo)
        nombre_png = nombre_archivo.replace(".dxf", ".png")
        ruta_png = os.path.join(carpeta_preview, nombre_png)

        print(f" -> Generando Lámina {lamina}: {descripcion}...")
        generador_func(ruta_dxf)
        renderizar_dxf_a_png(ruta_dxf, ruta_png)

        resultados.append({
            "lamina": lamina,
            "descripcion": descripcion,
            "dxf": ruta_dxf,
            "preview": ruta_png
        })

    print("=" * 70)
    print(f" [OK] {len(resultados)} Planos generados exitosamente en: {carpeta_dxf}")
    print("=" * 70 + "\n")
    return {"total_planos": len(resultados), "planos": resultados}


if __name__ == "__main__":
    exportar_todos_los_planos()
