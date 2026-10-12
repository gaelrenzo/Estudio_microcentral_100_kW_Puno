"""
MÓDULO: src/cad_bridge/hydraulic_drawings.py
Generadores CAD (ezdxf) para Planos 01 al 05 de Obras Civiles e Hidráulicas.
"""

import math
from typing import Dict, Any
import ezdxf
from ezdxf import colors
from .title_block import configurar_capas_estandar, dibujar_marco_y_cajetin


def generar_plano_01_ubicacion(ruta_dxf: str) -> str:
    """Plano 01 (U-01): Ubicación, Emplazamiento General y Red Geodésica IGN."""
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    configurar_capas_estandar(doc)

    notas = [
        "Coordenadas referidas al Sistema Geodésico Mundial WGS-84, Proyección UTM Zona 19 Sur.",
        "Puntos geodésicos monumentados según especificaciones REGGEN - Orden 'C' del IGN.",
        "Acceso vehicular principal desde la Carretera Interoceánica Sur (Ruta Nacional PE-34B, km 215).",
        "Límites de cuenca hidrográfico-topográficos determinados mediante DEM ALOS PALSAR 12.5 m."
    ]
    dibujar_marco_y_cajetin(
        msp,
        codigo_lamina="U-01",
        titulo_plano="PLANO DE UBICACIÓN, EMPLAZAMIENTO GENERAL Y RED GEODÉSICA IGN",
        especialidad="TOPOGRAFÍA Y GEODESIA",
        escala="1 : 10,000",
        notas=notas
    )

    # 1. Dibujo Esquemático de Microcuenca Río Blanco (Coordenadas en espacio papel mm o modelo)
    # Área de dibujo útil: x in [50, 580], y in [120, 550]
    # Macro-localización
    msp.add_text("ESQUEMA DE LOCALIZACIÓN Y RED DE CONTROL GEODÉSICO", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 4.5}).set_placement((60.0, 530.0))

    # Curvas de nivel envolventes
    cuenca_pts = [(100, 200), (80, 300), (120, 420), (220, 500), (380, 480), (480, 380), (450, 240), (320, 160), (200, 150), (100, 200)]
    msp.add_lwpolyline(cuenca_pts, close=True, dxfattribs={"layer": "CIVIL_TERRENO"})
    msp.add_text("DIVISORIA DE AGUAS - CUENCA RÍO BLANCO (Área = 28.4 km²)", dxfattribs={"layer": "CIVIL_TERRENO", "height": 3.0}).set_placement((150, 505))

    # Cauce principal del Río Blanco
    rio_pts = [(120, 410), (170, 360), (230, 320), (280, 260), (330, 220), (390, 180), (430, 150)]
    msp.add_lwpolyline(rio_pts, dxfattribs={"layer": "HIDRAULICA_AGUA"})
    msp.add_text("RÍO BLANCO (Q_medio = 0.523 m³/s)", dxfattribs={"layer": "HIDRAULICA_AGUA", "height": 3.0}).set_placement((180, 370))

    # Carretera Interoceánica
    via_pts = [(70, 140), (180, 130), (300, 125), (420, 115), (550, 110)]
    msp.add_lwpolyline(via_pts, dxfattribs={"layer": "0_MARCO_Y_BORDE"})
    msp.add_text("CARRETERA INTEROCEÁNICA SUR (KM 215) -> A PUERTO MALDONADO", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.8}).set_placement((190, 118))

    # Hitos Geodésicos
    hitos = [
        ("HG-01 (Bocatoma)", 230, 320, "E: 340,820.50 | N: 8,472,950.20 | Z: 2,420.00 msnm"),
        ("HG-02 (Cámara Carga)", 280, 260, "E: 341,250.50 | N: 8,473,310.80 | Z: 2,417.80 msnm"),
        ("HG-03 (Casa Máquinas)", 330, 220, "E: 341,480.10 | N: 8,473,650.40 | Z: 2,302.80 msnm")
    ]
    for nom, x, y, coords in hitos:
        msp.add_circle((x, y), 3.5, dxfattribs={"layer": "COTAS_Y_NIVELES"})
        msp.add_circle((x, y), 1.0, dxfattribs={"layer": "0_TEXTOS_ROTULO"})
        msp.add_text(nom, dxfattribs={"layer": "COTAS_Y_NIVELES", "height": 3.2}).set_placement((x + 5, y + 2))
        msp.add_text(coords, dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.2}).set_placement((x + 5, y - 3))

    # Cuadro de Coordenadas de Infraestructura
    t_x, t_y = 60.0, 480.0
    msp.add_text("CUADRO OFICIAL DE VÉRTICES Y COORDENADAS REGGEN ORDEN 'C'", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 3.2}).set_placement((t_x, t_y))
    # Marco de tabla
    msp.add_lwpolyline([(t_x, t_y - 5), (t_x + 280, t_y - 5), (t_x + 280, t_y - 55), (t_x, t_y - 55), (t_x, t_y - 5)], close=True, dxfattribs={"layer": "0_CAJETIN"})
    headers = ["ESTACIÓN", "ESTE [m]", "NORTE [m]", "COTA [msnm]", "DESCRIPCIÓN TÉCNICA"]
    msp.add_text(" | ".join(headers), dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.4}).set_placement((t_x + 5, t_y - 12))
    rows = [
        "HG-01   | 340,820.500 | 8,472,950.200 | 2,420.000 | Bocatoma Tirolesa y Azud",
        "HG-02   | 341,250.500 | 8,473,310.800 | 2,417.800 | Cámara de Carga (Forebay)",
        "HG-03   | 341,480.100 | 8,473,650.400 | 2,302.800 | Casa de Máquinas y Subestación"
    ]
    for idx, r in enumerate(rows):
        msp.add_text(r, dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.2}).set_placement((t_x + 5, t_y - 22 - (idx * 9)))

    doc.saveas(ruta_dxf)
    return ruta_dxf


