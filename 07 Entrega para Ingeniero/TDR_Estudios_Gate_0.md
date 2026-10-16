# Términos de referencia para cotización — Gate 0 y estudios opcionales

**Proyecto:** Microcentral Hidroeléctrica Río Blanco, 100 kW — Ollachea, Puno<br>
**Versión:** base de solicitud de cotización, 16 de octubre de 2026<br>
**Estado:** prefactibilidad; emplazamientos y trazados conceptuales, sin replanteo de campo.

## 1. Objeto y reglas de cotización

Solicitar propuestas comparables para reducir primero la incertidumbre de sitio y decidir si se financian los estudios de factibilidad. El paquete de **Gate 0 debe cotizarse separado** de las campañas completas que se indican como opciones: un ciclo hidrológico de 12 meses y una exploración geotécnica extensa pueden exceder el tope preliminar de USD 10,000–25,000.

Cada postor presentará precio por lote y por etapa, impuestos, viáticos, movilización, plazo, supuestos, exclusiones, vigencia de la oferta, forma de pago, perfiles del equipo y disponibilidad. Identificará cantidades unitarias y precios por ampliación. La cotización solo será vinculante bajo los términos aceptados en una orden/contrato firmado; este TDR no constituye adjudicación.

### Paquetes a cotizar

| Código | Incluido en Gate 0 | Opción ampliada, activar solo con aprobación escrita |
|---|---|---|
| A — Topografía/geodesia | Revisión de cartografía, reconocimiento, control de campo y levantamiento de decisión dentro de un polígono base de hasta 8 ha. | Ampliación de área/eje, vuelos/ortofoto y puntos geodésicos formalmente certificados si la entidad competente lo requiere. |
| B — Hidrología/hidrometría | Auditoría de fuentes y serie; reconocimiento; instalación/lectura inicial de regla y sensor si se aprueba; 2–4 aforos iniciales y diagnóstico de brechas. | Operación por 12 meses, 15–20 aforos y estudio de disponibilidad hídrica completo para expediente ANA. |
| C — Geotecnia | Revisión geológica, reconocimiento y propuesta de ubicación/accesos; exploraciones mínimas solo si el titular aprueba presupuesto y seguridad. | Programa indicativo de 14 calicatas y 3 perforaciones; ensayos y recomendaciones de factibilidad. |

El titular entregará a los postores el archivo de coordenadas conceptuales y el trazado disponible. El postor no lo tratará como levantamiento, límite de predio ni autorización de ingreso. Antes de iniciar, las partes aprobarán el polígono, permisos de acceso, seguridad, plan de trabajo y cantidades. No se permite abrir calicatas ni ingresar a predios/comunidad sin autorización.

## 2. Lote A — Levantamiento topográfico y geodésico

### 2.1 Alcance base

- Levantar hasta **8 ha como cantidad de cotización**, no como metrado definitivo. Antes de movilizar, cerrar el polígono en GIS/CAD y dejar el área medida en acta; liquidar ampliaciones por hectárea y por metro de eje según precios unitarios ofertados.
- Cubrir bocatoma, desarenador, canal conceptual de aproximadamente 450 m, cámara de carga, eje conceptual de tubería de aproximadamente 380–425 m, casa de máquinas, restitución y accesos inmediatos. Incluir franja de hasta 25 m a cada lado de los ejes como base, ensanchando en estructuras, curvas, cruces, taludes y variantes acordadas.
- Ejecutar control horizontal con GNSS y detalle con estación total/nivelación donde la cobertura RTK, el relieve o la precisión vertical lo requieran. Establecer al menos dos puntos monumentados de control fuera de zonas inundables y amarrar las cotas hidráulicas a una referencia vertical declarada.
- La oferta incluirá como partida base la metodología compatible con la especificación IGN vigente para puntos de orden C, cuando resulte aplicable. Cotizar por separado tasas, revisión o certificación formal por IGN. El postor señalará si puede tramitarla y qué evidencia oficial entregará; no rotulará un punto como “certificado IGN” sin constancia.
- Entregar secciones en captación y restitución, cubriendo cauce y márgenes relevantes; perfiles longitudinales del canal/tubería y terreno; puntos de lámina de agua observados durante la visita, identificados como lecturas puntuales y con hora/condición.

### 2.2 Sistema de referencia y precisión

La propuesta identificará CRS horizontal con código EPSG, datum/realización y época cuando corresponda, zona UTM comprobada, unidades, sistema vertical y método de enlace. No aceptar solamente el texto “Datum IGN” o `Datum_Vertical=IGN_PERU`: indicar BM de origen o modelo geoidal, separación geoidal, metodología y precisión estimada. El eje del proyecto se encuentra en prefactibilidad; confirmar zona UTM con coordenadas y ubicación real antes del levantamiento.

Objetivos de representación: planos 1:200 en las huellas de las obras críticas y 1:500 para corredores y estructuras restantes, o escalas justificadas por el relieve y densidad de puntos. El postor declarará tolerancias horizontal/vertical, cierres, control independiente y método de comprobación; las tolerancias deben ser compatibles con la finalidad y especificación IGN vigente, no prometerlas sin cálculo.

