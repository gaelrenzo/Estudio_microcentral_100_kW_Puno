"""
MÓDULO: src/cad_bridge/electromechanical_drawings.py
Generadores CAD (ezdxf) para Planos 06 al 08 de Ingeniería Electromecánica,
Sistemas Eléctricos de Potencia y Subestación SAB-1.
"""

import math
from typing import Dict, Any
import ezdxf
from ezdxf import colors
from .title_block import configurar_capas_estandar, dibujar_marco_y_cajetin


def generar_plano_06_grupo_pelton(ruta_dxf: str) -> str:
    """Plano 06 (EM-01): Disposición Electromecánica del Grupo Turbina Pelton - Generador."""
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    configurar_capas_estandar(doc)

    notas = [
        "Rodete Pelton monobloque en acero inoxidable martensítico ASTM A743 CA6NM (13% Cr, 4% Ni).",
        "Diámetro primitivo D1 = 324.1 mm con 19 cucharas elípticas de doble cubeta y arista afilada.",
        "Dos toberas/inyectores simétricos con aguja reguladora y deflector rápido contra sobrevelocidad.",
        "Válvula de guardia tipo mariposa DN 250 PN 16 con cierre por contrapeso y apertura oleohidráulica.",
        "Eje motriz fabricado en acero AISI 4140 bonificado con chaveta según DIN 6885 y tolerancias ISO 2768-mK."
    ]
    dibujar_marco_y_cajetin(
        msp,
        codigo_lamina="EM-01",
        titulo_plano="DISPOSICIÓN ELECTROMECÁNICA: TURBINA PELTON 2 INYECTORES Y GENERADOR",
        especialidad="INGENIERÍA MECÁNICA",
        escala="1 : 15 / 1 : 10",
        notas=notas
    )

    msp.add_text("DETALLE ELECTROMECÁNICO DEL GRUPO TURBO-GENERADOR 104.4 kW (1200 RPM)", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 4.5}).set_placement((60.0, 530.0))

    # 1. Tubería de alimentación y Bifurcador simétrico en Y (DN 250 -> 2 x DN 175)
    # Eje x in [80, 260], y in [240, 440]
    msp.add_line((70, 340), (120, 340), dxfattribs={"layer": "MECANICA_TUBERIA"})
    msp.add_line((70, 360), (120, 360), dxfattribs={"layer": "MECANICA_TUBERIA"})
    msp.add_text("Penstock DN 250", dxfattribs={"layer": "MECANICA_TUBERIA", "height": 2.6}).set_placement((75, 365))

    # Brida ASME B16.5 Clase 150
    msp.add_lwpolyline([(120, 330), (128, 330), (128, 370), (120, 370), (120, 330)], close=True, dxfattribs={"layer": "MECANICA_TUBERIA"})
    msp.add_text("Brida ASME B16.5 DN 250", dxfattribs={"layer": "MECANICA_TUBERIA", "height": 2.2}).set_placement((110, 315))

    # Válvula Mariposa
    msp.add_circle((145, 350), 18.0, dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_line((145, 332), (145, 368), dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_text("Válvula Mariposa DN 250 PN 16", dxfattribs={"layer": "MECANICA_EQUIPOS", "height": 2.6}).set_placement((130, 375))

    # Bifurcador en Y
    msp.add_lwpolyline([(165, 360), (195, 410), (225, 410)], dxfattribs={"layer": "MECANICA_TUBERIA"})
    msp.add_lwpolyline([(165, 340), (195, 290), (225, 290)], dxfattribs={"layer": "MECANICA_TUBERIA"})
    msp.add_text("Bifurcación Simétrica en Y", dxfattribs={"layer": "MECANICA_TUBERIA", "height": 2.4}).set_placement((175, 350))

    # Inyectores (Toberas 1 y 2)
    # Inyector 1 Superior
    msp.add_lwpolyline([(225, 415), (255, 405), (255, 395), (225, 405), (225, 415)], close=True, dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_text("Inyector 1 (do=36.8mm)", dxfattribs={"layer": "MECANICA_EQUIPOS", "height": 2.2}).set_placement((225, 422))
    # Inyector 2 Inferior
    msp.add_lwpolyline([(225, 295), (255, 305), (255, 285), (225, 285), (225, 295)], close=True, dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_text("Inyector 2 (do=36.8mm)", dxfattribs={"layer": "MECANICA_EQUIPOS", "height": 2.2}).set_placement((225, 275))

    # 2. Rodete Pelton (D1 = 324.1 mm)
    rx, ry = 285.0, 350.0
    msp.add_circle((rx, ry), 25.0, dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_circle((rx, ry), 8.0, dxfattribs={"layer": "EJES_Y_CENTROS"})
    msp.add_text("Rodete Pelton D1=324.1mm (19 Cucharas CA6NM)", dxfattribs={"layer": "MECANICA_EQUIPOS", "height": 2.6}).set_placement((rx - 40, ry - 35))

    # Carcasa de turbina (Chapa estructural 6mm con deflectores)
    msp.add_lwpolyline([(240, 260), (330, 260), (330, 440), (240, 440), (240, 260)], close=True, dxfattribs={"layer": "CIVIL_CONCRETO"})
    msp.add_text("Carcasa Acero A36", dxfattribs={"layer": "CIVIL_CONCRETO", "height": 2.2}).set_placement((245, 445))

    # 3. Eje de transmisión y Acoplamiento elástico
    msp.add_line((rx + 8, ry), (370, ry), dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_lwpolyline([(365, ry - 15), (375, ry - 15), (375, ry + 15), (365, ry + 15), (365, ry - 15)], close=True, dxfattribs={"layer": "MECANICA_EQUIPOS"})
    msp.add_text("Acoplamiento Elástico", dxfattribs={"layer": "MECANICA_EQUIPOS", "height": 2.2}).set_placement((350, ry + 20))

    # 4. Generador Síncrono Trifásico (125 kVA, 1200 RPM)
    gx0, gy0 = 380.0, 305.0
    msp.add_lwpolyline([(gx0, gy0), (gx0 + 90, gy0), (gx0 + 90, gy0 + 90), (gx0, gy0 + 90), (gx0, gy0)], close=True, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("GENERADOR SÍNCRONO TRIFÁSICO", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.6}).set_placement((gx0 + 5, gy0 + 75))
    msp.add_text("125 kVA | 380 V | 60 Hz | 1200 RPM", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.2}).set_placement((gx0 + 5, gy0 + 65))
    msp.add_text("6 Polos | cos φ = 0.8 | IP23", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.2}).set_placement((gx0 + 5, gy0 + 55))

    # 5. Bancada Estructural Común (AISC 360)
    msp.add_lwpolyline([(210, 240), (gx0 + 105, 240), (gx0 + 105, 255), (210, 255), (210, 240)], close=True, dxfattribs={"layer": "0_MARCO_Y_BORDE"})
    msp.add_text("Bancada Estructural Unificada (Perfiles UPN 200 - Acero ASTM A36 / AISC 360)", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.6}).set_placement((220, 228))

    doc.saveas(ruta_dxf)
    return ruta_dxf


def generar_plano_07_diagrama_unifilar(ruta_dxf: str) -> str:
    """Plano 07 (IE-01): Diagrama Unifilar, Protecciones y Puesta a Tierra."""
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    configurar_capas_estandar(doc)

    notas = [
        "Sistema eléctrico trifásico a 4 hilos (3F + N + PE) en 380/220 V a 60 Hz.",
        "Regulador Electrónico de Carga (ELC) de 120 kW con banco de resistencias ballast de disipación hídrica/aire.",
        "Protección según CNE Suministro: Sobrecarga (51), Cortocircuito (50), Sobre/Sub-tensión (27/59), Frecuencia (81O/U).",
        "Malla de puesta a tierra diseñada bajo norma IEEE Std 80 con resistencia de dispersión Rpat <= 10 Ohmios."
    ]
    dibujar_marco_y_cajetin(
        msp,
        codigo_lamina="IE-01",
        titulo_plano="DIAGRAMA UNIFILAR, TABLERO GENERAL BT Y PUESTA A TIERRA",
        especialidad="INGENIERÍA ELÉCTRICA",
        escala="SIN ESCALA (ESQUEMÁTICO)",
        notas=notas
    )

    msp.add_text("DIAGRAMA UNIFILAR GENERAL - GENERACIÓN, CONTROL E INTERCONEXIÓN", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 4.5}).set_placement((60.0, 530.0))

    # 1. Generador Síncrono (Símbolo G)
    msp.add_circle((120, 440), 16.0, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("G", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 9.0}).set_placement((116, 435))
    msp.add_text("3 ~ 60 Hz", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.5}).set_placement((112, 420))
    msp.add_text("125 kVA | 380 V | In = 190 A", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.4}).set_placement((70, 465))

    # Línea hacia interruptor principal
    msp.add_line((120, 424), (120, 370), dxfattribs={"layer": "ELECTRICA_LINEAS"})

    # 2. Interruptor Termomagnético Principal (52G)
    msp.add_lwpolyline([(112, 370), (128, 370), (128, 345), (112, 345), (112, 370)], close=True, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("QG: 3 x 250 A", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.4}).set_placement((132, 360))
    msp.add_text("Icc = 36 kA | Motorizado", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.0}).set_placement((132, 350))

    # 3. Barra Principal de Baja Tensión 380 V
    msp.add_line((80, 310), (420, 310), dxfattribs={"layer": "ELECTRICA_LINEAS"})
    msp.add_text("BARRA GENERAL BT 380 V, 3F+N, 60 Hz (Cu 40 x 5 mm)", dxfattribs={"layer": "ELECTRICA_LINEAS", "height": 3.0}).set_placement((120, 315))

    # Derivación 1: Regulador Electrónico de Carga (ELC) y Resistencia Lastre
    msp.add_line((160, 310), (160, 240), dxfattribs={"layer": "ELECTRICA_LINEAS"})
    msp.add_lwpolyline([(145, 240), (175, 240), (175, 200), (145, 200), (145, 240)], close=True, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("REGULADOR ELC", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.4}).set_placement((148, 225))
    msp.add_text("120 kW (PWM)", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.0}).set_placement((148, 215))
    msp.add_line((160, 200), (160, 160), dxfattribs={"layer": "ELECTRICA_LINEAS"})
    # Banco de Resistencias
    msp.add_lwpolyline([(140, 160), (180, 160), (180, 130), (140, 130), (140, 160)], close=True, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("Resistencia Lastre (Ballast)", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.2}).set_placement((135, 140))

    # Derivación 2: Servicios Auxiliares SSAA
    msp.add_line((250, 310), (250, 240), dxfattribs={"layer": "ELECTRICA_LINEAS"})
    msp.add_lwpolyline([(240, 240), (260, 240), (260, 215), (240, 215), (240, 240)], close=True, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("Tablero SSAA (Ilum, Tomas)", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.2}).set_placement((230, 200))

    # Derivación 3: Salida a Transformador Elevador y Red Primaria
    msp.add_line((360, 310), (360, 250), dxfattribs={"layer": "ELECTRICA_LINEAS"})
    # Interruptor de salida
    msp.add_lwpolyline([(352, 250), (368, 250), (368, 230), (352, 230), (352, 250)], close=True, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("Q-TRAFO: 3 x 200 A", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.2}).set_placement((372, 240))
    msp.add_line((360, 230), (360, 180), dxfattribs={"layer": "ELECTRICA_LINEAS"})

    # Transformador Elevador (Símbolo 2 círculos entrelazados)
    msp.add_circle((360, 165), 14.0, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_circle((360, 145), 14.0, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("TRAFO 125 kVA", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.5}).set_placement((380, 160))
    msp.add_text("0.38 / 22.9 kV | Dyn5", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.2}).set_placement((380, 150))
    msp.add_text("A Red Primaria MT", dxfattribs={"layer": "ELECTRICA_LINEAS", "height": 2.6}).set_placement((380, 120))

    # 4. Malla de Puesta a Tierra (Esquema IEEE 80 en la esquina derecha)
    mx0, my0 = 460.0, 420.0
    msp.add_text("MALLA EQUIPOTENCIAL DE PUESTA A TIERRA (IEEE 80)", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 3.0}).set_placement((mx0, my0 + 20))
    # Retícula de tierra 4x4
    for i in range(5):
        msp.add_line((mx0, my0 - i * 15), (mx0 + 60, my0 - i * 15), dxfattribs={"layer": "CIVIL_TERRENO"})
        msp.add_line((mx0 + i * 15, my0), (mx0 + i * 15, my0 - 60), dxfattribs={"layer": "CIVIL_TERRENO"})
        # Electrodos verticales en esquinas
        msp.add_circle((mx0 + i * 15, my0), 1.5, dxfattribs={"layer": "COTAS_Y_NIVELES"})
        msp.add_circle((mx0 + i * 15, my0 - 60), 1.5, dxfattribs={"layer": "COTAS_Y_NIVELES"})
    msp.add_text("Cable Cu Desnudo 50 mm² | Rpat <= 10 Ω", dxfattribs={"layer": "CIVIL_TERRENO", "height": 2.2}).set_placement((mx0, my0 - 72))

    doc.saveas(ruta_dxf)
    return ruta_dxf


