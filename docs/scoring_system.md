# Sistema de Puntuación Global

Este documento define la arquitectura teórica del sistema de puntuación para **Winners**, consolidando su filosofía como un motor de evaluación cuantitativa. 

## 1. Objetivo del Sistema

El propósito exclusivo de este sistema es convertir la información histórica y los datos estructurales del fútbol en valores numéricos. Winners actúa como un motor de evaluación estricto que, a través de sus cuatro niveles conceptuales (Ligas, Equipos, Enfrentamientos, Motor Diario), califica objetivamente cada componente para determinar si existen las asimetrías y condiciones estructurales que el proyecto busca explotar. Toda conclusión debe estar justificada matemáticamente. Ninguna entidad (liga, equipo o partido) es válida hasta que los números lo demuestren.

## 2. Principios Matemáticos

El diseño y cálculo de toda métrica en Winners se rige por los siguientes axiomas inquebrantables:

- **Reproducibilidad:** Dados los mismos datos de entrada, el sistema siempre debe producir exactamente la misma puntuación.
- **Objetividad:** Ninguna métrica puede depender de factores cualitativos, narrativas o apreciaciones humanas (cero subjetividad).
- **Independencia de Variables:** Las métricas deben medir fenómenos distintos, evitando la multicolinealidad (es decir, evitar inflar el puntaje midiendo lo mismo dos veces con nombres diferentes).
- **Normalización:** Todo dato en bruto debe transformarse a una escala estandarizada para permitir comparaciones directas en todo el universo de datos.
- **Comparabilidad:** La puntuación de una entidad debe poder compararse matemáticamente y de manera justa contra cualquier otra entidad en su mismo nivel de análisis.

## 3. Definición de Métricas

Para calificar un entorno competitivo en el "Universo de Ligas", el sistema observará fenómenos estructurales que serán convertidos en las siguientes métricas fundamentales:

- **Dominancia Histórica:** Medición del monopolio o control prolongado de los recursos deportivos.
- **Estabilidad Competitiva:** Evaluación de la varianza en las posiciones y el rendimiento a lo largo del tiempo.
- **Concentración de Títulos:** Índice de aglomeración del éxito en la cúspide de la pirámide de la liga.
- **Volatilidad:** Fluctuación general o grado de agitación constante en el ecosistema.
- **Predictibilidad:** Nivel base de entropía de los resultados (cuán lógicos o ilógicos son los marcadores promedio).
- **Ventaja Local:** Impacto paramétrico del factor campo en la estructura de puntos general.
- **Calidad de Datos:** Medida de confianza sobre la profundidad, limpieza e integridad histórica de los registros disponibles.
- **Regularidad del Calendario:** Estabilidad en el formato competitivo y la frecuencia de los partidos.

## 4. Proceso de Evaluación

El ciclo de vida de la información sigue un flujo unidireccional y auditable:

1. **Entrada:** Ingesta de los datos estructurales crudos.
2. **↓ Extracción:** Aislamiento de las dimensiones estadísticas relevantes.
3. **↓ Normalización:** Estandarización de las variables a escalas universales.
4. **↓ Puntuación:** Aplicación de las reglas matemáticas de evaluación a las variables normalizadas.
5. **↓ Calificación Final:** Agregación de las puntuaciones en un veredicto definitivo.

## 5. Clasificación Final

El resultado de aplicar el sistema de puntuación a una entidad (por ejemplo, en el Nivel 1) asignará a dicha entidad a una de las siguientes categorías estrictas. Estas determinan su viabilidad para ser analizada en niveles posteriores:

- **Élite**
- **Alta**
- **Media**
- **Baja**
- **Descartada**

*(Nota: Los umbrales que delimitan estas categorías se establecerán posteriormente).*

## 6. Coeficiente Global de Confiabilidad (CGC)

El **Coeficiente Global de Confiabilidad (CGC)** (anteriormente denominado ICP) es el modificador maestro de seguridad y el pilar fundamental del proyecto Winners. No es una métrica acumulativa, sino un ponderador universal.

- **¿Qué representa?** Es un multiplicador numérico que expresa el grado de orden, madurez y predictibilidad estructural de un ecosistema competitivo.
- **¿Qué pretende medir?** Mide la "entropía estructural" o el ruido inherente a un torneo. Busca cuantificar qué tan caótico es el ecosistema.
- **¿Por qué es importante?** Porque una puntuación alta en métricas de "dominancia" carece de valor si ocurre en un entorno regido por el azar. El CGC actúa penalizando o validando al resto del sistema. Si el entorno es demasiado caótico, el coeficiente atenúa o invalida las puntuaciones generadas por las demás métricas de la liga.
- **Composición conceptual:** Se alimentará de la tasa de sorpresas históricas (upsets), la varianza de la media de puntos de los bloques de equipos, la estabilidad en los ascensos/descensos y la resiliencia histórica ante factores o cambios estructurales.

## 7. Evolución del Sistema

El motor matemático de Winners está concebido para ser estrictamente **incremental**:

- Las variables del ecosistema podrán crecer.
- Las métricas genéricas podrán subdividirse o granularse.
- Los pesos y ponderaciones podrán iterarse y optimizarse.

**Restricción Fundamental:** Toda modificación del modelo deberá ser retrocompatible. Cualquier evolución en la lógica matemática implicará el recálculo histórico del universo completo para preservar el principio absoluto de Comparabilidad y Reproducibilidad. El registro de cada versión de la fórmula será permanente.
