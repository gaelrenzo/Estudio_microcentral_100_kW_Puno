#!/usr/bin/env python3
"""
Generador Maestro de Cartografía Satelital, Geográfica y Geodésica de Alta Precisión
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Ollachea, Carabaya, Puno
Autor: Consultoría de Ingeniería Hidroeléctrica / UNAP FIME
"""
import os
import io
import math
import shutil
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe
from PIL import Image
import pyproj

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
MAPAS_DIR = str(BASE_DIR / "04 Mapas")
ANEXOS_DIR = str(BASE_DIR / "06 Anexos")
os.makedirs(MAPAS_DIR, exist_ok=True)
os.makedirs(ANEXOS_DIR, exist_ok=True)

# Inicializar convertidor de coordenadas WGS84 UTM Zona 19 Sur
utm_proj = pyproj.Proj(proj='utm', zone=19, south=True, ellps='WGS84')

def descargar_satelite(min_lon, min_lat, max_lon, max_lat, width=1600, height=1200):
    """Descarga ortofoto satelital ESRI World Imagery."""
    url = (f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?"
           f"bbox={min_lon},{min_lat},{max_lon},{max_lat}&bboxSR=4326&imageSR=4326&size={width},{height}&format=png&f=image")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            img = Image.open(io.BytesIO(data)).convert("RGB")
            return np.array(img)
    except Exception as e:
        print(f"Error descargando satélite: {e}")
        # Fondo sintético de respaldo
        arr = np.zeros((height, width, 3), dtype=np.uint8)
        arr[:, :, 0] = 30; arr[:, :, 1] = 50; arr[:, :, 2] = 35
        return arr

def agregar_membrete(ax, titulo_plano, lamina_cod, escala="1 : 10,000", autor="UNAP - FIME / Consultoría Energética"):
    """Agrega membrete oficial de ingeniería de alta calidad."""
    rect = patches.Rectangle((0.66, 0.03), 0.32, 0.17, transform=ax.transAxes,
                             facecolor='#FFFFFF', edgecolor='#1F4E79', linewidth=1.8, zorder=150, alpha=0.95)
    ax.add_patch(rect)
    ax.text(0.67, 0.175, "UNIVERSIDAD NACIONAL DEL ALTIPLANO PUNO", transform=ax.transAxes,
            fontsize=8, fontweight='bold', color='#1F4E79', zorder=151)
    ax.text(0.67, 0.155, "FACULTAD DE INGENIERÍA MECÁNICA ELÉCTRICA", transform=ax.transAxes,
            fontsize=6.8, fontweight='bold', color='#2F5597', zorder=151)
    ax.text(0.67, 0.135, "PROYECTO: MCH RÍO BLANCO 100 kW - OLLACHEA", transform=ax.transAxes,
            fontsize=7.2, fontweight='bold', color='#000000', zorder=151)
    ax.text(0.67, 0.112, f"PLANO: {titulo_plano}", transform=ax.transAxes,
            fontsize=7.5, fontweight='bold', color='#B00020', zorder=151)
    ax.text(0.67, 0.090, f"DATUM: WGS-84 | ZONA: 19 SUR | ESCALA: {escala}", transform=ax.transAxes,
            fontsize=6.2, color='#222222', zorder=151)
    ax.text(0.67, 0.068, f"FECHA: SETIEMBRE 2024 / 2026 | LÁMINA: {lamina_cod}", transform=ax.transAxes,
            fontsize=6.8, fontweight='bold', color='#1F4E79', zorder=151)
    ax.text(0.67, 0.045, f"RESPONSABLE: {autor}", transform=ax.transAxes,
            fontsize=6.0, fontstyle='italic', color='#444444', zorder=151)

def agregar_norte_y_escala(ax, x_pos=0.06, y_pos=0.88, escala_texto="500 m"):
    """Dibuja el norte magnético/geodésico y escala gráfica."""
    ax.annotate('N', xy=(x_pos, y_pos), xytext=(x_pos, y_pos - 0.06),
                transform=ax.transAxes,
                arrowprops=dict(facecolor='#C00000', edgecolor='white', width=3.5, headwidth=11),
                ha='center', va='center', fontsize=12, fontweight='bold', color='#C00000', zorder=160,
                path_effects=[pe.withStroke(linewidth=2, foreground="white")])
    # Barra de escala
    bar_rect = patches.Rectangle((x_pos - 0.03, y_pos - 0.11), 0.14, 0.015, transform=ax.transAxes,
                                 facecolor='black', edgecolor='white', linewidth=1.2, zorder=160)
    ax.add_patch(bar_rect)
    ax.text(x_pos + 0.04, y_pos - 0.14, escala_texto, transform=ax.transAxes,
            fontsize=8, fontweight='bold', color='white', zorder=161,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#111111', alpha=0.85, edgecolor='white'))

def sincronizar_anexos(filename):
    """Copia el plano generado hacia 06 Anexos."""
    src = os.path.join(MAPAS_DIR, filename)
    dst = os.path.join(ANEXOS_DIR, filename)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f" -> Sincronizado en Anexos: {filename}")

