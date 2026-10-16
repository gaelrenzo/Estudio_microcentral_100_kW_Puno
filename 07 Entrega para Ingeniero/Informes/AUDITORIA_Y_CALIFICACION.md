# Auditoría y calificación de prefactibilidad — MCH Río Blanco, 100 kW

**Fecha:** 16 de octubre de 2026<br>
**Alcance:** revisión documental y reproducción de cálculos seleccionados. No es auditoría independiente de datos primarios, visita de campo, aprobación regulatoria ni diseño firmado.

## Dictamen

**Calificación actual: 39/100.** La carpeta ahora presenta una base de cálculo coherente y reproducible para discutir una alternativa conceptual de 100 kW. Sigue siendo insuficiente para afirmar viabilidad, solicitar inversión o tramitar permisos: los insumos críticos no tienen trazabilidad primaria y faltan los estudios de campo y confirmaciones externas. La nota mide la calidad del expediente disponible, no el potencial real del río.

### Rúbrica punto por punto

Cada nota va de 0 a 5. Aporte = peso × nota / 5.

| Área | Peso | Nota / 5 | Aporte | Evaluación actual |
|---|---:|---:|---:|---|
| Alcance y coherencia | 5 | 4.0 | 4.0 | Se identifica como prefactibilidad y se advierte que coordenadas, diseños y resultados son provisionales. Revisar todavía lenguaje y planos heredados que pueden parecer ejecutivos. |
| Hidrología y datos | 20 | 1.0 | 4.0 | La serie tiene 3.652 fechas diarias sin duplicados, nulos ni negativos; fuente, estación, método, aforos, curva de gasto y control de calidad no están acreditados. El mínimo repetido de 0,125 m³/s necesita explicación. |
| Agua y energía | 15 | 2.0 | 6.0 | El script reproduce 862,92 MWh/año y FP 98,51 % con Qeco 30 L/s, Qd 125 L/s, salto bruto 115 m y eficiencia global simplificada. La serie no es verificable; faltan perfil mensual validado, pérdidas parciales, indisponibilidad y restricciones de conexión. |
| Obras, hidráulica y geotecnia | 15 | 1.5 | 4.5 | Hay dimensionamiento preliminar; no hay topografía de campo, geotecnia, hidrogramas de diseño, ensayos ni verificación estructural firmada. El salto 115 m es un supuesto y debe contrastarse con cotas reales. |
| Turbina y generador | 10 | 2.0 | 4.0 | El cálculo arroja 104,43 kW y el generador supuesto admite 100 kW a FP 0,8. No hay ficha/curvas comerciales ni operación garantizada; se requiere coordinación y limitación de potencia. |
| Sistema eléctrico e interconexión | 10 | 1.5 | 3.0 | Se adoptó 400/230 V y transformador conceptual 125 kVA, 0,4/10 kV para uniformar el escenario. Tensión, punto de conexión, protecciones, servidumbre y costos dependen de confirmación de la distribuidora. Planos heredados pueden conservar 380 V o 22,9 kV. |
| Agua, ambiente y permisos | 10 | 1.5 | 3.0 | Se declaran pendientes el derecho de agua, caudal ecológico específico, autorizaciones, evaluación ambiental, propiedad y servidumbres. No se acreditan resoluciones o permisos. |
| Costos y economía | 10 | 2.5 | 5.0 | Se corrigió B/C a VP beneficios / VP costos y se alineó la base con la energía calculada. Resultados: VAN USD 274.741,65; TIR 23,20 %; payback simple 4,29 años; LCOE USD 39,90/MWh; B/C 1,88. CAPEX, OPEX, tarifa y tasa son supuestos sin cotizaciones ni contrato. Sensibilidad ilustrativa, no probabilística. |
| Demanda y beneficios | 5 | 1.0 | 1.0 | Usos productivos se mantienen como hipótesis; faltan encuesta, perfiles horarios, acuerdos, operador y tarifa. Beneficios sociales y emisiones no cuantificados. |
| Trazabilidad y reproducibilidad | 5 | 4.0 | 4.0 | Se corrigieron avisos que presentaban referencias y levantamientos no demostrados como oficiales. Reproducción acotada incluida. Las fuentes primarias siguen faltando; planos/PDF heredados no se regeneraron integralmente. |
| **Total** | **100** |  | **39/100** | **Útil para revisión técnica inicial; no sustenta decisión de inversión ni paso directo a factibilidad.** |

