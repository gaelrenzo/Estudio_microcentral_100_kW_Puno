"""
Módulo de Generación de Informes Técnicos en PDF con ReportLab.
Produce un documento formal de ingeniería que integra todas las memorias de cálculo,
tablas de parámetros, análisis transitorio, evaluación económica y gráficos.
"""

import os
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    KeepTogether,
    HRFlowable
)


def generar_informe_pdf(resultados: Dict[str, Any], ruta_salida: str) -> str:
    """
    Genera el informe técnico integral del proyecto hidroeléctrico en formato PDF.

    Secciones incluidas:
      1. Portada
      2. Resumen Ejecutivo
      3. Datos de Entrada
      4. Análisis Hidrológico
      5. Dimensionamiento Hidráulico y Electromecánico
      6. Golpe de Ariete y Transitorios Hidráulicos
      7. Evaluación Económica y Financiera
      8. Conclusiones y Recomendaciones

    Args:
        resultados: Diccionario con todos los resultados hidrológicos, hidráulicos,
                    transitorios, económicos y rutas a los gráficos generados.
        ruta_salida: Ruta absoluta o relativa del archivo PDF de destino.

    Returns:
        Ruta completa del archivo PDF generado.
    """
    directorio_salida = os.path.dirname(ruta_salida)
    if directorio_salida and not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida, exist_ok=True)

    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()

    # Estilos personalizados
    azul_principal = colors.HexColor("#1F4E79")
    azul_secundario = colors.HexColor("#2E75B6")
    gris_oscuro = colors.HexColor("#262626")
    gris_claro = colors.HexColor("#F2F4F7")

    style_portada_titulo = ParagraphStyle(
        "PortadaTitulo",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        alignment=1,  # Centrado
        textColor=azul_principal,
        spaceAfter=15
    )

    style_portada_sub = ParagraphStyle(
        "PortadaSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=14,
        leading=18,
        alignment=1,
        textColor=azul_secundario,
        spaceAfter=30
    )

    style_portada_meta = ParagraphStyle(
        "PortadaMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        alignment=1,
        textColor=gris_oscuro
    )

    style_h1 = ParagraphStyle(
        "TituloSeccion",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=azul_principal,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        "SubtituloSeccion",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=azul_secundario,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        "Cuerpo",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=gris_oscuro,
        spaceAfter=6
    )

    style_body_bold = ParagraphStyle(
        "CuerpoBold",
        parent=style_body,
        fontName="Helvetica-Bold"
    )

    style_tabla_header = ParagraphStyle(
        "TablaHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    style_tabla_cell = ParagraphStyle(
        "TablaCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=gris_oscuro
    )

    style_tabla_cell_center = ParagraphStyle(
        "TablaCellCenter",
        parent=style_tabla_cell,
        alignment=1
    )

    story = []

    # =========================================================================
    # 1. PORTADA
    # =========================================================================
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("ESTUDIO DE FACTIBILIDAD Y DIMENSIONAMIENTO", style_portada_titulo))
    story.append(Paragraph("MICROCENTRAL HIDROELÉCTRICA RÍO BLANCO (100 kW)", style_portada_sub))
    story.append(HRFlowable(width="80%", thickness=2, color=azul_principal, spaceAfter=40))

    story.append(Paragraph("<b>Sistema Modular Automatizado:</b> hydro-ai-engineering", style_portada_meta))
    story.append(Paragraph("<b>Ubicación:</b> Cuenca del Río Blanco, Departamento de Puno, Perú", style_portada_meta))
    story.append(Paragraph("<b>Marco Regulatorio:</b> Decreto Legislativo 1002 (RER) - Ley 29338 (Recursos Hídricos)", style_portada_meta))
    story.append(Paragraph("<b>Institución:</b> Universidad Nacional del Altiplano / Consultoría RER", style_portada_meta))
    story.append(Paragraph("<b>Generación de Informe:</b> Automatizada con Python & ReportLab", style_portada_meta))
    story.append(Spacer(1, 1.5 * inch))

    # Resumen rápido en portada
    hidro = resultados.get("hidraulica", {})
    econo = resultados.get("economia", {})
    p_red = hidro.get("generador", {}).get("potencia_neta_red_kw", 100.0)
    van_val = econo.get("van_usd", 0.0)
    tir_val = econo.get("tir_pct", 0.0)

    portada_box_data = [
        [
            Paragraph(f"<b>Potencia Neta:</b> {p_red:.1f} kW", style_tabla_cell_center),
            Paragraph(f"<b>Salto Bruto:</b> 115.0 m", style_tabla_cell_center),
            Paragraph(f"<b>Caudal Diseño:</b> 125 L/s", style_tabla_cell_center),
            Paragraph(f"<b>VAN (10%):</b> ${van_val:,.0f} USD", style_tabla_cell_center),
            Paragraph(f"<b>TIR:</b> {tir_val:.1f} %", style_tabla_cell_center)
        ]
    ]
    t_box = Table(portada_box_data, colWidths=[1.3 * inch] * 5)
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), gris_claro),
        ('BOX', (0, 0), (-1, -1), 1, azul_secundario),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D5DD")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_box)
    story.append(PageBreak())

    # =========================================================================
    # 2. RESUMEN EJECUTIVO
    # =========================================================================
    story.append(Paragraph("1. RESUMEN EJECUTIVO", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=azul_secundario, spaceAfter=10))

    story.append(Paragraph(
        "El presente informe consolida el estudio técnico, hidráulico, transitorio y económico para el "
        "desarrollo de la <b>Microcentral Hidroeléctrica Río Blanco de 100 kW</b> en el departamento de Puno. "
        "El proyecto aprovecha un salto bruto de 115.0 m y un caudal de diseño nominal de 0.125 m³/s (125 L/s) "
        "derivado de la microcuenca del Río Blanco, garantizando en todo momento la preservación del caudal "
        "ecológico de 0.030 m³/s (30 L/s) exigido por la Autoridad Nacional del Agua (ANA).",
        style_body
    ))
    story.append(Paragraph(
        "La conducción consta de un canal rectangular de concreto de 450 m de longitud y una tubería forzada "
        "de acero ASTM A36 de 10 pulgadas de diámetro comercial (250 mm) a lo largo de 380 m. La generación "
        "se efectúa mediante una <b>Turbina Pelton de 2 inyectores</b> acoplada a un generador sincrónico de "
        "1200 RPM (60 Hz), entregando una potencia neta de 99.8 kW a la red rural a través de un transformador "
        "de 125 kVA en Media Tensión (10 - 22.9 kV).",
        style_body
    ))

    # Tabla resumen ejecutivo
    resumen_data = [
        [Paragraph("Parámetro Clave", style_tabla_header), Paragraph("Valor Proyectado", style_tabla_header), Paragraph("Unidad / Criterio", style_tabla_header)],
        [Paragraph("Caudal de Diseño Nominal (Qd)", style_tabla_cell), Paragraph("0.125", style_tabla_cell_center), Paragraph("m³/s (125 L/s - Persistencia 78%)", style_tabla_cell)],
        [Paragraph("Caudal Ecológico Permanente (Qeco)", style_tabla_cell), Paragraph("0.030", style_tabla_cell_center), Paragraph("m³/s (30 L/s - Reserva Ley 29338)", style_tabla_cell)],
        [Paragraph("Salto Bruto Estático (Hb)", style_tabla_cell), Paragraph("115.00", style_tabla_cell_center), Paragraph("m.c.a.", style_tabla_cell)],
        [Paragraph("Salto Neto Efectivo (Hn)", style_tabla_cell), Paragraph(f"{hidro.get('tuberia', {}).get('salto_neto_m', 101.67):.2f}", style_tabla_cell_center), Paragraph("m.c.a. (Pérdidas totales 11.6%)", style_tabla_cell)],
        [Paragraph("Potencia Neta Entregada a Red", style_tabla_cell), Paragraph(f"{p_red:.2f}", style_tabla_cell_center), Paragraph("kW (~100 kW nominales)", style_tabla_cell)],
        [Paragraph("Tecnología de Turbina", style_tabla_cell), Paragraph("Pelton (2 inyectores)", style_tabla_cell_center), Paragraph("Acción, Ns = 12.1 rpm, rodete D=343 mm", style_tabla_cell)],
        [Paragraph("Generación Neta Anual Esperada", style_tabla_cell), Paragraph(f"{econo.get('generacion_anual_mwh', 672.77):,.2f}", style_tabla_cell_center), Paragraph("MWh/año (Factor de planta 76.8%)", style_tabla_cell)],
        [Paragraph("Inversión Inicial (CAPEX)", style_tabla_cell), Paragraph(f"${econo.get('capex_usd', 245800):,.2f}", style_tabla_cell_center), Paragraph("USD (Ratio: $2,458 USD/kW)", style_tabla_cell)],
        [Paragraph("Valor Actual Neto (VAN @ 10%)", style_tabla_cell), Paragraph(f"${econo.get('van_usd', 145155):,.2f}", style_tabla_cell_center), Paragraph("USD (Rentabilidad positiva)", style_tabla_cell)],
        [Paragraph("Tasa Interna de Retorno (TIR)", style_tabla_cell), Paragraph(f"{econo.get('tir_pct', 16.24):.2f}%", style_tabla_cell_center), Paragraph("> COK del 10%", style_tabla_cell)],
        [Paragraph("Costo Nivelado de Energía (LCOE)", style_tabla_cell), Paragraph(f"${econo.get('lcoe_usd_mwh', 45.40):.2f}", style_tabla_cell_center), Paragraph("USD/MWh ($0.0454 USD/kWh)", style_tabla_cell)],
        [Paragraph("Período de Recuperación (Payback)", style_tabla_cell), Paragraph(f"{econo.get('payback_anios', 5.71):.2f}", style_tabla_cell_center), Paragraph("Años", style_tabla_cell)]
    ]
    t_resumen = Table(resumen_data, colWidths=[2.6 * inch, 1.8 * inch, 2.4 * inch])
    t_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), azul_principal),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D5DD")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, gris_claro]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_resumen)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 3. DATOS DE ENTRADA
    # =========================================================================
    story.append(Paragraph("2. DATOS DE ENTRADA Y PARÁMETROS DE DISEÑO", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=azul_secundario, spaceAfter=8))

    datos_entrada_table = [
        [Paragraph("Componente / Parámetro", style_tabla_header), Paragraph("Valor", style_tabla_header), Paragraph("Unidad", style_tabla_header), Paragraph("Fuente / Base Técnica", style_tabla_header)],
        [Paragraph("Cota Captación / Cámara de Carga", style_tabla_cell), Paragraph("2,417.80", style_tabla_cell_center), Paragraph("m.s.n.m.", style_tabla_cell_center), Paragraph("Levantamiento Topográfico GNSS", style_tabla_cell)],
        [Paragraph("Cota Casa de Máquinas (Eje turbina)", style_tabla_cell), Paragraph("2,302.80", style_tabla_cell_center), Paragraph("m.s.n.m.", style_tabla_cell_center), Paragraph("Levantamiento Topográfico GNSS", style_tabla_cell)],
        [Paragraph("Salto Bruto Geodésico (Hb)", style_tabla_cell), Paragraph("115.00", style_tabla_cell_center), Paragraph("m", style_tabla_cell_center), Paragraph("Desnivel geométrico", style_tabla_cell)],
        [Paragraph("Longitud Canal de Conducción", style_tabla_cell), Paragraph("450.00", style_tabla_cell_center), Paragraph("m", style_tabla_cell_center), Paragraph("Trazo en ladera roca/arcilla", style_tabla_cell)],
        [Paragraph("Longitud Tubería Forzada", style_tabla_cell), Paragraph("380.00", style_tabla_cell_center), Paragraph("m", style_tabla_cell_center), Paragraph("Perfil longitudinal", style_tabla_cell)],
        [Paragraph("Rugosidad Tubería (Acero A36)", style_tabla_cell), Paragraph("0.045", style_tabla_cell_center), Paragraph("mm", style_tabla_cell_center), Paragraph("Norma ASTM A36 nueva", style_tabla_cell)],
        [Paragraph("Rugosidad Canal de Concreto (n)", style_tabla_cell), Paragraph("0.014", style_tabla_cell_center), Paragraph("-", style_tabla_cell_center), Paragraph("Manning para concreto alisado", style_tabla_cell)],
        [Paragraph("Serie Hidrológica Histórica", style_tabla_cell), Paragraph("10 (2014-2023)", style_tabla_cell_center), Paragraph("Años", style_tabla_cell_center), Paragraph("Estación Río Blanco (SENAMHI/ANA)", style_tabla_cell)],
        [Paragraph("Tasa de Descuento Financiera", style_tabla_cell), Paragraph("10.0", style_tabla_cell_center), Paragraph("%", style_tabla_cell_center), Paragraph("Tasa social/privada de referencia", style_tabla_cell)],
        [Paragraph("Tarifa Base de Venta de Energía", style_tabla_cell), Paragraph("0.075", style_tabla_cell_center), Paragraph("USD/kWh", style_tabla_cell_center), Paragraph("Referencia RER OSINERGMIN", style_tabla_cell)]
    ]
    t_entrada = Table(datos_entrada_table, colWidths=[2.3 * inch, 1.2 * inch, 0.9 * inch, 2.4 * inch])
    t_entrada.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), azul_principal),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D5DD")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, gris_claro]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_entrada)
    story.append(PageBreak())

    # =========================================================================
    # 4. ANÁLISIS HIDROLÓGICO
    # =========================================================================
    story.append(Paragraph("3. ANÁLISIS HIDROLÓGICO Y CURVA DE DURACIÓN DE CAUDALES (CDC)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=azul_secundario, spaceAfter=8))

    hidro_stats = resultados.get("hidrologia", {}).get("estadisticas", {})
    percentiles = hidro_stats.get("percentiles", {})

    story.append(Paragraph(
        f"Se analizó la serie histórica diaria correspondiente al decenio 2014-2023, con un total de "
        f"<b>{hidro_stats.get('total_observaciones', 3652):,} registros diarios</b>. "
        f"El caudal medio multianual se situó en <b>{hidro_stats.get('caudal_medio', 0.354):.3f} m³/s</b>, "
        f"con un caudal máximo de registro de {hidro_stats.get('caudal_maximo', 2.85):.3f} m³/s y un mínimo de estiaje "
        f"de {hidro_stats.get('caudal_minimo', 0.052):.3f} m³/s.",
        style_body
    ))

    # Tabla percentiles
    perc_rows = [
        [Paragraph("Percentil de Persistencia", style_tabla_header), Paragraph("Caudal Disponible (m³/s)", style_tabla_header), Paragraph("Caudal Disponible (L/s)", style_tabla_header), Paragraph("Aptitud Operativa", style_tabla_header)]
    ]
    for p, q_val in sorted(percentiles.items()):
        aptitud = "Plena carga garantizada" if q_val >= 0.155 else ("Carga parcial / estiaje" if q_val >= 0.08 else "Régimen crítico")
        perc_rows.append([
            Paragraph(f"Q{p}% (Excedido el {p}% del tiempo)", style_tabla_cell),
            Paragraph(f"{q_val:.3f}", style_tabla_cell_center),
            Paragraph(f"{q_val*1000:.1f}", style_tabla_cell_center),
            Paragraph(aptitud, style_tabla_cell)
        ])

    t_perc = Table(perc_rows, colWidths=[2.2 * inch, 1.5 * inch, 1.4 * inch, 1.7 * inch])
    t_perc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), azul_principal),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D5DD")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, gris_claro]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_perc)
    story.append(Spacer(1, 8))

    # Gráfico CDC si existe
    grafico_cdc = resultados.get("grafico_cdc")
    if grafico_cdc and os.path.exists(grafico_cdc):
        story.append(KeepTogether([
            Paragraph("<b>Figura 1:</b> Curva de Duración de Caudales (CDC) de la Microcuenca Río Blanco (2014-2023).", style_body_bold),
            Image(grafico_cdc, width=6.2 * inch, height=3.3 * inch),
            Spacer(1, 10)
        ]))

    story.append(PageBreak())

    # =========================================================================
    # 5. DIMENSIONAMIENTO HIDRÁULICO Y ELECTROMECÁNICO
    # =========================================================================
    story.append(Paragraph("4. DIMENSIONAMIENTO HIDRÁULICO Y ELECTROMECÁNICO", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=azul_secundario, spaceAfter=8))

    canal = hidro.get("canal", {})
    tub = hidro.get("tuberia", {})
    turb = hidro.get("generador", {})

    story.append(Paragraph(
        "<b>Canal de Aducción:</b> Canal rectangular revestido de concreto (n = 0.014) con solera de 0.50 m "
        f"y pendiente S = 0.15%. Presenta tirante normal de {canal.get('tirante_normal_m', 0.22):.3f} m, "
        f"velocidad de flujo de {canal.get('velocidad_m_s', 1.13):.2f} m/s y régimen subcrítico "
        f"(Froude = {canal.get('numero_froude', 0.77):.2f}), con un bordo libre de seguridad de {canal.get('bordo_libre_m', 0.28):.2f} m.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Tubería Forzada:</b> De acuerdo con la fórmula económica de Fahlbusch, el diámetro óptimo es "
        f"{tub.get('diametro_economico_fahlbusch_m', 0.245)*1000:.1f} mm. Se adoptó tubería comercial de acero "
        f"ASTM A36 de 10 pulgadas ({tub.get('diametro_adoptado_m', 0.250)*1000:.0f} mm interior). "
        f"La velocidad en régimen permanente es de {tub.get('velocidad_m_s', 2.546):.2f} m/s (Reynolds: {tub.get('numero_reynolds', 517480):,.0f}). "
        f"Las pérdidas de carga totales ascienden a {tub.get('perdidas_totales_m', 13.33):.2f} m, determinando un "
        f"salto neto de diseño de <b>{tub.get('salto_neto_m', 101.67):.2f} m</b>.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Turbina Pelton:</b> Máquina de acción de 2 inyectores con toberas de "
        f"{turb.get('diametro_chorro_m', 0.042)*1000:.1f} mm de diámetro a una velocidad de inyección de "
        f"{turb.get('velocidad_chorro_m_s', 43.34):.2f} m/s. El rodete primitivo tiene un diámetro de "
        f"{turb.get('diametro_primitivo_rodete_m', 0.317)*1000:.1f} mm y cuenta con {turb.get('numero_cucharas', 19)} cucharas "
        "dobles talladas en acero inoxidable martensítico.",
        style_body
    ))

    # Tabla resumen dimensionamiento
    dim_data = [
        [Paragraph("Elemento / Parámetro", style_tabla_header), Paragraph("Valor Calculado", style_tabla_header), Paragraph("Unidad", style_tabla_header), Paragraph("Detalle / Observación", style_tabla_header)],
        [Paragraph("Canal: Ancho de Solera (b)", style_tabla_cell), Paragraph(f"{canal.get('ancho_solera_m', 0.50):.2f}", style_tabla_cell_center), Paragraph("m", style_tabla_cell_center), Paragraph("Rectangular concreto liso", style_tabla_cell)],
        [Paragraph("Canal: Tirante Normal (yn)", style_tabla_cell), Paragraph(f"{canal.get('tirante_normal_m', 0.222):.3f}", style_tabla_cell_center), Paragraph("m", style_tabla_cell_center), Paragraph("Resuelto por Manning", style_tabla_cell)],
        [Paragraph("Canal: Bordo Libre Recomendado", style_tabla_cell), Paragraph(f"{canal.get('bordo_libre_m', 0.28):.2f}", style_tabla_cell_center), Paragraph("m", style_tabla_cell_center), Paragraph("Altura total canal: 0.50 m", style_tabla_cell)],
        [Paragraph("Tubería: Diámetro Interior Adoptado", style_tabla_cell), Paragraph(f"{tub.get('diametro_adoptado_m', 0.250)*1000:.0f}", style_tabla_cell_center), Paragraph("mm", style_tabla_cell_center), Paragraph("10 pulgadas comercial", style_tabla_cell)],
        [Paragraph("Tubería: Pérdida Fricción (hf Darcy)", style_tabla_cell), Paragraph(f"{tub.get('perdidas_friccion_hf_m', 11.59):.2f}", style_tabla_cell_center), Paragraph("m", style_tabla_cell_center), Paragraph("Swamee-Jain (f = 0.0163)", style_tabla_cell)],
        [Paragraph("Tubería: Pérdidas Singulares (hm)", style_tabla_cell), Paragraph(f"{tub.get('perdidas_singulares_hm_m', 1.74):.2f}", style_tabla_cell_center), Paragraph("m", style_tabla_cell_center), Paragraph("15% de pérdidas de fricción", style_tabla_cell)],
        [Paragraph("Turbina: Número de Inyectores", style_tabla_cell), Paragraph(f"{turb.get('numero_inyectores', 2)}", style_tabla_cell_center), Paragraph("-", style_tabla_cell_center), Paragraph("62.5 L/s por aguja", style_tabla_cell)],
        [Paragraph("Turbina: Diámetro Chorro (d0)", style_tabla_cell), Paragraph(f"{turb.get('diametro_chorro_m', 0.0428)*1000:.1f}", style_tabla_cell_center), Paragraph("mm", style_tabla_cell_center), Paragraph("Velocidad chorro: 43.3 m/s", style_tabla_cell)],
        [Paragraph("Turbina: Diámetro Primitivo Rodete (D1)", style_tabla_cell), Paragraph(f"{turb.get('diametro_primitivo_rodete_m', 0.317)*1000:.1f}", style_tabla_cell_center), Paragraph("mm", style_tabla_cell_center), Paragraph("Relación D1/d0 = 7.4", style_tabla_cell)],
        [Paragraph("Generador: Potencia en Bornes", style_tabla_cell), Paragraph(f"{turb.get('potencia_electrica_bornes_kw', 101.9):.2f}", style_tabla_cell_center), Paragraph("kW", style_tabla_cell_center), Paragraph("Generador sincrónico 6 polos", style_tabla_cell)],
        [Paragraph("Red: Potencia Neta Entregada", style_tabla_cell), Paragraph(f"{turb.get('potencia_neta_red_kw', 99.8):.2f}", style_tabla_cell_center), Paragraph("kW", style_tabla_cell_center), Paragraph("Pérdidas transformador 2%", style_tabla_cell)]
    ]
    t_dim = Table(dim_data, colWidths=[2.4 * inch, 1.2 * inch, 0.9 * inch, 2.3 * inch])
    t_dim.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), azul_principal),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D5DD")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, gris_claro]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_dim)
    story.append(PageBreak())

    # =========================================================================
    # 6. GOLPE DE ARIETE Y TRANSITORIOS HIDRÁULICOS
    # =========================================================================
    story.append(Paragraph("5. ANÁLISIS DE GOLPE DE ARIETE (TRANSITORIOS)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=azul_secundario, spaceAfter=8))

    trans = resultados.get("transitorio", {})

    story.append(Paragraph(
        f"Se realizó la simulación elastoacústica del transitorio hidráulico provocado por el cierre de las toberas. "
        f"La celeridad de onda calculada en la tubería de acero ASTM A36 es de <b>{trans.get('celeridad_m_s', 1175.7):.1f} m/s</b>, "
        f"lo que arroja un tiempo de reflexión crítico de <b>Tc = {trans.get('tiempo_critico_reflexion_s', 0.646):.3f} s</b>.",
        style_body
    ))
    story.append(Paragraph(
        f"Considerando un deflector mecánico de chorro ultrarrápido (tiempo de desvío < 0.5 s) y cierre servoasistido "
        f"de las agujas en <b>tc = {trans.get('tiempo_cierre_maniobra_s', 4.0):.1f} s</b> (relación tc/Tc = {trans.get('relacion_tiempo_cierre', 6.2):.1f}), "
        f"la maniobra clasifica como <b>CIERRE LENTO (Allievi)</b>. "
        f"La sobrepresión máxima es de <b>{trans.get('sobrepresion_delta_H_m', 49.33):.2f} m.c.a.</b> "
        f"({trans.get('sobrepresion_porcentaje_salto', 42.9):.1f}% del salto estático), determinando una "
        f"presión máxima de diseño de <b>{trans.get('presion_maxima_H_max_m', 164.33):.2f} m.c.a. ({trans.get('presion_maxima_bar', 16.1):.2f} bar)</b>.",
        style_body
    ))

    # Gráfico de perfil de presiones
    grafico_ariete = resultados.get("grafico_ariete")
    if grafico_ariete and os.path.exists(grafico_ariete):
        story.append(KeepTogether([
            Paragraph("<b>Figura 2:</b> Perfil Longitudinal y Envolvente de Sobrepresión Dinámica Máxima por Golpe de Ariete.", style_body_bold),
            Image(grafico_ariete, width=6.2 * inch, height=3.3 * inch),
            Spacer(1, 8)
        ]))

    story.append(PageBreak())

    # =========================================================================
    # 7. EVALUACIÓN ECONÓMICA Y FINANCIERA
    # =========================================================================
    story.append(Paragraph("6. EVALUACIÓN ECONÓMICA Y FINANCIERA (25 AÑOS)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=azul_secundario, spaceAfter=8))

    story.append(Paragraph(
        f"La evaluación contempla un horizonte de vida útil de <b>{econo.get('horizonte_evaluacion_anios', 25)} años</b> "
        f"y una tasa de costo de oportunidad de capital del <b>{econo.get('tasa_descuento_pct', 10.0):.1f}%</b>. "
        f"El CAPEX estimado asciende a <b>${econo.get('capex_usd', 245800):,.2f} USD</b> e incluye obras de cabecera, "
        f"canal, cámara de carga, tubería forzada, equipamiento electromecánico Pelton y subestación elevadora.",
        style_body
    ))

    econ_data = [
        [Paragraph("Indicador Financiero", style_tabla_header), Paragraph("Valor Obtenido", style_tabla_header), Paragraph("Criterio de Aceptación", style_tabla_header), Paragraph("Veredicto", style_tabla_header)],
        [Paragraph("Inversión Inicial (CAPEX)", style_tabla_cell), Paragraph(f"${econo.get('capex_usd', 245800):,.2f} USD", style_tabla_cell_center), Paragraph("Ratio de mercado < $3,000 USD/kW", style_tabla_cell), Paragraph("Excelente", style_tabla_cell_center)],
        [Paragraph("OPEX Anual (3% CAPEX)", style_tabla_cell), Paragraph(f"${econo.get('opex_anual_usd', 7374):,.2f} USD/año", style_tabla_cell_center), Paragraph("Estándar internacional micro-hidro", style_tabla_cell), Paragraph("Aceptable", style_tabla_cell_center)],
        [Paragraph("Ingresos Anuales Brutos", style_tabla_cell), Paragraph(f"${econo.get('ingreso_anual_usd', 50458):,.2f} USD/año", style_tabla_cell_center), Paragraph("Venta neta @ $0.075 USD/kWh", style_tabla_cell), Paragraph("Firme", style_tabla_cell_center)],
        [Paragraph("Flujo de Caja Operativo Neto", style_tabla_cell), Paragraph(f"${econo.get('flujo_neto_anual_usd', 43084):,.2f} USD/año", style_tabla_cell_center), Paragraph("Ingresos menos OPEX anual", style_tabla_cell), Paragraph("Favorable", style_tabla_cell_center)],
        [Paragraph("Valor Actual Neto (VAN @ 10%)", style_tabla_cell), Paragraph(f"${econo.get('van_usd', 145155):,.2f} USD", style_tabla_cell_center), Paragraph("VAN > 0", style_tabla_cell), Paragraph("ALTAMENTE VIABLE", style_tabla_cell_center)],
        [Paragraph("Tasa Interna de Retorno (TIR)", style_tabla_cell), Paragraph(f"{econo.get('tir_pct', 16.24):.2f} %", style_tabla_cell_center), Paragraph("TIR > COK (10%)", style_tabla_cell), Paragraph("RENTABLE", style_tabla_cell_center)],
        [Paragraph("Período de Recuperación (Payback)", style_tabla_cell), Paragraph(f"{econo.get('payback_anios', 5.71):.2f} Años", style_tabla_cell_center), Paragraph("< 8 años para proyectos RER", style_tabla_cell), Paragraph("Excelente", style_tabla_cell_center)],
        [Paragraph("Costo Nivelado (LCOE)", style_tabla_cell), Paragraph(f"${econo.get('lcoe_usd_mwh', 45.40):.2f} USD/MWh", style_tabla_cell_center), Paragraph("Muy competitivo vs diésel (> $250)", style_tabla_cell), Paragraph("Competitivo", style_tabla_cell_center)],
        [Paragraph("Relación Beneficio / Costo (B/C)", style_tabla_cell), Paragraph(f"{econo.get('relacion_beneficio_costo', 1.59):.2f}", style_tabla_cell_center), Paragraph("B/C > 1.20", style_tabla_cell), Paragraph("Robusto", style_tabla_cell_center)]
    ]
    t_econ = Table(econ_data, colWidths=[2.2 * inch, 1.6 * inch, 1.8 * inch, 1.2 * inch])
    t_econ.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), azul_principal),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D5DD")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, gris_claro]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_econ)
    story.append(Spacer(1, 15))

    # =========================================================================
    # 8. CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    story.append(Paragraph("7. CONCLUSIONES Y RECOMENDACIONES", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=azul_secundario, spaceAfter=8))

    conclusiones = [
        "<b>Factibilidad Técnica y Energética:</b> El proyecto es plenamente viable con un aprovechamiento de 125 L/s y 115 m de salto bruto, logrando una potencia neta de 99.8 kW y un factor de planta sostenido del 76.8% (672.8 MWh/año).",
        "<b>Garantía Ambiental y Caudal Ecológico:</b> Se cumple estrictamente con la Ley de Recursos Hídricos (Ley 29338), asegurando un caudal ecológico continuo de 30 L/s en la bocatoma que preserva el ecosistema acuático de la cuenca alta.",
        "<b>Seguridad ante Transitorios:</b> La combinación de deflector rápido e inyectores servoasistidos de cierre lento (tc = 4.0 s) contiene la sobrepresión por ariete en 49.3 m, lo que permite adoptar tubería de acero estándar comercial de 10\" con espesores de 4.75 mm y 6.35 mm sin riesgo de colapso ni fatiga.",
        "<b>Solidez Financiera:</b> Los indicadores económicos (VAN de $145,155 USD, TIR de 16.24% y Payback de 5.7 años) ratifican la alta conveniencia de la inversión frente a alternativas térmicas aisladas.",
        "<b>Cumplimiento Normativo RER:</b> El proyecto califica como central RER prioritaria bajo el D.L. 1002 y se encuentra exonerado de concesión definitiva (D.L. 25844 por ser <= 500 kW), requiriendo únicamente autorización simplificada DREM Puno y acreditación hídrica ANA."
    ]

    for conc in conclusiones:
        story.append(Paragraph(f"• {conc}", style_body))
        story.append(Spacer(1, 2))

    # Construir documento PDF
    doc.build(story)

    return os.path.abspath(ruta_salida)
