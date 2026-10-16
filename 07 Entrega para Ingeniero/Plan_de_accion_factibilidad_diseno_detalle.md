# Plan de acción para factibilidad y diseño de detalle

**Proyecto:** Microcentral hidroeléctrica de 100 kW, Puno<br>
**Estado:** plan para convertir la prefactibilidad en una base de diseño verificable. No es memoria de cálculo aprobada, expediente de permisos ni autorización para construir.<br>
**Responsable de cierre:** ingeniero colegiado habilitado y especialistas de hidrología, geotecnia, electricidad, ambiente y topografía.

## Matriz de evaluación del expediente

| Área | Peso |
|---|---:|
| Hidrología y topografía | 20% |
| Obras civiles y geotecnia | 15% |
| Electromecánica e interconexión | 20% |
| Economía y demanda | 15% |
| Permisos y medio ambiente | 10% |
| Trazabilidad, modelación y gestión de calidad | 20% |
| **Total** | **100%** |

## Reglas para el equipo

- Cada dato debe conservar: fuente, fecha, ubicación, unidad, método, instrumento, responsable, incertidumbre y estado (`medido`, `certificado`, `estimado`, `supuesto` o `pendiente`). No sobrescribir originales; guardar copia original y copia procesada con control de versiones.
- Marcar en planos y cálculos los valores que aún no tienen levantamiento, ensayo, cotización o respuesta formal de autoridad/empresa eléctrica.
- Los umbrales numéricos de campaña de este plan son controles de calidad propuestos para contratar el estudio; no se presentan como tolerancias reglamentarias. Aplicar siempre la norma peruana y el TUPA vigentes al presentar expedientes.
- No declarar “diseño definitivo” hasta que caudal ecológico, caudales mensuales disponibles, salto neto, geotecnia, inundación, permisos, conexión y ofertas garantizadas estén cerrados.

## Base de prefactibilidad que debe mantenerse como escenario

| Parámetro | Valor de escenario | Tratamiento para la siguiente etapa |
|---|---:|---|
| Potencia nominal de proyecto | 100 kW | Confirmar potencia garantizada y criterio de limitación del conjunto turbina-generador. |
| Caudal de diseño | 125 L/s | Supuesto de dimensionamiento; probar frente a curva de duración y caudal ecológico. |
| Salto bruto | 115 m | Supuesto; sustituir por control topográfico y niveles operativos. |
| Salto neto | 106.18 m | Estimación anterior; recalcular con pérdidas de conducción por caudal. |
| Caudal ecológico usado | 30 L/s | Supuesto no aprobado; determinar con estudio y ANA. |
| Generador preliminar | 125 kVA, fp 0.8 | Equivale a 100 kW a fp 0.8 antes de derating; validar altitud, temperatura y servicio. |
| Demanda | 672.77 MWh/año | Hipótesis sin medición de cargas; equivale a potencia media aritmética de 76.8 kW durante 8,760 h, no a demanda máxima ni energía firme. |
| Serie diaria | 3,652 registros (2014–2023); Qmedia reportado 0.523 m³/s y Q95 de excedencia 0.126 m³/s | Conteo calendario plausible; valores reproducidos del escenario, con procedencia y medición aún por acreditar. |

La simulación de prefactibilidad reportó 862.92 MWh/año; no es energía firme ni venta garantizada. La diferencia aritmética frente a la demanda hipotética no demuestra excedente utilizable. El registro de caudales debe validarse antes de usar cualquiera de esas cifras para financiar o dimensionar.

## Secuencia de trabajo y dependencias

1. **Línea base física:** topografía, hidrología y aforos; define energía disponible y plausibilidad del salto. La consulta temprana de restricciones ambientales y prediales debe correr en paralelo para evitar levantar una alternativa inviable.
2. **Línea base geotécnica:** exploraciones y ensayos en las huellas seleccionadas; condiciona cimentaciones, apoyos y estabilidad.
3. **Ingeniería electromecánica:** selección y cotización de equipos e interconexión, usando caudales, salto, geotecnia y carta de factibilidad de la distribuidora.
4. **Viabilidad legal y ambiental:** tramitar los derechos ANA, certificación ambiental y servidumbres aplicables con diseño suficientemente definido.
5. **Cierre financiero:** cerrar metrados, CAPEX/OPEX, censo de cargas y evaluación económica con ofertas y datos sustentados.
6. **Aseguramiento de calidad:** revisión independiente y cierre documentado de observaciones antes de emitir la factibilidad como base de diseño detallado.

# 1. Hidrología y topografía — peso de revisión 20%

## 1.1 Protocolo para auditar los 3,652 datos diarios

### A. Custodia y reconstrucción

1. Solicitar el archivo fuente sin edición, metadatos, institución/persona que lo generó, nombre/código de estación, coordenadas, datum, método de aforo, frecuencia, unidad, fecha de inicio y cierre, cambios de estación/instrumento y códigos de calidad. Registrar URL, correo o acta de entrega y fecha de descarga.
2. Congelar copia de solo lectura y calcular hash SHA-256. Crear copia de trabajo; documentar cada transformación con script reproducible.
3. Verificar que el calendario 2014-01-01 a 2023-12-31 tenga exactamente 3,652 fechas únicas (incluye 29-feb-2016 y 29-feb-2020). Reportar duplicados, fechas faltantes, marcas de hora/zona, registros fuera de rango y días repetidos.
4. Confirmar si cada valor es caudal medio diario, instantáneo, aforado, modelado o imputado. No mezclar esas clases. Identificar unidades, redondeo, ceros, negativos, valores censurados y límites instrumentales.
5. Auditar constantes o repeticiones. En la serie revisada previamente, 0.125 m³/s aparece como mínimo repetido en 181 días; investigar si representa caudal real, imputación, límite de detección o relleno artificial. No sustituirlo ni eliminarlo sin evidencia.
6. Hacer una tabla de procedencia por tramo temporal y una tabla de faltantes/ediciones. Conservar valores originales y agregar columnas de valor corregido, bandera, motivo y autor.

### B. Pruebas y productos

