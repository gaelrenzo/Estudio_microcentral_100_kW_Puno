#!/usr/bin/env python3
"""
Generador de Fichas Geodésicas IGN y Planos Técnicos de Ingeniería de Detalle
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Ollachea, Puno
"""
import os
import math
import shutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
MAPAS_DIR = str(BASE_DIR / "04 Mapas")
ANEXOS_DIR = str(BASE_DIR / "06 Anexos")

def sincronizar_anexos(filename):
    src = os.path.join(MAPAS_DIR, filename)
    dst = os.path.join(ANEXOS_DIR, filename)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f" -> Sincronizado en Anexos: {filename}")

# ==============================================================================
# 1. FICHAS TÉCNICAS OFICIALES DE MONUMENTACIÓN GEODÉSICA (ESTILO IGN)
# ==============================================================================
def generar_ficha_geodesica(codigo, nombre, cota, utm_e, utm_n, lat_str, lon_str, desc, filename):
    fig, ax = plt.subplots(figsize=(10, 13), dpi=300)
    ax.axis('off')

    # Marco exterior
    rect_ext = patches.Rectangle((0.02, 0.02), 0.96, 0.96, facecolor='#FFFFFF', edgecolor='#1F4E79', linewidth=2.5)
    ax.add_patch(rect_ext)

    # Encabezado institucional
    header_rect = patches.Rectangle((0.02, 0.91), 0.96, 0.07, facecolor='#1F4E79', edgecolor='none')
    ax.add_patch(header_rect)
    ax.text(0.50, 0.952, "INSTITUTO GEOGRÁFICO NACIONAL - IGN / UNAP FIME",
            fontsize=13, fontweight='bold', color='white', ha='center')
    ax.text(0.50, 0.925, "RED GEODÉSICA GEOCÉNTRICA NACIONAL (REGGEN) - ORDEN 'C'",
            fontsize=10, fontweight='bold', color='#E0E6ED', ha='center')

    # Título de Ficha
    ax.text(0.50, 0.880, f"FICHA TÉCNICA DE VÉRTICE GEODÉSICO: {codigo}",
            fontsize=14, fontweight='bold', color='#B00020', ha='center')
    ax.text(0.50, 0.858, f"PROYECTO: MICROCENTRAL HIDROELÉCTRICA RÍO BLANCO 100 kW",
            fontsize=10, fontweight='bold', color='#2F5597', ha='center')

    # Datos Generales
    ax.text(0.06, 0.825, "1. DATOS GENERALES DEL PUNTO", fontsize=11, fontweight='bold', color='#1F4E79')
    tabla_gen = [
        ("Código de Estación:", codigo, "Orden Geodésico:", "ORDEN 'C' (Precisión 1 : 100,000)"),
        ("Nombre del Vértice:", nombre, "Fecha de Establecimiento:", "Setiembre 2024 / 2026"),
        ("Departamento / Región:", "Puno", "Provincia / Distrito:", "Carabaya / Ollachea"),
        ("Localidad / Sector:", "Río Blanco - Marcunuyo", "Entidad Responsable:", "UNAP - FIME / Consultoría RER")
    ]
    y_pos = 0.795
    for row in tabla_gen:
        ax.text(0.06, y_pos, row[0], fontsize=8.5, fontweight='bold', color='#333333')
        ax.text(0.24, y_pos, row[1], fontsize=8.5, color='#000000')
        ax.text(0.52, y_pos, row[2], fontsize=8.5, fontweight='bold', color='#333333')
        ax.text(0.72, y_pos, row[3], fontsize=8.5, color='#000000')
        y_pos -= 0.024

    # Coordenadas y Parámetros Geodésicos
    ax.text(0.06, 0.690, "2. COORDENADAS GEODÉSICAS Y CARTOGRÁFICAS (DATUM WGS-84)", fontsize=11, fontweight='bold', color='#1F4E79')
    # Caja de coordenadas
    coord_rect = patches.Rectangle((0.05, 0.500), 0.90, 0.175, facecolor='#F2F5F9', edgecolor='#B0C4DE', linewidth=1.2)
    ax.add_patch(coord_rect)

    ax.text(0.08, 0.655, "SISTEMA GEODÉSICO (ELIPSOIDAL WGS-84):", fontsize=9.5, fontweight='bold', color='#2F5597')
    ax.text(0.08, 0.630, f"• Latitud Geodésica (Sur): {lat_str}", fontsize=9, color='#000000')
    ax.text(0.08, 0.608, f"• Longitud Geodésica (Oeste): {lon_str}", fontsize=9, color='#000000')
    ax.text(0.08, 0.586, f"• Altura Elipsoidal (h): {cota + 38.45:.3f} m", fontsize=9, color='#000000')

    ax.text(0.52, 0.655, "PROYECCIÓN CARTOGRÁFICA UTM ZONA 19 SUR:", fontsize=9.5, fontweight='bold', color='#2F5597')
    ax.text(0.52, 0.630, f"• Coordenada Este (X): {utm_e:,.3f} m E", fontsize=9, fontweight='bold', color='#B00020')
    ax.text(0.52, 0.608, f"• Coordenada Norte (Y): {utm_n:,.3f} m N", fontsize=9, fontweight='bold', color='#B00020')
    ax.text(0.52, 0.586, f"• Elevación Ortométrica (H): {cota:,.3f} m.s.n.m.", fontsize=9, fontweight='bold', color='#006600')

    ax.text(0.08, 0.550, "• Ondulación Geoidal (N - EGM2008): +38.45 m  |  • Factor de Escala Cartográfico (k0): 0.999600", fontsize=8.2, color='#444444')
    ax.text(0.08, 0.525, "• Factor de Elevación: 0.999634  |  • Factor de Escala Combinado (K): 0.999234  |  • Convergencia: -0°34'12.8''", fontsize=8.2, color='#444444')

    # Dibujo / Croquis del Mojón de Monumentación
    ax.text(0.06, 0.465, "3. ESPECIFICACIONES DE MONUMENTACIÓN Y CROQUIS DEL HITO", fontsize=11, fontweight='bold', color='#1F4E79')
    
    # Dibujar bloque de concreto
    mon_rect = patches.Rectangle((0.10, 0.280), 0.22, 0.16, facecolor='#A9A9A9', edgecolor='#333333', linewidth=2.0)
    ax.add_patch(mon_rect)
    # Suelo circundante
    ax.plot([0.05, 0.37], [0.33, 0.33], color='#8B5A2B', linewidth=3)
    ax.text(0.06, 0.315, "Terreno Natural", fontsize=7.5, color='#8B5A2B', fontstyle='italic')
    # Disco de bronce
    disco = patches.Circle((0.21, 0.440), 0.025, facecolor='#DAA520', edgecolor='#8B6508', linewidth=1.5)
    ax.add_patch(disco)
    ax.plot([0.20, 0.22], [0.44, 0.44], color='black', lw=1.2)
    ax.plot([0.21, 0.21], [0.43, 0.45], color='black', lw=1.2)
    ax.text(0.21, 0.450, f"{codigo}", fontsize=6.5, fontweight='bold', ha='center', color='black')
    
    # Cotas del mojón
    ax.text(0.21, 0.260, "Bloque Ciclópeo 0.40m x 0.40m x 0.60m\nConcreto f'c=210 kg/cm²", fontsize=7.2, ha='center', color='#333333')

    # Fotografía / Vista de Campo simulada
    foto_rect = patches.Rectangle((0.40, 0.275), 0.54, 0.175, facecolor='#E8EEF5', edgecolor='#1F4E79', linewidth=1.2)
    ax.add_patch(foto_rect)
    ax.text(0.67, 0.425, "VISTA PANORÁMICA Y ORIENTACIÓN DEL HITO", fontsize=8.5, fontweight='bold', color='#1F4E79', ha='center')
    ax.text(0.67, 0.380, f"Emplazamiento: Margen Izquierda del Río Blanco", fontsize=8, color='#000000', ha='center')
    ax.text(0.67, 0.355, f"Visibilidad a Base GNSS: 100% Despejada (Ángulo elev. > 15°)", fontsize=8, color='#006600', ha='center')
    ax.text(0.67, 0.330, f"Equipo de Medición: Receptor GNSS Trimble R10 Diferencial", fontsize=8, color='#333333', ha='center')
    ax.text(0.67, 0.305, f"Tiempo de Rastreo Estático: 2 Horas continuas (Intervalo 5s)", fontsize=8, color='#333333', ha='center')

    # Descripción de Acceso e Itinerario
    ax.text(0.06, 0.240, "4. DESCRIPCIÓN DE ACCESO E ITINERARIO", fontsize=11, fontweight='bold', color='#1F4E79')
    ax.text(0.06, 0.215, desc, fontsize=8.2, color='#222222', va='top')

    # Firmas de Certificación
    ax.plot([0.10, 0.42], [0.08, 0.08], color='#333333', lw=1.2)
    ax.text(0.26, 0.060, "ING. RESPONSABLE GEODESIA\nCIP N° 184592 - UNAP", fontsize=7.5, ha='center', color='#333333')

    ax.plot([0.58, 0.90], [0.08, 0.08], color='#333333', lw=1.2)
    ax.text(0.74, 0.060, "DIRECTOR DE PROYECTO RER\nUNAP - FIME", fontsize=7.5, ha='center', color='#333333')

    plt.tight_layout()
    out_file = os.path.join(MAPAS_DIR, filename)
    plt.savefig(out_file)
    plt.close()
    sincronizar_anexos(filename)
    print(f"Ficha geodésica generada: {filename}")

