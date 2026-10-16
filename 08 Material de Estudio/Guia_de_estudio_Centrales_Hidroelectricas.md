# Guía de estudio — Centrales hidroeléctricas

**Ruta de refuerzo para el curso**

**Aplicación:** microcentral hidroeléctrica de referencia de 100 kW, Río Blanco, Ollachea, Puno

**Duración sugerida:** 8 semanas · 5–6 horas por semana

**Nivel:** pregrado, con énfasis en prefactibilidad y diseño conceptual

> **Propósito.** Aprender a pasar de datos de cuenca y topografía a una estimación defendible de potencia, energía y riesgos. Los valores del caso Río Blanco que aparecen aquí son hipótesis didácticas del expediente: no acreditan disponibilidad hídrica, salto medido, rentabilidad ni autorización de diseño.

## Cómo usar la guía

Cada semana combina lectura, resolución manual y una entrega corta. Mantén una hoja de cálculo con unidades y fuentes; no copies un resultado sin poder reconstruirlo. Cuando un dato no esté medido, márcalo como supuesto y evalúa un rango.

## Ruta de ocho semanas

| Semana | Tema | Qué debes poder hacer | Entrega sugerida |
|---|---|---|---|
| 1 | Sistemas hidroeléctricos y balance de energía | Dibujar el esquema desde la cuenca hasta la red y distinguir potencia de energía | Diagrama de una central de pasada con variables y fronteras |
| 2 | Hidrología, aforos y caudal firme | Revisar una serie, ordenar una curva de duración y distinguir caudal del río, ecológico y turbinable | CDC explicada y lista de datos faltantes |
| 3 | Hidráulica y conducción | Calcular velocidad, Reynolds, pérdidas distribuidas/locales y salto neto | Comparación de dos diámetros de tubería |
| 4 | Turbinas y energía | Justificar una familia de turbina con salto, caudal, velocidad específica y curvas de fabricante | Ficha técnica preliminar con condiciones garantizadas |
| 5 | Obras civiles, sedimentos y geotecnia | Explicar captación, desarenador, cámara de carga, aliviadero y fundaciones | Croquis hidráulico con riesgos y exploraciones necesarias |
| 6 | Transitorios y seguridad | Estimar el orden de magnitud del golpe de ariete y enumerar protecciones | Nota de cálculo conceptual y límites del método |
| 7 | Generador, transformación e interconexión | Calcular magnitudes trifásicas y bosquejar la cadena de protecciones | Diagrama unifilar conceptual y lista de consultas a distribuidora |
| 8 | Economía, incertidumbre e integración | Construir escenarios, reconocer sensibilidad y emitir recomendación de avance | Dictamen breve Go / Hold / No-Go con evidencia pendiente |

## 1. Conceptos de sistema que debes dominar

Una central de pasada toma una fracción del caudal, la conduce hasta una turbina y devuelve el agua al cauce. Su cadena funcional es:

**cuenca → captación → desarenado → conducción / cámara de carga → tubería forzada → turbina → generador → transformador → punto de conexión → restitución**

- **Salto bruto,** (H_b): diferencia entre niveles de agua aguas arriba y aguas abajo para el estado analizado.
- **Salto neto,** (H_n): energía por unidad de peso disponible en la turbina después de pérdidas hidráulicas y diferencias de velocidad/presión pertinentes.
- **Caudal de río,** (Q_r): flujo que pasa por la sección natural.
- **Caudal ecológico,** (Q_e): requerimiento que debe respetarse conforme a la determinación y autorización aplicable.
- **Caudal turbinable,** (Q_t): agua efectivamente derivable, limitada por disponibilidad, permisos, conducción y equipo. Una aproximación de balance es (Q_t = min(Q_d, Q_r-Q_e-Q_otros)), con cada término definido para el mismo instante.
- **Potencia,** kW: tasa instantánea de conversión de energía. **Energía,** kWh o MWh: potencia integrada en el tiempo.
- **Potencia instalada** no es producción firme. Una turbina de 100 kW no genera 100 kW todo el año si el caudal o la disponibilidad son menores.

## 2. Hidrología e hidrometría

### Serie y control de calidad

