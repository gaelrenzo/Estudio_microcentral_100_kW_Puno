"""
PAQUETE: src/cad_bridge
Integración de CAD Paramétrico y Generación de Planos de Ingeniería (DXF / ezdxf)
para la Microcentral Hidroeléctrica de 100 kW.
"""

from .title_block import dibujar_marco_y_cajetin, configurar_capas_estandar
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
from .export_pipeline import exportar_todos_los_planos

__all__ = [
    "dibujar_marco_y_cajetin",
    "configurar_capas_estandar",
    "generar_plano_01_ubicacion",
    "generar_plano_02_planta_general",
    "generar_plano_03_bocatoma_desarenador",
    "generar_plano_04_perfil_tuberia",
    "generar_plano_05_casa_maquinas",
    "generar_plano_06_grupo_pelton",
    "generar_plano_07_diagrama_unifilar",
    "generar_plano_08_subestacion_sab1",
    "exportar_todos_los_planos",
]