# ==============================================================================
# MAPA 01: UBICACIÓN REGIONAL Y DEPARTAMENTAL (IMAGEN SATELITAL REAL)
# ==============================================================================
def generar_mapa_01():
    print("\n--- Generando Mapa 01: Ubicación Regional Puno con Satélite Real ---")
    min_lon, max_lon = -71.8, -68.5
    min_lat, max_lat = -16.6, -13.0
    img = descargar_satelite(min_lon, min_lat, max_lon, max_lat, width=1600, height=1200)

    fig, ax = plt.subplots(figsize=(12, 9), dpi=300)
    ax.imshow(img, extent=[min_lon, max_lon, min_lat, max_lat], aspect='auto')

    # Destacar puntos clave regionales
    puntos_regionales = [
        {"nombre": "ZONA DEL PROYECTO\nMCH RÍO BLANCO (Ollachea)", "lon": -70.47, "lat": -13.80, "color": "#FF0000", "size": 120, "marker": "*"},
        {"nombre": "C.H. San Gabán II (110 MW)", "lon": -70.40, "lat": -13.43, "color": "#00FFFF", "size": 70, "marker": "s"},
        {"nombre": "Macusani (Carabaya)", "lon": -70.43, "lat": -14.07, "color": "#FFFF00", "size": 60, "marker": "o"},
        {"nombre": "Juliaca", "lon": -70.13, "lat": -15.50, "color": "#FFFFFF", "size": 70, "marker": "o"},
        {"nombre": "Puno (Capital)", "lon": -70.02, "lat": -15.84, "color": "#FFFFFF", "size": 80, "marker": "D"},
        {"nombre": "Lago Titicaca (3,812 msnm)", "lon": -69.60, "lat": -15.70, "color": "#66B2FF", "size": 0, "marker": ""},
        {"nombre": "Sandia", "lon": -69.43, "lat": -14.33, "color": "#FFFF00", "size": 50, "marker": "o"},
        {"nombre": "Puerto Maldonado (Madre de Dios)", "lon": -69.18, "lat": -12.59, "color": "#00FF66", "size": 60, "marker": "o"}
    ]

    for p in puntos_regionales:
        if p["size"] > 0:
            ax.scatter(p["lon"], p["lat"], color=p["color"], s=p["size"], edgecolors='black', linewidth=1.5, zorder=20, marker=p["marker"])
        ax.text(p["lon"] + 0.06, p["lat"] - 0.02, p["nombre"], fontsize=8.5, fontweight='bold', color=p["color"],
                zorder=25, path_effects=[pe.withStroke(linewidth=3, foreground="black")])

    # Trazo de la Carretera Interoceánica Sur (PE-34B)
    ruta_lon = [-70.02, -70.13, -70.43, -70.47, -70.40, -70.30, -69.80, -69.18]
    ruta_lat = [-15.84, -15.50, -14.07, -13.80, -13.43, -13.30, -13.00, -12.59]
    ax.plot(ruta_lon, ruta_lat, color='#FF9900', linestyle='--', linewidth=2.5, label='Carretera Interoceánica Sur (PE-34B)', zorder=15)

    # Recuadro delimitador de la zona de proyecto
    rect_proj = patches.Rectangle((-70.55, -13.88), 0.16, 0.14, linewidth=2.5, edgecolor='#FF0000', facecolor='none', linestyle='-', zorder=30)
    ax.add_patch(rect_proj)
    ax.text(-70.54, -13.73, "DETALLE MCH 100 kW", fontsize=9, fontweight='bold', color='#FF0000',
            bbox=dict(boxstyle="square,pad=0.2", facecolor='black', alpha=0.75, edgecolor='#FF0000'), zorder=31)

    # Rejilla y etiquetas geográficas
    ax.grid(True, linestyle=':', color='white', alpha=0.5)
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    ax.set_xlabel("Longitud Oeste (WGS-84)", fontsize=10, fontweight='bold')
    ax.set_ylabel("Latitud Sur (WGS-84)", fontsize=10, fontweight='bold')
    ax.set_title("MAPA DE UBICACIÓN REGIONAL Y ACCESO VIAL - DEPARTAMENTO DE PUNO\nProyecto Microcentral Hidroeléctrica Río Blanco 100 kW (Ollachea, Carabaya)",
                 fontsize=11.5, fontweight='bold', color='#1F4E79', pad=12)

    agregar_norte_y_escala(ax, x_pos=0.08, y_pos=0.88, escala_texto="50 km")
    agregar_membrete(ax, "UBICACIÓN REGIONAL Y MACROLOCALIZACIÓN", "LAM-01", escala="1 : 1,000,000")
    ax.legend(loc='lower left', frameon=True, facecolor='#111111', edgecolor='white', labelcolor='white', fontsize=8.5)

    plt.tight_layout()
    output_path = os.path.join(MAPAS_DIR, "Mapa_01_Ubicacion_Regional_Puno.png")
    plt.savefig(output_path)
    plt.close()
    sincronizar_anexos("Mapa_01_Ubicacion_Regional_Puno.png")
    print("Mapa 01 generado exitosamente.")

