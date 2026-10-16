# Prefactibilidad: prueba de estrés y decisión de inversión en estudios

**Propósito de decisión:** determinar si conviene financiar la siguiente etapa de investigación. Este documento no es autorización de obra ni diseño de detalle. Los valores provienen del escenario de prefactibilidad y de alcances propuestos para cotizar.

## 1. Prueba de estrés económico

### Base reproducida

Se usó la serie de 3,652 días 2014–2023 del repositorio y el mismo modelo `src/electrical.py` / `src/economics.py`: 100 kW instalados, `Qeco=30 L/s`, rendimiento global 0.73, tarifa 0.075 USD/kWh, OPEX 3% del CAPEX por año, horizonte 25 años y descuento 10%. La serie y estos parámetros no están validados como datos de diseño.

| Escenario | Energía modelada (MWh/año) | CAPEX (USD) | VAN (USD) | TIR | B/C | LCOE (USD/MWh) |
|---|---:|---:|---:|---:|---:|---:|
| Base publicada | 862.92 | 245,800 | 274,742 | 23.20% | 1.88 | 39.90 |
| Salto bruto 100 m | 770.51 | 245,800 | 211,826 | 20.31% | 1.68 | 44.70 |
| Caudal de diseño 80 L/s | 577.54 | 245,800 | 80,447 | 14.08% | 1.26 | 59.70 |
| CAPEX +30% | 862.92 | 319,540 | 180,921 | 16.91% | 1.45 | 51.90 |
| **Combinado: 100 m, 80 L/s de diseño, CAPEX +30%** | **502.21** | **319,540** | **−64,660** | **7.27%** | **0.84** | **89.20** |

**Lectura directiva:** cada choque aislado conserva VAN positivo bajo el modelo actual. La combinación de los tres cruza el umbral: VAN < 0, TIR < 10% y B/C < 1. La decisión no debe basarse en TIR 23.2% como si fuera una previsión; el caso conjunto prueba que la aparente holgura no cubre incertidumbres correlacionadas.

### Ambigüedad de “80 L/s”

El cálculo principal interpreta 80 L/s como **caudal máximo de diseño de turbina (`Qd`)**, conservando la serie histórica hipotética. Si 80 L/s significa **caudal total del río durante todo el año**, el modelo deja 30 L/s en el cauce y sólo permite turbinar hasta 50 L/s. El escenario constante extremo da aproximadamente 361 MWh/año y VAN de −66,974 USD al salto 115 m y CAPEX base; al combinar 100 m y CAPEX +30%, VAN ≈ −192,878 USD. No debe confundirse esta condición permanente con un estiaje de duración desconocida: para valorar un estiaje real hace falta la curva de duración y cuántos días persiste ese caudal.

### Límites que afectan la prueba

- El cálculo mantiene la arquitectura de energía del expediente; `energia_anual()` aplica el salto bruto y no resta las pérdidas de la tubería día por día. Por eso la energía/finanzas pueden ser optimistas. La longitud 380 m, D interior 250 mm, rugosidad y pérdidas locales tampoco están acreditados.
- No se modificaron tarifa, demanda, impuestos, reemplazos, financiación, indisponibilidad, curva de eficiencia por carga, pérdidas de evacuación ni costo de conexión. El OPEX sigue siendo 3% del CAPEX. La prueba es un estrés parcial, no un caso bancable.
- Reproducción: `python '07 Entrega para Ingeniero/analisis_sensibilidad_prefactibilidad.py'`. Resultados en `07 Entrega para Ingeniero/data/sensibilidad_extrema.csv`.

## 2. TDR base para cotizar los estudios

Los siguientes son mínimos propuestos para solicitar ofertas comparables. No son cantidades normativas universales; el consultor deberá ajustar el programa y justificar cambios antes de movilizarse.

### 2.1 Topografía y geodesia

**Cantidad base de licitación: hasta 8 ha**, con pago por hectárea adicional y por metro de eje adicional. La cifra no puede declararse como el área exacta del proyecto mientras el eje sólo sea conceptual. Antes de adjudicar, el topógrafo debe dibujar el polígono GIS de trabajo y cerrar el metrado contractual.