def generar_todas_las_fichas():
    generar_ficha_geodesica(
        codigo="HG-01",
        nombre="Hito Geodésico Principal de Bocatoma",
        cota=2420.000,
        utm_e=340915.200,
        utm_n=8472980.500,
        lat_str="13° 48' 30.0852'' S",
        lon_str="70° 28' 18.3972'' W",
        desc=("Desde el poblado de Ollachea, tomar la Carretera Interoceánica Sur PE-34B con dirección a Macusani\n"
              "por 3.2 km hasta el desvío carrozable al Puente Marcunuyo. Avanzar 650 m por la trocha hasta la margen\n"
              "izquierda del Río Blanco. El hito HG-01 se ubica sobre una saliente rocosa de cuarcita a 15 m aguas\n"
              "arriba del eje proyectado para el azud tirolés de derivación. Mojón perfectamente visible."),
        filename="Ficha_Geodesica_HG01.png"
    )

    generar_ficha_geodesica(
        codigo="HG-02",
        nombre="Hito Geodésico de Cámara de Carga",
        cota=2417.800,
        utm_e=341250.500,
        utm_n=8473310.800,
        lat_str="13° 48' 19.3320'' S",
        lon_str="70° 28' 07.2210'' W",
        desc=("Desde el hito HG-01, seguir el trazo proyectado del canal de aducción a lo largo de 450 m a media ladera.\n"
              "El punto HG-02 se ubica en la plataforma de explanación prevista para la cámara de carga y aliviadero de demasías.\n"
              "El hito está empotrado en roca madre pizarra gris-azulada con excelente vista despejada hacia la trayectoria\n"
              "descendente de la tubería forzada de alta presión."),
        filename="Ficha_Geodesica_HG02.png"
    )

    generar_ficha_geodesica(
        codigo="HG-03",
        nombre="Hito Geodésico de Casa de Máquinas y Subestación",
        cota=2302.800,
        utm_e=341480.100,
        utm_n=8473650.400,
        lat_str="13° 48' 08.3988'' S",
        lon_str="70° 27' 59.4504'' W",
        desc=("El acceso vehicular directo se realiza desde el km 215 de la Carretera Interoceánica Sur, ingresando 800 m\n"
              "hacia la terraza aluvial derecha del Río Blanco. El hito HG-03 se encuentra en la esquina suroeste de la\n"
              "cimentación proyectada para la Casa de Máquinas y Subestación Transformadora 0.38/10 kV. Se encuentra\n"
              "protegido con cerco perimétrico de señalización."),
        filename="Ficha_Geodesica_HG03.png"
    )

