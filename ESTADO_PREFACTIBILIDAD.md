# Estado de la prefactibilidad — MCH Río Blanco, 100 kW

## Alcance

Este es un estudio de **prefactibilidad** para una central hidroeléctrica de 100 kW. Los diseños, mapas, presupuestos e indicadores del repositorio son alternativas y estimaciones preliminares; no equivalen a ingeniería de detalle, permisos obtenidos ni una decisión de inversión.

## Hallazgos que deben leerse junto con los resultados

- **Hidrología:** el CSV contiene 3.652 valores diarios para 2014–2023. Las copias de data/ y 02 Datos/ tienen el mismo SHA-256, pero el repositorio no incluye las fuentes primarias, archivos descargados, certificados, curvas de gasto ni controles de calidad que permitan verificar su atribución a estaciones y aforos. La serie debe tratarse como **provisional**, no como dato medido acreditado.
- **Energía:** ejecutando src/electrical.py con ese CSV se obtienen **862,92 MWh/año** y factor de planta 98,51 %, con 115 m de salto bruto, eficiencia global 0,73, caudal ecológico supuesto de 30 L/s, límite de 125 L/s turbinados y tope de 100 kW. El caso económico existente en src/main.py fija el factor en 76,8 % y produce **672,77 MWh/año**; es un escenario distinto, no la salida económica de la simulación hidrológica.
- **Ejecución integrada de prefactibilidad:** al pasar a la evaluación económica el factor calculado por el modelo hidrológico, con CAPEX USD 245.800, OPEX 3 %, tarifa USD 0,075/kWh, horizonte 25 años y descuento 10 %, se obtienen VAN USD 274.741,65; TIR 23,20 %; payback 4,29 años; LCOE USD 39,90/MWh y B/C 2,12. Son resultados de escenario sobre datos provisionales, no una recomendación de inversión.
- **Potencia:** el cálculo preliminar de la turbina entrega 104,43 kW a la salida modelada. Un generador de 125 kVA con factor de potencia 0,8 corresponde a 100 kW activos nominales; por ello 104,43 kW no debe describirse como potencia neta entregada a red. La compatibilidad del punto de operación necesita ajuste de diseño y selección de equipos.
- **Caudal ecológico:** los 30 L/s son una hipótesis del caso. No se demuestra un cálculo específico del tramo ni una aprobación de ANA. La determinación debe seguir los lineamientos aplicables y considerar la disponibilidad mensual y los usos existentes.
- **Economía:** CAPEX de USD 245.800, tarifa de USD 0,075/kWh, OPEX del 3 % y tasa de descuento del 10 % son entradas del caso económico. Sin cotizaciones, estudio de mercado, costos de conexión, impuestos, contingencias y financiamiento, VAN, TIR, payback y LCOE son solo indicadores ilustrativos.
- **Ubicación e ingeniería:** coordenadas, topografía, geotecnia, hidrología de diseño, crecidas, caudal ecológico, servidumbres, demanda, conexión y trazados requieren contraste de campo y con las entidades/operadores competentes. Los planos son conceptuales y no aptos para construcción.

## Cierre de prefactibilidad recomendado

Antes de afirmar viabilidad, sustituir o validar la serie con registros trazables, recalcular la curva de duración y la energía mensual con pérdidas y caudal ecológico aprobado, armonizar turbina-generador-transformador, y actualizar el CAPEX con cotizaciones y alcance completo. Después, completar reconocimiento topográfico, geotécnico, ambiental, social, de derechos de agua y de interconexión. La decisión de pasar a factibilidad debe basarse en esos resultados.

## Fuentes normativas de referencia

- [ANA — Resolución Jefatural N.° 267-2019-ANA, lineamientos generales para determinar caudales ecológicos](https://www.gob.pe/institucion/ana/normas-legales/537631-rj-267-2019-ana).
- [ANA — Ley N.° 29338, Ley de Recursos Hídricos](https://www.ana.gob.pe/sites/default/files/publication/files/ley_29338_0.pdf).
- [El Peruano — modificación del marco de la Ley de Concesiones Eléctricas para generación RER](https://busquedas.elperuano.pe/api/visor_html/1938549-1).

Estas referencias orientan la revisión; no sustituyen la consulta del texto vigente ni el pronunciamiento de la autoridad para el proyecto concreto.