| Control | Aplicación | Salida/decisión |
|---|---|---|
| Rango físico y consistencia temporal | Q < 0, saltos imposibles, unidades, duplicados, calendario y codificación de faltantes | Lista de errores con referencia a registro original; corregir solo con fuente trazable. |
| Gráficas y estadística descriptiva | Serie diaria, mensual/anual; histogramas, ECDF, caja por mes/año, curva de duración, máximos/mínimos anuales | Media, mediana, CV, percentiles, estacionalidad, datos censurados y valores atípicos candidatos. |
| Curva de duración | Ordenar Q de mayor a menor; probabilidad de excedencia de Weibull `P=m/(n+1)` | Aclarar que `Q95` suele significar caudal excedido 95% del tiempo (bajo caudal), no percentil no excedido 95%. |
| Doble masa | Acumular caudal del sitio frente a estación vecina de régimen, área y periodo comparables; también lluvia acumulada cuando aplique | Quiebre de pendiente puede indicar cambio de estación, instrumento o relación; no autentica por sí solo la serie. No comparar cuencas incompatibles. |
| Puntos de cambio/saltos | Pettitt, SNHT, Buishand (rango/estadístico) y von Neumann; probar cambios documentados, homogeneidad por meses/estación y significancia con autocorrelación considerada | Fechas candidatas y p-valor/intervalo; corroborar con metadatos. Ajustar únicamente con justificación hidrológica y preservar serie original. |
| Tendencia | Mann-Kendall (estacional si corresponde) y pendiente de Sen; ajustar significancia por dependencia serial cuando proceda | Separar tendencia climática de ruptura instrumental; reportar magnitud e incertidumbre. |
| Dependencia y extremos | Autocorrelación, años hidrológicos, máximos anuales y POT solo con umbral/independencia documentados | No inferir crecidas de diseño de una serie corta de promedios diarios. Obtener máximos instantáneos y marcas de avenida. |
| Consistencia regional | Correlación y regresión con estaciones SENAMHI/ANA u otras verificables; análisis por estación y periodo solapado | Comparar volúmenes, estacionalidad y razón de áreas/altitudes; justificar cualquier transferencia o relleno. |

**Cierre de auditoría:** tabla de registros válidos, observados, imputados y sospechosos; informe de metadatos; gráficas; resultados de pruebas; curva de duración con incertidumbre; scripts y decisión firmada sobre uso. Diez años son pocos para estimar con precisión eventos raros: complementar crecidas con regionalización y modelación lluvia-escorrentía, no extrapolar una distribución sin intervalos de confianza.

## 1.2 Campaña de aforos y curva de gasto

