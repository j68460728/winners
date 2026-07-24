# Taxonomía de Hipótesis

Este documento establece el marco conceptual y de clasificación para todas las hipótesis del proyecto **Winners**. Las hipótesis no se agrupan simplemente por su dominio temático, sino por su **escala estructural**. 

Winners no es un modelo predictivo único, sino una **jerarquía de modelos**. Cada nivel explica un aspecto diferente del ecosistema futbolístico, permitiendo aislar el ruido y medir el poder predictivo con precisión quirúrgica.

---

## 1. Definición de Escalas

El sistema se divide en cuatro escalas de conocimiento:

- **Escala L1 — Liga:** Hipótesis que describen propiedades globales, estructurales y sistémicas del campeonato en su conjunto. Analizan el ecosistema donde ocurre la competencia.
- **Escala L2 — Equipo:** Hipótesis relacionadas con las propiedades intrínsecas, históricas o de rendimiento de un club de manera aislada.
- **Escala L3 — Enfrentamiento (Matchup):** Hipótesis que *solo existen* cuando dos equipos interactúan. Miden la asimetría relativa o el contexto histórico entre ambos escudos, independientemente de cuándo jueguen.
- **Escala L4 — Partido (Evento):** Hipótesis relacionadas exclusivamente con el evento espacio-temporal concreto. Factores dinámicos y efímeros que alteran el resultado en ese día específico.

---

## 2. Criterios de Asignación de Escala

Para determinar a qué escala pertenece una nueva hipótesis, se debe aplicar el siguiente filtro secuencial:
1. *¿La hipótesis depende de la fecha, la hora, el árbitro asignado o el clima de ese día?* **→ L4 (Partido)**
2. *¿La hipótesis requiere conocer quién es el rival para poder evaluarse (ej. historial, distancia entre ciudades, rivalidad)?* **→ L3 (Enfrentamiento)**
3. *¿La hipótesis evalúa el estilo de juego, economía o métricas de un solo club de forma aislada?* **→ L2 (Equipo)**
4. *¿La hipótesis describe el formato, la distribución económica global o la historia del torneo en sí?* **→ L1 (Liga)**

---

## 3. Reubicación de las 15 Hipótesis Actuales

Las hipótesis originales han sido reasignadas a su escala correspondiente, actualizando su identificador oficial.

### Escala L1 (Liga)
- **L1-H-0001:** Estabilidad de Campeones (Concentración histórica de títulos).
- **L1-H-0002:** Límite Salarial y Entropía (Regulaciones financieras globales).
- **L1-H-0004:** Volatilidad por Torneos Cortos (Formatos de competición).
- **L1-H-0008:** Efecto del Arbitraje Tecnológico (Presencia de VAR).
- **L1-H-0009:** Desigualdad en Derechos de TV (Distribución de ingresos).
- **L1-H-0011:** Efecto Ascensor (Brecha estructural entre divisiones).
- **L1-H-0015:** Contradicción del Factor Campo (Nula ventaja local en países logísticamente eficientes).

### Escala L2 (Equipo)
- **L2-H-0005:** Control de Posesión como Seguros contra el Azar (Dominio táctico y PPDA de un equipo).
- **L2-H-0012:** Inestabilidad Directiva (Alta rotación de entrenadores de un club, reubicada de L1 a L2 por su naturaleza aislada).

### Escala L3 (Enfrentamiento)
- **L3-H-0013:** El Sesgo Geográfico de la Altitud (Diferencial de altitud entre el equipo local y el visitante).
- **L3-H-0014:** Inflación Artificial por Derbis (Rivalidades históricas entre dos equipos específicos).
- **L3-H-0003:** Impacto de las Grandes Distancias (Desgaste logístico en un viaje específico entre dos ciudades).

### Escala L4 (Partido)
- **L4-H-0006:** Congestión del Calendario (Fatiga puntual por acumulación de torneos en la fecha del evento).
- **L4-H-0007:** Ruido Arbitral (Impacto del sesgo del colegiado asignado y tarjetas rojas en ese evento).
- **L4-H-0010:** Resiliencia Climática (Clima extremo el día del partido).

---

## 4. Identificación de Hipótesis Mal Ubicadas o Superpuestas

La auditoría de reclasificación reveló importantes solapamientos conceptuales en el registro original:

- **H-0003 (Grandes Distancias) vs H-0015 (Contradicción del Factor Campo):** Inicialmente concebidas como características globales de la liga (L1), pero en realidad, la distancia (H-0003) se mide entre dos rivales específicos (L3). H-0015 sí es L1 porque describe el ecosistema global de un país pequeño.
- **H-0006 (Congestión del Calendario):** Originalmente generalizada, pero la fatiga no es estructural (L1) ni intrínseca al equipo siempre (L2), es una variable temporal que solo afecta a **partidos específicos** (L4) jugados 72 horas después de un torneo continental.
- **H-0012 (Inestabilidad Directiva):** Estaba pensada como la suma de despidos de una liga, pero matemáticamente es mucho más predictiva si se evalúa a nivel de club (L2) para medir la crisis interna de un equipo antes de un enfrentamiento.

---

## 5. Reglas Metodológicas para Futuras Hipótesis

1. **Prefijo Obligatorio:** Todo identificador deberá nacer con el prefijo de su escala (ej. `L3-H-0050`).
2. **Principio de Especificidad:** Si una hipótesis parece encajar en dos niveles, se debe asignar siempre al **nivel más específico (más profundo)** posible. (Ejemplo: Si duda entre L1 y L2, es L2. Si duda entre L2 y L4, es L4).
3. **Múltiples escalas, múltiples hipótesis:** Si un concepto afecta a más de una escala, no se fusiona; se dividen en dos hipótesis distintas (Ej. L1-H-XXXX para "Tasa de penaltis de la liga" y L4-H-YYYY para "Sesgo del árbitro de turno").
