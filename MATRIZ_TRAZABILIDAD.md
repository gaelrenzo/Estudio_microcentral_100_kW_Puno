# MATRIZ DE TRAZABILIDAD TÉCNICA, FUENTES Y NORMATIVA

**Proyecto:** Microcentral Hidroeléctrica Río Blanco de 100 kW  
**Emplazamiento:** Distrito de Ollachea, Provincia de Carabaya, Departamento de Puno, Perú  
**Institución:** Universidad Nacional del Altiplano Puno (UNAP) — Facultad de Ingeniería Mecánica Eléctrica (FIME)  
**Fecha de Emisión:** Octubre 2026  

---

## 1. Clasificación Metodológica de Datos y Parámetros

Para distinguir el origen y el estado de validación, los datos se clasifican en cinco categorías. Esta clasificación no acredita por sí sola que una fuente primaria haya sido verificada:

- **[MED] Dato Medido / Instrumental:** Registro físico verificado en campo o hidrometeorología continua.
- **[BIB] Dato Bibliográfico / Oficial:** Obtenido de instituciones rectoras (ANA, SENAMHI, IGN, MINEM, OSINERGMIN) o normas técnicas vigentes.
- **[CAL] Resultado de Cálculo Verificado:** Obtenido mediante ecuaciones físicas y modelos matemáticos computables reproducibles.
- **[HIP] Hipótesis de Trabajo de Ingeniería:** Asunciones técnicas fundadas pendientes de confirmación en ingeniería de detalle.
- **[PEN] Dato Pendiente de Validación:** Parámetro que requiere campaña geotécnica o topográfica complementaria in situ.

---

## 2. Matriz de Requisitos, Evidencia y Componentes

