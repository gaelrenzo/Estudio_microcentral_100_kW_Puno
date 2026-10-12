"""
MÓDULO: src/cad_bridge/title_block.py
Generador de Formato Normalizado A1 (841 x 594 mm) con Marco, Márgenes,
Cajetín Institucional Oficial UNAP FIME, Rosa de los Vientos y Tabla de Revisiones.
"""

from typing import Dict, Any, Optional
import ezdxf
from ezdxf import colors


def configurar_capas_estandar(doc: ezdxf.document.Drawing) -> None:
    """Configura las capas normalizadas con colores y estilos según el estándar de dibujo técnico."""
    capas = [
        ("0_MARCO_Y_BORDE", colors.CYAN),
        ("0_CAJETIN", colors.YELLOW),
        ("0_TEXTOS_ROTULO", colors.WHITE),
        ("COTAS_Y_NIVELES", colors.WHITE),
        ("EJES_Y_CENTROS", colors.RED),
        ("CIVIL_CONCRETO", colors.CYAN),
        ("CIVIL_TERRENO", colors.GREEN),
        ("HIDRAULICA_AGUA", colors.BLUE),
        ("MECANICA_TUBERIA", colors.MAGENTA),
        ("MECANICA_EQUIPOS", colors.YELLOW),
        ("ELECTRICA_LINEAS", colors.RED),
        ("ELECTRICA_EQUIPOS", colors.MAGENTA),
        ("NOTAS_TECNICAS", colors.WHITE),
    ]
    for nombre, color in capas:
        if nombre not in doc.layers:
            doc.layers.add(nombre, color=color)