def generar_plano_02_planta_general(ruta_dxf: str) -> str:
    """Plano 02 (GH-01): Planta General del Trazo Hidráulico y Obras Conexas."""
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    configurar_capas_estandar(doc)

    notas = [
        "Longitud total del canal de aducción: L = 450.00 m en concreto ciclópeo f'c = 175 kg/cm².",
        "Longitud inclinada de tubería forzada: L = 380.00 m en acero ASTM A36 DN 250 mm.",
        "Caudal de diseño nominal derivado: Qd = 125 L/s (0.125 m³/s).",
        "Caudal ecológico permanente en el cauce del Río Blanco: Qeco >= 30 L/s."
    ]
    dibujar_marco_y_cajetin(
        msp,
        codigo_lamina="GH-01",
        titulo_plano="PLANTA GENERAL Y ESQUEMA INTEGRAL DE OBRAS HIDRÁULICAS",
        especialidad="INGENIERÍA HIDRÁULICA",
        escala="1 : 2,500",
        notas=notas
    )

    msp.add_text("TRAZO GENERAL EN PLANTA: CAPTACIÓN -> CANAL -> CÁMARA DE CARGA -> TUBERÍA -> CASA DE MÁQUINAS", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 4.5}).set_placement((50.0, 540.0))

    # 1. Río Blanco en planta
    rio = [(60, 480), (120, 440), (180, 390), (240, 320), (320, 240), (420, 180), (500, 150)]
    msp.add_lwpolyline(rio, dxfattribs={"layer": "HIDRAULICA_AGUA"})
    msp.add_text("Cauce Río Blanco", dxfattribs={"layer": "HIDRAULICA_AGUA", "height": 3.0}).set_placement((100, 460))

    # 2. Bocatoma y Desarenador (Prog 0+000)
    msp.add_lwpolyline([(120, 440), (128, 445), (135, 435), (127, 430), (120, 440)], close=True, dxfattribs={"layer": "CIVIL_CONCRETO"})
    msp.add_text("BOCATOMA TIROLESA (0+000) | Cota: 2,420.00 m", dxfattribs={"layer": "CIVIL_CONCRETO", "height": 3.0}).set_placement((135, 450))

    # Desarenador 2 Naves
    msp.add_lwpolyline([(135, 435), (150, 425), (155, 432), (140, 442), (135, 435)], close=True, dxfattribs={"layer": "CIVIL_CONCRETO"})
    msp.add_text("DESARENADOR 2 NAVES (0+015)", dxfattribs={"layer": "CIVIL_CONCRETO", "height": 2.8}).set_placement((155, 440))

    # 3. Canal de Aducción (L = 450 m)
    canal = [(150, 425), (200, 400), (250, 360), (300, 310), (340, 260)]
    msp.add_lwpolyline(canal, dxfattribs={"layer": "CIVIL_CONCRETO"})
    msp.add_text("CANAL DE ADUCCIÓN RECTANGULAR L=450m (S=0.0015, b=0.50m, yn=0.33m)", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.8}).set_placement((210, 390))

    # 4. Cámara de Carga (Prog 0+475)
    msp.add_lwpolyline([(340, 260), (355, 255), (358, 265), (343, 270), (340, 260)], close=True, dxfattribs={"layer": "CIVIL_CONCRETO"})
    msp.add_text("CÁMARA DE CARGA (0+475) | Cota: 2,417.80 m | V=22.5 m³", dxfattribs={"layer": "CIVIL_CONCRETO", "height": 3.0}).set_placement((360, 270))

    # 5. Tubería Forzada (Penstock L = 380 m)
    penstock = [(355, 255), (380, 230), (410, 195), (440, 160)]
    msp.add_lwpolyline(penstock, dxfattribs={"layer": "MECANICA_TUBERIA"})
    msp.add_text("TUBERÍA FORZADA ACERO ASTM A36 DN 250mm (L=380m, e=4.75 a 6.35mm)", dxfattribs={"layer": "MECANICA_TUBERIA", "height": 2.8}).set_placement((390, 220))

    # Bloques de Anclaje
    for idx, (bx, by) in enumerate([(355, 255), (380, 230), (410, 195), (440, 160)]):
        msp.add_circle((bx, by), 2.5, dxfattribs={"layer": "CIVIL_CONCRETO"})
        msp.add_text(f"BA-0{idx+1}", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.2}).set_placement((bx + 3, by - 2))

    # 6. Casa de Máquinas (Prog 0+855)
    msp.add_lwpolyline([(440, 160), (465, 145), (475, 160), (450, 175), (440, 160)], close=True, dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_text("CASA DE MÁQUINAS (0+855) | Cota: 2,305.00 m | Salto Bruto = 115.0 m", dxfattribs={"layer": "MECANICA_EQUIPOS", "height": 3.0}).set_placement((475, 175))

    # Canal de Descarga
    msp.add_lwpolyline([(465, 145), (480, 140)], dxfattribs={"layer": "HIDRAULICA_AGUA"})
    msp.add_text("Descarga al Río", dxfattribs={"layer": "HIDRAULICA_AGUA", "height": 2.2}).set_placement((485, 140))

    doc.saveas(ruta_dxf)
    return ruta_dxf


def generar_plano_03_bocatoma_desarenador(ruta_dxf: str) -> str:
    """Plano 03 (CH-01): Bocatoma Tirolesa y Desarenador de Doble Nave."""
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    configurar_capas_estandar(doc)

    notas = [
        "Concreto en azud derivador: f'c = 175 kg/cm² con 30% piedra desplazadora (concreto ciclópeo).",
        "Rejilla Coanda de fondo: barras de acero inoxidable AISI 304 (e = 25 mm, inclinación = 20°).",
        "Desarenador de doble nave: operación continua en nave 1 y purga periódica en nave 2.",
        "Vertedero de salida tipo Sutro para mantener velocidad horizontal Vh <= 0.20 m/s."
    ]
    dibujar_marco_y_cajetin(
        msp,
        codigo_lamina="CH-01",
        titulo_plano="CAPTACIÓN Y DESARENADOR: BOCATOMA TIROLESA Y 2 NAVES",
        especialidad="OBRAS HIDRÁULICAS",
        escala="1 : 50 / 1 : 25",
        notas=notas
    )

    # VISTA 1: CORTE DEL AZUD TIROLESA (Zona izquierda)
    msp.add_text("CORTE A-A: BOCATOMA TIROLESA (AZUD DERIVADOR)", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 4.0}).set_placement((60.0, 520.0))
    # Azud
    azud_pts = [(70, 360), (100, 440), (150, 440), (220, 390), (270, 360), (270, 320), (70, 320), (70, 360)]
    msp.add_lwpolyline(azud_pts, close=True, dxfattribs={"layer": "CIVIL_CONCRETO"})
    msp.add_text("Azud de Concreto Ciclópeo f'c=175 kg/cm²", dxfattribs={"layer": "CIVIL_CONCRETO", "height": 2.8}).set_placement((100, 340))

    # Rejilla Tirolesa inclinada
    msp.add_line((150, 440), (220, 390), dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_text("Rejilla Coanda AISI 304 (e=25mm, α=20°)", dxfattribs={"layer": "MECANICA_EQUIPOS", "height": 2.6}).set_placement((155, 420))

    # Canal colector de fondo
    msp.add_lwpolyline([(150, 440), (150, 370), (220, 370), (220, 390)], dxfattribs={"layer": "CIVIL_CONCRETO"})
    msp.add_text("Canal Colector Qd=125 L/s", dxfattribs={"layer": "HIDRAULICA_AGUA", "height": 2.5}).set_placement((155, 380))

    # VISTA 2: DESARENADOR EN PLANTA (Zona derecha)
    msp.add_text("VISTA EN PLANTA: DESARENADOR DE DOBLE NAVE (L = 8.00 m)", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 4.0}).set_placement((350.0, 520.0))

    # Muro perimétrico y naves
    # Nave 1
    msp.add_lwpolyline([(360, 410), (540, 410), (540, 460), (360, 460), (360, 410)], close=True, dxfattribs={"layer": "CIVIL_CONCRETO"})
    msp.add_text("NAVE 1 (Operación Continua)", dxfattribs={"layer": "HIDRAULICA_AGUA", "height": 2.8}).set_placement((400, 435))

    # Nave 2
    msp.add_lwpolyline([(360, 350), (540, 350), (540, 400), (360, 400), (360, 350)], close=True, dxfattribs={"layer": "CIVIL_CONCRETO"})
    msp.add_text("NAVE 2 (Reserva y Purga)", dxfattribs={"layer": "HIDRAULICA_AGUA", "height": 2.8}).set_placement((400, 375))

    # Muro divisor
    msp.add_line((360, 405), (540, 405), dxfattribs={"layer": "CIVIL_CONCRETO"})

    # Compuertas de limpia rápida
    msp.add_circle((540, 435), 4.0, dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_circle((540, 375), 4.0, dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_text("Compuertas de Limpia Rápida DN 200", dxfattribs={"layer": "MECANICA_EQUIPOS", "height": 2.4}).set_placement((548, 405))

    # Dimensiones
    msp.add_text("Largo Útil = 8.00 m | Ancho Nave = 0.90 m c/u | d >= 0.20 mm", dxfattribs={"layer": "COTAS_Y_NIVELES", "height": 2.6}).set_placement((370, 335))

    doc.saveas(ruta_dxf)
    return ruta_dxf


def generar_plano_04_perfil_tuberia(ruta_dxf: str) -> str:
    """Plano 04 (TF-01): Perfil Longitudinal de Conducción y Tubería Forzada."""
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    configurar_capas_estandar(doc)

    notas = [
        "Tubería de acero ASTM A36 con junta electrosoldada e inspección radiográfica al 100%.",
        "Espesores: e = 4.75 mm (3/16\") en tramo superior (0-200m) y e = 6.35 mm (1/4\") en tramo inferior (200-380m).",
        "Envolvente de sobrepresión calculada mediante teoría elastoacústica de Allievi (tc = 4.0 s, ΔH = 49.31 m).",
        "Bloques de anclaje de concreto armado f'c = 210 kg/cm² dimensionados al volteo y deslizamiento (FS >= 1.5)."
    ]
    dibujar_marco_y_cajetin(
        msp,
        codigo_lamina="TF-01",
        titulo_plano="PERFIL LONGITUDINAL: TUBERÍA FORZADA Y ENVOLVENTE DE ARIETE",
        especialidad="MECÁNICA Y FLUIDOS",
        escala="H: 1:1,000 / V: 1:500",
        notas=notas
    )

    msp.add_text("PERFIL LONGITUDINAL DEL PENSTOCK CON LÍNEAS PIEZOMÉTRICAS Y BLOQUES DE ANCLAJE", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 4.5}).set_placement((50.0, 535.0))

    # Perfil del terreno / Tubería: Desde Cota 2417.80 (Cámara de Carga) hasta Cota 2302.80 (Casa Máquinas)
    # Eje horizontal: 0 a 380 m -> Mapeado en plano: x in [80, 520] (dx = 440 mm)
    # Eje vertical: 2300 a 2480 m -> Mapeado en plano: y in [180, 480] (dy = 300 mm)
    def map_pt(prog, cota):
        px = 80.0 + (prog / 380.0) * 440.0
        py = 180.0 + ((cota - 2300.0) / 180.0) * 280.0
        return (px, py)

    # Puntos del Penstock
    p0 = map_pt(0, 2417.80)       # Forebay
    p1 = map_pt(110, 2390.00)     # BA-2
    p2 = map_pt(240, 2350.00)     # BA-3
    p3 = map_pt(380, 2305.00)     # BA-4 (Casa Máquinas)

    # 1. Tubería forzada física
    msp.add_lwpolyline([p0, p1, p2, p3], dxfattribs={"layer": "MECANICA_TUBERIA"})
    msp.add_text("Tubería Forzada DN 250 mm (ASTM A36)", dxfattribs={"layer": "MECANICA_TUBERIA", "height": 3.0}).set_placement((p1[0] - 20, p1[1] - 15))

    # 2. Línea Piezométrica Estática (Cota constante 2,417.80 msnm)
    pe0 = map_pt(0, 2417.80)
    pe3 = map_pt(380, 2417.80)
    msp.add_line(pe0, pe3, dxfattribs={"layer": "COTAS_Y_NIVELES"})
    msp.add_text("Línea Piezométrica Estática (Cota 2,417.80 msnm | Salto Bruto Hb = 115.00 m)", dxfattribs={"layer": "COTAS_Y_NIVELES", "height": 2.6}).set_placement((150, pe0[1] + 4))

    # 3. Línea Piezométrica Dinámica (Pérdidas continuas hf = 8.82 m -> Cota 2408.98 msnm en CM)
    pd0 = map_pt(0, 2417.80)
    pd3 = map_pt(380, 2417.80 - 8.82)
    msp.add_line(pd0, pd3, dxfattribs={"layer": "HIDRAULICA_AGUA"})
    msp.add_text("Línea Piezométrica Dinámica (Salto Neto Hn = 106.18 m, hf = 8.82 m)", dxfattribs={"layer": "HIDRAULICA_AGUA", "height": 2.5}).set_placement((180, pd3[1] + 25))

    # 4. Envolvente Máxima por Golpe de Ariete (Allievi: Sobrepresión ΔH = +49.31 m -> Cota 2467.11 msnm)
    pa0 = map_pt(0, 2417.80)
    pa3 = map_pt(380, 2417.80 + 49.31)
    msp.add_line(pa0, pa3, dxfattribs={"layer": "0_TEXTOS_ROTULO"})
    msp.add_text("Envolvente Máxima Golpe de Ariete (ΔH = +49.31 m, Hmax = 164.31 m / 16.1 bar)", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.6}).set_placement((160, pa3[1] + 4))

    # Bloques de Anclaje
    for idx, (bx, by) in enumerate([p0, p1, p2, p3]):
        msp.add_circle((bx, by), 4.0, dxfattribs={"layer": "CIVIL_CONCRETO"})
        msp.add_text(f"BA-0{idx+1}", dxfattribs={"layer": "CIVIL_CONCRETO", "height": 2.4}).set_placement((bx - 5, by - 12))

    doc.saveas(ruta_dxf)
    return ruta_dxf


