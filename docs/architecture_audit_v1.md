# Auditoría Arquitectónica v1.0

**Objetivo del documento:** Evaluar críticamente la arquitectura conceptual actual de Winners frente a un escenario de escala masiva (150 ligas, 500 hipótesis, 300 métricas, 30 años de datos), detectando cuellos de botella, inconsistencias y deuda conceptual. El auditor evidencia; no diseña.

---

## 1. Coherencia Conceptual

Análisis de las relaciones entre `knowledge_inventory.md`, `hypothesis_registry.md`, `hypothesis_taxonomy.md`, `metric_lifecycle.md` y `scoring_system.md`.

- **Acoplamiento innecesario:** Existe una dependencia frágil entre `hypothesis_registry.md` y `hypothesis_taxonomy.md`. Actualmente, la taxonomía dicta las reglas, pero el registro contiene los datos. En un escenario de 500 hipótesis, mantener dos archivos sincronizados (si una hipótesis cambia de L2 a L3) provocará errores humanos inevitables.
- **Responsabilidades difusas en el Flujo:** `scoring_system.md` define "Métricas" (ej. Dominancia Histórica, Volatilidad) de forma explícita. Sin embargo, `metric_lifecycle.md` establece que ninguna métrica nace sin antes ser una hipótesis validada. Esto significa que las métricas listadas en el Scoring System son actualmente ilegales bajo nuestras propias reglas, ya que no nacieron de un proceso experimental.
- **Jerarquía rota:** Hemos definido escalas L1 a L4 para las *Hipótesis*, pero el *Scoring System* no refleja formalmente si las métricas generadas por esas hipótesis mantendrán esa misma jerarquía escalar o si todas colapsan en una sola calificación plana.

## 2. Escalabilidad

Evaluación del sistema con proyecciones a 3 años (volumen masivo de datos y variables).

- **Cuello de botella en Aprobación (Etapa 7 del Ciclo de Vida):** El protocolo exige que *solo Ares* apruebe el paso de "Experimental" a "Métrica Oficial". Con 300 métricas y cientos de iteraciones, la validación centralizada humana (o de un solo agente) colapsará el pipeline de investigación.
- **Gestión del Inventario del Conocimiento:** Un `knowledge_inventory.md` en formato texto plano es insostenible para un mapeo de datos real de 30 años en 150 ligas. Mapear qué proveedor de datos nos entrega qué variable requerirá un esquema relacional (JSON/Base de datos), no un archivo Markdown.
- **Explosión Combinatoria L3 y L4:** A nivel Liga (L1) hay 150 entidades. A nivel Partido (L4), en 30 años, hablamos de millones de entidades. Si las métricas L4 requieren validación retrocompatible (recalcular todo el universo ante un cambio), los costos computacionales serán astronómicos sin una arquitectura de partición de datos que aún no hemos definido conceptualmente.

## 3. Consistencia Metodológica

Búsqueda de contradicciones y ambigüedades en la literatura actual.

- **Contradicción del CGC:** El Coeficiente Global de Confiabilidad se define como el "pilar maestro". Pero conceptualmente se describe evaluando factores L1 (formato de liga, ascensos) y L2 (media de puntos). No queda metodológicamente claro si el CGC aplica *solo* a la liga (L1) y penaliza todo hacia abajo, o si existen CGCs a nivel de enfrentamiento (L3).
- **Ambigüedad del término "Sistema":** Se utiliza "sistema" para referirse al código, al modelo de puntuación (Scoring System) y a las ligas en sí mismas (ecosistemas). 
- **Inconsistencia de la "Normalización":** Declaramos que todo dato se normalizará para ser comparable de forma universal. Sin embargo, ciertas métricas (ej. L3-H-0013, Sesgo de Altitud) no existen en el 90% de las ligas europeas. No es matemáticamente consistente normalizar un valor que estructuralmente no aplica a un subconjunto masivo de la muestra.