# ==============================================================================
# MAPA 03: ORTOFOTO SATELITAL DE ALTA RESOLUCIÓN Y TRAZADO INTEGRAL DE OBRAS
# ==============================================================================
def generar_mapa_03():
    print("\n--- Generando Mapa 03: Ortofoto Satelital HD y Trazo de Obras Civiles ---")
    min_lon, max_lon = -70.478, -70.460
    min_lat, max_lat = -13.814, -13.798
    img = descargar_satelite(min_lon, min_lat, max_lon, max_lat, width=1800, height=1400)

    fig, ax = plt.subplots(figsize=(13, 9.5), dpi=300)
    ax.imshow(img, extent=[min_lon, max_lon, min_lat, max_lat], aspect='auto')

    # Coordenadas UTM de infraestructura oficial
    obras = [
        {"id": "BOC-01", "nom": "Bocatoma Tirolesa con Azud\nCota: 2,420.0 msnm | Qd = 125 L/s", "utm_e": 340915.2, "utm_n": 8472980.5, "color": "#00FFCC", "marker": "D"},
        {"id": "DES-01", "nom": "Desarenador Doble Nave\nCota: 2,418.5 msnm | d >= 0.20 mm", "utm_e": 340940.8, "utm_n": 8473020.1, "color": "#00FFCC", "marker": "s"},
        {"id": "CAN-MED", "nom": "Canal de Aducción (L=450m)\nb=0.50m, h=0.60m, S=1.5 ‰", "utm_e": 341100.4, "utm_n": 8473180.2, "color": "#FFFF00", "marker": "^"},
        {"id": "CAM-CAR", "nom": "Cámara de Carga y Aliviadero\nCota: 2,417.8 msnm | Vol = 22.5 m³", "utm_e": 341250.5, "utm_n": 8473310.8, "color": "#FF9900", "marker": "p"},
        {"id": "ANC-1", "nom": "Anclaje A-1 (Inflexión 18°)", "utm_e": 341300.0, "utm_n": 8473380.0, "color": "#FFFFFF", "marker": "o"},
        {"id": "ANC-2", "nom": "Anclaje A-2 (Inflexión 24°)", "utm_e": 341365.0, "utm_n": 8473480.0, "color": "#FFFFFF", "marker": "o"},
        {"id": "ANC-3", "nom": "Anclaje A-3 (Inflexión 31°)", "utm_e": 341420.0, "utm_n": 8473560.0, "color": "#FFFFFF", "marker": "o"},
        {"id": "CAS-MAQ", "nom": "Casa de Máquinas (Turbina Pelton)\nCota: 2,302.8 msnm | Salto Hb=115m", "utm_e": 341480.1, "utm_n": 8473650.4, "color": "#FF0033", "marker": "P"},
        {"id": "SUB-EST", "nom": "Subestación Elevadora 0.38/10 kV\nTrafo 125 kVA ONAN", "utm_e": 341495.0, "utm_n": 8473665.0, "color": "#FF00FF", "marker": "*"},
        {"id": "DES-RES", "nom": "Restitución al Río Blanco\nCota: 2,301.5 msnm", "utm_e": 341510.3, "utm_n": 8473675.8, "color": "#00B0F0", "marker": "v"}
    ]

    # Convertir coordenadas UTM a WGS84 para graficar sobre el mapa satelital
    puntos_wgs = []
    for ob in obras:
        lon, lat = utm_proj(ob["utm_e"], ob["utm_n"], inverse=True)
        ob["lon"] = lon
        ob["lat"] = lat
        puntos_wgs.append(ob)

    # Trazo de canal (cian/amarillo)
    canal_e = [340915.2, 340940.8, 340960.0, 341050.0, 341100.4, 341180.0, 341250.5]
    canal_n = [8472980.5, 8473020.1, 8473045.0, 8473130.0, 8473180.2, 8473250.0, 8473310.8]
    canal_lons, canal_lats = utm_proj(canal_e, canal_n, inverse=True)
    ax.plot(canal_lons, canal_lats, color='#00FFCC', linewidth=4.0, label='Canal de Aducción Rectangular (L=450m)', zorder=20,
            path_effects=[pe.withStroke(linewidth=6, foreground="black")])

    # Trazo de tubería forzada (rojo/naranja)
    tub_e = [341250.5, 341300.0, 341365.0, 341420.0, 341480.1]
    tub_n = [8473310.8, 8473380.0, 8473480.0, 8473560.0, 8473650.4]
    tub_lons, tub_lats = utm_proj(tub_e, tub_n, inverse=True)
    ax.plot(tub_lons, tub_lats, color='#FF3300', linewidth=4.5, linestyle='-', label='Tubería Forzada Penstock (L=380m, D=250mm)', zorder=22,
            path_effects=[pe.withStroke(linewidth=6.5, foreground="black")])

    # Cauce natural del Río Blanco (azul brillante)
    rio_e = [340850, 340915, 340980, 341080, 341200, 341350, 341480, 341550]
    rio_n = [8472850, 8472980, 8473090, 8473200, 8473350, 8473520, 8473650, 8473750]
    rio_lons, rio_lats = utm_proj(rio_e, rio_n, inverse=True)
    ax.plot(rio_lons, rio_lats, color='#3399FF', linewidth=3.0, linestyle='-.', label='Cauce Natural Río Blanco', zorder=18,
            path_effects=[pe.withStroke(linewidth=5, foreground="navy")])

    # Dibujar puntos y etiquetas de ingeniería
    for ob in puntos_wgs:
        ax.scatter(ob["lon"], ob["lat"], color=ob["color"], s=100, edgecolors='black', linewidth=1.5, zorder=30, marker=ob["marker"])
        # Desplazamientos inteligentes de etiquetas
        dx = 0.0006 if ob["utm_e"] > 341200 else -0.0035
        dy = 0.0003 if "Bocatoma" in ob["nom"] or "Casa" in ob["nom"] else -0.0005
        ax.annotate(f"[{ob['id']}] {ob['nom']}", xy=(ob["lon"], ob["lat"]), xytext=(ob["lon"] + dx, ob["lat"] + dy),
                    fontsize=7.2, fontweight='bold', color='white', zorder=35,
                    bbox=dict(boxstyle="round,pad=0.25", facecolor='#111111', alpha=0.88, edgecolor=ob["color"], linewidth=1.2),
                    arrowprops=dict(arrowstyle="->", color='white', lw=1.2))

    # Grilla de coordenadas UTM sobre el mapa satelital
    ax.grid(True, linestyle='--', color='white', alpha=0.45)
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    ax.set_xlabel("Longitud WGS-84", fontsize=10, fontweight='bold')
    ax.set_ylabel("Latitud WGS-84", fontsize=10, fontweight='bold')
    ax.set_title("ORTOFOTO SATELITAL DE ALTA RESOLUCIÓN Y TRAZADO INTEGRAL DE OBRAS HIDRÁULICAS\nMicrocentral Hidroeléctrica Río Blanco 100 kW - Ollachea, Puno",
                 fontsize=11.5, fontweight='bold', color='#1F4E79', pad=12)

    agregar_norte_y_escala(ax, x_pos=0.08, y_pos=0.88, escala_texto="200 m")
    agregar_membrete(ax, "DISPOSICIÓN GENERAL DE OBRAS CIVILES", "LAM-03", escala="1 : 2,500")
    ax.legend(loc='lower left', frameon=True, facecolor='#111111', edgecolor='white', labelcolor='white', fontsize=8)

    plt.tight_layout()
    output_path = os.path.join(MAPAS_DIR, "Mapa_03_Esquema_Obras_Hidraulicas_Trazo.png")
    plt.savefig(output_path)
    plt.close()
    sincronizar_anexos("Mapa_03_Esquema_Obras_Hidraulicas_Trazo.png")
    print("Mapa 03 generado exitosamente.")