def dibujar_marco_y_cajetin(
    msp,
    codigo_lamina: str,
    titulo_plano: str,
    especialidad: str,
    escala: str = "INDICADA",
    ancho: float = 841.0,
    alto: float = 594.0,
    margen_izq: float = 25.0,
    margen_gen: float = 10.0,
    notas: Optional[list] = None
) -> None:
    """
    Dibuja el marco exterior, marco interior con margen de archivado (25 mm)
    y cajetín institucional UNAP FIME en la esquina inferior derecha.
    """
    # 1. Borde de corte exterior
    msp.add_lwpolyline(
        [(0, 0), (ancho, 0), (ancho, alto), (0, alto), (0, 0)],
        close=True,
        dxfattribs={"layer": "0_MARCO_Y_BORDE"}
    )

    # 2. Marco interior útil
    x_min, y_min = margen_izq, margen_gen
    x_max, y_max = ancho - margen_gen, alto - margen_gen
    msp.add_lwpolyline(
        [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max), (x_min, y_min)],
        close=True,
        dxfattribs={"layer": "0_MARCO_Y_BORDE"}
    )

    # 3. Cajetín Institucional en esquina inferior derecha (Ancho = 220 mm, Alto = 100 mm)
    c_w = 220.0
    c_h = 100.0
    c_x0 = x_max - c_w
    c_y0 = y_min

    # Contorno del cajetín
    msp.add_lwpolyline(
        [(c_x0, c_y0), (x_max, c_y0), (x_max, c_y0 + c_h), (c_x0, c_y0 + c_h), (c_x0, c_y0)],
        close=True,
        dxfattribs={"layer": "0_CAJETIN"}
    )

    # Divisiones horizontales del cajetín
    y_divs = [c_y0 + 20.0, c_y0 + 38.0, c_y0 + 60.0, c_y0 + 82.0]
    for y in y_divs:
        msp.add_line((c_x0, y), (x_max, y), dxfattribs={"layer": "0_CAJETIN"})

    # Divisiones verticales en zona inferior (c_y0 a c_y0 + 20)
    msp.add_line((c_x0 + 60.0, c_y0), (c_x0 + 60.0, c_y0 + 20.0), dxfattribs={"layer": "0_CAJETIN"})
    msp.add_line((c_x0 + 120.0, c_y0), (c_x0 + 120.0, c_y0 + 20.0), dxfattribs={"layer": "0_CAJETIN"})
    msp.add_line((c_x0 + 165.0, c_y0), (c_x0 + 165.0, c_y0 + 20.0), dxfattribs={"layer": "0_CAJETIN"})

    # Textos del Cajetín
    # Franja 1: Institución
    msp.add_text("UNIVERSIDAD NACIONAL DEL ALTIPLANO PUNO", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 3.8}).set_placement((c_x0 + 110.0, c_y0 + 92.0), align=ezdxf.enums.TextEntityAlignment.CENTER)
    msp.add_text("FACULTAD DE INGENIERÍA MECÁNICA ELÉCTRICA", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 3.0}).set_placement((c_x0 + 110.0, c_y0 + 86.0), align=ezdxf.enums.TextEntityAlignment.CENTER)

    # Franja 2: Proyecto
    msp.add_text("PROYECTO:", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.2}).set_placement((c_x0 + 5.0, c_y0 + 77.0))
    msp.add_text("MODERNIZACIÓN DE MICROCENTRAL HIDROELÉCTRICA 100 kW", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 3.2}).set_placement((c_x0 + 5.0, c_y0 + 71.0))
    msp.add_text("RÍO BLANCO - OLLACHEA - CARABAYA - PUNO", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.6}).set_placement((c_x0 + 5.0, c_y0 + 64.0))

    # Franja 3: Título de Plano
    msp.add_text("CONTENIDO / PLANO:", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.2}).set_placement((c_x0 + 5.0, c_y0 + 54.0))
    msp.add_text(titulo_plano[:42], dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 3.4}).set_placement((c_x0 + 5.0, c_y0 + 47.0))
    if len(titulo_plano) > 42:
        msp.add_text(titulo_plano[42:85], dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 3.0}).set_placement((c_x0 + 5.0, c_y0 + 41.0))

    # Franja 4: Especialidad y Ubicación
    msp.add_text(f"ESPECIALIDAD: {especialidad.upper()}", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.6}).set_placement((c_x0 + 5.0, c_y0 + 31.0))
    msp.add_text("DATUM: WGS-84 / UTM ZONA 19 SUR | H = 2,300 - 2,420 msnm", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.2}).set_placement((c_x0 + 5.0, c_y0 + 24.0))

    # Franja 5: Metadatos inferiores
    msp.add_text("ESCALA:", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.0}).set_placement((c_x0 + 5.0, c_y0 + 14.0))
    msp.add_text(escala, dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 3.0}).set_placement((c_x0 + 15.0, c_y0 + 5.0))

    msp.add_text("FECHA:", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.0}).set_placement((c_x0 + 65.0, c_y0 + 14.0))
    msp.add_text("OCTUBRE 2026", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.8}).set_placement((c_x0 + 65.0, c_y0 + 5.0))

    msp.add_text("REV.:", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.0}).set_placement((c_x0 + 125.0, c_y0 + 14.0))
    msp.add_text("REV. 01", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.8}).set_placement((c_x0 + 125.0, c_y0 + 5.0))

    msp.add_text("LÁMINA N°:", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 2.0}).set_placement((c_x0 + 170.0, c_y0 + 14.0))
    msp.add_text(codigo_lamina, dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 4.5}).set_placement((c_x0 + 175.0, c_y0 + 4.0))

    # 4. Rosa de los Vientos (Norte Magnético / Geográfico)
    norte_x = x_max - 25.0
    norte_y = y_max - 25.0
    msp.add_circle((norte_x, norte_y), 12.0, dxfattribs={"layer": "0_MARCO_Y_BORDE"})
    msp.add_lwpolyline(
        [(norte_x, norte_y + 12.0), (norte_x - 3.5, norte_y - 8.0), (norte_x, norte_y - 2.0), (norte_x, norte_y + 12.0)],
        close=True,
        dxfattribs={"layer": "0_MARCO_Y_BORDE"}
    )
    msp.add_text("N", dxfattribs={"layer": "0_TEXTOS_ROTULO", "height": 4.5}).set_placement((norte_x, norte_y + 14.0), align=ezdxf.enums.TextEntityAlignment.CENTER)

    # 5. Cuadro de Notas Técnicas si existen
    if notas:
        nota_x = x_min + 10.0
        nota_y = y_min + 12.0
        msp.add_text("NOTAS TÉCNICAS Y ESPECIFICACIONES GENERALES:", dxfattribs={"layer": "NOTAS_TECNICAS", "height": 2.8}).set_placement((nota_x, nota_y + (len(notas) * 4.5) + 2.0))
        for i, n in enumerate(notas):
            msp.add_text(f"{i+1}. {n}", dxfattribs={"layer": "NOTAS_TECNICAS", "height": 2.2}).set_placement((nota_x, nota_y + ((len(notas) - 1 - i) * 4.5)))