def generar_plano_05_casa_maquinas(ruta_dxf: str) -> str:
    """Plano 05 (CM-01): Casa de Máquinas y Obras Civiles de Descarga."""
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    configurar_capas_estandar(doc)

    notas = [
        "Muros y losa de cimentación en concreto armado f'c = 210 kg/cm² con acero fy = 4200 kg/cm².",
        "Puente grúa manual monorriel de 2.0 toneladas con polipasto de cadena a cota +4.50 m.",
        "Fosa de turbina Pelton con salida libre al canal de restitución (descarga por gravedad).",
        "Protección contra inundaciones: cota de piso terminado (+2,305.00 msnm) superior a crecida Tr=100a (+2,303.50 msnm)."
    ]
    dibujar_marco_y_cajetin(
        msp,
        codigo_lamina="CM-01",
        titulo_plano="CASA DE MÁQUINAS: PLANTA ARQUITECTÓNICA, CORTES Y FOSA",
        especialidad="OBRAS CIVILES Y ARQUITECTURA",
        escala="1 : 25 / 1 : 50",
        notas=notas
    )

    msp.add_text("DISTRIBUCIÓN EN PLANTA - CASA DE MÁQUINAS (8.50 m x 6.00 m)", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 4.5}).set_placement((60.0, 525.0))

    # Muros perimétricos (e = 0.25 m)
    # Área útil x in [80, 500], y in [200, 480]
    # Escala: 1m = 40mm -> 8.5m = 340mm, 6.0m = 240mm
    x0, y0 = 100.0, 220.0
    w, h = 340.0, 240.0
    msp.add_lwpolyline([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0)], close=True, dxfattribs={"layer": "CIVIL_CONCRETO"})
    msp.add_lwpolyline([(x0 + 10, y0 + 10), (x0 + w - 10, y0 + 10), (x0 + w - 10, y0 + h - 10), (x0 + 10, y0 + h - 10), (x0 + 10, y0 + 10)], close=True, dxfattribs={"layer": "CIVIL_CONCRETO"})

    # 1. Grupo Turbina Pelton - Generador
    # Bancada
    bx0, by0 = x0 + 70.0, y0 + 60.0
    msp.add_lwpolyline([(bx0, by0), (bx0 + 120, by0), (bx0 + 120, by0 + 70), (bx0, by0 + 70), (bx0, by0)], close=True, dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_text("Bancada Estructural AISC 360", dxfattribs={"layer": "MECANICA_EQUIPOS", "height": 2.5}).set_placement((bx0 + 10, by0 + 75))

    # Carcasa de turbina Pelton
    msp.add_circle((bx0 + 35, by0 + 35), 25.0, dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_text("Turbina Pelton 2 Iny", dxfattribs={"layer": "MECANICA_EQUIPOS", "height": 2.5}).set_placement((bx0 + 15, by0 + 35))

    # Generador síncrono 125 kVA
    msp.add_lwpolyline([(bx0 + 65, by0 + 10), (bx0 + 115, by0 + 10), (bx0 + 115, by0 + 60), (bx0 + 65, by0 + 60), (bx0 + 65, by0 + 10)], close=True, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("Generador 125 kVA", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.5}).set_placement((bx0 + 68, by0 + 35))

    # 2. Válvula Mariposa y Tubería de entrada
    msp.add_line((x0, by0 + 35), (bx0 + 10, by0 + 35), dxfattribs={"layer": "MECANICA_TUBERIA"})
    msp.add_circle((x0 + 30, by0 + 35), 7.0, dxfattribs={"layer": "MECANICA_TUBERIA"})
    msp.add_text("Válvula Mariposa DN 250", dxfattribs={"layer": "MECANICA_TUBERIA", "height": 2.2}).set_placement((x0 + 10, by0 + 47))

    # 3. Tableros Eléctricos y Control ELC
    tx0, ty0 = x0 + 230.0, y0 + 150.0
    msp.add_lwpolyline([(tx0, ty0), (tx0 + 80, ty0), (tx0 + 80, ty0 + 30), (tx0, ty0 + 30), (tx0, ty0)], close=True, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("Tablero BT / Control ELC 120 kW (IEC 61439)", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.4}).set_placement((tx0 + 5, ty0 + 35))

    # 4. Fosa de descarga bajo turbina
    msp.add_lwpolyline([(bx0 + 10, y0 + 10), (bx0 + 60, y0 + 10), (bx0 + 60, by0 + 10), (bx0 + 10, by0 + 10), (bx0 + 10, y0 + 10)], close=True, dxfattribs={"layer": "HIDRAULICA_AGUA"})
    msp.add_text("Canal de Fuga a Río", dxfattribs={"layer": "HIDRAULICA_AGUA", "height": 2.2}).set_placement((bx0 + 10, y0 - 8))

    doc.saveas(ruta_dxf)
    return ruta_dxf
