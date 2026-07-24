# Guía para Futuros Colaboradores

¡Bienvenido al proyecto **Winners**!

Este documento establece las pautas para asegurar que cualquier persona o agente que se integre al proyecto pueda mantener los altos estándares de ingeniería impuestos por la dirección técnica.

## 1. Conoce el Proyecto
Antes de tocar cualquier línea de código, lee obligatoriamente:
- `README.md`
- `docs/vision.md`
- `docs/architecture.md`

## 2. Respeta los Roles
- Las reglas de negocio, la lógica algorítmica y las definiciones estadísticas son exclusivas del Arquitecto del Sistema (**Ares**).
- No introduzcas alteraciones funcionales, cálculos nuevos o pesos en variables sin la aprobación previa de Ares o la Dirección del Proyecto (**Jaalsima**).

## 3. Normas de Integración (PRs)
- **Cero Código "Sucio":** Cualquier script o función debe tener dependencias inyectadas o centralizadas, nunca variables mágicas dispersas.
- **Evidencia Empírica:** Si propones una nueva métrica matemática, acompáñala de un script experimental en la carpeta `research/` que demuestre su utilidad cuantitativamente.
- **Documentación en Tiempo Real:** Actualiza la documentación relevante dentro de `docs/` en el mismo Pull Request o sesión de trabajo en el que alteres el código.
- **No a la subjetividad:** Todo cálculo debe tener justificación objetiva y determinista.

## 4. Comunicación
Ante cualquier duda en el diseño o interpretación de una métrica, paraliza la implementación y eleva una consulta técnica al Arquitecto del Sistema. En este proyecto preferimos detenernos a confirmar la matemática que implementar supuestos incorrectos.
