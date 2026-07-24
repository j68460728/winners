# Estructura de Carpetas

La arquitectura del sistema de archivos está diseñada para mantener los componentes aislados, permitiendo escalar el sistema analítico sin desorden.

## Directorios y su Justificación

- `config/`
  Contiene los archivos de configuración globales (variables de entorno, hiperparámetros de modelos, rutas estáticas). Justificación: Centralizar la configuración evita números "mágicos" esparcidos en el código fuente.
- `datasets/`
  Almacenará todos los datos obtenidos (bases de datos, CSVs, JSONs). Se dividirá internamente en `raw/` (crudos) y `processed/` (limpios). Justificación: Asegura la inmutabilidad de la información original y permite reproducir los procesos.
- `docs/`
  Centro de toda la documentación arquitectónica, filosófica y técnica del proyecto. Justificación: Un proyecto complejo basado en evidencia estadística muere si no está rigurosamente documentado.
- `leagues/`
  Módulos y configuraciones específicas para aislar la lógica o las peculiaridades de cada liga analizada. Justificación: Cada liga tiene contextos diferentes (tamaño, formato) que deben ser abstraídos de la lógica principal.
- `metrics/`
  Módulos encargados puramente de la transformación matemática y estadística de los datos en indicadores numéricos. Justificación: Desacoplar las fórmulas matemáticas de los scripts de ejecución permite realizar tests unitarios sobre la precisión de los cálculos.
- `models/`
  Implementaciones de los algoritmos de evaluación y sistemas de decisión basados en las métricas. Justificación: Permite iterar y probar diferentes aproximaciones (modelos A/B) de manera intercambiable.
- `prompts/`
  Directorio dedicado a almacenar y versionar los prompts (en texto plano o JSON) utilizados si se integran LLMs en el pipeline. Justificación: Tratar los prompts como código versionable es vital para la reproducibilidad de respuestas de los LLMs.
- `research/`
  Entorno tipo *sandbox* para libretas de experimentación (Jupyter notebooks, scripts de prueba). Justificación: Fomenta la exploración de datos sin ensuciar el código productivo.
- `results/`
  Almacenamiento de las salidas, reportes generados, gráficos y conclusiones derivadas de las ejecuciones del sistema. Justificación: Separa la salida final del código que la produce.
- `scripts/`
  Puntos de entrada de la aplicación, utilerías de terminal y orquestadores (pipelines) que unen todo el flujo. Justificación: Mantiene la lógica de ejecución separada de la lógica de negocio (métricas/modelos).
- `tests/`
  Suite de pruebas (unitarias y de integración) para asegurar que el sistema es determinista y no contiene fallas estadísticas. Justificación: La calidad y confianza del sistema dependen de comprobar empíricamente que funciona bien.