- Cubrir el canal conceptual (≈450 m), tubería de presión (≈380 m), restitución, accesos y alternativas de alineamiento. Para traza: corredor mínimo de 25 m a cada lado del eje propuesto; ampliar en curvas, cruces, taludes, alternativas y huella de obras.
- Reservar áreas de detalle para bocatoma, desarenador, cámara de carga y casa de máquinas; levantar cauce y márgenes. Secciones transversales de control en toma y restitución, aguas arriba/abajo, hasta cubrir el cauce y la planicie que controle niveles de avenida.
- Monumentar dos BM fuera de zona inundable; enlazar a marco geodésico y datum vertical identificados. Entregar EPSG, modelo geoidal/referencia vertical, época, método, cierres, precisiones y RINEX/archivos crudos. No aceptar “Datum IGN” sin materializar la referencia y su vínculo.
- Productos: nube/puntos XYZ con códigos; poligonales y nivelación; perfiles y secciones; TIN/DEM; curvas de nivel; ortofoto si se ofrece; DWG/DXF y GeoPackage; memoria de control y reporte de precisión. Escala objetivo 1:500 en estructuras y 1:1,000 en corredor, sujeta al relieve y a la precisión ofertada.
- Aceptación: cierres reportados, controles independientes, perfiles con puntos de quiebre y cambios de pendiente, láminas de agua medidas (no sustituidas por cotas de terreno), sistema de unidades coherente y archivos crudos reproducibles.

### 2.2 Geotecnia

Programa para oferta: **14 calicatas de hasta 3 m como mínimo operativo o hasta rechazo/agua/roca**, lo que ocurra primero, con permiso y estabilidad de excavación; ampliar profundidad si la influencia de la cimentación lo requiere. En cauce activo, sustituir por perforación o exploración segura, no abrir excavación insegura.

| Área | Cantidad inicial | Ubicación / propósito |
|---|---:|---|
| Bocatoma y barraje | 3 | Márgenes y huella de cimentación; aluvial, roca, filtración y socavación. |
| Desarenador | 2 | Huella y zona de purga/descarga. |
| Cámara de carga | 2 | Huella, relleno/corte y estabilidad de talud. |
| Casa de máquinas | 3 | Esquinas/huella y apoyo del grupo turbina-generador. |
| Tubería/anclajes | 4 | Codos/anclajes y cambios geológicos o zonas inestables de la ruta. |

Incluir **3 perforaciones geotécnicas de hasta 8 m iniciales** en estructuras de mayor carga (casa de máquinas, bocatoma y cámara de carga), profundizadas si no se alcanza estrato competente o si la zona de influencia de cimentación continúa. En roca, recuperación de testigo, RQD y descripción de discontinuidades. Si SPT no es apto por bolones/refusal, proponer alternativa en vez de reportar rechazo como resistencia.

Ensayos: registro estratigráfico y nivel freático; humedad, granulometría, límites de Atterberg cuando aplique, densidad; corte directo/triaxial según suelo; permeabilidad; química de suelo/agua para durabilidad; roca UCS o índice de carga puntual si corresponde. El informe debe calcular capacidad portante/asentamientos y estabilidad, dar parámetros característicos, indicar limitaciones y recomendar cimentación, drenaje, excavabilidad y sostenimiento. Geofísica MASW/refracción como partida opcional condicionada a la geología.

### 2.3 Hidrología y aforos

- Instalar regla limnimétrica referida al BM y un registrador continuo de nivel con intervalo objetivo de 15 minutos; operación de **12 meses que cubran un ciclo hidrológico completo**. La regla, sensores, reloj, mantenimiento, telemetría y respaldo de datos deben describirse y cotizarse.
- Ejecutar **15–20 aforos velocidad-área** distribuidos entre estiaje, transición y avenida; aumentar visitas durante cambios rápidos de nivel y registrar marcas de avenida. No se exige arriesgar personal durante crecidas.
- Registrar aforo simultáneo a nivel, método/equipo/calibración, incertidumbre, geometría de sección, fechas/UTC, fotos, condiciones del cauce y usos aguas arriba/abajo. Entregar aforos crudos y curva de gasto por tramos/control, residuos, incertidumbre y rango de extrapolación.
- Contrastar la serie histórica original con SENAMHI/ANA y documentar fuente. No convertir 10 años hipotéticos ni un aforo puntual en caudal firme. Estimar avenidas por más de un método y marcar explícitamente incertidumbre.

