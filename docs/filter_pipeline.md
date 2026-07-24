# Pipelines de Filtros (Motores de Decisión)

**Filosofía Central:** Winners busca motivos estadísticos implacables para destruir hipótesis. Solo aquello que sobrevive a esta criba binaria tiene valor. La versión más simple que produce exactamente la misma decisión siempre será la correcta.

Para maximizar la eficiencia computacional y separar el diseño estructural de la operación diaria, el sistema se divide en dos motores completamente independientes.

---

## Pipeline A — Certificación de Ligas

Este motor se ejecuta de manera ocasional (ej. al terminar una temporada, al añadir una liga nueva o para una recalibración). Su única misión es auditar el universo global y producir una **Lista Blanca**.

- **Estado final de una liga:** `Certificada` o `No Certificada`.

### Filtro A1: Integridad y Profundidad de Datos
- **Objetivo:** Garantizar que exista materia prima suficiente y confiable.
- **Entrada:** Universo total de ligas (ej. 50 ligas).
- **Salida:** Ligas con datos operables.
- **Criterio de aprobación:** Historial ininterrumpido de resultados verificables durante los últimos N años.
- **Criterio de descarte:** Datos corruptos, temporadas faltantes o historial insuficiente.

### Filtro A2: Estabilidad Estructural
- **Objetivo:** Descartar ecosistemas caóticos en su organización y reglas.
- **Entrada:** Ligas con datos operables.
- **Salida:** Ligas estructuralmente estables.
- **Criterio de aprobación:** El formato de competición se ha mantenido intacto sin modificaciones reglamentarias drásticas.
- **Criterio de descarte:** Cambios constantes de formato o reglas que rompen la comparabilidad histórica.

### Filtro A3: Jerarquía Deportiva (Asimetría)
- **Objetivo:** Confirmar empíricamente que existe una casta dominante.
- **Entrada:** Ligas estructuralmente estables.
- **Salida:** Ligas asimétricas.
- **Criterio de aprobación:** Brecha histórica clara y sostenida de puntos/rendimiento entre el bloque dominante y el bloque inferior.
- **Criterio de descarte:** Paridad extrema; la diferencia de nivel es demasiado estrecha.

### Filtro A4: Confiabilidad de la Jerarquía
- **Objetivo:** Eliminar ligas donde los equipos débiles roban puntos con demasiada frecuencia a los fuertes.
- **Entrada:** Ligas asimétricas.
- **Salida:** **Lista Blanca (Ligas Certificadas)**.
- **Criterio de aprobación:** En duelos asimétricos, el favorito cumple la lógica histórica en la inmensa mayoría de los casos.
- **Criterio de descarte:** Tasa de sorpresas (upsets) inaceptablemente alta o errática.

---

## Pipeline B — Selección Diaria

Este motor se ejecuta todos los días. Ya no audita ligas; asume que la estructura es correcta. Consume exclusivamente la **Lista Blanca** generada por el Pipeline A.

- **Estado final de un partido:** `Candidato` o `Descartado`.

### Filtro B1: Relevancia Temporal
- **Objetivo:** Identificar rápidamente qué ligas de la Lista Blanca tienen actividad.
- **Entrada:** Lista Blanca (Ligas Certificadas).
- **Salida:** Ligas certificadas con partidos programados hoy.
- **Criterio de aprobación:** La liga tiene jornada activa en la ventana de análisis (ej. próximas 24-48 horas).
- **Criterio de descarte:** Liga en receso o sin partidos inminentes.

### Filtro B2: Asimetría del Enfrentamiento
- **Objetivo:** Descartar partidos parejos dentro de las jornadas activas, aislando solo las oportunidades estructurales comprobadas.
- **Entrada:** Partidos programados de las ligas activas hoy.
- **Salida:** **Partidos Candidatos**.
- **Criterio de aprobación:** El enfrentamiento cruza estrictamente a un equipo catalogado como "Dominante" contra uno "Inferior", según la jerarquía de la liga.
- **Criterio de descarte:** Partidos competitivamente parejos (Derbis, duelos en la cima, duelos en el fondo) o estadísticamente ruidosos.
