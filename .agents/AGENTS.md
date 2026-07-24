# Winners v1.0.0 - Reglas y Directrices Metodológicas

Estas directrices son **estrictamente vinculantes** para todos los agentes de IA y desarrolladores operando en el proyecto Winners. La fase de diseño concluyó. La fase actual es: **Fase VI — Recolección Prospectiva de Evidencia**.

## 1. Estado del Proyecto
- **Rama Principal (Producción):** Congelada. 
  - Código: `Winners v1.0.0`
  - Algoritmo: Congelado.
  - Parámetros: Congelados.
  - No se permiten adiciones de variables predictivas (xG, lesiones, modelos, ML, etc.).
  - Solo se permiten modificaciones para corregir bugs, problemas de estabilidad técnica o de auditoría.

## 2. Principio de Conservación de la Evidencia
Toda decisión futura debe responder a: *¿Esta modificación mejora la evidencia o únicamente mejora el resultado del backtest?* Si es lo segundo, se rechaza.
- La evidencia recogida prospectivamente (Paper Trading) tiene un valor infinitamente superior a cualquier cantidad de evidencia retrospectiva (Backtesting).
- Un año de *paper trading* vale más que cien nuevos backtests.
- Un resultado negativo prospectivo vale más que un resultado positivo retrospectivo.
- La capacidad de refutar la hipótesis es más importante que la capacidad de confirmarla.

## 3. Política de Ramas e Investigación
- Cualquier innovación o experimentación debe nacer obligatoriamente en una **rama de investigación independiente**.
- Ningún experimento puede contaminar la rama de Producción.
- Las ideas solo se promocionan si superan un protocolo prospectivo propio.

## 4. Criterios de Revisión
- Quedan estrictamente prohibidas las revisiones del modelo por resultados aislados.
- Las revisiones metodológicas se habilitarán exclusivamente al cruzar hitos volumétricos prospectivos:
  - 100 predicciones liquidadas.
  - 250 predicciones liquidadas.
  - 500 predicciones liquidadas.
  - 1000 predicciones liquidadas.
- Entre hitos, el sistema es intocable metodológicamente.

## 5. Política de Versiones
- **v1.x:** Correcciones técnicas (bugs, estabilidad, infraestructura, auditoría).
- **v2.0:** Primera versión que demuestre una mejora mediante evidencia prospectiva suficiente.
- **v3.0+:** Promociones posteriores tras repetir el mismo protocolo científico estricto.

## 6. Lenguaje
- Prohibido el lenguaje triunfalista, eufórico o definitivo ("ventaja confirmada", "hipótesis demostrada").
- Usar un léxico riguroso, científico y probabilístico ("la evidencia sugiere", "los resultados son consistentes con").

## 7. Principio de Humildad Epistémica
- Todo resultado obtenido por Winners será tratado como una estimación, nunca como una verdad.
- La ausencia de evidencia en contra no constituye evidencia definitiva a favor.
- Si el experimento demuestra que la ventaja desaparece, se aceptará con la misma naturalidad que una confirmación. Nuestro compromiso es con la realidad, no con el algoritmo.

## 8. Principio de Reproducibilidad
- Todo resultado importante deberá poder reproducirse desde cero.
- Cualquier investigador que utilice la misma versión del código, la misma configuración, los mismos datos y el mismo protocolo debe obtener idénticas conclusiones. Si no se puede reproducir, no forma parte de la evidencia.

## 9. Principio de Trazabilidad
- Cada número publicado debe responder inmediatamente a tres preguntas: ¿De qué datos proviene?, ¿Qué versión del algoritmo lo generó? y ¿Qué proceso lo transformó?
- Si alguna respuesta falla, el dato es descartado de cualquier conclusión.

## 10. Criterio de Éxito del Proyecto
- Winners no tendrá éxito por obtener un ROI positivo. Tendrá éxito si, al finalizar el experimento, se puede afirmar: *"Hemos construido un sistema cuyo proceso de generación de evidencia es confiable, auditable, reproducible y resistente al sesgo."*
- La rentabilidad económica es, en todo caso, una consecuencia del método riguroso, no su justificación.

## 11. Principio de Identidad Permanente
- Cada predicción constituye un expediente permanente.
- Un expediente nunca cambia de identidad ni de ubicación física.
- Su ciclo de vida se representa exclusivamente mediante la evolución de su estado interno y la incorporación de nueva evidencia.
- La estabilidad de la identidad tiene prioridad sobre la comodidad operacional.

## 12. Principio de Primacía de la Evidencia
- Ninguna convicción, expectativa o resultado retrospectivo tiene autoridad sobre la evidencia prospectiva observada.
- Cuando exista conflicto entre una hipótesis y los datos, se conserva el dato y se descarta la hipótesis.
- Winners no busca tener razón; busca medir la realidad con el menor sesgo posible.

## 13. Principio de Neutralidad ante el Resultado
- El laboratorio no tiene preferencia por confirmar ni por refutar la hipótesis.
- Un resultado negativo posee exactamente el mismo valor científico que un resultado positivo cuando ambos provienen de un proceso metodológicamente sólido.
- El éxito del proyecto se mide por la calidad de la evidencia obtenida, no por la dirección de sus conclusiones.

## 14. Principio de Continuidad Operacional
- La ausencia de predicciones no constituye evidencia. Si el calendario o los filtros no generan candidatos, el experimento sigue siendo válido.
- El sistema nunca deberá "forzar" oportunidades para mantener actividad.

## 15. Principio de Calidad sobre Cantidad
- Una única predicción correctamente registrada vale más que cien registros dudosos.
- Ante cualquier incertidumbre (cuotas, identidad, integridad, hash), la decisión correcta es no registrar la predicción y reportar el motivo. La ausencia de un dato es preferible a un dato contaminado.

## 16. Principio de Degradación Segura
- Si un componente falla (red, lectura, escritura), el sistema debe: detener el proceso afectado, registrar el error, conservar la evidencia y evitar estados parcialmente válidos.
- Un experimento incompleto es aceptable; un experimento corrupto no lo es.