**Cronograma mínimo:** instalación y línea base en el mes 0; control mensual y aforos en cada visita; informe preliminar al mes 3; cierre hidrológico al completar 12 meses y ciclo estacional; actualización de modelo y disponibilidad hídrica después del cierre. Si el cronograma inversor no permite esperar 12 meses, el resultado debe denominarse provisional y usar regionalización/estaciones vecinas documentadas.

## 3. Presupuesto de desarrollo para el gate de inversión

No hay cotización de consultor para este proyecto. El presupuesto es de **orden de magnitud para solicitar propuestas**, no una oferta ni precio oficial. Como referencia local, documentos de requerimientos del Gobierno Regional de Puno 2025 muestran montos de S/17,500–40,000 para levantamientos topográficos/RTK y productos afines, y partidas de suelos de aproximadamente S/17,600–39,000; los alcances no son idénticos y no deben tratarse como tarifa por hectárea ([GORE Puno, requerimiento 2025](https://www.regionpuno.gob.pe/wp-content/uploads/2025/09/0001029344_1_0001029250.pdf), [GORE Puno, costos de estudios 2025](https://www.regionpuno.gob.pe/wp-content/uploads/2025/06/0000779936_1_ANEXO4CMNVERSIONN02F.pdf)).

| Paquete | Alcance | Rango de planificación (USD) |
|---|---|---:|
| Gate 0: screening de decisión | Conciliar ubicación/ejes, preconsulta GIS, revisar serie y modelo, cotizar TDR, visita de reconocimiento y uno o dos aforos; no incluye año hidrológico ni diseño de detalle. | **10,000–25,000** |
| Gate 1: factibilidad de sitio | Topografía/geodesia hasta 8 ha; programa geotécnico inicial; instrumentación y ciclo hidrológico/aforos; balances de agua/energía; alternativa civil/electromecánica; screening predial y ambiental; expediente de acreditación hídrica a nivel requerido. | **30,000–60,000** |
| Gate 2: factibilidad cerrada y diseño de detalle | Diseños civiles/estructurales e hidráulicos coordinados, transitorios, especificaciones/cotizaciones, interconexión, permisos y expediente ambiental según clasificación, metrados/APU, planos IFC y soporte de revisión. | **60,000–110,000** |

Los rangos son secuenciales y no deben sumarse mecánicamente si se contrata un paquete integrado; Gate 0 es la primera autorización de fondos y evita comprometer de inmediato el Gate 2. Equivalencia presupuestal orientativa: **S/3.39 por USD** según serie de venta interbancaria consultada del BCRP al 15–16/10/2026; actualizar al contratar ([BCRP, serie diaria de tipo de cambio](https://estadisticas.bcrp.gob.pe/estadisticas/series/diarias/tipo-de-cambio)).

El pago administrativo ANA no sustituye el estudio técnico ni honorarios. La ficha estatal publicada muestra S/238.10 para acreditación (procedimiento 13), pero la página del TUPA ANA lista modificaciones posteriores; confirmar tasa, procedimiento y anexos vigentes al presentar ([trámite ANA](https://www.gob.pe/10824-obtener-la-acreditacion-de-disponibilidad-hidrica-para-el-otorgamiento-de-derechos-de-uso-de-agua), [TUPA ANA](https://www.gob.pe/institucion/ana/informes-publicaciones/5630557)). Para ambiente, no presupuestar DIA automáticamente: el titular pide clasificación con EVAP si aplica a su tipología y la autoridad determina el instrumento ([clasificación de estudios eléctricos](https://www.gob.pe/30652-solicitar-la-clasificacion-de-estudios-ambientales-para-proyectos-electricos-al-gobierno-regional), [DGAAE-MINEM](https://www.gob.pe/7787-ministerio-de-energia-y-minas-direccion-general-de-asuntos-ambientales-de-electricidad)).

## 4. Restricciones fatales: pre-screen geoespacial

**Resultado actual: ninguna restricción queda descartada ni confirmada.** El CSV de coordenadas está marcado como conceptual; son puntos de infraestructura, no polígono topográfico ni eje completo, y no define las áreas temporales/permanentes. Un mapa base o una búsqueda por punto no da prueba predial ni autorización. Por esa razón no se declara “sin superposición”.

| Visor/tema | Qué se revisará cuando se cierre el polígono | Hallazgo que sería alerta; por qué no es automáticamente fatal |
|---|---|---|
| [GEOCATMIN / Catastro Minero](https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_CATASTRO_MINERO_WGS84/MapServer) | Intersección de toma, casa y corredor con polígonos; código, titular, estado y vigencia del derecho minero; revisar concesiones tituladas, trámites y áreas restringidas. El servicio dice actualización diaria y carácter referencial ([INGEMMET REST](https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_CATASTRO_MINERO_WGS84/MapServer)). | Un derecho minero no es título de propiedad superficial; una intersección exige análisis de actividad, acceso, compatibilidad y acuerdos, no rechazo automático ([MINEM, Resolución 482-2022](https://cdn.www.gob.pe/uploads/document/file/3739247/482%20CP%20CINCO%20B.pdf.pdf)). |
| [SIGRID / CENEPRED](https://sigrid.cenepred.gob.pe/) | Superposición con susceptibilidad y escenarios de movimientos en masa, inundaciones y peligros publicados; guardar fecha, capa, escala y metadatos. SIGRID es una plataforma estatal de consulta de peligros/riesgos ([descripción oficial](https://sigrid.cenepred.gob.pe/sigridv3/documento/14901)). | La susceptibilidad cartográfica no certifica estabilidad de una ladera; alerta alta requiere reconocimiento geológico, topografía y estudio geotécnico. La ausencia de polígono de riesgo no significa ausencia de peligro. |
| [SICAR / MIDAGRI](https://georural.midagri.gob.pe/sicar/) | Preparar polígono corredor, estructuras, accesos y áreas auxiliares; revisar predios rurales, comunidades campesinas/nativas y servidumbres mapeadas. El visor publica capas de predio rural y comunidades, con actualización por entes generadores/GORE ([SICAR](https://georural.midagri.gob.pe/sicar/), [Geoportal MIDAGRI en IDEP](https://www.idep.gob.pe/wms/wms_minagri.html)). | Capa gráfica es screening, no certificado registral ni consentimiento comunal. Confirmar partidas/SUNARP, títulos y actas con propietarios/comunidad; verificar ocupantes y derechos de uso.

Para cerrar el pre-screen, el topógrafo entregará polígono GIS del corredor y las cuatro huellas de obra con CRS confirmado; luego un especialista repetirá intersecciones, conservará mapa/fecha/fuente y abrirá consultas formales donde exista traslape. También deben verificarse faja marginal/ANA, áreas protegidas, arqueología, bosques/zonas frágiles y usuarios de agua: no quedan cubiertos por los tres visores anteriores.

## 5. Recomendación de gate

1. **Autorizar únicamente Gate 0 (USD 10k–25k) con entregables contractuales**: reconciliar coordenadas/ruta, mapa oficial documentado, revisión del modelo y datos originales, TDR cotizados, primera topografía de control y aforos de reconocimiento. No pagar todavía diseños completos.
2. **Condiciones para pasar a Gate 1:** no encontrar imposibilidad evidente de acceso/superficie; punto de conexión exploratoriamente viable; alternativas hidráulicas plausibles; términos de referencia cotizados; CAPEX del estudio financiable.
3. **Condición financiera:** con las premisas del modelo, los escenarios aislados superan VAN=0; el caso combinado lo cruza. Por tanto la prefactibilidad justifica comprar información de manera escalonada, pero no respalda aún inversión de construcción.
4. **Detener/replantear** si la revisión de caudal ecológico y usos aguas arriba deja caudal turbinable insuficiente, si no se obtiene corredor superficial viable, si el sitio cae en un peligro mitigable sólo a costo desproporcionado, si la interconexión requiere inversión que destruya el VAN, o si ofertas reales elevan simultáneamente CAPEX y estudios por encima de la capacidad financiera.

**Decisión sugerida hoy:** sí vale la pena gastar en la primera etapa de información (Gate 0), condicionada a un tope de USD 25,000 y a hitos de parada. No hay base para contratar directamente el expediente de detalle ni para sostener el 23.2% como rendimiento esperado.
