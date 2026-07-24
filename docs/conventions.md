# Convenciones del Proyecto

Para garantizar la mantenibilidad y consistencia del proyecto **Winners**, se deben respetar las siguientes convenciones en todo momento.

## 1. Convenciones de Nomenclatura

- **Carpetas y archivos:** En minúsculas, usando `kebab-case` o `snake_case` según el lenguaje principal que adoptemos (ej. `analisis_ligas.py`, `data-cleaning-script.sh`).
- **Variables y Funciones (código):** Se seguirá el estándar de la industria para el lenguaje escogido (ej. `snake_case` para Python, `camelCase` para JavaScript/TypeScript).
- **Archivos de datos:** Deben incluir versionado o sufijos temporales descriptivos (ej. `premier_league_2023_raw.csv`, `metrics_output_v1.2.json`).

## 2. Convenciones de Documentación

- Todos los archivos Markdown deben utilizar el estándar de GitHub Flavored Markdown (GFM).
- Cada documento técnico debe indicar brevemente su propósito en el primer párrafo.
- El código fuente debe estar ampliamente comentado, documentando el "por qué" y no solo el "qué". Las funciones deben incluir Docstrings describiendo entradas, salidas y el razonamiento estadístico/matemático cuando aplique.

## 3. Manejo de Datos

- **Inmutabilidad:** Los datos descargados y colocados en la carpeta `datasets/raw/` (cuando se cree) son de solo lectura. Las transformaciones deben guardarse en subdirectorios como `datasets/processed/`.
- **Limpieza de variables:** Se deben evitar por completo los nombres de columnas ambiguos en los datasets; se prefieren nombres explícitos y estandarizados en inglés para evitar problemas de codificación.

## 4. Control de Cambios

- Todo cambio arquitectónico o de lógica funcional debe ser propuesto, revisado y **aprobado por Ares** antes de su integración.
- Los scripts experimentales deben permanecer confinados a la carpeta `research/` hasta que se certifique su validez para pasar a `scripts/` o `metrics/`.

## 5. Diseño Cero Subjetividad

- Queda estrictamente prohibido introducir constantes "mágicas" o pesos variables en el código que no estén respaldados por un análisis estadístico documentado. Todo parámetro que modifique el comportamiento del sistema debe vivir en un archivo en la carpeta `config/`.
