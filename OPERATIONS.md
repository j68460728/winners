# Manual de Operaciones - Winners v1.0.0

Este documento contiene exclusivamente las guías operativas para mantener y ejecutar la infraestructura prospectiva.

## 1. Ejecución del Sistema (Flujo Diario)

El ciclo de recolección prospectiva se divide en tres procesos secuenciales. No deben solaparse.

1. **Ingesta y Generación de Expedientes:**
   ```bash
   python src/prospective_pipeline.py
   ```
   *Genera expedientes `WIN-YYYYMMDD-XXXXX.json` en `data/prospective/` con estado PENDING.*

2. **Liquidación Automática:**
   ```bash
   python src/prospective_settler.py
   ```
   *Cruza los archivos PENDING con los resultados finales. Muta el estado a SETTLED o INVALID.*

3. **Reconstrucción del Diario:**
   ```bash
   python src/prospective_journal.py
   ```
   *Regenera `data/prospective/journal.md` desde cero a partir de los JSON liquidados.*

## 2. Observabilidad y Monitoreo

Para consultar el estado del experimento sin modificar datos:

```bash
python src/dashboard.py
```
*Reconstruye en memoria todas las métricas operacionales y de rendimiento (ROI, Max Drawdown, Evidence Age, Alertas).*

## 3. Validación de Integridad

Para verificar que ningún expediente ha sido corrompido, alterado manual o accidentalmente:

```bash
python src/integrity_check.py
```
*Verificará la concordancia de los hashes de configuración, la secuencia de timestamps y reportará duplicidades.*

## 4. Backups y Restauración

### Crear un Backup
```bash
python src/backup.py
```
*Empaquetará `data/prospective/` y `logs/` en un archivo `.tar.gz` dentro de `data/backups/`, acompañado de su firma SHA256.*

### Recuperar un Backup
1. Identificar el archivo deseado en `data/backups/`.
2. Verificar su firma: `sha256sum -c <backup_file>.sha256`.
3. Extraer el contenido para sobrescribir el directorio corrupto:
   ```bash
   tar -xzf data/backups/<backup_file>.tar.gz -C ./
   ```

## 5. Interpretación de Errores

| Error | Causa Probable | Acción Correctiva |
|-------|----------------|-------------------|
| `INVALID (Config Hash mismatch)` | El archivo fue modificado manualmente o generado con una versión distinta. | Ninguna. El sistema aísla la predicción. No debe corregirse manualmente. |
| `WARNING: Endpoint devolvió 404` | El proveedor de datos está caído temporalmente. | Reintentar más tarde. El sistema es resiliente a caídas temporales. |
| `CRITICAL: Falta el directorio` | Estructura base eliminada. | Ejecutar los scripts con permisos adecuados; se auto-generarán, o recuperar desde backup. |

## 6. Health Check y Reinicios

Si el sistema parece inestable, ejecutar:
```bash
python src/health_check.py
```
Si un proceso se queda colgado (ej. fallo de red prolongado), simplemente interrumpir (`Ctrl+C`) y volver a ejecutar. Ningún script operacional mantiene estados en memoria entre ejecuciones, por lo que son seguros para reiniciar en frío.
