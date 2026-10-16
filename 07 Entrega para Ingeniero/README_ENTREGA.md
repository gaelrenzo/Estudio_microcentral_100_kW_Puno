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

## Reproducir los cálculos del escenario

Desde esta carpeta, con Python instalado:

```bash
pip install -r requirements-prefactibilidad.txt
python reproducir_prefactibilidad.py
```

El script lee `data/series_caudales_diarios_historicos_2014_2023.csv` y los módulos incluidos en `src/`. Reproduce el cálculo hidrológico, hidráulico, energético y una evaluación económica de escenario. No genera planos ni reemplaza una revisión de ingeniería.

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

## Estado y límites

Las cifras son resultados de un escenario sobre insumos aún no validados en campo. La serie diaria de caudales no incluye evidencia suficiente de origen, aforo, control de calidad ni representatividad. No asumir disponibilidad hídrica, derechos de agua, aprobación de caudal ecológico, interconexión, presupuesto cotizado ni viabilidad financiera. El paquete no es ingeniería de detalle, expediente de permisos ni autorización para construir.
