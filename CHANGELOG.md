# Changelog

Todas las modificaciones notables realizadas en este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.1] - 2026-10-12

### Corregido (Fixed)
- **Compilación LaTeX de Anexos (`06 Anexos/`):** Corrección de paquetes matemáticos (`amsmath`, `amssymb`) y definición de `\graphicspath{{../04 Mapas/}}` en las láminas de cartografía (`Anexo_A`), geodesia (`Anexo_F`) y desarrollo productivo (`Anexo_G`).

### Añadido (Added)
- **Entregables Finales Compilados en PDF:** Generación y control de versiones para los documentos oficiales de ingeniería:
  - `05 Informe/Informe_Final_MCH_100kW_Puno.pdf` (42 páginas integrando memoria de diseño, fórmulas, tablas, cartografía satelital y planos).
  - `06 Anexos/` (Anexos A, B, C, E, F y G completamente compilados).
- **Filtros de compilación en `.gitignore`:** Exclusión automática de archivos temporales de LaTeX (`.aux`, `.out`, `.toc`, `.lof`, `.lot`, `.fls`, `.log`, etc.).

---

## [2.0.0] - 2026-10-12

### Añadido (Added)
- **Suite de Planos CAD Vectoriales (`planos/dxf/`):** Generación de 8 láminas técnicas editables en formato DXF R2010+ mediante `ezdxf` con capas normalizadas, cotas, tolerancias y cajetín institucional UNAP FIME:
  - `Plano_01_Ubicacion_Red_Geodesica.dxf` (Lámina U-01).
  - `Plano_02_Planta_General_Obras_Hidraulicas.dxf` (Lámina GH-01).
  - `Plano_03_Bocatoma_Tirolesa_Desarenador.dxf` (Lámina CH-01).
  - `Plano_04_Perfil_Longitudinal_Tuberia_Forzada.dxf` (Lámina TF-01).
  - `Plano_05_Casa_Maquinas_Planta_Cortes.dxf` (Lámina CM-01).
  - `Plano_06_Disposicion_Electromecanica_Pelton.dxf` (Lámina EM-01).
  - `Plano_07_Diagrama_Unifilar_Puesta_Tierra.dxf` (Lámina IE-01).
  - `Plano_08_Subestacion_Aerea_Biposte_SAB1.dxf` (Lámina SE-01).
- **Módulo de Renderizado y Previsualización (`src/cad_bridge/`):** Conversión automática de DXF a imágenes de alta definición PNG (`planos/preview/`) integrables en memorias e informes técnicos.
- **Integración de Componentes Paramétricos de CAD Intelligence:**
  - Brida para penstock según ASME B16.5 Clase 150.
  - Eje motriz escalonado para rodete Pelton según ISO 2768-mK / DIN 6885.
  - Bancada estructural según AISC 360.
  - Tablero general de control según IEC 61439.
  - Subestación biposte SAB-1 y armados DGE según CNE y NTP 339.027.
- **Suite de Pruebas Automatizadas de CAD (`tests/test_cad_integration.py`):** Validación de capas, cajetines y exportación completa.
- **Matriz de Trazabilidad Técnica (`MATRIZ_TRAZABILIDAD.md`):** Clasificación de datos en categorías MED, BIB, CAL, HIP y PEN, relacionando requisitos, cálculos y normas peruanas.

### Modificado (Changed)
- **Portabilidad de Scripts Raíz:** Eliminación de rutas fijas de Termux (`/storage/emulated/0/...`) en `actualizar_presupuesto_apu.py`, `generar_cartografia_geodesica.py`, `generar_fichas_y_planos_ingenieria.py`, `generar_visor_web_sig.py` y `generar_word_completo.py`, sustituyéndolas por resolución dinámica multiplataforma (`pathlib.Path`).
- **Orquestador Principal (`src/main.py`):** Integración del pipeline de exportación CAD como paso 7 dentro del flujo de ejecución estándar.
- **Dependencias (`requirements.txt`):** Incorporación formal de `ezdxf`, `openpyxl`, `python-docx`, `pyproj` y `pillow`.
- **Filtros de Versiones (`.gitignore`):** Exclusión de archivos `desktop.ini`, binarios compilados > 50 MB (`Informe_Final...pdf`, `Anexo_A...pdf`) y duplicados en `06 Anexos/`.

### Corregido (Fixed)
- Error de importación de `Any` en `export_pipeline.py`.
- Bloqueo en ejecución de pruebas al estandarizar el comando de ejecución bajo módulo (`python -m pytest tests/`).

---

## [1.0.0] - 2026-09-26

### Añadido (Added)
- Núcleo de cálculo en Python: `hydrology.py`, `hydraulics.py`, `turbines.py`, `electrical.py`, `transient.py`, `economics.py`, `reports.py`.
- Base de datos histórica hidrometeorológica (2014-2023) y coordenadas georreferenciadas.
- Agente normativo determinista `HydroAgent` para legislación RER y ANA.
- Pruebas unitarias iniciales en `tests/test_hydraulics.py`.
- Memoria descriptiva en formato LaTeX y generación de informe en PDF con ReportLab.
