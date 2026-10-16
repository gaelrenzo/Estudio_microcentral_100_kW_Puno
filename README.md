# Hydro AI Engineering ⚡🌊

**Herramientas y estudio de prefactibilidad de una microcentral hidroeléctrica de 100 kW**

> Proyecto aplicado al caso de estudio: **Microcentral Hidroeléctrica Río Blanco de 100 kW**  
> Emplazamiento: **Distrito de Ollachea, Provincia de Carabaya, Departamento de Puno, Perú**  
> Entidad Académica: **Universidad Nacional del Altiplano Puno (UNAP) — FIME**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-passing-brightgreen.svg)]()
[![CAD-as-Code](https://img.shields.io/badge/CAD-ezdxf%20%7C%20DXF%20R2010+-orange.svg)]()
[![Normativa](https://img.shields.io/badge/normativa-D.L.%201002%20%7C%20ANA%2029338%20%7C%20CNE-red.svg)]()

---

## 📋 Descripción General

`Hydro AI Engineering` reúne cálculos preliminares, documentos y herramientas para evaluar una microcentral hidroeléctrica de 100 kW en etapa de prefactibilidad. Los resultados son referenciales y requieren validación de datos, estudios de campo, cotizaciones y permisos antes de usarse para inversión, construcción o trámite.

> **Alcance:** este repositorio no constituye un expediente definitivo ni acredita mediciones de campo, disponibilidad hídrica, licencia de agua, viabilidad ambiental, conexión eléctrica, costos cotizados o rentabilidad bancaria. Consulta [ESTADO_PREFACTIBILIDAD.md](ESTADO_PREFACTIBILIDAD.md) para las discrepancias y validaciones pendientes.

El repositorio contiene módulos y documentos conceptuales; sus salidas deben tratarse como escenarios de prefactibilidad, no como verificaciones de campo:
1. **Análisis Hidrológico:** Curva de Duración de Caudales (CDC) con distribución de Weibull sobre series diarias (2014-2023), determinando persistencia $Q_{95} = 0.126\text{ m}^3\text{/s}$ y preservación de caudal ecológico ($Q_{\text{eco}} = 30\text{ L/s}$).
2. **Dimensionamiento Hidráulico y Civil:** Canal de aducción rectangular ($L=450\text{ m}$) mediante Manning por Newton-Raphson, cámara de carga con criterio de sumergencia de Gordon, y tubería forzada de acero ASTM A36 ($D=250\text{ mm}$, $L=380\text{ m}$) según Fahlbusch y Darcy-Weisbach / Swamee-Jain.
3. **Selección y Modelado de Turbina:** Turbina Pelton de eje horizontal con 2 inyectores simétricos ($N_s = 12.8\text{ rpm}$, $1200\text{ RPM}$, $D_1 = 324.1\text{ mm}$, 19 cucharas en acero inoxidable ASTM A743 CA6NM).
4. **Transitorios Hidráulicos (Golpe de Ariete):** Simulación elastoacústica según ecuaciones de Allievi y Joukowsky ($a = 1,195.8\text{ m/s}$), maniobra de cierre lento en $4.0\text{ s}$ ($\Delta H = +49.31\text{ m}$, $P_{\max} = 16.1\text{ bar}$) y verificación estructural de espesor de calderería.
5. **Ingeniería Eléctrica y Subestación:** Alternativa de escenario: generador 125 kVA, 400/230 V, y transformador 125 kVA, 0.4/10 kV; seleccionar equipos, tensión, protecciones y conexión con estudios y aprobación de distribuidora.
6. **CAD Paramétrico y Generación de Planos Vectoriales:** Motor autónomo en `ezdxf` que genera los **8 láminas conceptuales DXF editables** con cajetín institucional UNAP FIME, cotas normalizadas y vistas de revisión en alta resolución.
7. **Evaluación Financiera a 25 Años:** Modelo de flujos descontados para un escenario con entradas supuestas; revisar la tabla reproducible y sus limitaciones.
8. **Agente Normativo Peruano (`HydroAgent`):** Módulo experto determinista que audita el marco del D.L. 1002 (RER), Ley 29338 (ANA), D.L. 25844 y CNE Suministro.

---

## 📊 Síntesis del escenario computacional preliminar

| Parámetro | Valor de Diseño | Unidad | Estado / Justificación |
| :--- | :---: | :---: | :--- |
| **Caudal de Diseño Nominal ($Q_d$)** | `125` | L/s | Comparación aritmética con la serie incluida, de origen no acreditado; no demuestra disponibilidad |
| **Caudal ecológico del escenario** | `30` | L/s | Supuesto de cálculo; requiere determinación y aprobación aplicables |
| **Salto Bruto ($H_b$) / Salto Neto ($H_n$)** | `115.00` / `106.18` | m | Salida del modelo con geometría provisional, pendiente de levantamiento |
| **Tubería Forzada (Penstock)** | `250` (10") | mm | Acero ASTM A36 ($e = 4.75\text{ mm}$ y $6.35\text{ mm}$, $v = 2.55\text{ m/s}$) |
| **Sobrepresión por Ariete ($\Delta H$)** | `+49.31` | m | Maniobra de cierre lento Allievi ($t_c = 4.0\text{ s} > 2L/a = 0.635\text{ s}$) |
| **Presión Máxima Total ($H_{\max}$)** | `164.31` (16.1) | m (bar) | Estimación analítica preliminar; no constituye verificación estructural |
| **Tecnología de Turbina** | **Pelton** | — | 2 Inyectores, $N = 1200\text{ RPM}$, $N_s = 12.8\text{ rpm}$ |
| **Rodete Pelton** | `324.1` | mm | Diámetro primitivo $D_1$, 19 cucharas ASTM A743 CA6NM |
| **Potencia calculada del conjunto** | `104.43` | kW | Resultado preliminar del modelo; el generador de $125\text{ kVA}$ a $\cos\phi=0.8$ limita la salida activa nominal a $100\text{ kW}$ |
| **Energía modelada** | `862.92` | MWh/año | Salida del modelo con serie provisional; no es energía acreditada ni P50/P90 |
| **Inversión de Capital (CAPEX)** | `$245,800.00` | USD | Estimación sin cotizaciones verificables; falta revisar metrados, transporte y conexión |
| **VAN (10%)** | `$274,741.65` | USD | Caso económico modelado; depende de insumos no cotizados ni validados |
| **TIR** | `23.20` | % | Indicador de escenario; no implica decisión de inversión |
| **Payback simple** | `4.29` | años | Estimación del escenario, antes de impuestos y financiamiento |
| **LCOE** | `39.90` | USD/MWh | Resultado preliminar dependiente de CAPEX, energía y tasa asumidos |

---

## 📐 Suite de Planos de Ingeniería CAD (Norma NTP / ISO)

Los planos editables en formato vectorial **AutoCAD R2010+ (`.dxf`)** se localizan en [`planos/dxf/`](planos/dxf/) y sus vistas previas en [`planos/preview/`](planos/preview/):

1. **Lámina U-01:** Plano de Ubicación, Emplazamiento General y Red Geodésica REGGEN (Hitos HG-01, HG-02, HG-03).
2. **Lámina GH-01:** Planta General y Esquema Integral de Obras Hidráulicas (Progresivas $0+000$ a $0+855$).
3. **Lámina CH-01:** Captación y Desarenador: Bocatoma Tirolesa con Rejilla Coanda y Desarenador de Doble Nave.
4. **Lámina TF-01:** Perfil Longitudinal: Conducción, Tubería Forzada, Bloques de Anclaje y Envolvente de Ariete.
5. **Lámina CM-01:** Casa de Máquinas: Planta Arquitectónica, Cortes Estructurales y Fosa de Turbina.
6. **Lámina EM-01:** Disposición Electromecánica: Grupo Turbina Pelton de 2 Inyectores y Generador Síncrono.
7. **Lámina IE-01:** Diagrama Unifilar General, Tableros de Control ELC y Malla de Puesta a Tierra (IEEE Std 80).
8. **Lámina SE-01:** Subestación conceptual; tensión, transformador y armados deben verificarse antes de uso externo.

---

## 🚀 Reproducción limitada a prefactibilidad

### 1. Clonar el repositorio
```bash
git clone https://github.com/gaelrenzo/Estudio_microcentral_100_kW_Puno.git
cd Estudio_microcentral_100_kW_Puno
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv

# En Windows:
.\venv\Scripts\activate

# En Linux / macOS:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

El paquete de entrega incluye `07 Entrega para Ingeniero/reproducir_prefactibilidad.py`, que reproduce solo los cálculos hidrológicos, hidráulicos, energéticos y económicos. No ejecute el orquestador integral para esta revisión: genera planos y otros productos que exceden el alcance solicitado.

### 5. Ejecutar la suite de pruebas unitarias
```bash
python -m pytest tests/ -v
```

---

## 📁 Estructura del Repositorio

```text
Estudio_microcentral_100_kW_Puno/
├── README.md                                          # Memoria general e instrucciones de reproducción
├── CHANGELOG.md                                       # Registro de versiones y cambios (Keep a Changelog)
├── MATRIZ_TRAZABILIDAD.md                             # Trazabilidad de datos, fórmulas, normas y planos
├── requirements.txt                                   # Dependencias fijadas del ecosistema Python
├── .gitignore                                         # Filtros de control de versiones y seguridad
├── data/                                              # Series hidrológicas diarias y georreferenciación
│   ├── series_caudales_diarios_historicos_2014_2023.csv
│   ├── series_precipitacion_mensual_senamhi_1994_2023.csv
│   └── coordenadas_infraestructura_mch.geojson
├── src/                                               # Módulos del núcleo de cálculo de ingeniería
│   ├── __init__.py
│   ├── hydrology.py                                   # Curva CDC, persistencia y Weibull
│   ├── hydraulics.py                                  # Manning, Fahlbusch, Darcy-Weisbach y Pelton
│   ├── turbines.py                                    # Selección técnica, velocidad específica y torque
│   ├── electrical.py                                  # Transformador, factor de planta y balance
│   ├── transient.py                                   # Celeridad, Allievi, sobrepresión y espesor
│   ├── economics.py                                   # VAN, TIR, Payback, LCOE y flujo de caja
│   ├── reports.py                                     # Compilación de informe formal en PDF
│   ├── cad_bridge/                                    # Generadores de planos CAD vectoriales (.dxf)
│   │   ├── __init__.py
│   │   ├── title_block.py                             # Marco A1 y cajetín institucional UNAP FIME
│   │   ├── hydraulic_drawings.py                      # Láminas U-01, GH-01, CH-01, TF-01, CM-01
│   │   ├── electromechanical_drawings.py              # Láminas EM-01, IE-01, SE-01
│   │   └── export_pipeline.py                         # Orquestador y renderizador DXF a PNG
│   └── main.py                                        # Orquestador del flujo integral de ingeniería
├── planos/                                            # Entregables técnicos de dibujo de ingeniería
│   ├── dxf/                                           # 8 Archivos CAD vectoriales editables (AutoCAD R2010+)
│   └── preview/                                       # 8 Vistas previas en alta resolución (PNG)
├── ai/                                                # Asesoría normativa y base experta
│   ├── agent.py                                       # Agente HydroAgent
│   └── knowledge/
│       └── normativa_peruana.md                       # Compendio legal D.L. 1002, Ley 29338 y CNE
├── tests/                                             # Pruebas unitarias automatizadas (pytest)
│   ├── test_hydraulics.py                             # Verificación de ecuaciones hidráulicas y físicas
│   └── test_cad_integration.py                       # Verificación de capas, cajetines y planos DXF
└── .github/
    └── workflows/
        └── analysis.yml                               # Pipeline de Integración Continua (CI) en GitHub
```

---

## ⚖️ Marco Regulatorio y Legal Peruano

- **Decreto Legislativo N° 1002 (Promoción de la Inversión en RER):** Régimen prioritario para centrales hidroeléctricas con potencia $\le 20\text{ MW}$.
- **Decreto Ley N° 25844 (Ley de Concesiones Eléctricas) y modificatorias:** El umbral de concesión definitiva no elimina otros requisitos sectoriales, ambientales, de agua ni de interconexión; confirmar el encuadre del proyecto con las autoridades competentes.
- **Ley N° 29338 (Ley de Recursos Hídricos):** El uso de agua requiere el derecho correspondiente; el caudal ecológico debe determinarse conforme a los lineamientos vigentes de ANA y no se presume aprobado.
- **Código Nacional de Electricidad (CNE Suministro 2011):** Criterios de seguridad en Media Tensión, distancias de seguridad y puesta a tierra.
- **R.D. N° 018-2003-EM/DGE:** Bases para el Diseño de Líneas y Redes Primarias para Electrificación Rural.

---

## 📜 Licencia y Autoría

Desarrollado bajo estándares rigurosos de ingeniería electromecánica e hidráulica para la **Universidad Nacional del Altiplano Puno (UNAP)**, Facultad de Ingeniería Mecánica Eléctrica.