### 2.3 Entregables y aceptación

1. Plan de trabajo, polígono aprobado, CRS y referencias, cronograma, permisos y matriz de riesgos de campo.
2. CSV de puntos con `ID,Punto,Este_m,Norte_m,Cota_m,Tipo_Cota,Incertidumbre_m,Progresiva_m,Descripcion`; incluir datos de campaña en cabecera o archivo de metadatos. Diferenciar terreno, solera, nivel de agua, eje de tubería y eje de turbina.
3. Archivos crudos GNSS/RINEX, estación total y nivelación; bitácoras, calibración/verificación, cierres y ajuste de red.
4. Planos PDF y DWG/DXF, perfiles, secciones, superficie TIN/DEM, puntos XYZ codificados y archivos GIS GeoPackage/SHP.
5. Informe de control de calidad, limitaciones, áreas efectivamente cubiertas, puntos inaccesibles y lista de discrepancias con el trazado conceptual.

Se aceptará tras revisar sistema de referencia, consistencia de archivos, cierre/precisiones declaradas, presencia de controles, perfiles y secciones completos y correspondencia entre entregables. La aprobación no certifica límites de propiedad ni reemplaza trámites de servidumbre.

## 3. Lote B — Estudio hidrológico e hidrométrico

### 3.1 Gate 0

- Inventariar origen, unidades, periodo, estación, resolución y vacíos de las series 2014–2023 y de las estaciones cercanas SENAMHI/ANA disponibles. Distinguir valores observados, derivados y sintéticos; no completar ni corregir silenciosamente.
- Revisar consistencia temporal, cambios de estación/régimen, atípicos y doble masa con estaciones comparables cuando existan. Entregar datos originales intactos, copia procesada y bitácora de decisiones.
- Reconocer la sección de captación, describir controles hidráulicos, accesibilidad y seguridad; recomendar emplazamiento de regla limnimétrica y sensor con referencia a BM.
- Cotizar instalación, lectura inicial y **2–4 aforos de reconocimiento** como base opcional de Gate 0. El número y temporada se acordarán según fecha de adjudicación; un aforo puntual no establece curva de gasto ni caudal firme.

### 3.2 Opción de campaña ampliada

- Instalar regla y registrador de nivel, con intervalo objetivo de 15 minutos, referencia a BM, reloj verificado, mantenimiento, respaldo y protocolo ante pérdida de datos.
- Operar durante **12 meses continuos** que cubran un ciclo hidrológico completo. Programar 15–20 aforos velocidad-área repartidos entre estiaje, transición y época húmeda; agregar aforos si hay cambios de control o niveles fuera del rango calibrado. No exponer personal durante avenidas peligrosas.
- En cada aforo registrar fecha/hora, nivel simultáneo, ancho/profundidad por subsección, velocidades, instrumento y calibración, método, incertidumbre, geometría, fotografías y condiciones del cauce. Entregar hojas crudas y cálculo reproducible.
- Ajustar curva de gasto `Q(h)` por tramos cuando haya cambio de control, residuos e incertidumbre; señalar rango medido y límites de extrapolación. Desarrollar curva de duración, balance de caudales ecológicos/usos y escenarios de caudal turbinable.
- Para crecidas, comparar análisis de frecuencia con regionalización y modelación lluvia-escorrentía cuando los datos permitan; presentar supuestos e incertidumbre para Tr=50 y 100 años. No inferir estos caudales de una campaña de 12 meses por sí sola.
- Para trámite, elaborar el estudio/memoria según formato y requisitos vigentes de ANA y responder observaciones dentro del alcance contratado. La acreditación de disponibilidad no autoriza por sí misma el uso del agua ni la ejecución de obras.

### 3.3 Entregables y aceptación

Datos crudos y procesados, metadatos de estaciones, bitácora de calidad, planillas de aforo, curva de gasto, curva de duración, balance hídrico mensual, análisis de crecidas, memoria de disponibilidad, informe de incertidumbre y archivos de cálculo abiertos. Identificar por separado evidencia de campo y fuentes secundarias. La aceptación requiere trazabilidad de cada caudal y que no se presente la serie conceptual como observación oficial.

## 4. Lote C — Exploración geotécnica

### 4.1 Gate 0

Revisar cartografía geológica disponible, accesos, geomorfología y peligros visibles; recorrer, fotografiar y georreferenciar las cuatro áreas de obra y el corredor accesible; emitir programa de investigación y costo por unidad. Las excavaciones de reconocimiento quedan condicionadas a autorización predial, evaluación de seguridad y aprobación del titular.

### 4.2 Opción de investigación ampliada para cotizar

Cotizar como cantidades iniciales separadas:

| Investigación | Cantidad base de opción | Distribución indicativa |
|---|---:|---|
| Calicatas | 14, hasta 3 m o rechazo/agua/roca, lo que ocurra primero | Captación/barraje 3; desarenador 2; cámara de carga 2; casa de máquinas 3; anclajes/cambios de terreno en tubería 4. |
| Perforaciones | 3, hasta 8 m iniciales o profundidad de influencia/estrato competente | Una en captación, una en cámara de carga y una en casa de máquinas; ajustar ubicación con el especialista y estructuras reales. |