| Componente | Parámetro Clave | Valor Adoptado | Cat. | Norma / Fuente Oficial | Validación Matemática | Plano / Entregable Asociado |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| **Localización** | Coordenadas Captación | E: 340,915.2 m, N: 8,472,980.5 m (Z: 2420 msnm; coordenada provisional del CSV, no levantamiento verificado) | **[PEN]** | Coordenadas del repositorio; no se adjunta libreta/acta de levantamiento IGN | Contrastar en campo y en cartografía oficial | Plano U-01 |
| **Localización** | Coordenadas Casa Máquinas | E: 341,480.1 m, N: 8,473,650.4 m (Z: 2302.8 msnm; coordenada provisional del CSV, no levantamiento verificado) | **[PEN]** | Coordenadas del repositorio; no se adjunta libreta/acta de levantamiento IGN | Desnivel de 115 m es preliminar, requiere topografía | Plano U-01 / CM-01 |
| **Hidrología** | Serie Diaria Caudales | 3,652 registros (2014-2023) | **[PEN]** | CSV del repositorio; no se adjunta fuente primaria, certificado ni control de calidad verificable | Curva de Duración de Caudales (Weibull) sobre serie provisional | Anexo B / CDC Gráfico |
| **Hidrología** | Caudal Medio | $0.523\text{ m}^3\text{/s}$ | **[CAL]** | Cálculo sobre serie provisional incluida en el repositorio | Promedio aritmético; no valida la procedencia de la serie | `src/hydrology.py` |
| **Hidrología** | Caudal de Diseño ($Q_d$) | $0.125\text{ m}^3\text{/s}$ ($125\text{ L/s}$) | **[CAL]** | Persistencia $Q_{95} = 0.126\text{ m}^3\text{/s} \ge Q_d$ | Selección para operación continua en estiaje | `src/main.py` |
| **Ambiental** | Caudal Ecológico ($Q_{\text{eco}}$) | $0.030\text{ m}^3\text{/s}$ ($30\text{ L/s}$) | **[HIP]** | Supuesto del caso; determinar según R.J. N° 267-2019-ANA y evaluación específica, sin aprobación adjunta | Requiere serie validada, balance mensual y trámite ante ANA | `ai/knowledge/` |
| **Obras Civiles** | Captación | Bocatoma Tirolesa con Azud Ciclópeo | **[CAL]** | Manual de Obras Hidráulicas ANA / MINEM | Azud $f'c = 175\text{ kg/cm}^2$, Rejilla Coanda $\alpha=20^\circ$ | Plano CH-01 |
| **Obras Civiles** | Desarenador | Doble Nave ($L=8.0\text{ m}$, $B=1.8\text{ m}$) | **[CAL]** | Criterio de Camp y sedimentación de Stokes | $V_h = 0.18\text{ m/s} \le 0.20\text{ m/s}$, remoción $d \ge 0.2\text{ mm}$ | Plano CH-01 |
| **Conducción** | Canal de Aducción | Sección rectangular $0.50 \times 0.50\text{ m}$ ($L=450\text{ m}$) | **[CAL]** | Manning ($n=0.014$, $S=0.0015$) | $y_n = 0.3313\text{ m}$, $\text{Fr} = 0.419$ (Régimen Subcrítico) | Plano GH-01 / TF-01 |
| **Cámara de Carga** | Volumen y Sumergencia | $V = 22.5\text{ m}^3$, $h_s = 1.40\text{ m}$ | **[CAL]** | Criterio de Gordon ($h_s \ge c \cdot V \cdot D^{0.5}$) | 3 min de regulación rápida, evita vórtices de aire | Plano TF-01 |
| **Tubería Forzada** | Diámetro y Material | $D = 250\text{ mm}$ ($10''$), Acero ASTM A36 | **[CAL]** | Fórmula Económica de Fahlbusch / Sarkaria | Velocidad $v = 2.546\text{ m/s}$, pérdidas $h_f = 7.67\%$ | Plano TF-01 |
| **Salto y Pérdidas** | Salto Bruto / Salto Neto | $H_b = 115.00\text{ m}$, $H_n = 106.18\text{ m}$ | **[CAL]** | Darcy-Weisbach y Swamee-Jain ($k=0.045\text{ mm}$) | Pérdidas continuas $\Delta h_f = 8.82\text{ m}$ | `src/hydraulics.py` |
| **Transitorios** | Celeridad de Onda | $a = 1,195.8\text{ m/s}$ | **[CAL]** | Fórmula de Allievi / Joukowsky para acero | Celeridad elastoacústica con módulo del acero y agua | `src/transient.py` |
| **Transitorios** | Tiempo de Cierre | $t_c = 4.00\text{ s}$ | **[HIP]** | Servomotor hidráulico y deflector de chorro | Cierre Lento ($t_c > 2L/a = 0.635\text{ s}$) | `src/transient.py` |
| **Transitorios** | Sobrepresión Ariete | $\Delta H = +49.31\text{ m}$ ($H_{\max} = 164.31\text{ m}$) | **[CAL]** | Ecuación de Cierre Lento de Allievi | Presión máxima dinámica: $16.1\text{ bar}$ | Plano TF-01 |
| **Calderería** | Espesor de Tubería | $e_{\text{com}} = 4.75\text{ mm}$ y $6.35\text{ mm}$ | **[CAL]** | ASME B31.3 / Barlow ($\sigma_{\text{adm}} = 125\text{ MPa}$) | Espesor mínimo $e_{\text{req}} = 3.11\text{ mm}$ (Factor Seg. 2.0) | Plano TF-01 |
| **Turbina** | Tipo y Configuración | Pelton Eje Horizontal, 2 Inyectores | **[CAL]** | Diagrama de Selección Siervo & Pavesi | $N_s = 12.8\text{ rpm}$, $N = 1200\text{ RPM}$ ($60\text{ Hz}$) | Plano EM-01 |
| **Rodete Pelton** | Dimensiones y Cucharas | $D_1 = 324.1\text{ mm}$, 19 Cucharas | **[CAL]** | Relación empírica $z = 0.5 \cdot (D_1/d_0) + 15$ | Acero fundido ASTM A743 CA6NM | Plano EM-01 |
| **Generador** | Potencia y Tensión | $125\text{ kVA}$, $400/230\text{ V}$, $60\text{ Hz}$, $1200\text{ RPM}$ | **[HIP]** | Equipo de referencia; no se adjunta ficha de fabricante seleccionada | A $\cos\phi=0.8$, potencia activa nominal = $100\text{ kW}$; cálculo preliminar de turbina ($104.43\text{ kW}$) excede ese valor | Plano IE-01 |
| **Regulación** | Sistema de Control | ELC (Electronic Load Controller) $120\text{ kW}$ | **[BIB]** | Norma IEC 60034 / Guías NRECA RER | Banco de resistencias ballast de disipación PWM | Plano IE-01 |
| **Subestación** | Subestación Aérea | Alternativa conceptual: transformador $125\text{ kVA}$, $0.4/10\text{ kV}$; validar tensión, equipo y conexión con distribuidora | **[BIB]** | Bases DGE (R.D. 018-2003-EM/DGE) | Biposte C.A.C. 13/400 (NTP 339.027) | Plano SE-01 |
| **Puesta a Tierra** | Malla Equipotencial | Cable Cu $50\text{ mm}^2$ con electrodos $5/8''$ | **[CAL]** | IEEE Std 80 / CNE Suministro | Resistencia de dispersión $R_{\text{pat}} \le 10\ \Omega$ | Plano IE-01 |
| **Economía** | Inversión (CAPEX) | $\$245,800.00\text{ USD}$ | **[HIP]** | Estimación referencial del Anexo D; cotizaciones y alcance no acreditados | Requiere cotizaciones, contingencias y validación de costos de conexión | Anexo D / Excel |
| **Evaluación** | Indicadores Financieros | $\text{VAN} = \$274,742\text{ USD}$, $\text{TIR} = 23.20\%$ | **[CAL]** | Escenario reproducible: 25 años, descuento 10%; CAPEX, tarifa, OPEX y energía no validados | Payback: $4.29$ años; LCOE: $39.90 USD/MWh; B/C: 1.88 | `src/economics.py` |
| **Marco Legal** | Concesiones Eléctricas | Umbral de concesión definitiva | **[BIB]** | D.L. 25844 y modificatorias | El encuadre a 100 kW no elimina otros permisos, requisitos sectoriales ni derechos de agua; confirmar con la autoridad competente | `ai/knowledge/` |
| **Geotecnia** | Capacidad Portante Suelo | $\sigma_{\text{adm}} = 2.0\text{ kg/cm}^2$ en ladera | **[HIP]** | Formación geológica Sandía (pizarras y lutitas) | Pendiente de estudio de mecánica de suelos con calicatas | Plano TF-01 / CM-01 |

