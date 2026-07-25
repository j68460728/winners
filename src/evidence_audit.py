import os
import json
import glob
import sys
import re

PROSPECTIVE_DIR = "data/prospective"
JOURNAL_PATH = "data/prospective/journal.md"

def audit_evidence():
    print("Iniciando auditoría de evidencia prospectiva...")
    
    if not os.path.exists(PROSPECTIVE_DIR):
        print("El directorio de evidencia no existe.")
        sys.exit(1)
        
    json_files = glob.glob(os.path.join(PROSPECTIVE_DIR, "WIN-*.json"))
    
    status_counts = {"PENDING": 0, "SETTLED": 0, "INVALID": 0}
    corrupt_files = 0
    ids_seen = set()
    duplicates = 0
    
    for filepath in json_files:
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            pred_id = data.get("prediction_id")
            if not pred_id:
                print(f"Error: Archivo {filepath} no tiene prediction_id")
                corrupt_files += 1
                continue
                
            if pred_id in ids_seen:
                print(f"Error: ID duplicado detectado -> {pred_id}")
                duplicates += 1
            else:
                ids_seen.add(pred_id)
                
            status = data.get("status")
            if status in status_counts:
                status_counts[status] += 1
            else:
                print(f"Error: Estado desconocido '{status}' en {filepath}")
                corrupt_files += 1
                
        except json.JSONDecodeError:
            print(f"Error: Archivo corrupto (JSON inválido) -> {filepath}")
            corrupt_files += 1
        except Exception as e:
            print(f"Error inesperado procesando {filepath}: {e}")
            corrupt_files += 1

    print("\n--- Resultados de Auditoría de Expedientes ---")
    print(f"Total expedientes: {len(json_files)}")
    print(f"PENDING: {status_counts['PENDING']}")
    print(f"SETTLED: {status_counts['SETTLED']}")
    print(f"INVALID: {status_counts['INVALID']}")
    print(f"Archivos corruptos: {corrupt_files}")
    print(f"IDs duplicados: {duplicates}")
    
    if corrupt_files > 0 or duplicates > 0:
        print("FALLO: Se encontraron inconsistencias en los expedientes JSON.")
        sys.exit(1)
        
    # Validar journal.md
    if not os.path.exists(JOURNAL_PATH):
        if len(json_files) > 0:
            print("FALLO: journal.md no existe, pero hay expedientes.")
            sys.exit(1)
    else:
        with open(JOURNAL_PATH, 'r') as f:
            journal_content = f.read()
            
        # Buscar la línea de Muestra N
        match = re.search(r"\*\*Predicciones Liquidadas \(Muestra N\):\*\* (\d+)", journal_content)
        if match:
            journal_settled = int(match.group(1))
            if journal_settled != status_counts['SETTLED']:
                print(f"FALLO: Inconsistencia en journal.md. Reporta {journal_settled} liquidadas, pero hay {status_counts['SETTLED']} JSONs en estado SETTLED.")
                sys.exit(1)
        else:
            if status_counts['SETTLED'] > 0:
                print("FALLO: No se encontró la métrica de Predicciones Liquidadas en journal.md.")
                sys.exit(1)
                
    print("ÉXITO: Cadena de custodia validada. La evidencia es íntegra.")
    sys.exit(0)

if __name__ == "__main__":
    audit_evidence()