Antes de ajustar un modelo, confirma quién midió, dónde, con qué método, en qué unidad, con qué calendario y si los valores son observados, estimados o simulados. Revisa fechas duplicadas o faltantes, valores imposibles, cambios de estación/instrumento, consistencia con estaciones vecinas y saltos por cambios de régimen. La doble masa ayuda a identificar cambios relativos, pero no demuestra por sí sola que una serie sea correcta.

No rellenes vacíos sin conservar la serie original, el método de completación y una bandera de dato estimado. Para avenidas, diez años no permiten inferir con alta confianza eventos de retorno de 50 o 100 años: hay que combinar registros, regionalización y modelación, y reportar incertidumbre.

### Aforo y curva de gasto

La medición velocidad-área divide una sección en subsecciones y suma (Q = Σ A_i v_i). Mide geometría y velocidades de forma que representen la sección; registra fecha, nivel simultáneo, equipo, calibración, método, fotos y condiciones del cauce. En un cauce cambiante, repite aforos y revisa la curva después de crecidas o cambios de control.

Una curva potencial como (Q = a(h-h_0)^b) es empírica y solo se usa dentro del rango de niveles con respaldo suficiente. Si cambian el control hidráulico o la geometría, puede hacer falta una curva por tramos. No extrapoles una curva como si fuera observación.

### Curva de duración de caudales (CDC)

Ordena los caudales de mayor a menor y calcula el porcentaje de tiempo en que cada valor se iguala o supera. La CDC ayuda a ver cuánto tiempo hay agua para operar, pero pierde el orden cronológico: no describe por sí sola la duración de sequías, rampas, estacionalidad ni secuencia de bajos caudales. Complementa con series temporales y balances por mes/estación.

Para potencia firme, define primero el criterio de confiabilidad y el balance de agua. No confundas (Q_30), (Q_90), promedio anual, caudal de diseño de turbina y caudal mínimo ecológico.

## 3. Hidráulica de la conducción

### Ecuaciones esenciales

- Área de tubería circular: **A = πD²/4**.
- Velocidad media: **v = Q/A**.
- Reynolds: **Re = vD/ν**, con viscosidad cinemática ν según temperatura.
- Darcy–Weisbach: **hf = f(L/D)(v²/(2g))**.
- Pérdidas locales: **hm = Σ[Ki(vi²/(2g))]**. Usa el diámetro/velocidad de cada accesorio cuando corresponda.
- Balance conceptual: **Hn ≈ Hb − hf − hm − hotros**. La memoria final debe cerrar el balance entre niveles, presión y velocidad.
- Potencia eléctrica estimada: **Pe = ρgQtHn × ηt × ηg × ηtr × ηaux**. Si las eficiencias ya están combinadas, aplícalas una sola vez.

El factor (f) se obtiene con Colebrook–White o una aproximación explícita válida para el régimen y rugosidad relativos. Swamee–Jain puede servir en turbulencia; verifica Reynolds, unidades y dominio de aplicación. No uses una rugosidad única para todos los materiales ni una proporción arbitraria de pérdidas singulares si ya puedes definir los accesorios y sus (K).

### Decisión de diámetro

Al aumentar (D), disminuyen la velocidad y las pérdidas, pero suben el costo de tubería, válvulas y montaje. Compara alternativas usando presión de diseño, clase/espesor, soporte, transitorios, costos instalados y energía anual. La longitud hidráulica es la longitud del eje realmente instalado y su trazado, no necesariamente la distancia planar ni una cuerda 3D entre extremos.

## 4. Turbinas, generador y rendimiento

Para seleccionar turbina necesitas rango de salto neto y caudal operativo, variación estacional, sólidos, velocidad de giro, eficiencia en carga parcial, condiciones de instalación y curva garantizada del proveedor. Un salto alto y caudal moderado suele orientar a evaluar Pelton, pero el nombre de la turbina no sustituye la selección con curvas y condiciones de compra. Compara alternativas y solicita garantías de potencia, eficiencia, cavitación/erosión, rango operativo, pruebas y tolerancias.