## Mejoras realizadas en esta revisión

1. Cálculo B/C corregido a valor presente de ingresos dividido entre CAPEX más valor presente de OPEX; cambio aplicado al módulo compartido y copia de entrega.
2. El caso económico integrado toma el factor de planta producido por el balance energético, en lugar de imponer 76,8 %.
3. Se ejecutó exclusivamente `reproducir_prefactibilidad.py`: 3.652 registros; Qmedio 0,523 m³/s; Q95 de excedencia 0,126 m³/s; Hn 106,18 m; energía 862,92 MWh/año; VAN USD 274.741,65; TIR 23,20 %; payback 4,29 años; LCOE USD 39,90/MWh; B/C 1,88.
4. Se marcaron como referencias internas no autenticadas seis fichas antes presentadas como documentos oficiales; se eliminan afirmaciones de levantamiento GNSS, monumentación y precisión no respaldadas.
5. Se corrigieron descripciones de energía, economía, demanda y emisiones en el informe/paquete, y se alinearon coordenadas provisionales de la matriz con el CSV del repositorio.

## Pendientes críticos para subir la calidad de la prefactibilidad

1. **Hidrología:** obtener originales y metadatos de estaciones/aforos; confirmar área aportante, periodo, curva de gasto, vacíos, consistencia y origen del piso repetido en 0,125 m³/s. Sin ello no presentar P50/P90.
2. **Campo y terreno:** levantamiento topográfico/GNSS documentado; cotas y trazados; campaña geotécnica; sedimentos, crecidas y estabilidad de obras/anclajes.
3. **Energía y equipos:** modelar caudal ecológico aprobado o justificado, curva de eficiencia, pérdidas dependientes de caudal, disponibilidad, vertimientos, limitación a 100 kW y energía entregable; cotejar con fichas y garantías de fabricante.
4. **Interconexión:** carta de distribuidora con tensión y punto de conexión; estudios de cortocircuito, protecciones, puesta a tierra, calidad, servidumbres y presupuesto de conexión.
5. **Permisos y ambiente:** ruta vigente consultada para autorización de obras en fuente, disponibilidad/licencia de agua, instrumento ambiental y derechos de paso.
6. **Economía y demanda:** metrados/cotizaciones Puno con transporte, contingencia, impuestos, reposiciones, seguros, OPEX desglosado, financiamiento y tarifa/contrato; validar usuarios y perfil horario.
7. **Control de publicación:** revisar las láminas/CAD y compilar anexos derivados antes de distribuirlos, porque no se regeneró el paquete técnico completo en esta revisión.

## Fuentes regulatorias de consulta

- ANA, [R.J. N.° 267-2019-ANA — lineamientos de caudales ecológicos](https://www.gob.pe/institucion/ana/normas-legales/537631-rj-267-2019-ana).
- ANA, [R.J. N.° 007-2015-ANA — procedimiento de derechos y autorizaciones de agua](https://www.gob.pe/institucion/ana/normas-legales/539001-r-j-007-2015-ana).
- MINEM, [preguntas frecuentes del sector eléctrico](https://www.gob.pe/institucion/minem/informes-publicaciones/2147053-preguntas-frecuentes-sector-electrico); confirmar aplicabilidad y texto vigente para la modalidad concreta.

**Criterio de calificación:** subir a 80/100 requiere que las entradas de hidrología, topografía, demanda, costos, permisos e interconexión estén sustentadas; 100/100 no se puede asignar solo por editar documentos y exige validación independiente del alcance acordado.
