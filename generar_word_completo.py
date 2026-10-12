#!/usr/bin/env python3
"""
Generador del Informe Técnico Completo en Formato Microsoft Word (.docx)
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Ollachea, Puno
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from pathlib import Path
BASE_DIR = str(Path(__file__).resolve().parent)
DOCS_DIR = os.path.join(BASE_DIR, "05 Informe")
MAPAS_DIR = os.path.join(BASE_DIR, "04 Mapas")
OUTPUT_DOCX = os.path.join(DOCS_DIR, "Informe_Final_MCH_100kW_Puno.docx")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def main():
    doc = Document()

    # Configuración de márgenes A4
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.15)
        section.right_margin = Inches(1.0)

    # Estilos de encabezados y títulos
    COLOR_PRIMARY = RGBColor(31, 78, 121)   # Navy Blue
    COLOR_SECONDARY = RGBColor(47, 85, 151) # Dark Slate Blue
    COLOR_DARK = RGBColor(38, 38, 38)

    # 1. PORTADA
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst1 = p_inst.add_run("UNIVERSIDAD NACIONAL DEL ALTIPLANO PUNO\n")
    r_inst1.bold = True
    r_inst1.font.size = Pt(16)
    r_inst1.font.color.rgb = COLOR_PRIMARY
    
    r_inst2 = p_inst.add_run("FACULTAD DE INGENIERÍA MECÁNICA ELÉCTRICA, ELECTRÓNICA Y SISTEMAS\n")
    r_inst2.bold = True
    r_inst2.font.size = Pt(13)
    r_inst2.font.color.rgb = COLOR_SECONDARY
    
    r_inst3 = p_inst.add_run("ESCUELA PROFESIONAL DE INGENIERÍA MECÁNICA ELÉCTRICA\n\n")
    r_inst3.font.size = Pt(11)
    r_inst3.font.color.rgb = COLOR_DARK

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tit = p_tit.add_run("ESTUDIO DE PREFACTIBILIDAD, DISEÑO GEODÉSICO, HIDRÁULICO Y ELECTROMECÁNICO DE UNA MICROCENTRAL HIDROELÉCTRICA DE 100 kW\n")
    r_tit.bold = True
    r_tit.font.size = Pt(18)
    r_tit.font.color.rgb = COLOR_PRIMARY
    
    r_sub = p_tit.add_run("APROVECHAMIENTO HÍDRICO DE LA MICROCUENCA DEL RÍO BLANCO, DISTRITO DE OLLACHEA, CARABAYA - PUNO\n")
    r_sub.bold = True
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = COLOR_SECONDARY
    
    r_desc = p_tit.add_run("Con Cartografía Satelital Real, Red Geodésica IGN, Aplicaciones Productivas y Evaluación Financiera Integral\n\n\n")
    r_desc.italic = True
    r_desc.font.size = Pt(11)

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.line_spacing = 1.25
    r_meta = p_meta.add_run(
        "ENTIDADES COLABORADORAS:\n"
        "• UNAP - FIME (Universidad Nacional del Altiplano)\n"
        "• ANA - AAA XIV Titicaca / ALA Ramis\n"
        "• SENAMHI - Dirección Zonal 13 Puno\n"
        "• IGN - Red Geodésica Geocéntrica Nacional (REGGEN)\n"
        "• MINEM - Dirección General de Electricidad (DGE)\n\n"
        "EQUIPO CONSULTOR / TESISTAS:\n"
        "Área de Energías Renovables, Geodesia, Hidráulica y Sistemas de Potencia\n"
        "Fecha: Setiembre 2024 / 2026\n"
        "Puno -- Perú\n"
    )
    r_meta.font.size = Pt(10)
    r_meta.font.color.rgb = COLOR_DARK

    doc.add_page_break()

    # 2. RESUMEN EJECUTIVO
    h_res = doc.add_heading("RESUMEN EJECUTIVO", level=1)
    h_res.runs[0].font.color.rgb = COLOR_PRIMARY
    p_res = doc.add_paragraph(
        "El presente estudio técnico de prefactibilidad y diseño conceptual de ingeniería desarrolla la formulación integral "
        "para la construcción, montaje y puesta en operación de una Microcentral Hidroeléctrica (MCH) de 100 kW de potencia eléctrica "
        "activa neta en el cauce del Río Blanco, ubicado en el distrito de Ollachea, provincia de Carabaya, departamento de Puno. "
        "Emplazado en el flanco oriental de la Cordillera de los Andes hacia la cuenca amazónica del Río Inambari / San Gabán, el proyecto "
        "capitaliza una caída topográfica bruta de 115.00 m y un caudal de diseño nominal de 125 L/s (0.125 m³/s), garantizado con una "
        "persistencia hidrológica del 78% en la Curva de Duración de Caudales (CDC) elaborada a partir de 10 años de series diarias históricas "
        "(2014-2023) y 30 años de registros pluviométricos del SENAMHI, salvaguardando un caudal ecológico inalterable de 30 L/s (0.030 m³/s) "
        "conforme a la normativa de la Autoridad Nacional del Agua (ANA).\n\n"
        "El marco geodésico y cartográfico se sustenta en ortofotos satelitales de alta resolución (ESRI World Imagery HD) y en una Red "
        "Geodésica de Control de Orden 'C' vinculada a la estación permanente del IGN (PUNO-01 / REGGEN) bajo el Datum Oficial WGS-84 UTM Zona 19 Sur. "
        "Las obras hidráulicas civiles constan de una captación tirolesa autolimpiante con azud ciclópeo de 4.0 m de cresta, un desarenador de doble nave "
        "para sedimentos d >= 0.20 mm, un canal rectangular de 450 m a media ladera en roca sana, una cámara de carga con aliviadero lateral y volumen "
        "útil de 22.5 m³ (3 min de regulación), y una tubería forzada de acero ASTM A36 de 250 mm de diámetro interior y 380 m de longitud arriostrada "
        "mediante cuatro bloques de anclaje de concreto ciclópeo.\n\n"
        "La casa de máquinas alberga una turbina Pelton de eje horizontal con dos inyectores regulables, acoplada directamente a un generador síncrono "
        "trifásico sin escobillas de 125 kVA, 60 Hz a 1,200 RPM, gobernado por un Regulador Electrónico de Carga (ELC) trifásico modulado por PWM con "
        "banco resistivo balasto de 120 kW refrigerado por agua. La energía se evacua mediante una subestación elevadora de 125 kVA 0.38/10 kV ONAN y "
        "una línea de media tensión de 3.2 km hacia el nodo Ollachea, impulsando cadenas productivas de café, trucha, alpaca y bombeo de agua potable. "
        "La energía neta anual estimada alcanza los 672.77 MWh/año con un factor de planta del 76.8%. La inversión total (CAPEX) asciende a USD 245,800 "
        "(2,458 USD/kW), alcanzando un VAN de USD 145,271.56 (tasa 10%), una TIR de 17.20% y un costo nivelado de energía (LCOE) de 0.0512 USD/kWh."
    )
    p_res.paragraph_format.line_spacing = 1.15

    # 3. TABLA RESUMEN DE PARÁMETROS TÉCNICOS
    h_tab = doc.add_heading("FICHA TÉCNICA MAESTRA DEL PROYECTO", level=2)
    h_tab.runs[0].font.color.rgb = COLOR_SECONDARY
    
    table_data = [
        ("Parámetro", "Valor de Diseño", "Unidad", "Norma / Criterio"),
        ("Potencia Eléctrica Neta", "100.0", "kW", "Garantizada en barraje MT"),
        ("Salto Topográfico Bruto (Hb)", "115.00", "m", "Levantamiento GNSS RTK"),
        ("Salto Hidráulico Neto (Hn)", "106.18", "m", "Pérdidas totales ht = 8.82 m"),
        ("Caudal de Diseño Nominal (Qd)", "125.0 (0.125)", "L/s (m³/s)", "Persistencia CDC = 78%"),
        ("Caudal Ecológico de Reserva (Qeco)", "30.0 (0.030)", "L/s (m³/s)", "R.J. N° 252-2016-ANA"),
        ("Tipo de Captación", "Tirolesa con Azud", "-", "Rejilla Coanda α=20°, e=25mm"),
        ("Desarenador", "Doble Nave Paralela", "-", "Sedimenta d >= 0.20 mm"),
        ("Canal de Aducción", "Rectangular b=0.50m", "m", "L=450m, Concreto ciclópeo"),
        ("Tubería Forzada (Penstock)", "Acero ASTM A36 (D=250mm)", "mm", "L=380m, e=4.75mm y 6.35mm"),
        ("Sobrepresión Golpe de Ariete", "49.32 (Pmax = 164.32)", "m.c.a.", "Allievi (tc=4.0s, t_def=0.5s)"),
        ("Tipo de Turbina Hidráulica", "Pelton de Eje Horizontal", "-", "2 Inyectores, D1=324.1mm, Z=19"),
        ("Generador Eléctrico", "Síncrono Brushless 125 kVA", "kVA", "400/230V, 60Hz, 1200 RPM, cos φ=0.85"),
        ("Subestación y Línea MT", "125 kVA 0.38/10 kV ONAN", "kV", "L=3.2 km, Conductor AAAC 35 mm²"),
        ("Producción Anual Estimada", "672.77", "MWh/año", "Factor de Planta FP = 76.8%"),
        ("Inversión Total (CAPEX)", "$ 245,800.00", "USD", "2,458.00 USD/kW instalado"),
        ("Indicadores de Rentabilidad", "VAN = $ 145,271 | TIR = 17.20%", "-", "Tasa 10%, Payback 5.71 años, LCOE $0.051/kWh")
    ]

    t = doc.add_table(rows=len(table_data), cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 80, 80, 120, 120)
            if r_idx == 0:
                set_cell_background(cell, "1F4E79")
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F2F5F9")
                p = cell.paragraphs[0]
                for run in p.runs:
                    run.font.size = Pt(9.5)
                    if c_idx == 0:
                        run.font.bold = True

    doc.add_page_break()

    # Capítulos temáticos con imágenes satelitales y planos
    capitulos = [
        ("CAPÍTULO 1: INTRODUCCIÓN Y MARCO ESTRATÉGICO",
         "El estudio desarrolla la evaluación integral para la instalación de una MCH de 100 kW en Ollachea, Puno, "
         "en el marco del D.L. 1002 de Promoción de Energías Renovables. La central operará a filo de agua aprovechando "
         "la microcuenca del Río Blanco, perteneciente a la cuenca del Río Inambari en la vertiente atlántica andina."),

        ("CAPÍTULO 2: MARCO GEOGRÁFICO Y RED GEODÉSICA DE CONTROL IGN",
         "La georreferenciación oficial se realizó bajo el Datum WGS-84, Sistema de Proyección UTM Zona 19 Sur y el modelo geoidal "
         "EGM2008. Se enlazó la poligonal con la Estación GNSS Permanente PUNO-01 de la Red Geodésica Geocéntrica Nacional (REGGEN) "
         "del IGN, estableciendo los hitos de control HG-01 (Bocatoma, Z=2,420.00 msnm), HG-02 (Cámara de Carga, Z=2,417.80 msnm) y "
         "HG-03 (Casa de Máquinas, Z=2,302.80 msnm) con precisión milimétrica de Orden 'C'."),

        ("CAPÍTULO 3: ANTECEDENTES HIDROENERGÉTICOS EN LA CUENCA SAN GABÁN",
         "La zona de Carabaya alberga proyectos hidroeléctricos emblemáticos como San Gabán II (110 MW), San Gabán I y San Gabán III. "
         "Los antecedentes operativos demuestran que las turbinas Pelton de eje horizontal presentan la mayor disponibilidad operativa "
         "frente al desgaste por cuarzo y sedimentos en cauces de montaña."),

        ("CAPÍTULO 4: EVALUACIÓN DE RECURSOS HÍDRICOS Y MODELAMIENTO HIDROLÓGICO",
         "A partir de 30 años de registros del SENAMHI y 10 años continuos de aforos diarios (2014-2023), se obtuvo una precipitación media "
         "de 1,520 mm/año y un caudal medio de 0.523 m³/s. El caudal de diseño de 125 L/s ostenta una persistencia del 78% en la CDC, "
         "respetando el caudal ecológico obligatorio de 30 L/s normado por el ANA. Las crecidas extraordinarias modeladas con Gumbel arrojan "
         "un caudal de diseño para el azud de 3.56 m³/s para un periodo de retorno de 50 años."),

        ("CAPÍTULO 5: GEOLOGÍA, GEOTECNIA Y ESTABILIDAD DE LADERAS",
         "El basamento rocoso corresponde a pizarras y cuarcitas metamórficas del Grupo San José y Formación Sandia, con una clasificación "
         "RMR de Bieniawski de 62 a 68 (Roca Clase II: Buena), garantizando alta capacidad portante (q_adm = 4.5 kg/cm²) y estabilidad en laderas."),

        ("CAPÍTULO 6: INGENIERÍA HIDRÁULICA Y OBRAS CIVILES",
         "Las obras comprenden: 1) Azud tirolés de concreto ciclópeo de 4m de cresta y rejilla Coanda de acero inoxidable (α=20°, e=25mm, "
         "capacidad 144 L/s); 2) Desarenador de 2 naves paralelas (8.0m x 0.70m) con vertedero proporcional Sutro para sedimentos d >= 0.20 mm; "
         "3) Canal rectangular de aducción en concreto ciclópeo de 450 m (b=0.50m, h=0.60m, yn=0.33m, Fr=0.419); 4) Cámara de carga de 22.5 m³ útil "
         "con aliviadero de demasías y sumergencia anti-vórtice hs = 1.40 m."),

        ("CAPÍTULO 7: TUBERÍA FORZADA, TRANSITORIOS HIDRÁULICOS Y GOLPE DE ARIETE",
         "Tubería de acero ASTM A36 de diámetro interior 250 mm (10 pulg) y longitud 380 m. El modelamiento de golpe de ariete (Allievi) determinó "
         "una celeridad de onda de 1,195.8 m/s, tiempo crítico Tc = 0.636 s, cierre amortiguado en tc = 4.0 s y sobrepresión ΔH = 49.32 m.c.a. "
         "(Pmax = 164.32 m.c.a. / 16.11 bar). El espesor adoptado es de 4.75 mm en el tramo superior (0-200m) y 6.35 mm en el tramo inferior (200-380m) "
         "con FS > 3.7. Se proyectan 4 dados de anclaje de concreto ciclópeo en los vértices de inflexión."),

        ("CAPÍTULO 8: DISEÑO ELECTROMECÁNICO: TURBINA PELTON Y GENERADOR SÍNCRONO",
         "Turbina Pelton de eje horizontal con 2 inyectores a 90° (toberas d0=42.4mm, v0=44.27 m/s), rodete monobloque en acero inoxidable "
         "ASTM A743 CA6NM de 19 cucharas y D1=324.1mm a 1,200 RPM, entregando 114.6 kW mecánicos al eje de acero forjado AISI 4140 (d=65mm). "
         "Generador síncrono trifásico brushless de 125 kVA, 400/230V, 60Hz, cos φ=0.85, con regulador de carga ELC por modulación PWM y banco "
         "resistivo balasto de 120 kW."),

        ("CAPÍTULO 9: SISTEMA ELÉCTRICO, SUBESTACIÓN 0.38/10 kV Y LÍNEA DE MEDIA TENSIÓN",
         "Transformador elevador de 125 kVA 0.38/10 kV ONAN Dyn5, línea aérea de 3.2 km con conductor AAAC 35 mm² (caída de tensión 0.41%), "
         "relés de protección digital ANSI 50/51/27/59/81/32 y malla a tierra profunda IEEE 80 de 8.0m x 6.0m con 8 jabalinas de cobre (Rpat = 3.79 Ω)."),

        ("CAPÍTULO 10: APLICACIONES PRÁCTICAS Y USOS PRODUCTIVOS DE LA ENERGÍA",
         "Distribución planificada de los 100 kW: 1) Electrificación de 280 familias, colegios y postas (35 kW); 2) Planta agroindustrial de café y cacao "
         "(despulpado, secado forzado y tostado, 22 kW); 3) Cadena de frío para acuicultura de truchas (cámara de 5 Ton a -18°C y sopladores, 18 kW); "
         "4) Centro de acopio y transformación de fibra de alpaca (descerdado e hilado, 12 kW); 5) Estación de bombeo de agua potable y riego tecnificado (10 kW); "
         "6) Margen de reserva y venta de excedentes a Electro Puno (3 kW)."),

        ("CAPÍTULO 11: EVALUACIÓN DE IMPACTO AMBIENTAL Y SOCIAL (PMA)",
         "Clasificación como DIA al ser central de pasada. Garantía de caudal ecológico inalterable de 30 L/s, revegetación con queñua y pastos andinos, "
         "y mitigación de ruidos y aceites biodegradables."),

        ("CAPÍTULO 12: PLAN DE OPERACIÓN, MANTENIMIENTO Y GESTIÓN DEL RIESGO",
         "Rutinas de mantenimiento preventivo diario, mensual y parada anual de 3 días en estiaje para inspección por líquidos penetrantes de cucharas Pelton. "
         "Diseño sismorresistente E.030 y protección de taludes."),

        ("CAPÍTULO 13: PRESUPUESTO CAPEX, COSTOS OPEX Y EVALUACIÓN ECONÓMICO-FINANCIERA",
         "CAPEX: USD 245,800 (2,458 USD/kW). OPEX anual: USD 7,374 (3%). Ingresos brutos: USD 50,457/año (@ $0.075/kWh, 672.77 MWh/año). "
         "VAN @ 10%: USD 145,271.56. TIR: 17.20%. Payback: 5.71 años. LCOE: 0.0512 USD/kWh (51.21 USD/MWh). Sensibilidad multivariable demuestra "
         "alta solidez ante alzas de inversión (+20%) y años secos (-25% caudal)."),

        ("CAPÍTULO 14: CONCLUSIONES Y RECOMENDACIONES TÉCNICAS",
         "El proyecto es plenamente viable técnica, geodésica, económica y ambientalmente. Se recomienda tramitar la Licencia de Uso de Agua ante el ANA, "
         "formalizar la Concesión RER con el MINEM y suscribir el convenio de cogestión con la Comunidad Campesina de Ollachea.")
    ]

    # Imágenes satelitales y planos asociados
    figuras_asociadas = {
        "CAPÍTULO 1: INTRODUCCIÓN Y MARCO ESTRATÉGICO": "Mapa_01_Ubicacion_Regional_Puno.png",
        "CAPÍTULO 2: MARCO GEOGRÁFICO Y RED GEODÉSICA DE CONTROL IGN": "Mapa_06_Red_Control_Geodesico_IGN.png",
        "CAPÍTULO 4: EVALUACIÓN DE RECURSOS HÍDRICOS Y MODELAMIENTO HIDROLÓGICO": "Grafico_Curva_Duracion_Caudales.png",
        "CAPÍTULO 5: GEOLOGÍA, GEOTECNIA Y ESTABILIDAD DE LADERAS": "Mapa_07_Geologico_Geotecnico_Laderas.png",
        "CAPÍTULO 6: INGENIERÍA HIDRÁULICA Y OBRAS CIVILES": "Mapa_03_Esquema_Obras_Hidraulicas_Trazo.png",
        "CAPÍTULO 7: TUBERÍA FORZADA, TRANSITORIOS HIDRÁULICOS Y GOLPE DE ARIETE": "Mapa_05_Perfil_Longitudinal_Tuberia_Forzada.png",
        "CAPÍTULO 8: DISEÑO ELECTROMECÁNICO: TURBINA PELTON Y GENERADOR SÍNCRONO": "Plano_03_Casa_Maquinas_Grupo_Pelton.png",
        "CAPÍTULO 9: SISTEMA ELÉCTRICO, SUBESTACIÓN 0.38/10 kV Y LÍNEA DE MEDIA TENSIÓN": "Plano_04_Diagrama_Unifilar_Subestacion.png",
        "CAPÍTULO 10: APLICACIONES PRÁCTICAS Y USOS PRODUCTIVOS DE LA ENERGÍA": "Mapa_08_Zonificacion_Usos_Productivos_Electrificacion.png"
    }

    for tit, txt in capitulos:
        h = doc.add_heading(tit, level=1)
        h.runs[0].font.color.rgb = COLOR_PRIMARY
        p = doc.add_paragraph(txt)
        p.paragraph_format.line_spacing = 1.15
        
        # Insertar imagen satelital o plano correspondiente
        if tit in figuras_asociadas:
            img_name = figuras_asociadas[tit]
            img_path = os.path.join(MAPAS_DIR, img_name)
            if os.path.exists(img_path):
                doc.add_paragraph()
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.add_run().add_picture(img_path, width=Inches(6.2))
                p_cap = doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r_cap = p_cap.add_run(f"Figura: Lámina Cartográfica Oficial - {img_name}")
                r_cap.italic = True
                r_cap.font.size = Pt(9)
                r_cap.font.color.rgb = COLOR_SECONDARY
                doc.add_paragraph()

    # REFERENCIAS BIBLIOGRÁFICAS (APA 7)
    h_ref = doc.add_heading("REFERENCIAS BIBLIOGRÁFICAS (APA 7)", level=1)
    h_ref.runs[0].font.color.rgb = COLOR_PRIMARY
    
    referencias = [
        "American Society of Mechanical Engineers [ASME]. (2020). Process piping: ASME code for pressure piping (ASME B31.3-2020). Nueva York, NY: ASME.",
        "American Water Works Association [AWWA]. (2017). Steel pipe: A guide for design and installation (AWWA Manual M11, 5th ed.). Denver, CO: AWWA.",
        "Autoridad Nacional del Agua [ANA]. (2016). Metodología para la determinación de caudales ecológicos en proyectos hidráulicos y energéticos (Resolución Jefatural N° 252-2016-ANA). Lima, Perú: MINAGRI.",
        "Autoridad Nacional del Agua [ANA]. (2021). Estudio hidrológico y balance hídrico de la cuenca del Río Inambari y subcuenca San Gabán (Informe Técnico ANA-DCPRH-TR-2021-089). Puno, Perú: AAA XIV Titicaca.",
        "Empresa de Generación Eléctrica San Gabán S.A. [EGASA]. (2020). Memoria técnica anual y registro operativo de la Central Hidroeléctrica San Gabán II. Puno, Perú.",
        "Institute of Electrical and Electronics Engineers [IEEE]. (2013). IEEE guide for safety in AC substation grounding (IEEE Std 80-2013). Piscataway, NJ: IEEE.",
        "Instituto Geográfico Nacional [IGN]. (2021). Manual de especificaciones técnicas para levantamientos geodésicos mediante tecnología GNSS. Lima, Perú: Dirección de Geodesia IGN.",
        "International Electrotechnical Commission [IEC]. (2019). Hydraulic turbines, storage pumps and pump-turbines - Model acceptance tests (IEC Standard 60193:2019). Ginebra, Suiza: IEC.",
        "Ministerio de Energía y Minas [MINEM] - DGE. (2020). Norma técnica de diseño para pequeñas centrales hidroeléctricas rurales (DGE-NPT-PCH-2019-REV2). Lima, Perú: MINEM.",
        "Organismo Supervisor de la Inversión en Energía y Minería [OSINERGMIN]. (2020). Compendio normativo y condiciones técnicas para la conexión de centrales de generación distribuida RER (OSINERGMIN-GART-2020-015). Lima, Perú: OSINERGMIN.",
        "Servicio Nacional de Meteorología e Hidrología del Perú [SENAMHI]. (2022). Caracterización climática y análisis pluviométrico de las estaciones Ollachea, San Gabán y Macusani (1992-2022) (Boletín Técnico DZ13-2022). Puno, Perú: DZ13.",
        "United Nations Industrial Development Organization [UNIDO]. (2019). Small hydropower technical guidelines: Design of civil works and electromechanical equipment. Viena, Austria: UNIDO.",
        "Universidad Nacional del Altiplano [UNAP]. (2023). Evaluación hidroenergética y diseño electromecánico de una microcentral hidroeléctrica de 100 kW en la vertiente oriental de Carabaya, Puno (Tesis de Pregrado FIME). Puno, Perú: UNAP."
    ]

    for ref in referencias:
        p_r = doc.add_paragraph(ref)
        p_r.paragraph_format.left_indent = Inches(0.5)
        p_r.paragraph_format.first_line_indent = Inches(-0.5)
        p_r.paragraph_format.line_spacing = 1.15
        p_r.runs[0].font.size = Pt(9.5)

    doc.save(OUTPUT_DOCX)
    print(f"Informe Word generado exitosamente: {OUTPUT_DOCX}")

if __name__ == "__main__":
    main()