La potencia hidráulica disponible antes de pérdidas de conversión es P_h=ρ gQH. La potencia eléctrica cambia con salto, caudal y rendimiento en el punto de operación. No supongas eficiencia nominal constante en toda la curva.

Para un generador síncrono:

- Velocidad síncrona: **ns = 120f/p**, rpm, donde p es el número de polos.
- Potencia aparente trifásica: **S = √3 × VLL × IL**.
- Potencia activa trifásica: **P = √3 × VLL × IL × cosφ**.

Revisa factor de potencia, clase de aislamiento, elevación de temperatura, excitación, regulación de tensión, cortocircuito, puesta a tierra y comportamiento ante rechazo de carga. La capacidad del transformador debe coordinar con potencia aparente, armónicos/servicios auxiliares y condiciones de sobrecarga aplicables.

## 5. Obras hidráulicas, sedimentos y geotecnia

- **Captación:** deriva caudal controlando entrada de sólidos y manteniendo el paso del agua excedente. Analiza niveles, avenidas, socavación, rejillas y acceso de mantenimiento.
- **Desarenador:** dimensiona para el tamaño de partícula objetivo, caudal, temperatura/viscosidad, velocidad de sedimentación, longitud útil, purga y manejo de descarga. Declara qué fracción de sedimento se busca remover.
- **Cámara de carga:** estabiliza la alimentación, aloja rejilla y rebose, reduce entrada de aire y permite operación segura. Revisa niveles mínimos/máximos, oscilaciones y vaciado.
- **Aliviadero:** deriva excedentes con caudal de diseño sustentado por hidrología, tránsito/atenuación cuando aplique, resguardo, disipación y protección frente a erosión.
- **Tubería y anclajes:** revisa empujes en codos, apoyos, juntas, expansión térmica, drenaje, interacción suelo-tubería, presión estática y transitoria.
- **Fundaciones:** exploración y ensayos deben responder a las cargas y mecanismo de falla. Calicatas no sustituyen perforación donde se requiere conocer estratos profundos; SPT no se interpreta como resistencia única en bolones o roca.

Relaciona cada obra con su investigación: estratigrafía y nivel freático, granulometría/plasticidad, resistencia al corte, permeabilidad, asentamiento, estabilidad de taludes, agresividad química y calidad de roca según el sitio. Usa parámetros geotécnicos característicos justificados, no solo el valor promedio.

## 6. Golpe de ariete y transitorios

Un cierre/cambio rápido de caudal produce ondas de presión. La ecuación de Joukowsky da una primera aproximación de incremento de carga: Δ H = aΔ V/g, donde (a) depende de la elasticidad del agua/tubería y condiciones de anclaje. Compara tiempo de cierre con tiempo de viaje de onda (2L/a). El método simplificado no reemplaza una simulación transitoria cuando hay tuberías largas, válvulas rápidas, chimenea, derivaciones, rechazo de carga o riesgo estructural.

Para estudiar el fenómeno, dibuja perfil, diámetros y materiales, condiciones de borde, ley de cierre, inercia del grupo, regulador, válvulas y protecciones. Revisa máxima presión y vacío/columna separada; define estrategias con fabricante y diseñador hidráulico.

## 7. Interconexión y protecciones

Un estudio de conexión requiere punto eléctrico definido, nivel de tensión, capacidad de cortocircuito, límites de tensión/frecuencia, calidad de energía, esquema de medida, puesta a tierra, anti-isla, comunicaciones, coordinación y ajustes aceptados por la distribuidora. Un listado ANSI de funciones no es un diseño de protección: las funciones y ajustes dependen del estudio de coordinación, la topología y requisitos vigentes del operador.

Como mínimo aprende a leer un unifilar de generador, interruptor, transformador, celda, medición y punto de conexión. Entiende sobrecorriente de fase/tierra, subtensión/sobretensión, subfrecuencia/sobrefrecuencia, potencia inversa/direccional cuando aplique, pérdida de red, sincronismo y disparo de respaldo. Los ajustes finales deben ser aprobados por profesionales y la distribuidora.

## 8. Economía y evaluación bajo incertidumbre

