# Plantillas para la campaña de campo

Copiar los CSV completados directamente a `data_campo/` antes de ejecutar `main.py`. Los archivos dentro de `plantillas/` no se procesan.

## Topografía

Completar `topografia_plantilla.csv` con puntos levantados en un único sistema de referencia. Incluir puntos del eje con `Tipo_Cota=Eje_Tuberia`, más dos puntos de lámina de agua cuyo texto en `Punto` coincida exactamente con los argumentos del programa (por ejemplo, `NAV_BOC` y `NAV_COLA`). No confundir solera, terreno o eje de turbina con nivel de agua.

Reemplazar todos los metadatos vacíos. Declarar el CRS horizontal con su EPSG cuando se haya confirmado y registrar la referencia vertical concreta, BM utilizado, método y precisión. “IGN” o “WGS84 / Zona 19S” sin EPSG, control vertical y método no bastan para validar cotas. No copiar coordenadas ni cotas de ejemplos.

La polilínea se calcula con coordenadas 3D de puntos `Eje_Tuberia` ordenados por `Progresiva_m`; levantar suficientes puntos intermedios para representar curvas y cambios de dirección.

## Aforo

Completar `aforo_plantilla.csv` con una fila por vertical de medición, desde ambas márgenes. Registrar distancias crecientes, profundidad y velocidad medida a `0.6d` según el método y equipo aplicables. Añadir simultaneidad, fecha/hora, sección, equipo, calibración, operador y unidades en el acta/archivo fuente asociado; no alterar las lecturas crudas.

La integración del formato actual es una aproximación trapezoidal por intervalos. Un aforo aislado no determina disponibilidad hídrica ni caudal de diseño.

## Ejecución

Al tener exactamente un CSV topográfico completo y un CSV de aforo en la raíz de `data_campo/`, usar `python main.py --help` y proporcionar los identificadores reales de los niveles de agua y parámetros respaldados por medición, cálculo o ficha técnica. El reporte es preliminar y no convierte los insumos en diseño aprobado.