**Objetivo:** obtener pares simultáneos de nivel y caudal en un tramo estable para relacionar la altura `h` con `Q`. Cada tramo tiene una curva propia y esta cambia cuando se erosiona, deposita sedimento o cambia el control hidráulico. La práctica de medición y curva específica está descrita por USGS; usarla como metodología técnica, no como norma peruana ([USGS, Streamgaging Basics](https://www.usgs.gov/mission-areas/water-resources/science/streamgaging-basics), [medición de caudal](https://pubs.usgs.gov/tm/tm3-a8/tm3a8.pdf)).

1. **Seleccionar sección:** tramo recto, flujo uniforme, sin remanso, confluencia, toma, vegetación densa o lecho muy móvil; verificar ambas márgenes y acceso seguro. Levantar croquis, sección, control aguas abajo y fotografías con escala.
2. **Instalar control de nivel:** regla limnimétrica fijada y referida a un BM; sensor de presión/ventilado con barologger si hay registro continuo. Registrar nivel cada 15 minutos (o intervalo que capture crecidas), sincronizar reloj, verificar cero y hacer lectura manual de contraste en cada visita.
3. **Medir caudal:** molinete calibrado o ADCP, según ancho/profundidad/velocidad; método velocidad-área `Q = Σ(Aᵢ vᵢ)`. Dividir la sección en subsecciones, medir ancho, profundidad y velocidad representativa en cada una. En secciones pequeñas puede usarse aforo volumétrico/vertedero temporal solo si el montaje no altera peligrosamente el cauce y el método es válido. Registrar calibración, operador, condiciones y todas las lecturas. Para referencia de procedimiento, el USGS usa subdivisión de la sección y suma de caudales parciales.
4. **Cobertura:** campaña de al menos un ciclo hidrológico, con objetivo de 15–20 aforos distribuidos entre estiaje, transición y avenida, y mediciones extraordinarias seguras en niveles altos/bajos. Procurar varias mediciones a ambos lados de 125 L/s y cerca de los caudales bajos que gobiernan disponibilidad. Ese número es un objetivo de proyecto, no una prescripción universal; una curva no es confiable fuera del rango aforado.
5. **Repetibilidad:** en condiciones estables, repetir medición cuando haya duda o error de cierre; como control interno, investigar discrepancias mayores a 5% entre mediciones repetidas. Ese 5% es criterio de campaña propuesto, no límite legal. Si cambia el cauce, levantar nueva sección y evaluar curva por periodos o control variable.
6. **Ajuste:** ajustar `Q = a(h-h₀)^b` por tramo/control, evaluar ajuste ponderado, residuos, sesgo por rango y bandas de confianza; no extrapolar mucho por encima del mayor caudal medido. Mantener relación alternativa si hay histéresis/remanso o controles distintos. Verificar con aforos independientes.
7. **Crecidas no aforables:** medir marcas de agua alta, sección y pendiente; estimar pico por método hidráulico apropiado con incertidumbre (p. ej. perfil/energía), documentando que es aforo indirecto y no observación directa.

### Formato H-01 — hoja de aforo (una fila por vertical/subsección)

| Campo | Dato a registrar |
|---|---|
| Proyecto / código estación / fecha-hora local y UTC |  |
| Operador / equipo / número de serie / última calibración |  |
| Método (molinete, ADCP, volumétrico u otro) / modo / incertidumbre declarada |  |
| Coordenadas de sección / datum / BM / cota del cero de regla |  |
| Nivel en regla y sensor / lectura antes-después / barómetro si aplica |  |
| Estado del cauce (turbidez, vegetación, remanso, lluvia, maniobra, sedimento) |  |
| N.º subsección / distancia desde margen / ancho parcial / profundidad |  |
| Punto(s) de velocidad / profundidad de sensor / velocidad / tiempo de observación |  |
| Área parcial / velocidad media / caudal parcial |  |
| Caudal total / método de cálculo / control de cierre |  |
| Croquis, fotos, marcas de agua y observaciones / firmas |  |

## 1.3 Levantamiento topográfico para salto y tubería

- **Control geodésico:** establecer al menos dos puntos de control monumentados fuera de zona inundable/obras, ligados a marco/red oficial. GNSS estático relativo procesado siguiendo la especificación vigente del IGN; entregar datos crudos RINEX, antena/altura, efemérides, estaciones de referencia, época, marco, proyección, geoide, residuales, precisión y reporte de ajuste. No aceptar solo captura de coordenadas RTK sin control independiente. Consultar [especificación IGN de GNSS estático relativo](https://app8.ign.gob.pe/GestionDocumental/Documento.aspx?id=2634).
- **Altimetría:** amarrar las cotas de agua, toma, cámara de carga, eje de turbina, restitución y sección de aforo al mismo datum vertical. Hacer nivelación geométrica de ida/vuelta o circuito cerrado para el salto y controles hidráulicos; estación total para detalle y poligonal cerrada; GNSS para control, no como sustituto automático de nivelación fina.
- **Cobertura:** eje de tubería propuesto y alternativas, puntos de quiebre, curvas, apoyos/anclajes, accesos, cruces, taludes, cauces, zonas de deslizamiento, casas, redes, faja de servidumbre, toma, desarenador, cámara de carga, casa de máquinas, canal de restitución y posible subestación/línea. Levantar perfil longitudinal y secciones transversales en estructuras, cruces y cambios geomorfológicos.
- **Precisión contractual sugerida:** exigir tolerancia vertical relativa de ±0.02 m entre controles hidráulicos principales mediante nivelación y ±0.05 m en detalle de traza; horizontal de ±0.05 m en replanteo de estructuras. El topógrafo debe proponer instrumento/método y reportar error de cierre y ajuste; estas metas son requisitos del proyecto y deben revisarse según escala, relieve y especificación IGN, no son tolerancias legales citadas aquí.
- **Entregables:** informe de datum/métodos/precisiones; certificados de calibración; libreta y archivos crudos; CSV de puntos XYZ/códigos; poligonal y nivelación; ortofoto si se contrata; DWG/DXF, GeoPackage/shape, TIN/DEM, curvas de nivel, perfiles y secciones. Incluir BM y coordenadas en todos los planos.
- **Cálculo de salto:** `Hbruto = cota de nivel de agua de toma − cota de nivel de restitución` en condición de operación definida. Medir niveles de estiaje/operación y crecida, no inferir nivel a partir del terreno. Después, `Hnet(Q) = Hbruto − hL(Q)`. Para la conducción: `hf = f(L/D)(V²/2g)`, `V=4Q/(πD²)` y `hs=ΣK(V²/2g)`; usar Darcy–Weisbach y calcular `f` por Colebrook–White o una aproximación explícita como Swamee–Jain dentro de su rango de validez. Añadir pérdidas de entrada, rejilla, curvas, válvulas, bifurcación y descarga. La potencia estimada en bornes es `P=ρgQdisponible Hnet ηturbina ηgenerador ηtransmisión`; `Qdisponible` debe descontar caudal ecológico y otros usos según resolución. Reportar banda por incertidumbre topográfica y variación de niveles.

# 2. Obras civiles y geotecnia — peso 15%

## 2.1 Programa de investigación del subsuelo

Primero hacer reconocimiento geológico-geomorfológico, mapeo de afloramientos, deslizamientos, erosión, nivel freático, depósitos aluviales/coluviales y riesgo sísmico; después ubicar exploraciones sobre huella real. La tabla es un programa inicial de licitación que el geotécnico debe ajustar por tamaño, profundidad de cimentación y hallazgos.

| Sector | Exploración inicial propuesta | Ensayos y preguntas de diseño |
|---|---|---|
| Bocatoma y barraje | 2–3 calicatas en márgenes/huella; perforación con recuperación de testigo si roca o cimentación profunda; mapeo de discontinuidades | Granulometría/Atterberg, humedad/densidad, corte directo o triaxial, permeabilidad; RQD, fracturas, resistencia UCS/índice de carga puntual; infiltración/pérdida bajo barraje y socavación. |
| Desarenador y canal corto | 2 calicatas por huella o 1–2 perforaciones donde profundidad/agua lo exijan | Estratigrafía, SPT corregido por energía donde corresponda, granulometría de sedimentos, permeabilidad, asentamiento, agresividad química del suelo/agua al concreto. |
| Cámara de carga/forebay | 2 calicatas o sondeos distribuidos; sondeo adicional en talud o relleno | Capacidad portante y asentamiento, estabilidad global/local de talud, nivel freático, filtración, necesidad de drenaje/filtro y protección frente a erosión. |
| Casa de máquinas | 2–3 perforaciones en huella, profundizadas bajo zona de influencia de cimentación y hasta estrato competente; testigo si roca | SPT y perfil estratigráfico, corte/triaxial, consolidación si finos blandos, módulo/deformabilidad, roca UCS/RQD, nivel freático, licuación si suelo granular saturado, vibración/base de equipo. |
| Tubería y bloques de anclaje | Calicatas en cambios geológicos, codos, anclajes, cruces y zonas inestables; mapeo continuo de traza | Clasificar material excavable, estabilidad de zanja/talud, soporte, drenaje, agresividad, capacidad de apoyo del anclaje y resistencia de roca. |

**Complementarios:** refracción sísmica/MASW para continuidad de estratos y Vs, georradar si el terreno lo permite, ensayos de permeabilidad in situ; estos métodos complementan y no reemplazan calicatas/sondeos. En el lecho activo no abrir calicatas sin desvío y control de seguridad: investigar mediante perforaciones o ventanas de excavación con acceso seguro. SPT no es representativo en gravas con bolones/refusal; el geotécnico debe cambiar a testigo u otro método y explicar la correlación usada. Laboratorio: granulometría, límites de Atterberg, humedad, densidad, gravedad específica, Proctor, corte directo/triaxial, consolidación/permeabilidad según suelo; química de suelo/agua para durabilidad. En canteras/agregados: granulometría, abrasión, equivalente de arena y reactividad si corresponde. El informe debe incluir perfil geotécnico, parámetros de cálculo con valores característicos, asentamientos, estabilidad, excavabilidad, recomendaciones de cimentación/drenaje y limitaciones.

## 2.2 Crecida de diseño, vertedero y disipación

1. Delimitar cuenca y subcuencas con DEM corregido por campo; medir áreas, pendientes, longitudes, cobertura/uso de suelo, suelos, geología, lagunas/humedales y obstrucciones. Registrar cambios recientes de uso y huellas de inundación.
2. Reunir máximos instantáneos y diarios, lluvia diaria/subdiaria, curvas IDF/DDF y eventos históricos; revisar consistencia, estación, altitud, periodo y regionalización. El registro diario de caudales 2014–2023 no basta por sí solo para eventos raros.
3. Definir AEP/periodo de retorno para avenida de diseño y verificación a partir de clasificación/riesgo de falla de la obra, consecuencias aguas abajo, criterios de la autoridad/financiador y consulta con ANA. No seleccionar un retorno único “por costumbre”.
4. Estimar caudales por métodos independientes: análisis de frecuencia de máximos anuales si hay serie adecuada (GEV/Gumbel/LP3 con diagnóstico y límites de confianza); regionalización; y modelación lluvia-escorrentía (HEC-HMS u otro) con tormentas DDF, humedad antecedente, tránsito y calibración con eventos observados. Comparar métodos y sensibilidad, documentar supuestos; guía USACE para HEC-HMS destaca calibración, comparación de métodos e incertidumbre ([guía de frecuencia de crecidas](https://www.hec.usace.army.mil/confluence/hmsdocs/hmsag/flood-frequency-studies/background-for-flood-frequency-studies)).
5. Ejemplo estadístico que sirve como comprobación, no como criterio obligatorio: para Gumbel, `Q_T = μ + α y_T`, `y_T = −ln[−ln(1−1/T)]`, con parámetros estimados por método elegido. Presentar intervalo de confianza y contraste con regionalización/modelo. Para muestra de 10 años, extrapolación a retornos altos es muy incierta.
6. Traducir hidrograma/caudal de diseño a nivel y velocidad en la toma mediante levantamiento de secciones y modelo hidráulico (HEC-RAS 1D/2D u otro validado). Evaluar obstrucción por troncos, carga de sedimentos, remanso, erosión, inundación de obras, acceso y descarga.
7. Dimensionar vertedero con ecuación apropiada a geometría y régimen. Para vertedero rectangular de pared delgada, como referencia ideal: `Q = (2/3) C_d b √(2g) H^(3/2)`; para cresta ancha/lateral o estructura real usar coeficiente/ecuación y correcciones específicas (velocidad de aproximación, contracción, sumersión, aireación, rugosidad). Resolver ancho/longitud de cresta y carga `H` para el caudal adoptado.
8. Diseñar canal de demasías, transición, disipador, protección de márgenes y enrocado/filtros con velocidades, tirantes, número de Froude, socavación, nivel de cola, energía residual y descarga segura. Verificar borde libre y estabilidad estructural según norma de concreto, sismo y criterios de la autoridad aplicables. Incluir avenida de construcción/desvío y mantenimiento.

**Memoria requerida:** cuenca, fuentes, series y calidad; método(s), calibración, AEP, hidrogramas, incertidumbre; modelo geométrico/hidráulico; tabla Q–nivel–velocidad; plano de toma/vertedero/disipación; cálculo estructural/geotécnico; escenarios con obstrucción y erosión.

# 3. Electromecánica e interconexión — peso 20%

## 3.1 Data sheet para solicitud de cotización: turbina

Enviar la misma hoja a mínimo tres fabricantes/integradores y exigir cotización con garantías comparables. La selección tipo Pelton es preliminar dada la combinación de salto alto y caudal, pero debe verificarse con curva de operación y rango de caudal.

| Parámetro de consulta | Requisito preliminar / dato que debe completar proveedor |
|---|---|
| Proyecto/emplazamiento | Puno, Perú; coordenadas y elevación exacta pendientes de topografía. |
| Tipo de turbina solicitado | Pelton (ofertar alternativa si su análisis justifica otra). Horizontal/vertical y número de chorros a proponer. |
| Caudal nominal de diseño | 0.125 m³/s; presentar rango continuo mínimo/máximo y rendimiento parcial. |
| Salto bruto | 115 m, supuesto a confirmar. |
| Salto neto en boquilla | Pendiente de pérdidas confirmadas; ofertar para curva de Hnet y declarar límites de operación. |
| Potencia eléctrica neta objetivo | 100 kW en bornes de generador como objetivo del proyecto; separar potencia hidráulica, eje y bornes y explicar limitación. |
| Agua/sedimento | Adjuntar granulometría, concentración y dureza cuando se midan; ofertar material resistente a abrasión/corrosión y plan de inspección. |
| Condiciones del sitio | Altitud, temperatura ambiente, polvo, humedad, transporte/acceso y sismicidad: completar tras levantamiento. |
| Curvas garantizadas | Q, H, rpm, potencia de eje y eficiencia para 50/60/75/80/90/100/110/115/125 L/s y rango de H; definir garantías y tolerancias. |
| Gobernador y regulación | Deflector/inyector, servomotor, control de nivel/frecuencia, rechazo de carga, modo aislado y en paralelo, alimentación auxiliar y respuesta dinámica. |
| Velocidades | Velocidad nominal compatible con generador; velocidad de embalamiento, límites mecánicos, balanceo y cargas en rodamientos. |
| Transitorios | Cierre/apertura de inyector, golpe de ariete, tiempo de cierre, válvula principal, presión máxima y requerimiento de cámara/válvula de aire. |
| Fabricación | Materiales de rueda, inyectores, eje, carcasa, recubrimientos; planos de interfaz; tolerancias, soldaduras y NDT. |
| Auxiliares | Válvula principal, by-pass, filtros, lubricación, enfriamiento, sensores, herramientas, repuestos para 2 años. |
| Pruebas y normas | Ensayo de aceptación en campo conforme a acuerdo y procedimiento basado en IEC 60041; protocolo FAT/SAT, instrumentos, incertidumbre y criterios de garantía. No exigir ensayo de modelo IEC 60193 salvo que fabricante/ingeniero justifique aplicabilidad a esta escala. |
| Oferta | Precio, moneda, Incoterm, impuestos, flete, montaje, supervisión, repuestos, plazo, garantía, curva de eficiencia certificada, exclusiones y vigencia. |

**Comprobación física preliminar:** `P_hidráulica = ρgQH`; para 1000 kg/m³, 9.81 m/s², 0.125 m³/s y 115 m da aproximadamente 141 kW antes de pérdidas y eficiencia. A `Hnet = 106.18 m`, son aproximadamente 130 kW hidráulicos. El proveedor debe garantizar si la potencia se refiere al eje o a bornes y demostrar el punto nominal; no usar eficiencia global fija de 0.73 para aceptación.

## 3.2 Data sheet: generador síncrono

| Parámetro | Solicitud preliminar |
|---|---|
| Potencia aparente activa | 125 kVA; 100 kW a fp 0.8. Confirmar potencia continua a altitud/temperatura real y derating. |
| Tensión/fases/frecuencia | 400/230 V, 3 fases, 4 hilos, 60 Hz como base interna; coordinar con fabricante y esquema de conexión. |
| Velocidad/polos | Proveedor propone acoplamiento directo o multiplicadora. 1,200 rpm solo corresponde a 6 polos síncronos a 60 Hz; no fijar hasta cerrar velocidad de turbina. |
| Factor de potencia/reactivos | Indicar rango de operación adelantado/atrasado, curva de capacidad P-Q y límites térmicos. |
| Excitación/regulación | Excitación brushless o propuesta, AVR, regulación de tensión, entrada de control remoto, respuesta ante isla/paralelo. |
| Aislamiento/protección | Clase de aislamiento y elevación térmica propuestas para sitio; IP, enfriamiento, altitud, calentadores anticondensación, RTD y sensores. |
| Reactancias/falla | `Xd, X'd, X''d`, secuencia negativa/cero, constante de inercia, corriente de cortocircuito y decremento para estudios de protección. |
| Neutro/puesta a tierra | Diagrama de devanados, accesibilidad de neutro, método de puesta a tierra y coordinación con transformador/protección. |
| Rendimiento/calidad | Curva de eficiencia, regulación, THD/armónicos, desbalance, ruido y vibración garantizados. |
| Control/protecciones | Relé de generador, sincronismo, medición, breaker, CT/VT, parada de emergencia e interfaces de comunicación. |
| Documentación | Diagramas, planos, certificados de ensayos, lista de repuestos, manual O&M, garantía, FAT/SAT y servicio local. |

IEC 60034-1 es la familia de referencia para máquinas rotativas; pedir al proveedor la edición vigente aplicable al suministro y sus certificados. Para turbina, fijar contractualmente protocolo de aceptación y métodos de incertidumbre con base en IEC 60041.

## 3.3 Transformador y conexión en 10 kV

Solicitar a Electro Puno una **respuesta escrita de factibilidad y punto de conexión**, con coordenada, nivel de cortocircuito, capacidad disponible, esquema de medición, protecciones, tensión operativa y requisitos de telecontrol. No asumir aceptación por estar cerca de una línea. El expediente de conexión debe incluir:

- Perfil de generación horaria/estacional, potencia máxima exportada/importada, operación aislada/paralela, tensión de generador, elevación del sitio y factor de potencia.
- Diagrama unifilar desde alternador hasta red; memoria de demanda/corto circuito, flujo de carga, coordinación de protecciones, puesta a tierra, calidad de energía, armónicos/flicker, aislamiento, sobretensiones y coordinación BIL.
- Transformador elevador (125 kVA, 0.4/10 kV es solo alternativa preliminar): grupo vectorial, impedancia, taps, pérdidas, refrigeración, nivel de aislamiento, BIL, neutro, protección térmica/presión y accesibilidad.
- Celda MT con interruptor de corte, seccionamiento visible/enclavamientos, puesta a tierra, TC/TP, relé, descargadores, medición bidireccional y puntos de prueba; línea y estructura según estándar de Electro Puno.
- Relé de interconexión: funciones a evaluar con la distribuidora (no todas serán obligatorias): 27/59 subtensión/sobretensión; 81U/O frecuencia; 25 verificación de sincronismo; 50/51 sobrecorriente fase; 50N/51N tierra; 67/67N direccional si flujo bidireccional; 32 potencia inversa; 46 secuencia negativa; 49 térmica; 50BF falla interruptor; 86 bloqueo; anti-isla/transferencia de disparo si la empresa lo exige.
- Estudio de coordinación con reconectadores aguas arriba, reenganche, pérdida de red, tiempo de despeje, isla no intencional, secuencia de energización, sincronización, reconexión y pruebas de puesta en servicio.
- Medición comercial, calidad de energía, telemetría/SCADA, canal de comunicación, consignas de potencia/reactivos, control de tensión y protocolo de operación/mantenimiento según requerimiento del operador.
- Cumplir Código Nacional de Electricidad — Suministro y normas técnicas peruanas aplicables; requerimientos definitivos de conexión los fija la distribuidora para ese punto y deben quedar como carta/estudio aprobado.

# 4. Economía y demanda — peso 15%

## 4.1 WBS de presupuesto CAPEX/OPEX

Usar una fila por partida medible. Separar cantidad medida, costo cotizado y provisión; no aplicar un único porcentaje global sin explicar base.

| Código | Paquete de trabajo / costos que debe incluir |
|---|---|
| 1.0 | Desarrollo: topografía, hidrología, geología, geotecnia, laboratorio, batimetría/aforos, ingeniería, gestión de permisos y revisión independiente. |
| 2.0 | Terrenos y social: compra/arrendamiento, servidumbres, compensaciones, acuerdos comunales, liberación de interferencias, consulta aplicable. |
| 3.0 | Obras temporales: accesos, desvío de río, ataguías, campamento, seguridad, instalaciones provisionales, manejo de sedimentos y restauración. |
| 4.0 | Captación: barraje/toma, rejillas, compuertas, desripiador, desarenador, vertedero, disipación, defensas ribereñas. |
| 5.0 | Conducción: canal, cámara de carga, tubería por diámetro/material/espesor, uniones, codos, válvula, bloques de anclaje/apoyo, drenaje y protección. |
| 6.0 | Casa de máquinas y restitución: excavación, cimentaciones, edificio, puente grúa si aplica, canal de cola, estabilización y drenaje. |
| 7.0 | Electromecánico: turbina, generador, gobernador, válvulas, auxiliares, montaje, pruebas, repuestos iniciales y capacitación. |
| 8.0 | Eléctrico: tableros, control/protección, cableado, puesta a tierra, transformador, celdas MT, línea, medición, comunicación y conexión. |
| 9.0 | Ambiental/social y cierre: medidas de manejo, monitoreo, caudal ecológico, rescate/compensación si aplica, revegetación, residuos, plan de cierre. |
| 10.0 | Costos del propietario: supervisión, QA/QC, seguros, gestión de proyecto, permisos, impuestos no recuperables, financiamiento, IDC, importación/flete, contingencias y escalamiento separados. |
| O.1 | Personal de operación, administración, comunicaciones, seguridad y capacitación. |
| O.2 | Mantenimiento preventivo/correctivo, repuestos, aceites, rodamientos, limpieza de rejilla/desarenador, inspecciones de tubería/obras. |
| O.3 | Seguros, vigilancia, tasas/cargos de conexión o energía, servidumbres, monitoreo ambiental/social, gestión de residuos. |
| O.4 | Reserva de reposición mayor: gobernador, AVR, bobinado, impulsor/inyectores, relés, baterías y equipos de medición, con vida útil y calendario. |

### Formato E-01 — control de metrados y cotizaciones

| WBS | Descripción/especificación | Unidad | Metrado y plano fuente | Precio unitario | Moneda/fecha/vigencia | Proveedor y número de oferta | Incluye impuestos/flete/montaje | Instalación/indirectos | Contingencia justificada | Total base/alto/bajo | Estado y responsable |
|---|---|---:|---|---:|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |

Comparar al menos tres ofertas para equipos principales cuando sea viable; documentar excepciones. Fijar costo base, contingencia por riesgo identificado, escalamiento por fecha y tipo de cambio; evitar duplicar impuestos/indirectos. OPEX anual debe estar vinculado a energía realmente entregable, régimen de turnos, plan de mantenimiento, disponibilidad y costos locales.

## 4.2 Cuestionario técnico de usuarios

**Unidad de encuesta:** hogar, comercio, taller, entidad pública, sistema productivo. Usar identificador anónimo; explicar consentimiento, fin de la encuesta y tratamiento de datos. Entrevistar en época seca y lluviosa si la actividad es estacional.

| Bloque/pregunta | Registro |
|---|---|
| Identificación | Código de usuario, comunidad, coordenada aproximada, tipo de usuario, entrevistador, fecha, consentimiento. |
| Servicio existente | Fuente de suministro, tensión/fases, horas con servicio, interrupciones mensuales, voltaje/calidad, tarifa y gasto; fotografiar factura con autorización o transcribir 12 meses. |
| Equipos | Por equipo: cantidad, potencia de placa (W/kW), tensión, fases, fp si consta, corriente de arranque, año/estado. Incluir iluminación, refrigeración, bombeo, molienda, soldadura, cocina/calefacción y equipos futuros. |
| Uso horario | Días/mes y horas/día por equipo; hora de encendido/apagado; simultaneidad; temporada seca/lluviosa; días punta. Marcar carga crítica e interrumpible. |
| Medición | Si existe medidor, obtener curvas/lecturas 15 min por 7–14 días (idealmente campañas en épocas seca y lluviosa); tomar lecturas inicial/final y registrar número de medidor. |
| Crecimiento | Nueva carga prevista, equipo concreto, kW, fecha, financiamiento y evidencia (cotización/plan aprobado); evitar contar intención vaga como demanda firme. |
| Calidad y conexión | Distancia aproximada al punto, tensión necesaria, monofásico/trifásico, motores, sensibilidad a interrupción, puesta a tierra. |
| Disposición a conectarse | Interés, tarifa máxima explicada con escenarios, costo de conexión aceptable, posibilidad de pago, contrato/compromiso. No inducir respuestas ni prometer obra. |
| Validación | Firma/huella si corresponde, revisión de coherencia, foto de placa/medidor con permiso y observaciones. |

### Formato D-01 — registro de carga por equipo

`ID usuario | equipo | cantidad | W nominal | W medido | tensión/fases | corriente arranque | horas/día | días/mes | franja horaria | meses/año | crítico/interrumpible | fuente (placa/medidor/estimación) | foto/evidencia | observación`.

Calcular energía por equipo como `E_i = P_i × h_i` con unidad consistente, después sumar por franja y mes. Construir demanda coincidente (kW y kVA), factor de carga `E/(Pmax×horas)`, curva de duración y escenarios bajo/base/alto. Comparar energía anual medida con 672.77 MWh, pero validar también pico coincidente y pérdidas de red. La suma de energías individuales no determina por sí sola potencia de planta ni energía firme.

# 5. Permisos y medio ambiente — peso 10%

El listado final depende de ubicación, titular, régimen de operación/venta, trazo de línea, predios, áreas naturales y autoridad competente. Verificar TUPA y requisitos en fecha de cada presentación.

| Trámite/decisión | Qué cerrar y estudios/insumos típicos |
|---|---|
| ANA: acreditación de disponibilidad hídrica | Identificación de fuente y puntos UTM, memoria hidrológica sustentada, oferta mensual y demanda del proyecto, balance con usuarios/derechos existentes, calidad si corresponde, caudal ecológico, planos y verificación de campo según procedimiento/TUPA. La acreditación no es licencia de uso ni permiso para construir. Procedimientos sujetos a R.J. 007-2015-ANA y modificatorias; la R.J. 357-2024-ANA modificó requisitos. Revisar [R.J. 007-2015](https://www.gob.pe/institucion/ana/normas-legales/539001-r-j-007-2015-ana) y [TUPA ANA modificado en junio de 2026](https://www.gob.pe/institucion/ana/informes-publicaciones/5630557-texto-unico-de-procedimientos-administrativos-tupa-de-la-autoridad-nacional-del-agua-ana). |
| ANA: autorización de ejecución de obras en fuentes naturales | Memoria y planos de obras hidráulicas a nivel exigido, especificaciones, cronograma, manejo de desvío/avenidas, compatibilidad con disponibilidad acreditada y evaluación de efectos a terceros. Verificar autorización antes de ejecutar obra en cauce/ribera. |
| ANA: derecho de uso de agua | Determinar modalidad aplicable y obtener licencia/autorización/concesión que corresponda antes de usar el recurso; aprobación de disponibilidad por sí sola no confiere derecho de uso. Presentar sustento técnico, resolución previa y condiciones de operación/medición. |
| Caudal ecológico | Estudio de régimen ecológico y cumplimiento de lineamientos ANA R.J. 267-2019-ANA y requerimientos del instrumento ambiental. No asumir 30 L/s ni porcentaje fijo. [Lineamientos ANA](https://www.gob.pe/institucion/ana/normas-legales/537631-rj-267-2019-ana). |
| Certificación ambiental SEIA | Consultar por escrito a autoridad ambiental sectorial (MINEM/DGAAE u otra competente) la inclusión y categoría aplicable. Preparar ficha de proyecto, alternativas, área de influencia, línea base estacional, impactos, caudal y ecosistema acuático, biodiversidad, sedimentos, ruido, paisaje, residuos, riesgos, participación ciudadana, medidas/monitoreo y plan de cierre. No dar por hecho que corresponde una DIA solo por ser 100 kW: la categoría depende del listado/clasificación anticipada aplicable, componentes, impactos, ubicación y autoridad. Si el proyecto está sujeto al SEIA y no tiene clasificación anticipada aplicable, preparar la EVAP para solicitar clasificación ante la autoridad competente; verificar el procedimiento específico del subsector eléctrico antes de presentarla. Consultar [SEIA MINAM](https://www.minam.gob.pe/seia/), [listado de inclusión](https://www.gob.pe/institucion/minam/informes-publicaciones/308471-listado-de-inclusion-de-proyectos-de-inversion-sujetos-al-seia), [trámite de clasificación y EVAP](https://www.gob.pe/11396-solicitar-la-clasificacion-de-estudios-ambientales) y el Reglamento Ambiental de Electricidad D.S. 014-2019-EM y sus actualizaciones. |
| Terrenos y servidumbres | Títulos/catastro y posesión para toma, tubería, accesos, casa de máquinas, subestación y línea; acuerdos/contratos inscritos o trámite de imposición que corresponda. Servidumbre eléctrica no sustituye derecho predial ni autorización ambiental. |
| Derecho eléctrico / concesión | La FAQ vigente de MINEM indica concesión para generación hidráulica/RER por encima de 500 kW; 100 kW quedaría bajo ese umbral de concesión de generación según esa regla. Confirmar por escrito la clasificación y permisos del esquema concreto (venta, autoconsumo, distribución privada); la línea de transmisión que afecte bienes estatales o requiera servidumbre puede tener trámite propio. Consultar [FAQ MINEM](https://www.gob.pe/institucion/minem/informes-publicaciones/2147053-preguntas-frecuentes-sector-electrico) y [D.S. 056-2009-EM](https://www.gob.pe/institucion/minem/normas-legales/4718260-056-2009-em). |
| Interconexión | Solicitud de factibilidad a Electro Puno; estudios de conexión/protección/medición, acuerdo de operación y pruebas. No es sustituto de permisos de agua, ambientales o prediales. |
| Patrimonio cultural | Consultar CIRA/PMAR u obligaciones arqueológicas aplicables antes de movimiento de tierras ante Ministerio de Cultura; definir según huella y procedimiento vigente. |
| Áreas protegidas, bosque, biodiversidad | Cruce geográfico con SINANPE/zonas de amortiguamiento, ecosistemas frágiles y predios comunales; si corresponde, opinión/compatibilidad de SERNANP, autorización forestal SERFOR y estudio biológico estacional. |
| Comunidades y pueblos indígenas | Identificar comunidades y potencial afectación; plan de participación e información temprana. Determinar con autoridad si aplica consulta previa según ley y afectación directa; no sustituirlo con una encuesta de demanda. |

# 6. Trazabilidad, modelación y gestión de calidad — peso 20%

## Protocolo de integridad y auditoría

- Mantener un **registro maestro de datos**: ID, variable, valor/unidad, fecha, coordenadas/datum, fuente/archivo, hash SHA-256, estado (`medido`, `certificado`, `estimado`, `supuesto`, `pendiente`), precisión/incertidumbre, transformación, responsable y aprobación.
- Conservar los originales en solo lectura y separar `raw/`, `procesado/`, `modelos/`, `planos/` y `entregables/`. Cada procesamiento debe registrar versión de herramienta, parámetros, fecha, autor y archivo de salida; no editar el original.
- Parametrizar hojas de cálculo o scripts para los cálculos repetibles de hidrología, hidráulica, energía y economía. En estabilidad estructural, geotecnia y protecciones usar software y normas apropiados, con entradas/salidas archivadas y comprobación independiente de los casos críticos; no es necesario reprogramar software especializado.
- Elaborar una matriz de trazabilidad que enlace cada requisito → dato/ensayo → cálculo/modelo → plano/especificación → permiso/decisión. Toda hipótesis debe tener ID, responsable, justificación, sensibilidad y fecha límite de cierre.
- Controlar versiones de modelos, archivos CAD/BIM, hojas y documentos; mantener historial de cambios, revisiones, autor, aprobador y comentario resuelto. Congelar una revisión emitida para comentarios; evitar sobrescribir versiones aprobadas.
- Ejecutar controles cruzados: balance de agua y energía, unidades/dimensiones, pérdidas y salto neto, potencia respecto a placa del generador, comparación entre cálculos manuales independientes y software, revisión de fórmulas/rangos, escenarios bajo/base/alto y sensibilidad de supuestos dominantes.
- Revisiones por hitos: (1) datos y topografía; (2) hidrología/geotecnia; (3) diseño civil y electromecánico; (4) interconexión y ambiente; (5) CAPEX/OPEX y expediente integrado. Mantener lista de observaciones con ID, severidad, responsable, evidencia de cierre y aceptación del revisor.

### Paquete de auditoría por cálculo

| Elemento | Contenido mínimo |
|---|---|
| Identificación | Código de cálculo, disciplina, revisión, autor, revisor, fecha y software/versión. |
| Base de diseño | Requisitos aplicables, criterios/normas, supuestos y exclusiones, datos de entrada con ID de fuente y unidades. |
| Método | Ecuaciones/método, rango de validez, combinaciones/casos de carga y parámetros. |
| Resultado | Tablas, figuras, salida nativa del software, resultado adoptado y comparación independiente. |
| Incertidumbre | Sensibilidad, escenarios, límites de dato y efecto en diseño/costo/energía. |
| Cierre | Conclusión, comentarios, revisiones, aprobaciones y archivos relacionados (plano, oferta, permiso). |

## Flujo conceptual Google Earth → QGIS → Python

1. **Google Earth Pro — cribado visual:** importar/trazar KML/KMZ de toma, cámara, traza y restitución; revisar continuidad de ladera, cruces, accesos y desnivel de orden de magnitud. Su perfil de elevación es una consulta a un modelo de terreno de resolución y datum vertical no controlados por el proyecto; sirve para encontrar errores gruesos, no para validar `Hbruto`, calcular tubería ni replantear obras.
2. **QGIS — análisis espacial:** guardar las capas con CRS explícito y verificar zona/proyección con longitud y metadatos, no solo con la etiqueta “19S”. Cargar DEM identificado por producto, fecha, resolución, datum vertical y método; documentar que DEM de 12.5/30 m no equivale a topografía de detalle. Extraer perfil preliminar, delimitar cuenca con condicionamiento hidrológico del DEM y comparar alternativas. Transformar cotas verticales solo con modelo/geoid y parámetros documentados. Puntos GNSS y estación total se importan después de conservar archivos crudos y reporte de ajuste; no “corregir” una cota oficial por ajuste visual al raster.
3. **Python — cálculos trazables:** procesar tablas con esquemas explícitos, unidades y validaciones; almacenar perfil y aforos originales; producir tabla/figuras y reporte con fuentes. Para cota y desnivel, interpolar el perfil medido solo donde corresponda y usar niveles de agua medidos. Para curva de gasto, ajustar pares simultáneos `h,Q` con límites/diagnóstico de residuos y sin extrapolar fuera del rango aforado.

### Hallazgo de consistencia en los puntos conceptuales existentes

El archivo `02 Datos/coordenadas_infraestructura_mch.csv` contiene cotas/UTM que parecen de anteproyecto y no declara marco horizontal, datum vertical, método ni precisión. Sus diferencias aritméticas son: `CAM-CAR 2417.8 − CAS-MAQ 2302.8 = 115.0 m`; `CAM-CAR − DES-RES 2301.5 = 116.3 m`; `BOC-01 2420.0 − DES-RES = 118.5 m`. Esto hace **plausible como orden de magnitud** el supuesto de 115 m, pero no lo verifica: las cotas registradas no están identificadas como niveles de agua de operación, y el salto bruto requiere nivel aguas arriba menos nivel de restitución en condición definida.

Además, la separación horizontal UTM entre cámara y casa de máquinas es aproximadamente 410 m, mientras la descripción de `TUB-FOR` declara longitud 380 m. Una tubería física no puede ser más corta que la distancia horizontal entre esos extremos: revisar si coordenadas, longitud o alcance corresponden a versiones distintas antes de usarlas. Es discrepancia documental, no evidencia de error de campo.

### Correcciones obligatorias al código conceptual antes de automatizar

- `Hbruto` no es “cota de cámara menos eje/centro de turbina”: usar nivel de agua de cámara/toma menos nivel de agua de cola. El eje de turbina sirve para presión/cota de instalación, no define por sí solo el salto bruto.
- No adoptar `h_k = 0.10 h_f` como pérdida singular definitiva. Calcular `ΣK·V²/(2g)` para cada entrada, rejilla, curva, válvula, transición y descarga con geometría y referencia del fabricante; dejarlo como sensibilidad preliminar si faltan datos.
- El `k_rugosidad=0.0015 m` y `ν=1.007e-6 m²/s` son entradas asumidas (rugosidad alta para algunas tuberías y viscosidad del agua a ~20°C). Usar material/estado/temperatura reales; verificar Reynolds y régimen antes de aplicar Swamee–Jain. Tratar flujo laminar con `f=64/Re`; revisar la zona transicional y no usar fórmula turbulenta fuera de rango.
- Para caudal por velocidad-área no construir cada área como rectángulo `ancho×profundidad` sin definir cómo se delimitan las subsecciones. Registrar estación/distancia transversal y profundidad por vertical; usar áreas parciales por método de sección media (o integración trapezoidal explícita) y velocidades medias representativas, incluida la corrección de una o dos profundidades del protocolo del instrumento. Guardar `q_i=A_i·v_i` y sumar.
- `curve_fit` sin restricciones puede hacer que `h₀` y `a,b` se compensen y produzcan una curva físicamente absurda. Definir datum de mira, justificar/estimar el nivel de control, ajustar con restricciones y ponderaciones apropiadas; inspeccionar residuos, cambios de control e incertidumbre. Exigir `h−h₀>0` para todos los puntos usados. Priorizar la inspección/survey del control hidráulico; estimar `h₀` por ajuste solo si los datos cubren el rango suficiente y reportar incertidumbre/correlación de parámetros, no minimizar RMSE a ciegas.
- No imponer `1.3≤b≤2.5` como regla universal ni reglamentaria. El exponente depende del control, la geometría y el rango de niveles; un intervalo puede servir como alerta inicial cuando lo justifica el control local, pero un valor fuera de él exige revisar mediciones, segmentos, remanso y supuestos en vez de recortarlo automáticamente. Las curvas pueden ser segmentadas si cambia el control; la metodología USGS describe relaciones específicas del sitio y múltiples controles ([USGS](https://www.usgs.gov/mission-areas/water-resources/science/streamgaging-basics), [modelo de curva de potencia segmentada](https://thodson-usgs.github.io/ratingcurve/meta/background.html)).

### Esquema de datos de topografía

La plantilla propuesta en la conversación es buena base, pero separar el archivo de puntos de los metadatos de campaña (o mantener comentarios `#` que todos los importadores sepan ignorar). Para cada campaña registrar CRS horizontal con código EPSG y realización/época cuando aplique; sistema/datum vertical y modelo geoidal o BM de amarre; fecha/hora y método por punto; ID del BM; instrumento; incertidumbre y cómo se expresa (1σ o intervalo/95%); unidades; estación/progresiva y tipo de cota con vocabulario controlado (`terreno`, `solera`, `NAV_operación`, `NAV_mínimo`, `eje_tubería`, `eje_turbina`, `NAV_cola`). No usar `Datum_Vertical=IGN_PERU` sin especificar el control/modelo y la referencia concreta.

Cabecera sugerida: `ID,Punto,Este_m,Norte_m,Cota_m,CRS_Horizontal,Datum_Vertical,Tipo_Cota,ID_BM,Metodo_H,Metodo_V,Incertidumbre_m,Incertidumbre_tipo,FechaHora,Progresiva_m,Descripcion,Archivo_Fuente`. La fecha, EPSG:32719 (si se confirma WGS84/UTM 19S), precisión y cotas del ejemplo recibido son ilustrativas; no copiarlas como metadatos reales. Sus coordenadas/cotas tampoco coinciden con `02 Datos/coordenadas_infraestructura_mch.csv`, por lo que no deben mezclarse con el proyecto hasta confirmar si son un ejemplo o un nuevo emplazamiento.

### Módulo Python disponible

Se integró `scripts/procesamiento_hidraulico.py` con rutinas para cuerda 3D, longitud de polilínea medida, Darcy–Weisbach, potencia, integración de subsecciones y ajuste de una curva de potencia de un solo control. Instalar dependencias desde la raíz con `pip install -r requirements.txt`. Ejemplos:

```bash
python scripts/procesamiento_hidraulico.py --help
python scripts/procesamiento_hidraulico.py cuerda topografia.csv --inicio CAM-01 --fin CAS-MAQ
python scripts/procesamiento_hidraulico.py trazado topografia.csv --tipo-cota eje_tuberia
python scripts/procesamiento_hidraulico.py perdidas --q 0.125 --d 0.25 --l 425 --rugosidad 0.000045 --k-total 0.0
python scripts/procesamiento_hidraulico.py aforo aforo_subsecciones.csv
python scripts/procesamiento_hidraulico.py curva curva_gasto.csv --h-col nivel_m --q-col caudal_m3_s --h0-min 0.0 --h0-max 0.2 --h0-inicial 0.1
```

Los valores del comando de pérdidas son demostrativos, no parámetros aprobados. Sustituir `L` por longitud desarrollada del eje, `K_total` por suma sustentada de accesorios y `h0_bounds` por límites compatibles con la mira y el control levantado. El módulo no segmenta automáticamente curvas ni interpreta datum vertical. El ajuste admite incertidumbre de Q si se entrega `--sigma-col`, pero no propaga incertidumbre de nivel; esas decisiones requieren metadatos, evidencia de campo y revisión hidráulica.

## Primer paquete de campo para enviar aquí

Comenzar por un **levantamiento hidráulico-topográfico de control en la zona de captación y casa de máquinas**, acompañado de un aforo simultáneo. Entregar:

1. Tabla CSV de BM y puntos: `id, fecha_hora, este, norte, cota, datum_horizontal, datum_vertical, método, precisión, descripción`.
2. Perfil longitudinal de la posible tubería con progresiva, coordenadas y elevación; puntos de toma, cámara de carga, eje de turbina, restitución y cruces.
3. Secciones transversales del cauce en toma (una aguas arriba, eje de toma y aguas abajo), con distancia desde margen, cota de lecho y nivel de agua observado.
4. Hoja H-01 del primer aforo, lecturas por subsección, caudal total y lectura de regla tomada en el mismo intervalo; método, equipo y fotos con escala.
5. Fotos georreferenciadas de cauce, marcas de avenida, orillas, ruta de tubería, taludes y accesos; archivos crudos GNSS/estación total/nivelación y croquis.
6. Fecha/hora local, nombre de cuadrilla, instrumento y certificados/calibración disponibles. No enviar solo un punto GPS o un valor de “salto”: necesitamos la referencia vertical, el método y el archivo que permita revisar el cierre.

Con ese primer conjunto se puede comprobar si los 115 m son geométricamente plausibles, reconstruir una primera línea hidráulica y abrir una hoja de incertidumbre. El caudal del día será solo un punto de la futura curva; no valida la serie 2014–2023.

## Referencias técnicas principales

- ANA: [R.J. 007-2015-ANA](https://www.gob.pe/institucion/ana/normas-legales/539001-r-j-007-2015-ana), [TUPA ANA actualizado en 2026](https://www.gob.pe/institucion/ana/informes-publicaciones/5630557-texto-unico-de-procedimientos-administrativos-tupa-de-la-autoridad-nacional-del-agua-ana), [caudal ecológico R.J. 267-2019-ANA](https://www.gob.pe/institucion/ana/normas-legales/537631-rj-267-2019-ana).
- IGN: [norma técnica GNSS estático relativo](https://app8.ign.gob.pe/GestionDocumental/Documento.aspx?id=2634).
- Hidrometría: [USGS Streamgaging Basics](https://www.usgs.gov/mission-areas/water-resources/science/streamgaging-basics) y [manual de medición en estaciones](https://pubs.usgs.gov/tm/tm3-a8/tm3a8.pdf).
- Crecidas: [USACE HEC-HMS, frecuencia e incertidumbre](https://www.hec.usace.army.mil/confluence/hmsdocs/hmsag/flood-frequency-studies/background-for-flood-frequency-studies).
- Ambiental: [SEIA MINAM](https://www.minam.gob.pe/seia/), [listado de inclusión](https://www.gob.pe/institucion/minam/informes-publicaciones/308471-listado-de-inclusion-de-proyectos-de-inversion-sujetos-al-seia), [trámite de clasificación y EVAP](https://www.gob.pe/11396-solicitar-la-clasificacion-de-estudios-ambientales), [D.S. 014-2019-EM](https://sinia.minam.gob.pe/normas/reglamento-proteccion-ambiental-las-actividades-electricas).
- Eléctrico: [CNE Suministro 2011](https://cdn.www.gob.pe/uploads/document/file/95751/RM_214_2011_DM.pdf), [compendio de normas eléctricas MINEM](https://www.gob.pe/institucion/minem/colecciones/26481-normas-tecnicas-de-los-servicios-electricos).
- Equipo: IEC 60041, ensayos de aceptación en campo de turbinas; IEC 60034-1, máquinas eléctricas rotativas. Solicitar la edición vigente en el catálogo IEC al emitir las bases de compra.
