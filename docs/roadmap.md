# Roadmap de Desarrollo

El desarrollo de **Winners** se ejecutará en fases progresivas bajo la dirección de Ares (Arquitectura) y Jaalsima (Dirección).

## Fase 1: Fundamentación (Completada)
- Definición de roles (Ares, Forge, Jaalsima).
- Inicialización de la estructura de carpetas modular.
- Redacción de la documentación base (Visión, Arquitectura, Convenciones, Estructura).

## Fase 2: Recolección y Procesamiento (Próxima)
- *A la espera de definiciones de Ares:*
  - Selección de las fuentes de datos primarias.
  - Diseño de la estructura del dataset base.
  - Implementación de scripts de limpieza (`scripts/`, `datasets/`).

## Fase 3: Capa de Métricas y Análisis de Ligas
- *A la espera de definiciones de Ares:*
  - Desarrollo de funciones matemáticas puras en `metrics/` (ej. asimetría, momentum histórico).
  - Integración de los pipelines para evaluar el ecosistema de las `leagues/`.
  - Pruebas estadísticas formales en `tests/`.

## Fase 4: Modelado y Orquestación
- *A la espera de definiciones de Ares:*
  - Implementación de algoritmos de evaluación en `models/`.
  - Integración de posibles agentes de LLM usando artefactos de `prompts/`.
  - Ejecución de pipelines completos y guardado en `results/`.

## Fase 5: Validación y Ajustes
- Evaluación empírica de los resultados generados por los modelos.
- Ajustes de hiperparámetros en `config/`.
- Refinamiento de la arquitectura según los cuellos de botella detectados.
