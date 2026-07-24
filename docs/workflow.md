# Flujo de Trabajo

El flujo de trabajo en **Winners** está dictado por los roles establecidos en el proyecto y garantiza un desarrollo ordenado y riguroso.

## Roles y Responsabilidades

- **Ares (Arquitecto del Sistema):**
  Define las reglas, especificaciones, métricas matemáticas y diseño de prompts. Nada funcional se altera sin su autorización explícita.
- **Forge (Ingeniero Principal):**
  Implementa las especificaciones de Ares. Traduce los algoritmos en código eficiente y modular. Mantiene la estructura del proyecto e implementa mejoras técnicas no funcionales proactivamente.
- **Jaalsima (Director del Proyecto):**
  Aprueba las decisiones, define la estrategia a alto nivel y valida que el desarrollo cumpla con los objetivos comerciales y de producto.

## Ciclo de Desarrollo

1. **Definición (Ares):** Ares emite una especificación técnica o arquitectónica clara sobre lo que se debe analizar, medir o desarrollar.
2. **Revisión y Propuesta (Forge):** Forge recibe la instrucción, diseña un plan de implementación técnica (o arquitectura) y, si es complejo, lo valida con Ares y Jaalsima antes de escribir código.
3. **Aprobación (Jaalsima/Ares):** Se da luz verde a la implementación técnica.
4. **Implementación (Forge):** Forge escribe el código en las carpetas correspondientes (`metrics/`, `models/`, `scripts/`, etc.), asegurando adherencia a los estándares (modularidad, reproducibilidad).
5. **Pruebas y Verificación:** Se ejecutan los tests de la carpeta `tests/` para verificar la estabilidad y correctitud estadística.
6. **Entrega de Resultados:** Se generan los reportes en la carpeta `results/`.
7. **Iteración:** Los resultados son evaluados y se retroalimenta a Ares para afinar el modelo de ser necesario.