# ==============================================================================
# MAPA 06: RED GEODÉSICA DE CONTROL DE ORDEN "C" (IGN - REGGEN)
# ==============================================================================
def generar_mapa_06():
    print("\n--- Generando Mapa 06: Red Geodésica de Control IGN y Puntos de Apoyo ---")
    min_lon, max_lon = -70.482, -70.458
    min_lat, max_lat = -13.818, -13.796
    img = descargar_satelite(min_lon, min_lat, max_lon, max_lat, width=1800, height=1400)

    fig, ax = plt.subplots(figsize=(13, 9.5), dpi=300)
    ax.imshow(img, extent=[min_lon, max_lon, min_lat, max_lat], aspect='auto')

    # Vértices de la red geodésica
    vertices_geo = [
        {"cod": "PUNO-01", "nom": "Estación Permanente GNSS IGN (REGGEN)\nReceptor Trimble Alloy L1/L2/L5", "utm_e": 341650.0, "utm_n": 8472750.0, "cota": 2550.42, "tipo": "BASE_IGN"},
        {"cod": "HG-01", "nom": "Hito Geodésico HG-01 (Bocatoma)\nMojón de Concreto con Placa de Bronce", "utm_e": 340915.2, "utm_n": 8472980.5, "cota": 2420.00, "tipo": "HITO_PROY"},
        {"cod": "HG-02", "nom": "Hito Geodésico HG-02 (Cámara Carga)\nMojón de Concreto con Placa de Bronce", "utm_e": 341250.5, "utm_n": 8473310.8, "cota": 2417.80, "tipo": "HITO_PROY"},
        {"cod": "HG-03", "nom": "Hito Geodésico HG-03 (Casa Máquinas)\nMojón de Concreto con Placa de Bronce", "utm_e": 341480.1, "utm_n": 8473650.4, "cota": 2302.80, "tipo": "HITO_PROY"},
        {"cod": "BM-01", "nom": "Banco de Nivel Fijo BM-01 (Desarenador)", "utm_e": 340950.0, "utm_n": 8473030.0, "cota": 2418.52, "tipo": "BM"},
        {"cod": "BM-02", "nom": "Banco de Nivel Fijo BM-02 (Tubería Forzada)", "utm_e": 341350.0, "utm_n": 8473450.0, "cota": 2375.10, "tipo": "BM"},
        {"cod": "BM-03", "nom": "Banco de Nivel Fijo BM-03 (Subestación)", "utm_e": 341505.0, "utm_n": 8473680.0, "cota": 2302.50, "tipo": "BM"}
    ]

    for v in vertices_geo:
        lon, lat = utm_proj(v["utm_e"], v["utm_n"], inverse=True)
        v["lon"] = lon
        v["lat"] = lat

    # Dibujar líneas de base GNSS (vectores diferenciales post-procesados)
    base = vertices_geo[0] # PUNO-01
    for target in vertices_geo[1:4]: # HG-01, HG-02, HG-03
        ax.plot([base["lon"], target["lon"]], [base["lat"], target["lat"]],
                color='#FFFF00', linestyle='--', linewidth=1.8, zorder=20)
        # Etiqueta de vector diferencial GNSS
        dist_m = math.sqrt((base["utm_e"] - target["utm_e"])**2 + (base["utm_n"] - target["utm_n"])**2)
        mid_lon = (base["lon"] + target["lon"]) / 2.0
        mid_lat = (base["lat"] + target["lat"]) / 2.0
        ax.text(mid_lon, mid_lat, f"V-GNSS: {dist_m:.1f} m\n(Sigma <= 3mm)", fontsize=6.5, color='#FFFF00',
                bbox=dict(boxstyle="round,pad=0.15", facecolor='black', alpha=0.75, edgecolor='none'), zorder=22)

    # Triangulación interna HG-01 a HG-02 y HG-02 a HG-03
    ax.plot([vertices_geo[1]["lon"], vertices_geo[2]["lon"]], [vertices_geo[1]["lat"], vertices_geo[2]["lat"]],
            color='#00FFCC', linestyle='-', linewidth=2.0, zorder=20)
    ax.plot([vertices_geo[2]["lon"], vertices_geo[3]["lon"]], [vertices_geo[2]["lat"], vertices_geo[3]["lat"]],
            color='#00FFCC', linestyle='-', linewidth=2.0, zorder=20)

    # Dibujar puntos geodésicos
    for v in vertices_geo:
        color = '#FF0000' if v["tipo"] == "BASE_IGN" else ('#00FF00' if v["tipo"] == "HITO_PROY" else '#00FFFF')
        marker = 's' if v["tipo"] == "BASE_IGN" else ('^' if v["tipo"] == "HITO_PROY" else 'o')
        size = 130 if v["tipo"] == "BASE_IGN" else 100
        ax.scatter(v["lon"], v["lat"], color=color, s=size, edgecolors='black', linewidth=1.5, zorder=30, marker=marker)
        
        ax.annotate(f"[{v['cod']}]\nE: {v['utm_e']:.1f} m\nN: {v['utm_n']:.1f} m\nZ: {v['cota']:.2f} msnm",
                    xy=(v["lon"], v["lat"]), xytext=(v["lon"] + 0.0007, v["lat"] - 0.0006),
                    fontsize=6.8, fontweight='bold', color='white', zorder=35,
                    bbox=dict(boxstyle="round,pad=0.25", facecolor='#111111', alpha=0.90, edgecolor=color, linewidth=1.2),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.2))

    # Cuadro de especificaciones y parámetros geodésicos oficiales IGN
    cuadro_geo = (
        "PARÁMETROS GEODÉSICOS Y CARTOGRÁFICOS OFICIALES:\n"
        "--------------------------------------------------\n"
        "• Elipsoide de Referencia: WGS-84 (GRS80)\n"
        "• Semieje Mayor (a): 6,378,137.000 m | 1/f: 298.257223563\n"
        "• Sistema de Proyección: Universal Transversa de Mercator (UTM)\n"
        "• Zona / Hemisferio: Zona 19 Sur | Meridiano Central: 69° W\n"
        "• Falso Este: 500,000.000 m | Falso Norte: 10,000,000.000 m\n"
        "• Modelo Geoidal Global: EGM2008 (Ondulación N = +38.45 m)\n"
        "• Factor de Escala Cartográfico (k0): 0.999600\n"
        "• Factor de Elevación Medio: 0.999634\n"
        "• Factor de Escala Combinado (K): 0.999234\n"
        "• Convergencia de Meridianos: gamma = -0° 34' 12.8''\n"
        "• Precisión Relativa Horizontal: 1 : 100,000 (Orden C - IGN)\n"
        "• Método: GNSS Diferencial Estático Post-procesado (Bernese/TBC)"
    )
    ax.text(0.03, 0.22, cuadro_geo, transform=ax.transAxes, fontsize=6.8, color='white', zorder=120,
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#0D1B2A', alpha=0.92, edgecolor='#00FFCC', linewidth=1.5))

    ax.grid(True, linestyle='--', color='white', alpha=0.45)
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    ax.set_xlabel("Longitud WGS-84", fontsize=10, fontweight='bold')
    ax.set_ylabel("Latitud WGS-84", fontsize=10, fontweight='bold')
    ax.set_title("RED GEODÉSICA DE CONTROL HORIZONTAL Y VERTICAL DE ORDEN 'C' (IGN - REGGEN)\nMicrocentral Hidroeléctrica Río Blanco 100 kW - Ollachea, Carabaya, Puno",
                 fontsize=11.5, fontweight='bold', color='#1F4E79', pad=12)

    agregar_norte_y_escala(ax, x_pos=0.08, y_pos=0.88, escala_texto="200 m")
    agregar_membrete(ax, "RED GEODÉSICA Y CONTROL TOPOGRÁFICO", "LAM-06", escala="1 : 2,500")

    plt.tight_layout()
    output_path = os.path.join(MAPAS_DIR, "Mapa_06_Red_Control_Geodesico_IGN.png")
    plt.savefig(output_path)
    plt.close()
    sincronizar_anexos("Mapa_06_Red_Control_Geodesico_IGN.png")
    print("Mapa 06 generado exitosamente.")

# ==============================================================================
# MAPA 07: MAPA GEOLÓGICO, GEOTÉCNICO Y ESTABILIDAD DE TALUDES
# ==============================================================================
def generar_mapa_07():
    print("\n--- Generando Mapa 07: Geología, Geotecnia y Riesgos de Ladera ---")
    min_lon, max_lon = -70.480, -70.458
    min_lat, max_lat = -13.816, -13.798
    img = descargar_satelite(min_lon, min_lat, max_lon, max_lat, width=1800, height=1400)

    fig, ax = plt.subplots(figsize=(13, 9.5), dpi=300)
    # Satélite semi-transparente para apreciar litología
    ax.imshow(img, extent=[min_lon, max_lon, min_lat, max_lat], aspect='auto', alpha=0.75)

    # Superposición de polígonos litológicos
    # Formación Sandia (Pizarras y Cuarcitas competentes)
    poly_roca = patches.Polygon([
        [-70.480, -13.816], [-70.470, -13.816], [-70.463, -13.805], [-70.472, -13.798], [-70.480, -13.798]
    ], closed=True, facecolor='#2B5B84', alpha=0.35, edgecolor='#1B3B54', linewidth=1.5, zorder=10)
    ax.add_patch(poly_roca)
    ax.text(-70.477, -13.810, "MACIZO ROCOSO (Grupo San José / Sandia)\nPizarras y Cuarcitas Gris-Oscuras\nRMR = 62-68 (Roca Buena a Muy Buena)\nResistencia Compresión Simple: 85-110 MPa",
            fontsize=7.5, fontweight='bold', color='white',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#1F4E79', alpha=0.85, edgecolor='white'), zorder=15)

    # Depósito Aluvial y Fluvial (Cauce del Río Blanco)
    poly_aluvial = patches.Polygon([
        [-70.473, -13.814], [-70.470, -13.810], [-70.466, -13.803], [-70.463, -13.800],
        [-70.460, -13.800], [-70.464, -13.805], [-70.468, -13.812], [-70.471, -13.816]
    ], closed=True, facecolor='#C9A96E', alpha=0.45, edgecolor='#8B5A2B', linewidth=1.5, zorder=12)
    ax.add_patch(poly_aluvial)
    ax.text(-70.465, -13.812, "DEPÓSITO ALUVIAL / FLUVIAL (Qh-al)\nGravas y Bolonería Subredondeada\nPermeabilidad media a alta",
            fontsize=7, fontweight='bold', color='white',
            bbox=dict(boxstyle="round,pad=0.25", facecolor='#5C3813', alpha=0.85, edgecolor='white'), zorder=16)

    # Trazado de fallas geológicas regionales
    falla_lons = [-70.479, -70.472, -70.465, -70.459]
    falla_lats = [-13.815, -13.808, -13.802, -13.799]
    ax.plot(falla_lons, falla_lats, color='#FF0000', linestyle='--', linewidth=2.5, zorder=25,
            label='Falla Geológica Inversa Regional (Inactiva)')

    # Zonas de riesgo geodinámico y estabilidad de taludes
    ax.scatter([-70.469], [-13.806], color='#FF6600', s=150, marker='X', edgecolors='black', linewidth=1.5, zorder=30)
    ax.text(-70.468, -13.806, "Peligro Moderado: Caída de bloques aislados\nMedida: Malla electrosoldada y anclajes en berma",
            fontsize=6.8, fontweight='bold', color='white',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#CC5200', alpha=0.85, edgecolor='white'), zorder=31)

    # Línea de obras para correlación geológica
    canal_e = [340915.2, 340940.8, 340960.0, 341100.4, 341250.5]
    canal_n = [8472980.5, 8473020.1, 8473045.0, 8473180.2, 8473310.8]
    canal_lons, canal_lats = utm_proj(canal_e, canal_n, inverse=True)
    ax.plot(canal_lons, canal_lats, color='#00FFCC', linewidth=3.5, label='Trazo Canal (Roca Sana)', zorder=20)

    tub_e = [341250.5, 341365.0, 341480.1]
    tub_n = [8473310.8, 8473480.0, 8473650.4]
    tub_lons, tub_lats = utm_proj(tub_e, tub_n, inverse=True)
    ax.plot(tub_lons, tub_lats, color='#FF3300', linewidth=4.0, label='Tubería Forzada (Apoyada en Roca)', zorder=22)

    ax.grid(True, linestyle=':', color='white', alpha=0.5)
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    ax.set_xlabel("Longitud WGS-84", fontsize=10, fontweight='bold')
    ax.set_ylabel("Latitud WGS-84", fontsize=10, fontweight='bold')
    ax.set_title("MAPA GEOLÓGICO, GEOTÉCNICO Y DE RIESGOS GEODINÁMICOS DE LADERA\nMicrocentral Hidroeléctrica Río Blanco 100 kW - Ollachea, Puno",
                 fontsize=11.5, fontweight='bold', color='#1F4E79', pad=12)

    agregar_norte_y_escala(ax, x_pos=0.08, y_pos=0.88, escala_texto="200 m")
    agregar_membrete(ax, "GEOLOGÍA, GEOTECNIA Y RIESGOS", "LAM-07", escala="1 : 2,500")
    ax.legend(loc='lower left', frameon=True, facecolor='#111111', edgecolor='white', labelcolor='white', fontsize=8)

    plt.tight_layout()
    output_path = os.path.join(MAPAS_DIR, "Mapa_07_Geologico_Geotecnico_Laderas.png")
    plt.savefig(output_path)
    plt.close()
    sincronizar_anexos("Mapa_07_Geologico_Geotecnico_Laderas.png")
    print("Mapa 07 generado exitosamente.")

# ==============================================================================
# MAPA 08: ZONIFICACIÓN DE USOS PRODUCTIVOS Y ELECTRIFICACIÓN
# ==============================================================================
def generar_mapa_08():
    print("\n--- Generando Mapa 08: Usos Productivos y Electrificación Rural ---")
    min_lon, max_lon = -70.490, -70.450
    min_lat, max_lat = -13.825, -13.790
    img = descargar_satelite(min_lon, min_lat, max_lon, max_lat, width=1800, height=1400)

    fig, ax = plt.subplots(figsize=(13, 9.5), dpi=300)
    ax.imshow(img, extent=[min_lon, max_lon, min_lat, max_lat], aspect='auto')

    # Centros de carga y aplicaciones productivas
    aplicaciones = [
        {"nom": "CASA DE MÁQUINAS MCH (100 kW)\nGeneración Síncrona 0.38 kV", "lon": -70.4665, "lat": -13.8023, "col": "#FF0033", "m": "P", "kw": 100.0},
        {"nom": "CENTRO POBLADO OLLACHEA (280 Familias)\nElectrificación Domiciliaria, Escuelas y Centro de Salud", "lon": -70.4730, "lat": -13.7930, "col": "#FFFF00", "m": "o", "kw": 35.0},
        {"nom": "PLANTA AGROINDUSTRIAL CAFÉ & CACAO\nDespulpado, Secado Forzado, Tostado y Molienda", "lon": -70.4690, "lat": -13.7970, "col": "#00FF66", "m": "s", "kw": 22.0},
        {"nom": "PLANTA DE FRÍO PISCÍCOLA (Acuicultura Truchas)\nCámara de Conservación y Congelación (-18°C, 5 Ton)", "lon": -70.4630, "lat": -13.8010, "col": "#00FFFF", "m": "D", "kw": 18.0},
        {"nom": "CENTRO TEXTIL FIBRA DE ALPACA Y OVINO\nDescerdado, Cardado e Hilado Comunitario", "lon": -70.4780, "lat": -13.8040, "col": "#FF99FF", "m": "^", "kw": 12.0},
        {"nom": "ESTACIÓN DE BOMBEO AGUA & RIEGO TECNIFICADO\nBombeo a Reservorios Altos (Q=15 L/s, H=65m)", "lon": -70.4710, "lat": -13.8080, "col": "#3399FF", "m": "v", "kw": 10.0},
        {"nom": "INTERCONEXIÓN A RED ELECTRO PUNO (10 kV)\nEvacuación de Excedentes al SEIN (Marco RER)", "lon": -70.4580, "lat": -13.7915, "col": "#FF6600", "m": "*", "kw": 3.0}
    ]

    # Líneas de distribución en media tensión (10 kV) desde Casa de Máquinas
    cm_lon, cm_lat = -70.4665, -13.8023
    for ap in aplicaciones[1:]:
        ax.plot([cm_lon, ap["lon"]], [cm_lat, ap["lat"]], color='#FFFF00', linestyle=':', linewidth=2.0, zorder=15)
        # Línea de postes y vanos
        mid_x = (cm_lon + ap["lon"]) / 2.0
        mid_y = (cm_lat + ap["lat"]) / 2.0
        dist_km = math.sqrt(((cm_lon - ap["lon"])*111)**2 + ((cm_lat - ap["lat"])*111)**2)
        ax.text(mid_x, mid_y, f"MT 10 kV: {dist_km:.2f} km\n({ap['kw']} kW)", fontsize=6.2, color='#FFFF99',
                bbox=dict(boxstyle="round,pad=0.15", facecolor='black', alpha=0.75, edgecolor='none'), zorder=16)

    # Dibujar centros de carga
    for ap in aplicaciones:
        ax.scatter(ap["lon"], ap["lat"], color=ap["col"], s=130, edgecolors='black', linewidth=1.5, zorder=25, marker=ap["m"])
        ax.annotate(f"{ap['nom']}\nDemanda Nominal: {ap['kw']} kW", xy=(ap["lon"], ap["lat"]),
                    xytext=(ap["lon"] + 0.0012, ap["lat"] + 0.0008),
                    fontsize=7.0, fontweight='bold', color='white', zorder=30,
                    bbox=dict(boxstyle="round,pad=0.25", facecolor='#0B172A', alpha=0.92, edgecolor=ap["col"], linewidth=1.3),
                    arrowprops=dict(arrowstyle="->", color=ap["col"], lw=1.2))

    # Balance de potencia y demanda comunitaria
    balance_txt = (
        "BALANCE DE DEMANDA Y USOS PRODUCTIVOS:\n"
        "---------------------------------------\n"
        "• Potencia Eléctrica Neta Generada: 100.0 kW\n"
        "• Electrificación Residencial y Social: 35.0 kW (35%)\n"
        "• Agroindustria Café y Cacao de Altura: 22.0 kW (22%)\n"
        "• Cadena de Frío y Piscicultura Truchas: 18.0 kW (18%)\n"
        "• Transformación Textil Fibra Alpaca: 12.0 kW (12%)\n"
        "• Estación de Bombeo de Agua Potable: 10.0 kW (10%)\n"
        "• Margen de Reserva / Venta SEIN: 3.0 kW (3%)\n"
        "---------------------------------------\n"
        "FACTOR DE PLANTA ANUAL ESTIMADO: 76.8 %\n"
        "PRODUCCIÓN ANUAL ESTIMADA: 672.77 MWh/año"
    )
    ax.text(0.03, 0.22, balance_txt, transform=ax.transAxes, fontsize=7.2, color='white', zorder=120,
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#002244', alpha=0.92, edgecolor='#FFFF00', linewidth=1.5))

    ax.grid(True, linestyle='--', color='white', alpha=0.4)
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    ax.set_xlabel("Longitud WGS-84", fontsize=10, fontweight='bold')
    ax.set_ylabel("Latitud WGS-84", fontsize=10, fontweight='bold')
    ax.set_title("ZONIFICACIÓN DE USOS PRODUCTIVOS Y ELECTRIFICACIÓN RURAL INTEGRAL\nMicrocentral Hidroeléctrica Río Blanco 100 kW - Ollachea, Puno",
                 fontsize=11.5, fontweight='bold', color='#1F4E79', pad=12)

    agregar_norte_y_escala(ax, x_pos=0.08, y_pos=0.88, escala_texto="500 m")
    agregar_membrete(ax, "USOS PRODUCTIVOS Y ELECTRIFICACIÓN", "LAM-08", escala="1 : 5,000")

    plt.tight_layout()
    output_path = os.path.join(MAPAS_DIR, "Mapa_08_Zonificacion_Usos_Productivos_Electrificacion.png")
    plt.savefig(output_path)
    plt.close()
    sincronizar_anexos("Mapa_08_Zonificacion_Usos_Productivos_Electrificacion.png")
    print("Mapa 08 generado exitosamente.")

if __name__ == "__main__":
    generar_mapa_01()
    generar_mapa_03()
    generar_mapa_06()
    generar_mapa_07()
    generar_mapa_08()
    print("\n¡Toda la cartografía satelital y geodésica ha sido generada y sincronizada exitosamente!")