---

## 3. Repositorio de Fuentes Bibliográficas y Enlaces Oficiales

Los archivos listados a continuación son referencias bibliográficas declaradas por el proyecto. Su presencia no demuestra que los datos de entrada provengan de ellos; validar título, autoría, edición y correspondencia antes de usarlos como evidencia.

1. **Autoridad Nacional del Agua (ANA) — AAA XIV Titicaca:**
   - *Título:* Estudio Hidrológico de la Cuenca Inambari y Subcuenca San Gabán.
   - *Entidad:* Ministerio de Desarrollo Agrario y Riego (MIDAGRI) / ANA.
   - *Año:* 2021.
   - *Afirmación respaldada:* Series de caudales y delimitación fisiográfica de la cuenca del Río Blanco.
2. **Servicio Nacional de Meteorología e Hidrología (SENAMHI):**
   - *Título:* Caracterización Climática y Pluviométrica del Departamento de Puno.
   - *Entidad:* SENAMHI - Dirección Zonal 13 Puno.
   - *Año:* 2022.
   - *Afirmación respaldada:* Series de precipitación mensual 1994-2023 de la estación Ollachea (Código 112108).
3. **Ministerio de Energía y Minas (MINEM) — DGE:**
   - *Título:* Bases para el Diseño de Líneas y Redes Primarias para Electrificación Rural (R.D. N° 018-2003-EM/DGE) y Norma Técnica de Pequeñas Centrales Hidroeléctricas.
   - *Entidad:* Dirección General de Electricidad (MINEM).
   - *Afirmación respaldada:* El tipo de estructura, tensión, trazado y servidumbres requieren diseño y confirmación de la distribuidora.
4. **Organismo Supervisor de la Inversión en Energía y Minería (OSINERGMIN):**
   - *Título:* Guía Técnica de Generación Distribuida y Recursos Energéticos Renovables (RER).
   - *Entidad:* División de Generación y Transmisión Eléctrica.
   - *Año:* 2020.
   - *Afirmación respaldada:* Procedimientos de interconexión en MT y parámetros tarifarios RER.
5. **Instituto Geográfico Nacional (IGN):**
   - *Título:* Especificaciones Técnicas para Posicionamiento Geodésico Estático - Red Geodésica Geocéntrica Nacional (REGGEN).
   - *Entidad:* IGN Perú.
   - *Año:* 2020.
   - *Afirmación respaldada:* Monumentación y factores de escala en hitos HG-01, HG-02 y HG-03 (Orden C).
6. **Universidad Nacional del Altiplano Puno (UNAP) — FIME:**
   - *Título:* Tesis de Pregrado: Diseño y Prefactibilidad Técnica de Microcentrales Hidroeléctricas en Zonas Aisladas de Carabaya.
   - *Entidad:* FIME UNAP.
   - *Año:* 2023.
   - *Afirmación respaldada:* Coeficientes de rugosidad en canales locales y costos referenciales de mano de obra en Puno.
