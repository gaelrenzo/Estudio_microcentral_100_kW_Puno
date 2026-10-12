#!/usr/bin/env python3
"""
Generador del Visor Web SIG Interactivo de Geodesia e Infraestructura Hidroeléctrica
Proyecto: Microcentral Hidroeléctrica 100 kW - Río Blanco, Ollachea, Puno
"""
import os
import shutil

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
MAPAS_DIR = str(BASE_DIR / "04 Mapas")
ANEXOS_DIR = str(BASE_DIR / "06 Anexos")

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visor Geodésico y Cartográfico - MCH Río Blanco 100 kW (Puno)</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body, html { margin: 0; padding: 0; height: 100%; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
        #map { width: 100%; height: 100%; }
        .info-panel {
            position: absolute; top: 10px; right: 10px; z-index: 1000;
            background: rgba(255, 255, 255, 0.96); padding: 16px 20px; border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3); max-width: 360px; font-size: 13px; line-height: 1.45;
            border-left: 5px solid #1F4E79;
        }
        .info-panel h2 { margin: 0 0 6px 0; font-size: 15px; color: #1F4E79; font-weight: bold; }
        .info-panel h3 { margin: 4px 0; font-size: 12.5px; color: #B00020; }
        .info-panel p { margin: 4px 0 8px 0; color: #444; }
        .coord-box {
            position: absolute; bottom: 25px; left: 15px; z-index: 1000;
            background: rgba(13, 27, 42, 0.9); color: #00FFCC; padding: 8px 14px;
            border-radius: 6px; font-family: monospace; font-size: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.4); border: 1px solid #00FFCC;
        }
        .legend {
            position: absolute; bottom: 25px; right: 10px; z-index: 1000;
            background: rgba(255, 255, 255, 0.94); padding: 10px 14px; border-radius: 6px;
            font-size: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.25); line-height: 1.6;
        }
        .legend-item { display: flex; align-items: center; margin-bottom: 4px; }
        .legend-color { width: 14px; height: 14px; margin-right: 8px; border-radius: 3px; }
        .badge { display: inline-block; padding: 2px 6px; font-size: 10px; font-weight: bold; border-radius: 4px; color: white; }
    </style>
</head>
<body>
    <div id="map"></div>

    <div class="info-panel">
        <h2>MCH RÍO BLANCO 100 kW</h2>
        <h3>EXPEDIENTE TÉCNICO & GEODÉSICO OFICIAL</h3>
        <p><strong>Ubicación:</strong> Ollachea, Carabaya, Puno (Vertiente Atlántica - Río Inambari)</p>
        <p><strong>Parámetros de Diseño:</strong></p>
        <ul style="padding-left: 18px; margin: 4px 0;">
            <li>Caudal Nominal: <strong>125 L/s (0.125 m³/s)</strong> (Persistencia 78%)</li>
            <li>Caudal Ecológico (ANA): <strong>30 L/s</strong> (Inalterable)</li>
            <li>Caída Bruta / Neta: <strong>115.00 m / 106.18 m</strong></li>
            <li>Potencia Neta: <strong>100 kW</strong> (672.77 MWh/año)</li>
            <li>Turbina: <strong>Pelton 2 Inyectores (1,200 RPM, 60 Hz)</strong></li>
            <li>Generador: <strong>Síncrono Brushless 125 kVA (0.38 kV)</strong></li>
        </ul>
        <hr style="border: 0; border-top: 1px solid #ddd; margin: 8px 0;">
        <p style="font-size: 11.5px; color: #555;">
            <strong>Datum Oficial:</strong> WGS-84 / UTM Zona 19S (EPSG:32719)<br>
            <strong>Red Geodésica:</strong> Orden "C" certificada IGN (Base PUNO-01)
        </p>
    </div>

    <div class="coord-box" id="coords">
        Puntero: Lon: -70.47178° | Lat: -13.80836° | UTM 19S: 340,915 E, 8,472,980 N
    </div>

    <div class="legend">
        <strong>CAPAS VECTORIALES:</strong>
        <div class="legend-item"><div class="legend-color" style="background: #00FFCC; border: 1px solid black;"></div>Canal Aducción (450 m)</div>
        <div class="legend-item"><div class="legend-color" style="background: #FF3300; border: 1px solid black;"></div>Tubería Forzada (380 m)</div>
        <div class="legend-item"><div class="legend-color" style="background: #3399FF; border: 1px solid black;"></div>Cauce Río Blanco</div>
        <div class="legend-item"><div class="legend-color" style="background: #FF0000; border: 1px solid black;"></div>Obras Hidráulicas</div>
        <div class="legend-item"><div class="legend-color" style="background: #FFFF00; border: 1px solid black;"></div>Hitos Geodésicos IGN</div>
        <div class="legend-item"><div class="legend-color" style="background: #FF9900; border: 1px solid black;"></div>Red Media Tensión 10 kV</div>
    </div>

    <script>
        // Inicializar mapa centrado en Ollachea / Río Blanco
        var map = L.map('map', {
            center: [-13.8055, -70.4690],
            zoom: 16,
            zoomControl: true
        });

        // Capas Base
        var esriSat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            maxZoom: 19
        }).addTo(map);

        var topoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data: &copy; OpenStreetMap contributors, SRTM | Map style: &copy; OpenTopoMap (CC-BY-SA)',
            maxZoom: 17
        });

        var osmMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors',
            maxZoom: 19
        });

        // Capas Base Selector
        var baseMaps = {
            "Satélite ESRI HD (Ortofoto Real)": esriSat,
            "Topográfico con Curvas (OpenTopoMap)": topoMap,
            "Callejero (OpenStreetMap)": osmMap
        };

        // Grupos de capas
        var obrasGroup = L.layerGroup().addTo(map);
        var geoGroup = L.layerGroup().addTo(map);
        var lineasGroup = L.layerGroup().addTo(map);
        var usosGroup = L.layerGroup().addTo(map);

        // Trazo del Canal de Aducción
        var canalCoords = [
            [-13.808357, -70.471777],
            [-13.807999, -70.471540],
            [-13.807774, -70.471363],
            [-13.807005, -70.470530],
            [-13.806552, -70.470064],
            [-13.805922, -70.469327],
            [-13.805373, -70.468675]
        ];
        L.polyline(canalCoords, {color: '#00FFCC', weight: 5, opacity: 0.9}).addTo(lineasGroup)
            .bindPopup("<b>Canal de Aducción Rectangular</b><br>Longitud: 450 m | Sección: b=0.50m, h=0.60m<br>Pendiente: S=0.0015 | Tirante normal: yn=0.33 m<br>Concreto f'c=175 kg/cm² a media ladera en roca sana.");

        // Trazo de Tubería Forzada
        var penstockCoords = [
            [-13.805373, -70.468675],
            [-13.804748, -70.468217],
            [-13.803845, -70.467615],
            [-13.803123, -70.467106],
            [-13.802333, -70.466514]
        ];
        L.polyline(penstockCoords, {color: '#FF3300', weight: 6, opacity: 0.95}).addTo(lineasGroup)
            .bindPopup("<b>Tubería Forzada (Penstock de Alta Presión)</b><br>Longitud: 380 m | Diámetro interior: 250 mm (10 pulg)<br>Acero ASTM A36 e=4.75mm a 6.35mm<br>Salto bruto: 115.00 m | Salto neto: 106.18 m<br>Presión máx. con golpe de ariete: 164.32 m.c.a. (16.11 bar)");

        // Obras Hidráulicas
        var infra = [
            {nom: "Bocatoma Tirolesa con Azud (BOC-01)", lat: -13.808357, lon: -70.471777, cota: 2420.0, desc: "Captación de fondo en cauce con rejilla Coanda de acero inoxidable (α=20°, separación 25mm), azud ciclópeo de 4m cresta y cámara de derivación."},
            {nom: "Desarenador Doble Nave (DES-01)", lat: -13.807999, lon: -70.471540, cota: 2418.5, desc: "Estructura de decantación de 2 naves (8.0m x 0.70m) para partículas d >= 0.20 mm con vertedero proporcional Sutro y purga rápida."},
            {nom: "Cámara de Carga (Forebay) (CAM-CAR)", lat: -13.805373, lon: -70.468675, cota: 2417.8, desc: "Tanque de concreto armado de 4x3x2.2m (Volumen 22.5 m³, 3 min regulación), aliviadero lateral de demasías y tubo de ventilación anti-vacío."},
            {nom: "Casa de Máquinas (CAS-MAQ)", lat: -13.802333, lon: -70.466514, cota: 2302.8, desc: "Edificación de 8.5x6m albergando turbina Pelton de 2 inyectores (114.6 kW mecánicos) y alternador síncrono brushless 125 kVA a 1200 RPM."},
            {nom: "Subestación Elevadora (SUB-EST)", lat: -13.802200, lon: -70.466375, cota: 2303.0, desc: "Transformador trifásico 125 kVA 0.38/10 kV ONAN Dyn5, seccionadores cut-out 24kV, pararrayos poliméricos y malla de tierra IEEE 80 (R=3.82 Ω)."},
            {nom: "Canal de Restitución al Río (DES-RES)", lat: -13.802100, lon: -70.466230, cota: 2301.5, desc: "Retorno inmediato de los 125 L/s turbinados al cauce del Río Blanco sin desvío perenne ni afectación ecológica."}
        ];

        infra.forEach(function(item) {
            L.circleMarker([item.lat, item.lon], {
                radius: 8, fillColor: '#FF0033', color: '#FFFFFF', weight: 2, fillOpacity: 0.95
            }).addTo(obrasGroup).bindPopup("<b>" + item.nom + "</b><br><b>Cota:</b> " + item.cota.toFixed(2) + " msnm<br>" + item.desc);
        });

        // Hitos Geodésicos IGN
        var hitos = [
            {cod: "HG-01", nom: "Hito Geodésico Bocatoma", lat: -13.808357, lon: -70.471777, utme: 340915.2, utmn: 8472980.5, cota: 2420.00},
            {cod: "HG-02", nom: "Hito Geodésico Cámara de Carga", lat: -13.805373, lon: -70.468675, utme: 341250.5, utmn: 8473310.8, cota: 2417.80},
            {cod: "HG-03", nom: "Hito Geodésico Casa de Máquinas", lat: -13.802333, lon: -70.466514, utme: 341480.1, utmn: 8473650.4, cota: 2302.80},
            {cod: "BM-01", nom: "Banco de Nivel Fijo Desarenador", lat: -13.807900, lon: -70.471450, utme: 340950.0, utmn: 8473030.0, cota: 2418.52},
            {cod: "BM-03", nom: "Banco de Nivel Fijo Subestación", lat: -13.802050, lon: -70.466280, utme: 341505.0, utmn: 8473680.0, cota: 2302.50}
        ];

        hitos.forEach(function(h) {
            L.circleMarker([h.lat, h.lon], {
                radius: 6, fillColor: '#FFFF00', color: '#000000', weight: 2, fillOpacity: 1.0
            }).addTo(geoGroup).bindPopup("<b style='color:#B00020;'>[" + h.cod + "] " + h.nom + "</b><br>Red Geodésica REGGEN - Orden 'C' (IGN)<br><b>Este UTM:</b> " + h.utme.toLocaleString() + " m E<br><b>Norte UTM:</b> " + h.utmn.toLocaleString() + " m N<br><b>Elevación Ortométrica:</b> " + h.cota.toFixed(3) + " msnm<br><b>Factor Escala Combinado K:</b> 0.999234");
        });

        // Usos Productivos
        var usos = [
            {nom: "Poblado de Ollachea (280 Familias)", lat: -13.7930, lon: -70.4730, kw: 35, desc: "Electrificación rural domiciliaria, alumbrado público LED, postas médicas y centros educativos."},
            {nom: "Planta Agroindustrial Café & Cacao", lat: -13.7970, lon: -70.4690, kw: 22, desc: "Despulpado ecológico, secado por convección forzada, tostadoras y molinos comunitarios."},
            {nom: "Planta de Frío para Acuicultura de Truchas", lat: -13.8010, lon: -70.4630, kw: 18, desc: "Cámara frigorífica de conservación (-18°C, 5 Toneladas) y aireación forzada en estanques."},
            {nom: "Centro de Transformación Fibra de Alpaca", lat: -13.8040, lon: -70.4780, kw: 12, desc: "Descerdadoras, cardadoras e hiladoras eléctricas para fibra de alpaca de alta finura."},
            {nom: "Estación de Bombeo de Agua Potable", lat: -13.8080, lon: -70.4710, kw: 10, desc: "Elevación de agua potable a reservorios comunales y riego tecnificado por aspersión."}
        ];

        usos.forEach(function(u) {
            L.marker([u.lat, u.lon]).addTo(usosGroup)
                .bindPopup("<b style='color:#1F4E79;'>" + u.nom + "</b><br><span class='badge' style='background:#009933;'>Demanda: " + u.kw + " kW</span><br>" + u.desc);
        });

        // Control de Capas
        var overlayMaps = {
            "Obras Civiles e Hidráulicas": obrasGroup,
            "Trazo Conducción y Penstock": lineasGroup,
            "Red Geodésica de Control (IGN)": geoGroup,
            "Usos Productivos y Electrificación": usosGroup
        };
        L.control.layers(baseMaps, overlayMaps, {collapsed: false}).addTo(map);

        // Escala
        L.control.scale({metric: true, imperial: false, position: 'bottomleft'}).addTo(map);

        // Rastreador de Coordenadas
        map.on('mousemove', function(e) {
            // Conversión aproximada WGS84 a UTM 19S en zona Ollachea
            var lon = e.latlng.lng;
            var lat = e.latlng.lat;
            var utm_e = 340915.2 + (lon - (-70.471777)) * 108500;
            var utm_n = 8472980.5 + (lat - (-13.808357)) * 110500;
            document.getElementById('coords').innerHTML = 
                "Puntero: Lon: " + lon.toFixed(5) + "° | Lat: " + lat.toFixed(5) + "° | UTM 19S: " + Math.round(utm_e).toLocaleString() + " m E, " + Math.round(utm_n).toLocaleString() + " m N";
        });
    </script>
</body>
</html>
"""

with open(os.path.join(MAPAS_DIR, "Visor_Geodesico_Interactivo_MCH.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

shutil.copy2(os.path.join(MAPAS_DIR, "Visor_Geodesico_Interactivo_MCH.html"),
             os.path.join(ANEXOS_DIR, "Visor_Geodesico_Interactivo_MCH.html"))

print("Visor Web SIG Interactivo generado y sincronizado exitosamente en 04 Mapas y 06 Anexos!")
