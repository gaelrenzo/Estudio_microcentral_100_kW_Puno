# MATRIZ DE TRAZABILIDAD TÉCNICA, FUENTES Y NORMATIVA

**Proyecto:** Microcentral Hidroeléctrica Río Blanco de 100 kW  
**Emplazamiento:** Distrito de Ollachea, Provincia de Carabaya, Departamento de Puno, Perú  
**Institución:** Universidad Nacional del Altiplano Puno (UNAP) — Facultad de Ingeniería Mecánica Eléctrica (FIME)  
**Fecha de Emisión:** Octubre 2026  

---

## 1. Clasificación Metodológica de Datos y Parámetros

Para garantizar la honestidad técnica y académica ante jurados y comités revisores, todos los datos del proyecto se clasifican en cinco categorías epistemológicas:

- **[MED] Dato Medido / Instrumental:** Registro físico verificado en campo o hidrometeorología continua.
- **[BIB] Dato Bibliográfico / Oficial:** Obtenido de instituciones rectoras (ANA, SENAMHI, IGN, MINEM, OSINERGMIN) o normas técnicas vigentes.
- **[CAL] Resultado de Cálculo Verificado:** Obtenido mediante ecuaciones físicas y modelos matemáticos computables reproducibles.
- **[HIP] Hipótesis de Trabajo de Ingeniería:** Asunciones técnicas fundadas pendientes de confirmación en ingeniería de detalle.
- **[PEN] Dato Pendiente de Validación:** Parámetro que requiere campaña geotécnica o topográfica complementaria in situ.

---

## 2. Matriz de Requisitos, Evidencia y Componentes

| Componente | Parámetro Clave | Valor Adoptado | Cat. | Norma / Fuente Oficial | Validación Matemática | Plano / Entregable Asociado |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| **Localización** | Coordenadas Captación | E: 340,820.5 m, N: 8,472,950.2 m (Z: 2420 msnm) | **[BIB]** | IGN - REGGEN Orden C (WGS-84 UTM Zona 19S) | Verificación cartográfica y satelital ALOS PALSAR | Plano U-01 |
| **Localización** | Coordenadas Casa Máquinas | E: 341,480.1 m, N: 8,473,650.4 m (Z: 2305 msnm) | **[BIB]** | IGN - REGGEN Orden C (Hito HG-03) | Desnivel topográfico H = 115.00 m | Plano U-01 / CM-01 |
| **Hidrología** | Serie Diaria Caudales | 3,652 registros (2014-2023) | **[MED]** | ANA - AAA XIV Titicaca / SENAMHI Estación Ollachea | Curva de Duración de Caudales (Fórmula Weibull) | Anexo B / CDC Gráfico |
| **Hidrología** | Caudal Medio | $0.523\text{ m}^3\text{/s}$ | **[CAL]** | Serie histórica 10 años | Promedio aritmético e integración de persistencia | `src/hydrology.py` |
| **Hidrología** | Caudal de Diseño ($Q_d$) | $0.125\text{ m}^3\text{/s}$ ($125\text{ L/s}$) | **[CAL]** | Persistencia $Q_{95} = 0.126\text{ m}^3\text{/s} \ge Q_d$ | Selección para operación continua en estiaje | `src/main.py` |
| **Ambiental** | Caudal Ecológico ($Q_{\text{eco}}$) | $0.030\text{ m}^3\text{/s}$ ($30\text{ L/s}$) | **[BIB]** | Ley N° 29338 (Recursos Hídricos) y Guía RER | Preservación del 10% del caudal medio o $Q_{95}$ estiaje | `ai/knowledge/normativa_peruana.md` |
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
| **Generador** | Potencia y Tensión | $125\text{ kVA}$, $380\text{ V}$, $60\text{ Hz}$, $1200\text{ RPM}$ | **[BIB]** | Catálogo WEG / Leroy-Somer / CNE Suministro | Potencia neta a red: $104.43\text{ kW}$ ($\cos\phi=0.8$) | Plano IE-01 |
| **Regulación** | Sistema de Control | ELC (Electronic Load Controller) $120\text{ kW}$ | **[BIB]** | Norma IEC 60034 / Guías NRECA RER | Banco de resistencias ballast de disipación PWM | Plano IE-01 |
| **Subestación** | Subestación Aérea | Tipo SAB-1 $100\text{ kVA}$, $0.38/22.9\text{ kV}$ Dyn5 | **[BIB]** | Bases DGE (R.D. 018-2003-EM/DGE) | Biposte C.A.C. 13/400 (NTP 339.027) | Plano SE-01 |
| **Puesta a Tierra** | Malla Equipotencial | Cable Cu $50\text{ mm}^2$ con electrodos $5/8''$ | **[CAL]** | IEEE Std 80 / CNE Suministro | Resistencia de dispersión $R_{\text{pat}} \le 10\ \Omega$ | Plano IE-01 |
| **Economía** | Inversión (CAPEX) | $\$245,800.00\text{ USD}$ | **[BIB]** | Análisis de Precios Unitarios (APU) 2026 | $\$2,458\text{ USD/kW}$ (Consistente para microcentrales) | Anexo D / Excel |
| **Evaluación** | Indicadores Financieros | $\text{VAN} = \$145,271\text{ USD}$, $\text{TIR} = 17.20\%$ | **[CAL]** | Flujos de caja a 25 años ($10\%$ descuento) | Payback: $5.71\text{ años}$, LCOE: $\$51.20\text{ USD/MWh}$ | `src/economics.py` |
| **Marco Legal** | Concesiones Eléctricas | Exoneración concesión definitiva | **[BIB]** | D.L. 25844 (Ley de Concesiones Eléctricas) | Aplicable a centrales $\le 500\text{ kW}$ (Autorización DGE) | `ai/knowledge/` |
| **Geotecnia** | Capacidad Portante Suelo | $\sigma_{\text{adm}} = 2.0\text{ kg/cm}^2$ en ladera | **[HIP]** | Formación geológica Sandía (pizarras y lutitas) | Pendiente de estudio de mecánica de suelos con calicatas | Plano TF-01 / CM-01 |

---

## 3. Repositorio de Fuentes Bibliográficas y Enlaces Oficiales

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
   - *Afirmación respaldada:* Armados normalizados SAB-1, niveles de tensión 22.9 kV, postes C.A.C. y servidumbres.
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
