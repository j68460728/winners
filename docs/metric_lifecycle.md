# Ciclo de Vida de las Métricas

Este documento define el protocolo científico oficial para la creación y adopción de cualquier métrica dentro del ecosistema de **Winners**. El objetivo es garantizar que ninguna variable ingrese al modelo por simple intuición o criterio individual. Todo indicador debe superar un riguroso proceso de validación empírica y metodológica.

> **Principio Fundacional:**
> "Una métrica no es una idea. Es una hipótesis que sobrevivió a un proceso de validación."

---

## Protocolo Científico de Creación

Toda propuesta matemática destinada a convertirse en una métrica del sistema deberá someterse obligatoria y secuencialmente a las siguientes ocho etapas:

### Etapa 1 — Observación
Toda métrica nace de una anomalía o un patrón observado. Este origen puede surgir de:
- Regularidades matemáticas encontradas en un análisis exploratorio preliminar.
- Teorías consolidadas de la literatura deportiva, estadística o económica.
- Evidencia empírica o patrones de comportamiento estructural documentados.

### Etapa 2 — Hipótesis
La observación debe fundamentarse y registrarse como una teoría.
- Debe vincularse obligatoriamente con una hipótesis registrada en el `docs/hypothesis_registry.md`.
- Ninguna métrica podrá nacer ni avanzar en el ciclo de vida sin una hipótesis asociada que justifique conceptualmente su razón de ser.

### Etapa 3 — Identificación de Datos
Antes de formular cálculos, se debe identificar la materia prima.
- Se determinan los elementos de información en bruto requeridos apoyándose en el `docs/knowledge_inventory.md`.
- Se valida la integridad, disponibilidad y confianza de las fuentes antes de continuar.

### Etapa 4 — Diseño Matemático
Formulación conceptual de la arquitectura del cálculo.
- Se define la ruta lógica de transformación: cómo los datos crudos serán extraídos, normalizados y operados.
- Se debe asegurar matemáticamente la independencia de la métrica frente a las ya existentes para evitar multicolinealidad.

### Etapa 5 — Validación Experimental
Implementación aislada y contenida.
- La métrica se programa en código únicamente en el entorno de experimentación de la carpeta `research/`.
- Se ejecutan pruebas de estrés (backtesting) usando conjuntos de datos históricos controlados.

### Etapa 6 — Evaluación
Los resultados generados en la etapa de experimentación se auditan bajo los siguientes criterios de aceptación:
- **Estabilidad:** La métrica debe ser robusta frente a datos atípicos (outliers) y no presentar comportamientos erráticos.
- **Reproducibilidad:** El cálculo debe ser determinista frente a los mismos datos de entrada.
- **Capacidad discriminante:** Debe tener el poder real de separar y categorizar ecosistemas (ej. distinguir matemáticamente un torneo caótico de uno jerárquico).
- **Ausencia de sesgos evidentes:** La fórmula no debe favorecer artificialmente a ligas por variables ajenas a la hipótesis de estudio.
- **Coherencia entre distintas ligas:** Su capacidad de normalización debe permitir su uso justo tanto en ligas de formatos grandes como en formatos reducidos.

### Etapa 7 — Aprobación
Transición del estado Experimental a Oficial.
- La incorporación del algoritmo al sistema central es atribución única y exclusiva del Arquitecto del Sistema (**Ares**).
- Mientras no obtenga aprobación explícita, la métrica permanece congelada en estado experimental y no puede integrar el motor de evaluación (`metrics/`).

### Etapa 8 — Versionado
Una vez oficializada, la métrica se convierte en un artefacto estricto que debe registrar:
- Identificador único formal.
- Versión actual de la lógica matemática.
- Fecha de creación y aprobación oficial.
- Hipótesis de origen (Identificador de referencia).
- Datos específicos del inventario consumidos.
- Historial completo de modificaciones y recálculos.
