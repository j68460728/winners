# Arquitectura General

La arquitectura de **Winners** está diseñada para ser extremadamente modular, escalable y robusta, separando claramente las responsabilidades en distintas capas de procesamiento.

## Principios Arquitectónicos

1. **Separación de Responsabilidades (SoC):** La recolección de datos, la limpieza, el cálculo de métricas y la inferencia (modelos) operan de manera independiente.
2. **Inmutabilidad de Datos Crudos:** Los datasets iniciales nunca se sobrescriben. Todo procesamiento genera un nuevo artefacto de datos.
3. **Agnóstico al Modelo:** El motor de evaluación de ligas y partidos no debe depender estrechamente de una única tecnología o algoritmo. Se pueden intercambiar modelos predictivos/analíticos mediante interfaces estandarizadas.
4. **Trazabilidad:** Cada resultado de evaluación debe poder ser rastreado hacia las métricas y los datos crudos que lo originaron.

## Capas del Sistema (Propuesta Inicial)

1. **Capa de Datos (Data Layer):** 
   - Responsable de la obtención y almacenamiento estructurado de la información (estadísticas de ligas, resultados de partidos, clasificaciones históricas).
   - *Ubicación principal:* `datasets/`

2. **Capa Analítica y de Métricas (Analytics & Metrics Layer):**
   - Transforma los datos crudos en indicadores cuantificables (ej. índice de asimetría de la liga, métricas de dominancia, ratios de rendimiento).
   - *Ubicación principal:* `metrics/` y `leagues/`

3. **Capa de Inferencia (Modeling Layer):**
   - Aplica algoritmos y modelos estadísticos sobre las métricas calculadas para evaluar las "condiciones estructurales" y emitir una calificación o ranking.
   - *Ubicación principal:* `models/`

4. **Capa de Investigación y Prompts (Research & Prompting Layer):**
   - Entorno de trabajo para la experimentación con LLMs, iteración algorítmica y pruebas de concepto.
   - *Ubicación principal:* `research/` y `prompts/`

5. **Capa de Ejecución (Execution Layer):**
   - Orquesta el flujo de trabajo conectando los datos, las métricas y los modelos para generar salidas estructuradas.
   - *Ubicación principal:* `scripts/` y `results/`

*(Nota: Esta arquitectura será profundizada y ajustada de acuerdo con las especificaciones técnicas que defina Ares en las siguientes fases del desarrollo).*