- VAN: (VAN = -I_0 + Σ_t=1^N F_t/(1+r)^t).
- TIR: tasa (r) que hace (VAN=0); úsala junto con VAN y supuestos de financiación.
- Relación B/C: valor presente de beneficios dividido por valor presente de costos, con convención claramente declarada.
- Energía anual: (E = Σ_t P_tΔ t); en un modelo horario, potencia debe respetar disponibilidad de agua y equipo, pérdidas, paradas, restricciones y demanda/curtailment.
- Factor de planta: (FP=E/(P_instT)), con unidades compatibles.

Separa CAPEX, OPEX, contingencias, costos de desarrollo, reemplazos, conexión, impuestos, financiación y desmantelamiento. Incluye sensibilidad de salto, caudal, CAPEX, tarifa, eficiencia, disponibilidad y plazo. Combina escenarios correlacionados de forma explícita; no trates una cifra puntual como pronóstico.

## 9. Ejercicios resueltos

### Ejercicio 1 — Potencia en el eje eléctrico

Para (Q_t=0.125m^3/s), (H_n=105m) y eficiencia global η=0.80:


**Pe = 1000 × 9.81 × 0.125 × 105 × 0.80 / 1000 ≈ 103.0 kW.**


**Lectura:** el resultado supera 100 kW. El diseñador debe aclarar si 100 kW es potencia eléctrica nominal, si el caudal y salto coinciden simultáneamente y si las eficiencias y pérdidas están bien definidos; no basta con redondear.

### Ejercicio 2 — Velocidad y pérdidas ilustrativas

Con (Q=0.125m^3/s) y diámetro interior (D=0.40m):


**A = π × 0.40² / 4 = 0.1257 m²; v = Q/A ≈ 0.995 m/s.**


Tomando, solo para el ejercicio, L = 425.8 m, ε = 0.000045 m, agua cerca de 20 °C y Colebrook/Swamee–Jain, **Re ≈ 3.95 × 10⁵** y **f ≈ 0.015**. Entonces **hf ≈ 0.81 m**. Si **ΣK = 3**, **hm ≈ 3 × 0.995² / (2 × 9.81) ≈ 0.15 m**. Pérdidas ilustrativas: aproximadamente 0.96 m.

**Lectura:** el valor real depende del trazado, accesorios, material, temperatura, diámetro interior y condición de flujo. Un porcentaje fijo de la fricción no representa necesariamente los accesorios.

### Ejercicio 3 — Caudal disponible para turbinar

Si el río lleva 80 L/s y una condición de análisis reserva 30 L/s para el caudal ecológico, antes de otros usos la disponibilidad aritmética sería **80 − 30 = 50 L/s**. Con Hn = 110 m y η = 0.768:


**Pe ≈ 1000 × 9.81 × 0.050 × 110 × 0.768 / 1000 = 41.4 kW.**


**Lectura:** es una instantánea didáctica; no demuestra que el río permanezca en 80 L/s, ni establece el caudal ecológico legal ni el caudal firme.

### Ejercicio 4 — Corriente trifásica en 10 kV

Para S = 100 kVA a VLL = 10 kV:


**IL = S/(√3 × VLL) ≈ 100000/(1.732 × 10000) = 5.77 A.**


**Lectura:** es corriente nominal ideal del lado de 10 kV; no selecciona por sí sola conductor, celdas, fusibles ni protecciones.

### Ejercicio 5 — Comprobación energética

Una unidad de 100 kW funcionando a potencia nominal todo el año produciría como máximo teórico **100 × 8760 = 876,000 kWh = 876 MWh**, antes de paradas y pérdidas adicionales. Un modelo que reporte 862.92 MWh/año equivale a **862.92/876 = 98.5%** de factor de planta.

**Lectura:** ese nivel exige revisar cuidadosamente caudal disponible, paradas, eficiencias y si los 100 kW se definieron en bornes o en el eje. No es físicamente imposible en abstracto, pero una central de pasada no debe recibir ese factor sin una simulación horaria sustentada.

### Ejercicio 6 — Golpe de ariete de primera aproximación

Con a = 900 m/s, cambio de velocidad ΔV = 1 m/s y g = 9.81 m/s²:


**ΔH = a × ΔV / g ≈ 91.7 m.**


