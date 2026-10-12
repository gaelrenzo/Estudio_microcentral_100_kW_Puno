#!/usr/bin/env python3
"""
Generador Maestro del Presupuesto Detallado y Análisis de Precios Unitarios (APU)
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Ollachea, Puno
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = str(BASE_DIR / "06 Anexos" / "Anexo_D_Presupuesto_Analisis_Precios_Unitarios_APU.xlsx")

wb = openpyxl.Workbook()
# Eliminar hoja por defecto
wb.remove(wb.active)

# Estilos institucionales
font_title = Font(name="Calibri", size=14, bold=True, color="1F4E79")
font_subtitle = Font(name="Calibri", size=11, bold=True, color="2F5597")
font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=10, bold=True, color="000000")
font_regular = Font(name="Calibri", size=9.5, color="000000")

fill_header = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
fill_subtotal = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
fill_zebra = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='B0C4DE'),
    right=Side(style='thin', color='B0C4DE'),
    top=Side(style='thin', color='B0C4DE'),
    bottom=Side(style='thin', color='B0C4DE')
)

# ==============================================================================
# 1. HOJA: RESUMEN GENERAL DE INVERSIÓN (CAPEX)
# ==============================================================================
ws1 = wb.create_sheet(title="01_Resumen_CAPEX")
ws1.views.sheetView[0].showGridLines = True

ws1["B2"] = "UNIVERSIDAD NACIONAL DEL ALTIPLANO PUNO - FACULTAD DE INGENIERÍA MECÁNICA ELÉCTRICA"
ws1["B2"].font = font_title
ws1["B3"] = "PROYECTO: MICROCENTRAL HIDROELÉCTRICA RÍO BLANCO 100 kW (OLLACHEA, CARABAYA - PUNO)"
ws1["B3"].font = font_subtitle
ws1["B4"] = "RESUMEN EJECUTIVO DEL PRESUPUESTO DE INVERSIÓN (CAPEX) - MONEDA: USD"
ws1["B4"].font = Font(name="Calibri", size=10, bold=True, color="B00020")

headers1 = ["Ítem", "Componente de Inversión", "Costo Directo [USD]", "Gastos Grales y Utilidad", "Costo Total [USD]", "Participación"]
for col_idx, h in enumerate(headers1, start=2):
    cell = ws1.cell(row=6, column=col_idx, value=h)
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center")

resumen_items = [
    ("01.00", "Obras Civiles de Captación (Azud, Rejilla Coanda y Desarenador 2 Naves)", 34000.0, 8500.0, 42500.0, 0.1729),
    ("02.00", "Canal de Aducción Rectangular en Concreto Ciclópeo (450 m)", 33600.0, 8400.0, 42000.0, 0.1709),
    ("03.00", "Cámara de Carga (Forebay), Aliviadero y 4 Bloques de Anclaje", 21440.0, 5360.0, 26800.0, 0.1090),
    ("04.00", "Tubería Forzada Penstock de Acero ASTM A36 (D=250mm, L=380m)", 34800.0, 8700.0, 43500.0, 0.1770),
    ("05.00", "Equipamiento Hidromecánico (Turbina Pelton 2 Iny, Válvula, ELC 120 kW)", 36000.0, 9000.0, 45000.0, 0.1831),
    ("06.00", "Generador Síncrono 125 kVA, Tablero Control y Malla IEEE 80", 13200.0, 3300.0, 16500.0, 0.0671),
    ("07.00", "Subestación Elevadora 0.38/10 kV y Línea MT Aérea (3.2 km)", 11600.0, 2900.0, 14500.0, 0.0590),
    ("08.00", "Ingeniería de Detalle, Red Geodésica IGN, Cartografía y Supervisión", 6800.0, 1700.0, 8500.0, 0.0346),
    ("09.00", "Plan de Manejo Ambiental, Licencia ANA, CIRA y Contingencias", 5200.0, 1300.0, 6500.0, 0.0264)
]

for row_idx, item in enumerate(resumen_items, start=7):
    ws1.cell(row=row_idx, column=2, value=item[0]).alignment = Alignment(horizontal="center")
    ws1.cell(row=row_idx, column=3, value=item[1])
    ws1.cell(row=row_idx, column=4, value=item[2]).number_format = '$#,##0.00'
    ws1.cell(row=row_idx, column=5, value=item[3]).number_format = '$#,##0.00'
    ws1.cell(row=row_idx, column=6, value=item[4]).number_format = '$#,##0.00'
    ws1.cell(row=row_idx, column=7, value=item[5]).number_format = '0.00%'
    
    for c in range(2, 8):
        cell = ws1.cell(row=row_idx, column=c)
        cell.font = font_regular
        cell.border = thin_border
        if row_idx % 2 == 1:
            cell.fill = fill_zebra

# Fila Total
tot_row = len(resumen_items) + 7
ws1.cell(row=tot_row, column=2, value="")
ws1.cell(row=tot_row, column=3, value="TOTAL PRESUPUESTO DE INVERSIÓN (CAPEX)").font = font_bold
ws1.cell(row=tot_row, column=4, value=f"=SUM(D7:D{tot_row-1})").number_format = '$#,##0.00'
ws1.cell(row=tot_row, column=5, value=f"=SUM(E7:E{tot_row-1})").number_format = '$#,##0.00'
ws1.cell(row=tot_row, column=6, value=f"=SUM(F7:F{tot_row-1})").number_format = '$#,##0.00'
ws1.cell(row=tot_row, column=7, value=f"=SUM(G7:G{tot_row-1})").number_format = '0.00%'

for c in range(2, 8):
    cell = ws1.cell(row=tot_row, column=c)
    cell.font = font_bold
    cell.fill = fill_subtotal
    cell.border = thin_border

# Ratios clave
ws1.cell(row=tot_row+2, column=3, value="Costo Unitario por kW Instalado:").font = font_bold
ws1.cell(row=tot_row+2, column=4, value="=F" + str(tot_row) + "/100").number_format = '$#,##0.00'
ws1.cell(row=tot_row+2, column=5, value="USD / kW").font = font_bold

# ==============================================================================
# 2. HOJA: PRESUPUESTO DETALLADO POR PARTIDAS
# ==============================================================================
ws2 = wb.create_sheet(title="02_Presupuesto_Detallado")
ws2.views.sheetView[0].showGridLines = True

ws2["B2"] = "PRESUPUESTO DETALLADO POR PARTIDAS DE OBRA - MCH RÍO BLANCO 100 kW"
ws2["B2"].font = font_title

headers2 = ["Ítem", "Descripción de la Partida", "Unidad", "Metrado", "Precio Unitario [USD]", "Parcial [USD]"]
for col_idx, h in enumerate(headers2, start=2):
    cell = ws2.cell(row=4, column=col_idx, value=h)
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center")

partidas = [
    ("01.00", "OBRAS CIVILES PRELIMINARES Y BOCATOMA", "", "", "", ""),
    ("01.01", "Limpieza, desbroce y trazo geodésico con estación total / GNSS", "m2", 1500.0, 3.50, 5250.0),
    ("01.02", "Excavación en roca fija con martillo neumático para azud", "m3", 185.0, 48.00, 8880.0),
    ("01.03", "Concreto ciclópeo f'c=175 kg/cm2 + 30% PM en cuerpo de azud", "m3", 65.0, 135.00, 8775.0),
    ("01.04", "Rejilla Coanda autolimpiante de acero inoxidable AISI 304 (e=25mm)", "und", 1.0, 5500.00, 5500.0),
    ("01.05", "Compuerta plana deslizante de captación y limpia (0.80x0.80m)", "und", 2.0, 2800.00, 5600.0),
    ("02.00", "DESARENADOR DE DOBLE NAVE", "", "", "", ""),
    ("02.01", "Excavación en material común y roca fracturada", "m3", 120.0, 28.00, 3360.0),
    ("02.02", "Concreto armado f'c=210 kg/cm2 en muros y solera desarenador", "m3", 32.0, 240.00, 7680.0),
    ("02.03", "Acero corrugado fy=4200 kg/cm2 grado 60", "kg", 2400.0, 2.10, 5040.0),
    ("02.04", "Vertederos proporcionales tipo Sutro y compuertas de purga rápida", "glb", 1.0, 4500.00, 4500.0),
    ("03.00", "CANAL DE ADUCCIÓN RECTANGULAR (450 M)", "", "", "", ""),
    ("03.01", "Excavación en roca y material semirduro a media ladera", "m3", 380.0, 35.00, 13300.0),
    ("03.02", "Concreto ciclópeo f'c=175 kg/cm2 para canal rectangular (0.50x0.60m)", "m3", 115.0, 160.00, 18400.0),
    ("03.03", "Juntas de dilatación elastoméricas premoldeadas cada 6.0 m", "m", 150.0, 18.00, 2700.0),
    ("03.04", "Muros de protección y banquetas contra caída de piedras", "m", 90.0, 84.44, 7600.0),
    ("04.00", "CÁMARA DE CARGA, ALIVIADERO Y DADOS DE ANCLAJE", "", "", "", ""),
    ("04.01", "Excavación masiva para explanada de cámara de carga", "m3", 95.0, 26.00, 2470.0),
    ("04.02", "Concreto armado f'c=210 kg/cm2 en cámara de carga (V=22.5 m3)", "m3", 28.0, 250.00, 7000.0),
    ("04.03", "Rejilla fina con limpiarrejas manual y compuerta de admisión", "glb", 1.0, 4800.00, 4800.0),
    ("04.04", "Concreto ciclópeo f'c=175 kg/cm2 en 4 bloques de anclaje (A1 a A4)", "m3", 59.0, 145.00, 8555.0),
    ("04.05", "Tubo de ventilación anti-vacío de acero galvanizado DN 100mm", "und", 1.0, 1175.00, 1175.0),
    ("05.00", "TUBERÍA FORZADA PENSTOCK (D=250 MM, L=380 M)", "", "", "", ""),
    ("05.01", "Tubería de acero ASTM A36 soldada longitudinalmente e=4.75mm (0-200m)", "m", 200.0, 95.00, 19000.0),
    ("05.02", "Tubería de acero ASTM A36 soldada longitudinalmente e=6.35mm (200-380m)", "m", 180.0, 120.00, 21600.0),
    ("05.03", "Juntas de dilatación tipo Dresser para alta presión", "und", 4.0, 725.00, 2900.0),
    ("06.00", "EQUIPAMIENTO ELECTROMECÁNICO Y GENERADOR", "", "", "", ""),
    ("06.01", "Turbina Pelton horizontal de 2 inyectores con rodete CA6NM (114.6 kW)", "und", 1.0, 28500.00, 28500.0),
    ("06.02", "Válvula esférica de guarda DN 200 mm con contrapeso y cierre hidráulico", "und", 1.0, 6500.00, 6500.0),
    ("06.03", "Regulador Electrónico de Carga (ELC) PWM y banco resistivo 120 kW", "und", 1.0, 10000.00, 10000.0),
    ("06.04", "Generador síncrono trifásico brushless 125 kVA, 0.4 kV, 1200 RPM", "und", 1.0, 12500.00, 12500.0),
    ("06.05", "Tablero de control, sincronización y protecciones digitales ANSI", "und", 1.0, 4000.00, 4000.0),
    ("07.00", "SUBESTACIÓN ELEVADORA Y LÍNEA DE MEDIA TENSIÓN", "", "", "", ""),
    ("07.01", "Transformador trifásico elevador 125 kVA 0.38/10 kV ONAN Dyn5", "und", 1.0, 8200.00, 8200.0),
    ("07.02", "Línea aérea de media tensión 10 kV con conductor AAAC 35 mm2 (3.2 km)", "km", 3.2, 1500.00, 4800.0),
    ("07.03", "Malla de puesta a tierra profunda IEEE 80 con 8 jabalinas (Rpat=3.79 Ω)", "glb", 1.0, 1500.00, 1500.0)
]

for row_idx, p in enumerate(partidas, start=5):
    ws2.cell(row=row_idx, column=2, value=p[0]).alignment = Alignment(horizontal="center")
    ws2.cell(row=row_idx, column=3, value=p[1])
    ws2.cell(row=row_idx, column=4, value=p[2]).alignment = Alignment(horizontal="center")
    
    if p[3] != "":
        ws2.cell(row=row_idx, column=5, value=p[3]).number_format = '#,##0.00'
        ws2.cell(row=row_idx, column=6, value=p[4]).number_format = '$#,##0.00'
        ws2.cell(row=row_idx, column=7, value=p[5]).number_format = '$#,##0.00'
        for c in range(2, 8):
            cell = ws2.cell(row=row_idx, column=c)
            cell.font = font_regular
            cell.border = thin_border
    else:
        # Título de grupo
        for c in range(2, 8):
            cell = ws2.cell(row=row_idx, column=c)
            cell.font = font_bold
            cell.fill = fill_subtotal
            cell.border = thin_border

# ==============================================================================
# 3. HOJA: ANÁLISIS DE PRECIOS UNITARIOS (APU MUESTRA)
# ==============================================================================
ws3 = wb.create_sheet(title="03_APU_Muestras")
ws3.views.sheetView[0].showGridLines = True

ws3["B2"] = "ANÁLISIS DE PRECIOS UNITARIOS REPRESENTATIVOS (APU)"
ws3["B2"].font = font_title

apu_bloque = [
    ("PARTIDA: 01.03", "CONCRETO CICLÓPEO f'c=175 kg/cm2 + 30% PIEDRA MEDIANA", "Rendimiento: 12 m3/día", "Unidad: m3"),
    ("Recurso / Insumo", "Descripción del Recurso", "Unidad", "Cuadrilla", "Cantidad", "Precio [USD]", "Parcial [USD]"),
    ("MANO DE OBRA", "", "", "", "", "", ""),
    ("MO-01", "Capataz", "hh", 0.2, 0.133, 8.50, 1.13),
    ("MO-02", "Operario", "hh", 1.0, 0.667, 7.20, 4.80),
    ("MO-03", "Oficial", "hh", 1.0, 0.667, 5.80, 3.87),
    ("MO-04", "Peón", "hh", 6.0, 4.000, 4.50, 18.00),
    ("MATERIALES", "", "", "", "", "", ""),
    ("MAT-01", "Cemento Portland Tipo IP (Bolsa 42.5 kg)", "bol", "", 7.500, 8.20, 61.50),
    ("MAT-02", "Arena gruesa de río clasificada", "m3", "", 0.520, 22.00, 11.44),
    ("MAT-03", "Piedra chancada 1/2'' a 3/4''", "m3", "", 0.550, 24.00, 13.20),
    ("MAT-04", "Piedra mediana de río seleccionada (max 6'')", "m3", "", 0.350, 18.00, 6.30),
    ("MAT-05", "Agua para mezclado y curado", "m3", "", 0.180, 5.00, 0.90),
    ("EQUIPOS Y HERRAMIENTAS", "", "", "", "", "", ""),
    ("EQ-01", "Mezcladora de concreto tambor 9-11 p3", "hm", 1.0, 0.667, 12.00, 8.00),
    ("EQ-02", "Vibrador de concreto 4 HP 1.5'' cabezal", "hm", 1.0, 0.667, 6.50, 4.34),
    ("EQ-03", "Herramientas manuales (3% MO)", "%MO", "", 0.030, 27.80, 0.83),
    ("COSTO DIRECTO TOTAL UNITARIO", "", "", "", "", "", 134.31)
]

for r_i, fila in enumerate(apu_bloque, start=4):
    for c_i, valor in enumerate(fila, start=2):
        cell = ws3.cell(row=r_i, column=c_i, value=valor)
        if r_i == 4 or r_i == 5 or fila[0] in ["MANO DE OBRA", "MATERIALES", "EQUIPOS Y HERRAMIENTAS", "COSTO DIRECTO TOTAL UNITARIO"]:
            cell.font = font_bold
            if r_i == 5:
                cell.fill = fill_header
                cell.font = font_header
            elif fila[0] == "COSTO DIRECTO TOTAL UNITARIO":
                cell.fill = fill_subtotal
        else:
            cell.font = font_regular
            cell.border = thin_border
        if c_i in [6, 7, 8] and isinstance(valor, (int, float)):
            cell.number_format = '$#,##0.00'

# Autoajuste de anchos de columna para todas las hojas
for sheet in wb.worksheets:
    for col in sheet.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            if cell.value:
                val_str = str(cell.value)
                max_len = max(max_len, len(val_str))
        sheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

wb.save(FILE_PATH)
print(f"Archivo Excel de APU actualizado exitosamente: {FILE_PATH}")
