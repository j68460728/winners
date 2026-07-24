# Experimento MVP (Producto Mínimo Viable)

**Principio Rector:** La simplicidad es un requisito arquitectónico. Evidencia sobre perfección teórica.

Este documento define el alcance estricto del primer experimento de Winners. El objetivo es aislar la variable principal del proyecto y someterla a validación empírica inmediata, utilizando el mínimo nivel de complejidad técnica requerida. 

Todo lo que no pertenezca explícitamente a este documento queda fuera de la primera fase de análisis.

---

## 1. Hipótesis Principal a Validar

Solo vamos a responder una pregunta:
**"¿Existen ligas de fútbol cuya estructura histórica (asimetría de poder) es lo suficientemente consistente como para que la victoria de un equipo históricamente dominante sobre uno estadísticamente inferior sea predecible y explotable de manera sistemática?"**

Si la evidencia histórica refuta esta hipótesis, el proyecto carece de sentido. Si la valida, habremos encontrado el motor real de Winners.

## 2. Datos Mínimos Necesarios

Para no retrasar la validación con integraciones complejas, trabajaremos con un bloque de datos mínimo. No usaremos APIs avanzadas en esta etapa, solo bases de datos de resultados crudos.

- Fechas de los partidos (últimas 5 a 10 temporadas).
- Nombres de los equipos (Local / Visitante).
- Marcador final (Goles Local / Goles Visitante).
- Clasificación final por temporada (Puntos obtenidos) para poder definir jerarquías.

## 3. Ligas a Analizar Primero

El análisis se correrá sobre un *pool* de aproximadamente 50 competiciones para garantizar diversidad geográfica y estructural, buscando encontrar los entornos más asimétricos.

- **Europa Top:** Premier League, LaLiga, Serie A, Bundesliga, Ligue 1.
- **Europa Secundaria y Menor:** Eredivisie, Primeira Liga, Scottish Premiership, ligas escandinavas, Europa del Este, y segundas divisiones de torneos top (Championship, 2.Bundesliga).
- **América:** Brasileirão, Liga Argentina, MLS, Liga MX, ligas andinas principales.
- **Resto del Mundo:** J-League, K-League, ligas seleccionadas de Medio Oriente (para contrastar asimetrías por inversión económica reciente).

## 4. Variables Imprescindibles (Versión 1)

Nada de VAR, psicología, árbitros, xG, clima ni mercado de apuestas. Únicamente mediremos 3 variables derivadas de los datos crudos:

1. **Jerarquía (Brecha de Puntos):** Diferencia histórica de rendimiento (posiciones o media de puntos) entre el equipo A y el equipo B para poder etiquetarlos como "Favorito" vs "Inferior".
2. **Tasa de Sorpresas (Upsets):** Frecuencia (en %) con la que el equipo etiquetado como "Inferior" derrota al "Favorito" en el histórico.
3. **Varianza de Dominancia:** Estabilidad de esa Tasa de Sorpresas año tras año (para saber si la liga es caótica hoy pero fue estable ayer).

## 5. Criterios de Aceptación o Rechazo

Al correr los datos por el sistema, aplicaremos un filtro binario (blanco o negro) sobre las ligas:

- **Se RECHAZA una liga si:** La "Tasa de Sorpresas" en duelos asimétricos es demasiado alta y errática. Si el equipo inferior roba puntos habitualmente (ej. > 30% de los casos), la liga es caótica y se descarta inmediatamente.
- **Se ACEPTA una liga si:** Demuestra que, cuando se cruzan los extremos de su jerarquía (ej. Top 20% vs Bottom 20%), la lógica impera de forma aplastante (ej. el favorito gana/no pierde en el >80% de los casos) y este patrón se mantiene estable a lo largo de las temporadas analizadas.

## 6. Resultado Esperado del Experimento

Al concluir este MVP, el único entregable será una respuesta binaria para cada liga y una lista definitiva:

1. **Lista de Ligas Aprobadas:** Las únicas competiciones del mundo que sobrevivieron al filtro del caos y sobre las que vale la pena construir modelos predictivos.
2. **Confirmación del Proyecto:** Demostrar estadísticamente que Jaalsima tiene razón: la ventaja estructural existe y puede aislarse con datos muy simples.