**Lectura:** muestra por qué un cierre rápido puede crear presiones comparables al salto estático. No es un diseño de espesor; se necesita análisis transitorio del sistema completo.

### Ejercicio 7 — Factor de planta

Si el modelo anualiza 500 MWh para una planta de 100 kW: **FP = 500/(100 × 8.76) = 0.571**, es decir, 57.1%. Verifica que energía y potencia usen la misma frontera eléctrica.

## 10. Problemas para resolver por tu cuenta

1. Recalcula el Ejercicio 2 para (D=0.35m) y (D=0.45m). Compara velocidad, pérdidas y costo relativo. **Verifica:** las pérdidas caen con fuerza al aumentar diámetro, pero el costo de conducción aumenta.
2. Construye una CDC de 10 datos inventados y explica por qué no indica la secuencia de sequía. **Verifica:** el orden cronológico se pierde al ordenar.
3. Dibuja un balance instantáneo con río 140 L/s, ecológico 25 L/s, otros usos 10 L/s y turbina con capacidad de 125 L/s. **Resultado aritmético:** máximo turbinable 105 L/s antes de restricciones adicionales.
4. Para (f=0.015), (L=425.8m), (D=0.4m), (Q=0.125m^3/s), calcula (h_f). **Resultado aproximado:** 0.81 m.
5. Si una tarifa cambia 15% y energía anual baja 20%, identifica qué flujos del VAN debes recomputar; no cambies solamente la TIR.
6. Explica qué información falta para diseñar un aliviadero de 100 años. **Respuesta esperada:** cuenca y lluvias/caudales sustentados, método de frecuencia/lluvia-escorrentía, tránsito cuando aplique, hidráulica de estructura, resguardo, erosión y análisis de incertidumbre.
7. Enumera datos que solicitarías al proveedor de turbina para comparar ofertas: rango de salto/caudal, curvas de eficiencia, potencia garantizada, velocidad, cavitación/erosión, pruebas, tolerancias, alcance y exclusiones.
8. Distingue una respuesta de interconexión favorable de una autorización de construcción y de un contrato de compra de energía.

## 11. Autoevaluación

Marca cada habilidad como **puedo explicarla**, **puedo calcularla**, o **necesito repasar**:

- [ ] Distingo caudal observado, caudal de diseño, ecológico, turbinable y firme.
- [ ] Puedo auditar unidades, faltantes, datos estimados y fuente de una serie.
- [ ] Puedo calcular velocidad, Reynolds, Darcy–Weisbach y pérdidas locales.
- [ ] Puedo cerrar el balance entre salto bruto y neto y explicar cada pérdida.
- [ ] Puedo estimar potencia y energía sin confundir kW con kWh.
- [ ] Puedo justificar una turbina con rango operativo y curva del fabricante.
- [ ] Puedo explicar para qué sirven captación, desarenador, cámara de carga y aliviadero.
- [ ] Puedo explicar por qué el golpe de ariete exige analizar tiempos y condiciones de borde.
- [ ] Puedo leer un unifilar y describir el proceso de coordinación de protecciones.
- [ ] Puedo interpretar VAN/TIR junto con escenarios y riesgo de datos.

## 12. Orden recomendado para reforzar primero

1. **Hidrología y caudal firme:** define cuánto recurso podría convertirse en energía.
2. **Hidráulica y pérdidas:** conecta topografía, diámetro, salto neto y presión.
3. **Potencia/energía y selección de turbina:** transforma el recurso en producción y equipo.
4. **Transitorios y seguridad de conducciones:** evita subestimar presiones y riesgos.
5. **Obras civiles y geotecnia:** revisa si el sitio permite construir y operar las estructuras.
6. **Interconexión y economía:** comprueba si la potencia puede entregarse y si el valor económico resiste incertidumbre.

Para tu proyecto, empieza rehaciendo manualmente los ejercicios 1–5 y después reproduce el caso económico en una hoja propia. Cada cifra debe tener unidad, fuente, estado (medido/supuesto) y sensibilidad. Lleva las dudas normativas al docente y a la autoridad competente; esta guía no sustituye el sílabo ni el criterio de un ingeniero responsable.
