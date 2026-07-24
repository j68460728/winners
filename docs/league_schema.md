# Esquema Maestro de Ligas (League Schema)

Este documento define la estructura oficial que debe cumplir cualquier expediente de liga dentro del proyecto **Winners**. Sirve exclusivamente como archivo de configuración estática; no almacena historial ni datos dinámicos.

> **Principio de Separación (Configuración vs Evidencia):** La configuración es estática y define las reglas del juego. La evidencia (resultados, tablas, calendarios) es dinámica, cambia constantemente y se descarga en tiempo real. Un expediente de liga solo almacena configuración.
>
> **Principio de Utilidad Binaria:** Todo campo almacenado debe justificar su existencia alimentando directamente una decisión en el Pipeline A (Certificación). Si un dato no filtra, no existe.

---

## 1. Identidad (Identity)
El mínimo absoluto para saber de qué ecosistema estamos hablando.

- **`id_liga`**
  - *Descripción:* Identificador único alfanumérico interno.
  - *Tipo de dato:* String (Mayúsculas, formato ISO_NIVEL, ej. "GER_1")
  - *Prioridad:* Obligatorio
  - *Consumidor:* Todos
  - *Motivo:* Llave primaria del sistema para cruzar la configuración con la Evidencia descargada.

- **`nombre_oficial`**
  - *Descripción:* Nombre legible para humanos (ej. "Bundesliga").
  - *Tipo de dato:* String
  - *Prioridad:* Obligatorio
  - *Consumidor:* Logs / UI
  - *Motivo:* Permite a los humanos interpretar los resultados del sistema sin tener que memorizar IDs.

---

## 2. Estructura Competitiva (Format)
Define las reglas matemáticas inmutables del ecosistema. Si la Evidencia descargada no coincide con estas reglas, o si las reglas cambian, la liga pierde su certificación.

- **`formato_competencia`**
  - *Descripción:* Arquitectura del torneo (ej. "Todos contra todos").
  - *Tipo de dato:* Enum / String predefinido
  - *Prioridad:* Obligatorio
  - *Consumidor:* A2 (Estabilidad Estructural)
  - *Motivo:* Descartar ligas con formatos híbridos o caóticos.

- **`num_equipos`**
  - *Descripción:* Cantidad total de equipos participantes requeridos por temporada.
  - *Tipo de dato:* Integer
  - *Prioridad:* Obligatorio
  - *Consumidor:* A1 (Integridad) y A2 (Estabilidad)
  - *Motivo:* Altera el tamaño de la muestra; si un año hay 18 equipos y al siguiente 20, la serie histórica se contamina.

- **`total_jornadas_regular`**
  - *Descripción:* Número de partidos esperados por equipo en la fase regular.
  - *Tipo de dato:* Integer
  - *Prioridad:* Obligatorio
  - *Consumidor:* A1 (Integridad de Datos)
  - *Motivo:* Permite auditar matemáticamente si la Evidencia descargada está completa o corrupta.

- **`cupos_descenso_directo`**
  - *Descripción:* Número de equipos que pierden la categoría automáticamente.
  - *Tipo de dato:* Integer
  - *Prioridad:* Obligatorio
  - *Consumidor:* A2 (Estabilidad) y A3 (Jerarquía)
  - *Motivo:* Define matemáticamente la frontera del "Bloque Inferior" (Bottom) contra el cual se medirá la tasa de sorpresas del favorito.

---

## 3. Regulaciones Artificiales (Regulations)
Normativas que imponen paridad desde fuera del juego.

- **`limite_salarial_estricto`**
  - *Descripción:* Indica si existe una política de tope salarial forzado (Salary Cap).
  - *Tipo de dato:* Boolean
  - *Prioridad:* Obligatorio
  - *Consumidor:* A3 (Jerarquía Deportiva)
  - *Motivo:* Un `true` rechaza casi instantáneamente la liga al violar la premisa de asimetría natural (ej. MLS).