## 4. Riesgos Arquitectónicos

- **Crítico:** *Ruptura de la cadena de dependencia ontológica.* Si el conocimiento crudo cambia de formato o proveedor, todas las hipótesis y métricas atadas a él colapsan. No existe una capa de "abstracción" entre el dato crudo y la hipótesis.
- **Alto:** *Inconsistencia de propagación.* Si una métrica oficial es recalibrada, la regla de "evolución retrocompatible" obliga a recalcular toda la historia. No tenemos documentado un protocolo de versionado de *datos procesados*, solo de la fórmula.
- **Medio:** *Acoplamiento documental.* Mantener la trazabilidad manual cruzada entre el Inventario, la Hipótesis, la Métrica y la Calificación en archivos de texto será inmanejable más allá de 50 entidades.
- **Bajo:** *Conflictos semánticos.* Pequeñas diferencias en cómo se interpretan dominios vs escalas a medida que ingresen nuevos colaboradores al proyecto.

## 5. Deuda Conceptual

Ideas que funcionan para el MVP de diseño, pero colapsarán al escalar.

- **"El Dato Objetivo":** Asumimos implícitamente que un dato (ej. Posesión) es una verdad universal. En la realidad, Opta, StatsBomb y Wyscout calculan la posesión de forma diferente. El concepto de "dato limpio" es una deuda conceptual; ignoramos el sesgo del proveedor de datos.
- **Categorías estáticas en Nivel 1:** Definimos umbrales ("Élite, Alta, Media, Baja"). Esto es deuda. Un sistema verdaderamente dinámico debería clusterizar las ligas matemáticamente sin imponer etiquetas predefinidas.
- **Independencia absoluta de variables:** En el fútbol, el presupuesto (Económico) y la posesión (Estadístico) casi siempre están colineados. Asumir que encontraremos 300 métricas perfectamente ortogonales e independientes es estadísticamente ingenuo.

## 6. Principios Fundacionales (Sintetizados)

De toda la literatura generada, los axiomas reales que sostienen a Winners se reducen a cinco:
1. **Materialismo Estadístico:** Nada existe ni es evaluable si no se puede cuantificar y normalizar.
2. **Determinismo (Reproducibilidad Absoluta):** Mismos datos + Misma versión de métrica = Mismo veredicto exacto.
3. **Métrica = Hipótesis Comprobada:** Todo cálculo es hijo de una teoría preexistente, nunca fruto de la casualidad o del ajuste excesivo (*overfitting*).
4. **Evaluación Jerárquica:** El universo se disecciona en capas estrictas (Liga > Equipo > Matchup > Evento). El ruido de un nivel no contamina al otro.
5. **Evolución Retrocompatible:** El pasado se recalcula siempre que el sistema evoluciona; no coexisten dos versiones matemáticas vivas.

## 7. Recomendaciones (Preguntas Abiertas)

Preguntas críticas que deben resolverse antes de la implementación en código:

- ¿Deberían fusionarse el Registro de Hipótesis y la Taxonomía en una base de conocimiento relacional?
- ¿Si una hipótesis requiere variables de dos proveedores que miden de forma diferente, cómo se resuelve la colisión empírica?
- ¿Las métricas heredan la escala (L1-L4) de la hipótesis que les dio origen?
- ¿Puede el CGC de una liga (L1) invalidar por completo una métrica brillante a nivel de equipo (L2)?
- ¿Cómo se "deprecian" o eliminan las métricas oficiales cuando dejan de tener poder predictivo sin romper el historial?
- ¿Las hipótesis pueden tener dependencias entre sí (ej. una hipótesis L3 solo es evaluable si una hipótesis L1 resulta falsa)?
- ¿Podrá el sistema crear "Hipótesis Sintéticas" (algoritmos genéticos) de forma automatizada, o toda hipótesis siempre requerirá un origen humano/conceptual previo?