def generar_plano_08_subestacion_sab1(ruta_dxf: str) -> str:
    """Plano 08 (SE-01): Subestación Aérea Biposte SAB-1 e Interconexión a Red Primaria."""
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    configurar_capas_estandar(doc)

    notas = [
        "Estructura biposte con postes de Concreto Armado Centrifugado C.A.C. 13/400 (NTP 339.027).",
        "Interdistancia entre ejes de postes: 2.00 m. Empotramiento reglamentario: 1.50 m en suelo compactado.",
        "Plataforma metálica con perfiles UPN-120 galvanizados en caliente según ASTM A123.",
        "Seccionamiento en media tensión: Cortacircuito fusible Cut-Out 27 kV, 100 A, BIL 150 kV.",
        "Protección contra sobretensiones atmosféricas: Pararrayos de Óxido Metálico (ZnO) 21 kV, 10 kA."
    ]
    dibujar_marco_y_cajetin(
        msp,
        codigo_lamina="SE-01",
        titulo_plano="SUBESTACIÓN AÉREA BIPOSTE SAB-1 100 kVA (22.9 / 0.38 kV)",
        especialidad="SISTEMAS DE DISTRIBUCIÓN",
        escala="1 : 25 / 1 : 50",
        notas=notas
    )

    msp.add_text("ARMADO NORMALIZADO DGE SAB-1: SUBESTACIÓN BIPOSTE 22.9 kV (R.D. 018-2003-EM/DGE)", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 4.5}).set_placement((60.0, 530.0))

    # Dibujo de Subestación Frontal
    # Escala modelo en plano: Poste H = 13.0 m -> 260 mm (1m = 20mm)
    px_izq, px_der = 240.0, 280.0    # 2.0 m intereje = 40 mm
    y_base = 200.0                   # Nivel de Terreno Natural
    y_cima = y_base + 230.0          # Cima a +11.50 m sobre suelo (1.5m empotrado)

    # 1. Línea de Terreno Natural
    msp.add_line((180, y_base), (340, y_base), dxfattribs={"layer": "CIVIL_TERRENO"})
    msp.add_text("Nivel de Terreno Natural (N.T.N.)", dxfattribs={"layer": "CIVIL_TERRENO", "height": 2.4}).set_placement((345, y_base))

    # 2. Postes CAC 13/400
    # Poste Izquierdo
    msp.add_lwpolyline([(px_izq - 4, y_base - 30), (px_izq + 4, y_base - 30), (px_izq + 2, y_cima), (px_izq - 2, y_cima), (px_izq - 4, y_base - 30)], close=True, dxfattribs={"layer": "CIVIL_CONCRETO"})
    # Poste Derecho
    msp.add_lwpolyline([(px_der - 4, y_base - 30), (px_der + 4, y_base - 30), (px_der + 2, y_cima), (px_der - 2, y_cima), (px_der - 4, y_base - 30)], close=True, dxfattribs={"layer": "CIVIL_CONCRETO"})
    msp.add_text("Postes C.A.C. 13/400 (NTP 339.027)", dxfattribs={"layer": "CIVIL_CONCRETO", "height": 2.6}).set_placement((220, y_base - 40))

    # 3. Plataforma Metálica Portatransformador (a cota +6.0 m -> y = y_base + 120 mm)
    y_plat = y_base + 120.0
    msp.add_lwpolyline([(px_izq - 15, y_plat), (px_der + 15, y_plat), (px_der + 15, y_plat + 6), (px_izq - 15, y_plat + 6), (px_izq - 15, y_plat)], close=True, dxfattribs={"layer": "0_MARCO_Y_BORDE"})
    msp.add_text("Plataforma UPN-120 F°G°", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.2}).set_placement((px_der + 20, y_plat + 2))

    # 4. Transformador Trifásico 100/125 kVA (Cuba y boquillas MT)
    tx0 = (px_izq + px_der) / 2.0 - 15.0
    msp.add_lwpolyline([(tx0, y_plat + 6), (tx0 + 30, y_plat + 6), (tx0 + 30, y_plat + 32), (tx0, y_plat + 32), (tx0, y_plat + 6)], close=True, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("TRAFO 100 kVA", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.4}).set_placement((tx0 + 4, y_plat + 18))
    # Boquillas MT (3 aisladores)
    for bx in [tx0 + 5, tx0 + 15, tx0 + 25]:
        msp.add_line((bx, y_plat + 32), (bx, y_plat + 42), dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
        msp.add_circle((bx, y_plat + 42), 1.5, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})

    # 5. Crucetas y Equipos MT en Cabeza (Cut-Out y Pararrayos ZnO)
    y_cruc = y_cima - 15.0
    msp.add_line((px_izq - 25, y_cruc), (px_der + 25, y_cruc), dxfattribs={"layer": "0_MARCO_Y_BORDE"})
    for eq_x in [px_izq - 18, (px_izq + px_der)/2, px_der + 18]:
        # Cut-Out inclinado
        msp.add_line((eq_x - 3, y_cruc), (eq_x - 6, y_cruc + 15), dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
        # Pararrayos
        msp.add_line((eq_x + 3, y_cruc), (eq_x + 3, y_cruc + 12), dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("Seccionadores Cut-Out 27 kV y Pararrayos ZnO 21 kV", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.4}).set_placement((190, y_cima + 5))

    # 6. Tablero de Distribución General BT IP65 (montado a +1.80m)
    y_tab = y_base + 36.0
    msp.add_lwpolyline([(px_izq - 18, y_tab), (px_izq - 4, y_tab), (px_izq - 4, y_tab + 20), (px_izq - 18, y_tab + 20), (px_izq - 18, y_tab)], close=True, dxfattribs={"layer": "ELECTRICA_EQUIPOS"})
    msp.add_text("Tablero BT IP65", dxfattribs={"layer": "ELECTRICA_EQUIPOS", "height": 2.0}).set_placement((px_izq - 35, y_tab + 8))

    # 7. Retenida Mecánica R-1
    msp.add_line((px_izq, y_cruc), (140, y_base), dxfattribs={"layer": "0_TEXTOS_ROTULO"})
    msp.add_text("Retenida Inclinada R-1 (Cable 3/8\" E.H.S.)", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.2}).set_placement((100, y_base + 40))

    doc.saveas(ruta_dxf)
    return ruta_dxf
