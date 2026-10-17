# Paquete para revisión del ingeniero

**Proyecto:** MCH Río Blanco, Ollachea, Puno — 100 kW<br>
**Etapa:** prefactibilidad; documento de trabajo para revisión profesional<br>
**Fecha de emisión:** 16 de octubre de 2026

## Lectura recomendada

1. `Resumen_para_revision_del_ingeniero.pdf` (o DOCX): alcance, cifras de referencia y decisiones que requieren validación.
2. `Informe_Prefactibilidad_MCH_100kW.pdf`: informe principal.
3. `Anexo_Hidrologia.pdf`: registro y tratamiento hidrometeorológico incorporado al estudio.
4. `Informes/AUDITORIA_Y_CALIFICACION.md`: evaluación punto por punto, nota ponderada y acciones prioritarias.
5. `Informes/ESTADO_PREFACTIBILIDAD.md` y `Informes/MATRIZ_TRAZABILIDAD.md`: límites, trazabilidad y asuntos abiertos.
6. `Decision_prefactibilidad_prueba_estres_TDR.md`: prueba de estrés, TDR de cotización, presupuesto por etapas y estado del pre-screen de restricciones fatales.
7. `TDR_Estudios_Gate_0.md`: bases para solicitar cotizaciones por topografía, hidrología y geotecnia, con Gate 0 separado de las campañas ampliadas.
8. `Matriz_Restricciones_Fatales.csv`: registro editable de alertas, evidencias y decisiones de Gate 0.
9. `Presentacion_Directiva_MCH_Rio_Blanco.pdf/.pptx`: presentación ejecutiva de 10 diapositivas, lista para exponer y editable.
10. `TDR_Estudios_Gate_0.pdf/.docx` y `Decision_Gate_0.pdf/.docx`: versiones de lectura y editables para cotizar y revisar con el ingeniero.

## Expediente académico por capítulos

- `Informe_Expediente_Completo_MCH_Rio_Blanco_100kW.pdf/.tex`: expediente amplio de 65 páginas; incluye capítulos I–XI, matriz de revisiones, tablas de cálculos y presupuesto APU, y anexos disponibles. Cada capítulo comienza en hoja nueva.
- `Capitulos_I_II_MCH_Rio_Blanco.pdf/.docx`: Capítulo I, Memoria Descriptiva; Capítulo II, Cálculos Justificativos.
- `ESTRUCTURA_EXPEDIENTE_MCH.pdf/.docx/.md`: índice adaptado al formato de expediente con los capítulos I–XI y referencias a los anexos disponibles. Las partes pendientes de estudios de campo se identifican como tales.
- `Presentacion_Academica_MCH_Rio_Blanco_100kW.pptx`: exposición académica de 13 diapositivas basada en la memoria.
- `GUIA_CAPITULOS_Y_GUION.md`: temas y guion oral para la sustentación.

El formato toma como referencia expedientes académicos de instalaciones eléctricas, adaptando la secuencia a una microcentral hidroeléctrica. El contenido permanece en prefactibilidad; el índice no convierte los planos ni cálculos preliminares en documentos constructivos.

## Reproducir los cálculos del escenario

Desde esta carpeta, con Python instalado:

```bash
pip install -r requirements-prefactibilidad.txt
python reproducir_prefactibilidad.py
```

El script lee `data/series_caudales_diarios_historicos_2014_2023.csv` y los módulos incluidos en `src/`. Reproduce el cálculo hidrológico, hidráulico, energético y una evaluación económica de escenario. No genera planos ni reemplaza una revisión de ingeniería.

## Material ejecutivo y documentos de procura

Para regenerar la presentación y las versiones PDF/DOCX desde los Markdown:

```bash
pip install -r requirements-presentacion.txt
python crear_material_presentacion.py
```

Se requiere LibreOffice instalado para convertir los documentos DOCX a PDF. El script fuente queda junto a los archivos generados.

Para reproducir las sensibilidades de salto, caudal y CAPEX:

```bash
python analisis_sensibilidad_prefactibilidad.py
```

La tabla se guarda en `data/sensibilidad_extrema.csv`. Los escenarios son pruebas de escritorio sobre la serie no validada, no pronósticos.

## Contenido

- `Datos/`: metadatos recibidos. Los CSV usados en la reproducción se conservan una sola vez en `data/`.
- `data/` y `src/`: insumos y módulos mínimos del script, disponibles también para inspección.
- `Informes/`: auditoría/calificación, estado de prefactibilidad y matriz de trazabilidad.
- `Informe_Prefactibilidad_MCH_100kW.pdf` y `Anexo_Hidrologia.pdf`: documentos técnicos.
- `Resumen_para_revision_del_ingeniero.docx/.pdf`: nota de presentación editable y lista de revisión.
- `Presentacion_Directiva_MCH_Rio_Blanco.pdf/.pptx`: deck ejecutivo.
- `TDR_Estudios_Gate_0.pdf/.docx` y `Decision_Gate_0.pdf/.docx`: paquete de procura y decisión Gate 0.

## Estado y límites

Las cifras son resultados de un escenario sobre insumos aún no validados en campo. La serie diaria de caudales no incluye evidencia suficiente de origen, aforo, control de calidad ni representatividad. No asumir disponibilidad hídrica, derechos de agua, aprobación de caudal ecológico, interconexión, presupuesto cotizado ni viabilidad financiera. El paquete no es ingeniería de detalle, expediente de permisos ni autorización para construir.