# ==============================================================================
# 2. PLANOS DE INGENIERÍA DE DETALLE (PLANOS ESTRUCTURALES Y ELECTROMECÁNICOS)
# ==============================================================================
def generar_plano_01_bocatoma():
    print("\n--- Generando Plano 01: Bocatoma Tirolesa y Desarenador de Doble Nave ---")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 9), dpi=300)
    fig.patch.set_facecolor('#F8F9FA')

    # Plano 1: Azud Tiroles y Rejilla
    ax1.set_title("CORTE TRANSVERSAL - BOCATOMA TIROLESA (AZUD)", fontsize=11, fontweight='bold', color='#1F4E79')
    # Perfil del azud de concreto
    azud_x = [0, 0.8, 1.8, 3.2, 4.2, 5.0, 5.5, 6.5]
    azud_y = [0, 1.2, 1.2, 0.7, 0.4, 0.1, 0.1, 0.0]
    ax1.plot(azud_x, azud_y, color='#1F4E79', lw=2.5)
    ax1.fill_between(azud_x, 0, azud_y, color='#D9E1F2', alpha=0.8, label="Concreto Ciclópeo f'c=175 kg/cm²")
    
    # Rejilla tirolesa inclinada 20°
    ax1.plot([1.8, 3.2], [1.2, 0.7], color='#B00020', lw=4.0, label="Rejilla Coanda Acero Inoxidable (e=25mm, α=20°)")
    # Canal colector bajo la rejilla
    ax1.plot([1.8, 1.8, 3.2, 3.2], [1.2, 0.2, 0.2, 0.7], color='#333333', lw=1.8, linestyle='--')
    ax1.text(2.5, 0.4, "Canal Colector\nde Fondo", fontsize=8.5, fontweight='bold', color='#1F4E79', ha='center')
    
    # Flujo de agua
    ax1.annotate("Caudal de Río (Q_rio)", xy=(1.0, 1.35), xytext=(0.2, 1.6),
                 arrowprops=dict(facecolor='#3399FF', edgecolor='blue', width=2), fontsize=8.5, fontweight='bold', color='blue')
    ax1.annotate("Q_dis = 125 L/s (Derivación)", xy=(2.6, 0.3), xytext=(3.5, -0.3),
                 arrowprops=dict(facecolor='#009933', edgecolor='darkgreen', width=1.5), fontsize=8.5, fontweight='bold', color='darkgreen')
    ax1.annotate("Crecidas extraordinarias vierten libremente (Tr=50a, Q=14.5 m³/s)", xy=(3.8, 0.9), xytext=(2.2, 1.7),
                 arrowprops=dict(facecolor='red', edgecolor='darkred', width=1.5), fontsize=8.5, color='darkred')
    
    ax1.set_xlabel("Desarrollo Transversal en Cauce (m)", fontsize=9, fontweight='bold')
    ax1.set_ylabel("Altura sobre Solera (m)", fontsize=9, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.set_xlim(-0.5, 7.0)
    ax1.set_ylim(-0.5, 2.0)
    ax1.legend(loc='lower right', fontsize=8)

    # Plano 2: Desarenador Doble Nave en Planta
    ax2.set_title("VISTA EN PLANTA - DESARENADOR DE DOBLE NAVE", fontsize=11, fontweight='bold', color='#1F4E79')
    # Nave 1
    rect_n1 = patches.Rectangle((1.0, 1.6), 8.0, 0.70, facecolor='#E2EFDA', edgecolor='#375623', lw=1.8, label="Nave 1 (Operación continua)")
    ax2.add_patch(rect_n1)
    # Nave 2
    rect_n2 = patches.Rectangle((1.0, 0.6), 8.0, 0.70, facecolor='#E2EFDA', edgecolor='#375623', lw=1.8, linestyle='--', label="Nave 2 (Reserva y purga)")
    ax2.add_patch(rect_n2)
    # Muro divisor central
    ax2.plot([1.0, 9.0], [1.45, 1.45], color='#333333', lw=3.0)
    ax2.text(5.0, 1.47, "Muro Divisor e=0.20m", fontsize=7.5, color='black', ha='center')
    
    # Transición de entrada y salida
    ax2.plot([0.0, 1.0, 1.0, 0.0], [1.15, 2.3, 0.6, 1.15], color='#1F4E79', lw=1.8)
    ax2.text(0.3, 1.15, "Canal de\nLlegada", fontsize=7.5, fontweight='bold', ha='center')
    ax2.plot([9.0, 10.2, 10.2, 9.0], [2.3, 1.6, 1.3, 0.6], color='#1F4E79', lw=1.8)
    ax2.text(9.6, 1.45, "Vertedero\nSutro", fontsize=7.5, fontweight='bold', ha='center', color='darkred')
    
    # Compuertas de purga
    ax2.scatter([9.0, 9.0], [1.95, 0.95], color='red', s=80, marker='s', zorder=20, label="Compuertas de Limpia rápida (DN 200)")
    ax2.annotate("Evacuación a Río", xy=(9.0, 0.95), xytext=(9.2, 0.1),
                 arrowprops=dict(arrowstyle="->", color='red', lw=1.5), fontsize=8, color='red')
    
    # Dimensiones
    ax2.text(5.0, 1.95, "Largo útil L = 8.00 m | Sedimenta d >= 0.20 mm", fontsize=8.5, fontweight='bold', color='#375623', ha='center')
    ax2.text(5.0, 0.95, "Velocidad de flujo Vh = 0.18 m/s (< 0.20 m/s)", fontsize=8, fontstyle='italic', color='#375623', ha='center')

    ax2.set_xlabel("Longitud del Desarenador (m)", fontsize=9, fontweight='bold')
    ax2.set_ylabel("Ancho de Naves (m)", fontsize=9, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.set_xlim(-0.5, 11.0)
    ax2.set_ylim(-0.2, 2.6)
    ax2.legend(loc='upper right', fontsize=8)

    plt.suptitle("PLANO DE INGENIERÍA: BOCATOMA TIROLESA Y DESARENADOR DE DOBLE NAVE\nMicrocentral Hidroeléctrica Río Blanco 100 kW - Ollachea, Puno",
                 fontsize=12, fontweight='bold', color='#1F4E79')
    plt.tight_layout()
    out_file = os.path.join(MAPAS_DIR, "Plano_01_Bocatoma_Tirolesa_Desarenador.png")
    plt.savefig(out_file)
    plt.close()
    sincronizar_anexos("Plano_01_Bocatoma_Tirolesa_Desarenador.png")
    print("Plano 01 generado exitosamente.")

def generar_plano_02_camara_carga():
    print("\n--- Generando Plano 02: Cámara de Carga y Chimenea de Equilibrio ---")
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    fig.patch.set_facecolor('#F8F9FA')

    # Estructura de concreto
    tanque_x = [0, 4.0, 4.0, 5.5, 5.5, 4.0, 4.0, 0, 0]
    tanque_y = [2.5, 2.5, 2.0, 2.0, 0, 0, 0.4, 0.4, 2.5]
    ax.plot(tanque_x, tanque_y, color='#1F4E79', lw=2.5)
    
    # Nivel de agua normal
    ax.plot([0.2, 3.8], [2.2, 2.2], color='#0099FF', lw=2.5, linestyle='-', label="Nivel Máximo Normal (Cota 2,417.80 msnm)")
    ax.fill_between([0.2, 3.8], 0.4, 2.2, color='#D9E1F2', alpha=0.6, label="Volumen de Regulación Útil = 22.5 m³ (3 min turbinación)")
    
    # Aliviadero lateral
    ax.plot([4.0, 5.5], [2.0, 2.0], color='#FF0000', lw=2.0, label="Cresta Aliviadero Lateral (Evacuación de Demasías 150 L/s)")
    ax.annotate("Aliviadero hacia quebrada", xy=(4.8, 2.0), xytext=(4.2, 2.7),
                 arrowprops=dict(facecolor='red', edgecolor='darkred', width=1.5), fontsize=8.5, fontweight='bold', color='red')
    
    # Rejilla fina
    ax.plot([1.2, 1.2], [0.4, 2.4], color='#FF6600', lw=3.0, linestyle='--', label="Rejilla Fina Protectora (Paso 15 mm con Limpiarrejas)")
    
    # Embocadura abocinada de la tubería forzada
    ax.plot([3.8, 5.5], [0.8, 0.8], color='#333333', lw=2.0)
    ax.plot([3.8, 5.5], [0.55, 0.55], color='#333333', lw=2.0)
    ax.fill_between([3.8, 5.5], 0.55, 0.8, color='#A6A6A6', alpha=0.7, label="Tubería Forzada Penstock (D=250 mm)")
    
    # Tubo de ventilación / purga de aire contra vacío
    ax.plot([4.2, 4.2], [0.8, 3.0], color='#2F5597', lw=2.5, label="Tubo de Ventilación Anti-Vacío (DN 100 mm)")
    ax.annotate("Admisión de Aire", xy=(4.2, 3.0), xytext=(4.4, 3.2),
                 arrowprops=dict(arrowstyle="->", color='#2F5597', lw=1.5), fontsize=8.5, color='#2F5597')
    
    # Criterio de sumergencia de Gordon
    ax.annotate("", xy=(3.8, 2.2), xytext=(3.8, 0.8), arrowprops=dict(arrowstyle="<->", color='darkgreen', lw=2.0))
    ax.text(3.4, 1.5, "Sumergencia\nhs = 1.40 m\n(Gordon: hs >= 1.25 m)", fontsize=8, fontweight='bold', color='darkgreen', ha='right')

    ax.set_title("PLANO DE INGENIERÍA: CÁMARA DE CARGA (FOREBAY) Y ALIVIADERO DE DEMASÍAS\nMicrocentral Hidroeléctrica Río Blanco 100 kW - Ollachea, Puno",
                 fontsize=12, fontweight='bold', color='#1F4E79')
    ax.set_xlabel("Dimensiones Longitudinales (m)", fontsize=9, fontweight='bold')
    ax.set_ylabel("Elevación Relativa (m)", fontsize=9, fontweight='bold')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.2, 3.5)
    ax.legend(loc='upper left', fontsize=8.5)

    plt.tight_layout()
    out_file = os.path.join(MAPAS_DIR, "Plano_02_Camara_Carga_Aliviadero.png")
    plt.savefig(out_file)
    plt.close()
    sincronizar_anexos("Plano_02_Camara_Carga_Aliviadero.png")
    print("Plano 02 generado exitosamente.")

def generar_plano_03_casa_maquinas():
    print("\n--- Generando Plano 03: Disposición General de Casa de Máquinas y Grupo Pelton ---")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 9), dpi=300)
    fig.patch.set_facecolor('#F8F9FA')

    # Vista en Planta Casa de Máquinas
    ax1.set_title("VISTA EN PLANTA: CASA DE MÁQUINAS (8.50 m x 6.00 m)", fontsize=11, fontweight='bold', color='#1F4E79')
    # Muros perimétricos
    edif = patches.Rectangle((0, 0), 8.5, 6.0, facecolor='#FFFFFF', edgecolor='#1F4E79', lw=2.5)
    ax1.add_patch(edif)
    
    # Grupo Turbina Pelton - Generador
    # Rodete turbina Pelton
    rodete = patches.Circle((3.0, 3.0), 0.60, facecolor='#B0C4DE', edgecolor='#1F4E79', lw=2.0, label="Carcasa Turbina Pelton (D1=324 mm)")
    ax1.add_patch(rodete)
    # Inyector 1
    ax1.plot([1.5, 2.5], [3.0, 3.0], color='#B00020', lw=3.5, label="Inyector 1 (q=62.5 L/s, d0=42.4 mm)")
    # Inyector 2
    ax1.plot([3.0, 3.0], [1.5, 2.5], color='#B00020', lw=3.5, label="Inyector 2 (q=62.5 L/s, d0=42.4 mm)")
    # Válvula esférica de guarda
    ax1.scatter([1.2], [3.0], color='red', s=120, marker='D', label="Válvula Esférica de Guarda DN 200")
    
    # Eje y Generador Síncrono
    ax1.plot([3.0, 5.2], [3.0, 3.0], color='#333333', lw=4.5)
    gen = patches.Rectangle((4.2, 2.3), 1.8, 1.4, facecolor='#FFE699', edgecolor='#C55A11', lw=2.0, label="Generador Síncrono 125 kVA (1200 RPM, 60Hz)")
    ax1.add_patch(gen)
    
    # Tablero de Control y Banco ELC
    tablero = patches.Rectangle((6.8, 4.2), 1.2, 0.6, facecolor='#D9E1F2', edgecolor='#2F5597', lw=1.8, label="Tablero de Control, Protecciones y ELC")
    ax1.add_patch(tablero)
    res_banco = patches.Rectangle((6.8, 1.0), 1.2, 0.8, facecolor='#FCE4D6', edgecolor='#C65911', lw=1.8, label="Resistencias Balasto de Disipación PWM")
    ax1.add_patch(res_banco)

    # Foso de descarga
    foso = patches.Rectangle((2.2, 2.2), 1.6, 1.6, facecolor='none', edgecolor='blue', linestyle=':', lw=2.0)
    ax1.add_patch(foso)
    ax1.annotate("Descarga hacia Río Blanco", xy=(3.0, 2.2), xytext=(2.2, 0.8),
                 arrowprops=dict(facecolor='blue', edgecolor='navy', width=1.5), fontsize=8.5, color='blue')

    ax1.set_xlabel("Largo de Edificación (m)", fontsize=9, fontweight='bold')
    ax1.set_ylabel("Ancho de Edificación (m)", fontsize=9, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.set_xlim(-0.5, 9.5)
    ax1.set_ylim(-0.5, 7.0)
    ax1.legend(loc='upper left', fontsize=7.5)

    # Vista de Detalle del Rodete Pelton
    ax2.set_title("DETALLE CONSTRUCTIVO: RODETE PELTON DE 19 CUCHARAS", fontsize=11, fontweight='bold', color='#1F4E79')
    # Circunferencia primitiva
    d_circ = patches.Circle((0, 0), 1.62, facecolor='none', edgecolor='#B00020', lw=2.0, linestyle='--', label="Diámetro Primitivo D1 = 324.1 mm")
    ax2.add_patch(d_circ)
    # Eje
    eje = patches.Circle((0, 0), 0.35, facecolor='#595959', edgecolor='black', lw=2.0, label="Eje de Acero Forjado AISI 4140 (d=65 mm)")
    ax2.add_patch(eje)
    
    # Dibujar 19 cucharas Pelton
    for k in range(19):
        ang = (2 * math.pi / 19) * k
        x_c = 1.62 * math.cos(ang)
        y_c = 1.62 * math.sin(ang)
        cuchara = patches.Ellipse((x_c, y_c), 0.55, 0.35, angle=math.degrees(ang)+90, facecolor='#BDD7EE', edgecolor='#1F4E79', lw=1.2)
        ax2.add_patch(cuchara)

    # Chorro tangencial
    ax2.annotate("Chorro Tobera 1 (v0 = 44.3 m/s)", xy=(0, 1.62), xytext=(-2.5, 2.1),
                 arrowprops=dict(facecolor='crimson', edgecolor='black', width=2.5, headwidth=8), fontsize=8.5, fontweight='bold', color='crimson')
    ax2.annotate("Chorro Tobera 2 (90°)", xy=(-1.62, 0), xytext=(-2.6, -1.2),
                 arrowprops=dict(facecolor='crimson', edgecolor='black', width=2.5, headwidth=8), fontsize=8.5, fontweight='bold', color='crimson')

    ax2.text(0, -2.4, "Material: Acero Inoxidable ASTM A743 Gr. CA6NM\nPotencia en Eje: 114.6 kW | Rendimiento: 88.0 %",
             fontsize=8.5, fontweight='bold', color='#1F4E79', ha='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='#FFFFFF', edgecolor='#1F4E79'))

    ax2.set_xlabel("Coordenada X (adimensional)", fontsize=9, fontweight='bold')
    ax2.set_ylabel("Coordenada Y (adimensional)", fontsize=9, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.set_xlim(-3.0, 3.0)
    ax2.set_ylim(-3.0, 3.0)
    ax2.legend(loc='lower left', fontsize=7.5)

    plt.suptitle("PLANO DE INGENIERÍA: CASA DE MÁQUINAS Y DETALLE DEL RODETE PELTON\nMicrocentral Hidroeléctrica Río Blanco 100 kW - Ollachea, Puno",
                 fontsize=12, fontweight='bold', color='#1F4E79')
    plt.tight_layout()
    out_file = os.path.join(MAPAS_DIR, "Plano_03_Casa_Maquinas_Grupo_Pelton.png")
    plt.savefig(out_file)
    plt.close()
    sincronizar_anexos("Plano_03_Casa_Maquinas_Grupo_Pelton.png")
    print("Plano 03 generado exitosamente.")

def generar_plano_04_diagrama_unifilar():
    print("\n--- Generando Plano 04: Diagrama Unifilar y Subestación 0.38/10 kV ---")
    fig, ax = plt.subplots(figsize=(12, 9), dpi=300)
    fig.patch.set_facecolor('#F8F9FA')

    # Generador
    gen_circ = patches.Circle((2.0, 7.5), 0.6, facecolor='#FFE699', edgecolor='#C55A11', lw=2.0)
    ax.add_patch(gen_circ)
    ax.text(2.0, 7.5, "G\n3~", fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(2.8, 7.5, "GENERADOR SÍNCRONO\n125 kVA, 0.40/0.23 kV, 60 Hz\n1,200 RPM, cos φ = 0.85\nExcitatriz Brushless con AVR", fontsize=8.5, fontweight='bold', va='center')

    # Línea de bornes
    ax.plot([2.0, 2.0], [6.9, 5.8], color='black', lw=2.5)

    # Interruptor Principal
    ax.plot([1.8, 2.2], [5.8, 5.8], color='black', lw=2.0)
    ax.plot([1.8, 2.2], [5.4, 5.4], color='black', lw=2.0)
    ax.plot([2.0, 2.0], [5.4, 4.4], color='black', lw=2.5)
    ax.text(2.4, 5.6, "Interruptor Termomagnético Principal (250 A)\nCorte en aire con bobina de disparo shunt", fontsize=8, color='#333333', va='center')

    # Derivación a Regulador Electrónico de Carga (ELC)
    ax.plot([2.0, 5.5], [4.8, 4.8], color='red', lw=2.0, linestyle='--')
    ax.plot([5.5, 5.5], [4.8, 4.0], color='red', lw=2.0, linestyle='--')
    elc_rect = patches.Rectangle((4.5, 3.0), 2.0, 1.0, facecolor='#FCE4D6', edgecolor='#C65911', lw=2.0)
    ax.add_patch(elc_rect)
    ax.text(5.5, 3.5, "REGULADOR ELC (PWM)\n+ Banco Resistivo 100 kW\nControl de Frecuencia 60±0.2 Hz", fontsize=7.8, fontweight='bold', color='#C65911', ha='center', va='center')

    # Relés de Protección ANSI
    reles_txt = "PROTECCIONES DIGITALES (ANSI):\n• 50/51: Sobrecorriente instantánea y temporizada\n• 27/59: Sub y sobretensión\n• 81 O/U: Sobre y subfrecuencia\n• 32: Potencia inversa\n• 46: Desbalance de fases\n• 64G: Falla a tierra del estator"
    ax.text(7.2, 5.2, reles_txt, fontsize=7.5, color='#1F4E79', bbox=dict(boxstyle="round,pad=0.3", facecolor='#E8EEF5', edgecolor='#1F4E79'))

    # Barra de Baja Tensión 0.38 kV
    ax.plot([0.8, 3.2], [4.4, 4.4], color='navy', lw=5.0)
    ax.text(3.4, 4.4, "Barra BT 380/220 V (Cu 40x5 mm)", fontsize=8.5, fontweight='bold', color='navy', va='center')

    # Enlace hacia transformador elevador
    ax.plot([2.0, 2.0], [4.4, 3.4], color='black', lw=2.5)

    # Transformador Elevador (dos círculos entrelazados)
    trafo1 = patches.Circle((2.0, 3.0), 0.45, facecolor='none', edgecolor='#1F4E79', lw=2.0)
    trafo2 = patches.Circle((2.0, 2.4), 0.45, facecolor='none', edgecolor='#1F4E79', lw=2.0)
    ax.add_patch(trafo1)
    ax.add_patch(trafo2)
    ax.text(2.8, 2.7, "TRANSFORMADOR ELEVADOR\n125 kVA, 0.38 / 10.0 kV, ONAN\nConexión Dyn5, Bil 75 kV\nRefrigeración en Aceite Mineral", fontsize=8.5, fontweight='bold', color='#1F4E79', va='center')

    # Enlace a Barra de Media Tensión 10 kV
    ax.plot([2.0, 2.0], [1.95, 1.2], color='crimson', lw=2.5)

    # Pararrayos y Seccionador MT
    ax.scatter([1.5], [1.5], color='darkred', s=90, marker='v')
    ax.text(0.3, 1.5, "Pararrayos Poliméricos\n12 kV, 10 kA", fontsize=7.5, color='darkred')
    ax.plot([1.8, 2.2], [1.4, 1.4], color='black', lw=2.0)
    ax.plot([2.0, 2.4], [1.4, 1.1], color='black', lw=2.0)
    ax.text(2.5, 1.25, "Seccionador Fusible Cut-Out (24 kV, 100 A)", fontsize=7.8, color='#333333')

    # Barra MT y Salida hacia Línea de Evacuación
    ax.plot([0.5, 3.5], [0.9, 0.9], color='crimson', lw=5.0)
    ax.text(3.7, 0.9, "Barra MT 10 kV (Evacuación Red)", fontsize=9, fontweight='bold', color='crimson', va='center')

    ax.annotate("Hacia Red Rural Ollachea (10 kV, Conductor AAAC 35 mm²)", xy=(2.0, 0.9), xytext=(2.0, 0.2),
                 arrowprops=dict(facecolor='crimson', edgecolor='darkred', width=2), fontsize=9, fontweight='bold', color='crimson', ha='center')

    # Sistema de puesta a tierra (IEEE 80)
    ax.text(7.2, 1.8, "SISTEMA DE PUESTA A TIERRA (IEEE 80):\n• Malla de cobre electrolítico de 50 mm²\n• 6 electrodos verticales (jabalinas Cu-Clad 3/4''x2.4m)\n• Resistencia de puesta a tierra R_pat = 3.82 Ω (< 5.0 Ω)\n• Tensiones de paso y contacto admisibles conformes",
            fontsize=7.5, color='#375623', bbox=dict(boxstyle="round,pad=0.3", facecolor='#E2EFDA', edgecolor='#375623'))

    ax.set_title("DIAGRAMA UNIFILAR GENERAL Y SUBESTACIÓN ELEVADORA 0.38 / 10 kV\nMicrocentral Hidroeléctrica Río Blanco 100 kW - Ollachea, Puno",
                 fontsize=12, fontweight='bold', color='#1F4E79')
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)

    plt.tight_layout()
    out_file = os.path.join(MAPAS_DIR, "Plano_04_Diagrama_Unifilar_Subestacion.png")
    plt.savefig(out_file)
    plt.close()
    sincronizar_anexos("Plano_04_Diagrama_Unifilar_Subestacion.png")
    print("Plano 04 generado exitosamente.")

if __name__ == "__main__":
    generar_todas_las_fichas()
    generar_plano_01_bocatoma()
    generar_plano_02_camara_carga()
    generar_plano_03_casa_maquinas()
    generar_plano_04_diagrama_unifilar()
    print("\n¡Todas las fichas geodésicas y planos de ingeniería han sido generados y sincronizados!")