El geotecnista justificará si esas cantidades bastan y propondrá ampliaciones como precios unitarios. En depósitos de bolones, roca o rechazo de SPT, indicar método alternativo (perforación, testigo, penetración u otro aplicable); un rechazo no se reportará como valor de resistencia. En cauce activo o excavación inestable, prohibir ingreso y sustituir exploración insegura por método aprobado.

Realizar registro estratigráfico, nivel freático y muestreo representativo. Cotizar ensayos de humedad, granulometría, límites de Atterberg cuando apliquen, densidad, corte directo o triaxial según suelo, permeabilidad y química de suelo/agua (pH, sulfatos, cloruros y sales relevantes). Ensayos de roca solo cuando se encuentre roca. SPT según procedimiento aplicable donde el material lo permita.

### 4.3 Entregables y aceptación

Planos de ubicación y coordenadas, registros de calicatas/perforaciones, fotografías, cadena de custodia, certificados de laboratorio, perfiles estratigráficos, nivel freático observado, parámetros y correlaciones utilizadas, capacidad admisible con hipótesis y asentamientos, estabilidad local, excavabilidad, drenaje y recomendaciones de fundación/durabilidad. El informe diferenciará resultados medidos de correlaciones. No se aceptará una capacidad portante aislada sin indicar geometría, profundidad, cargas asumidas, nivel freático y criterio de seguridad.

## 5. Formato económico mínimo de propuesta

Cada postor llenará una tabla por lote indicando moneda, IGV, tiempo, precios unitarios y vigencia. Presentar los alcances Gate 0 y ampliados en líneas distintas.

| Partida | Unidad | Cantidad base | Precio unitario | Subtotal | Plazo | Supuestos/exclusiones |
|---|---|---:|---:|---:|---|---|
| Revisión/plan de trabajo y movilización | suma alzada | 1 | | | | |
| Levantamiento topográfico | ha | hasta 8 | | | | |
| Eje adicional | m | cotizar | | | | |
| Punto de control geodésico | punto | 2 | | | | Certificación formal por separado |
| Aforo de reconocimiento | unidad | 2–4 | | | | Indicar temporada/equipo |
| Regla y registrador | conjunto | opcional | | | | Equipo, intervalo, mantenimiento |
| Operación hidrométrica ampliada | mes | 12 | | | | Campaña completa opcional |
| Calicata | unidad | 14 opcional | | | | Profundidad/precio adicional |
| Perforación/ensayo SPT | m o unidad | 3 opcional | | | | Método y limitaciones |
| Ensayos de laboratorio | ensayo | según programa | | | | Listar norma/método |
| Informe y archivos editables | suma alzada | 1 | | | | |

## 6. Coordinación, salud y seguridad

El contratista es responsable de su personal, equipo, transporte, EPP, permisos laborales y plan de seguridad. Entregar análisis de riesgos por actividad, comunicación y respuesta a emergencias, restricciones por crecida, clima, altura y accesos. Coordinar permisos de ingreso con titular/comunidad antes de movilizar; detener el trabajo si no existe acceso autorizado o condiciones seguras.

No se autoriza tala, intervención de cauce, instalación permanente, apertura de accesos, excavación o toma de muestras fuera del alcance aprobado. Las actividades que requieran autorización de ANA, ambiental, arqueológica o predial se identificarán y cotizarán como excluidas/opcionales hasta contar con los permisos aplicables.

## 7. Criterios de evaluación de ofertas

Comparar cumplimiento técnico, trazabilidad y calidad de entregables, experiencia específica, disponibilidad, seguridad, plazo, desglose de precio y claridad de exclusiones. Rechazar propuestas que atribuyan precisión/certificación no demostrada, que traten los datos conceptuales como observados o que ofrezcan resultados de crecidas/caudales firmes sin declarar base e incertidumbre.

## Referencias públicas a verificar al contratar

- IGN, especificaciones para posicionamiento geodésico y punto de orden C: [documento técnico IGN](https://app8.ign.gob.pe/GestionDocumental/Documento.aspx?id=2634). El postor deberá comprobar versión vigente y requisitos formales.
- ANA, requisitos y formatos para solicitar acreditación de disponibilidad hídrica: [trámite oficial](https://www.gob.pe/10824-obtener-la-acreditacion-de-disponibilidad-hidrica-para-el-otorgamiento-de-derechos-de-uso-de-agua) y [TUPA vigente](https://www.gob.pe/institucion/ana/informes-publicaciones/5630557-texto-unico-de-procedimientos-administrativos-tupa-de-la-autoridad-nacional-del-agua-ana).

**Advertencia de uso:** documento de procura de prefactibilidad sujeto a revisión del titular y de especialistas responsables. No reemplaza el diseño, permisos, especificaciones de obra ni aprobación de la autoridad.
