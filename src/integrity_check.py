import json
import glob
import os
import datetime
from logger import log_event
from prospective_pipeline import get_config_hash

PROSPECTIVE_DIR = "data/prospective"

def run_integrity_check():
    print("Iniciando Verificador de Integridad...")
    
    if not os.path.exists(PROSPECTIVE_DIR):
        print("Directorio prospectivo no encontrado.")
        log_event("INTEGRITY_CHECK", "FAILED", extra_info="Directory missing")
        return
        
    files = glob.glob(os.path.join(PROSPECTIVE_DIR, "WIN-*.json"))
    
    expected_hash = get_config_hash()
    
    seen_ids = set()
    errors = []
    
    for filepath in sorted(files):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except Exception as e:
            errors.append(f"JSON Malformado en {filepath}: {e}")
            continue
            
        pred_id = data.get('prediction_id')
        if not pred_id:
            errors.append(f"Falta prediction_id en {filepath}")
            continue
            
        if pred_id in seen_ids:
            errors.append(f"ID Duplicado encontrado: {pred_id}")
        seen_ids.add(pred_id)
        
        meta = data.get('metadata', {})
        if meta.get('config_hash') != expected_hash:
            errors.append(f"Inconsistencia de Hash en {pred_id}. Esperado: {expected_hash}")
            
        # Timestamp logic
        gen_time_str = meta.get('timestamp_utc')
        if not gen_time_str:
            errors.append(f"Falta timestamp_utc en {pred_id}")
        else:
            try:
                gen_time = datetime.datetime.fromisoformat(gen_time_str)
                if data.get('status') == 'SETTLED':
                    set_time_str = data.get('settlement', {}).get('settlement_timestamp_utc')
                    if set_time_str:
                        set_time = datetime.datetime.fromisoformat(set_time_str)
                        if set_time < gen_time:
                            errors.append(f"Inconsistencia Temporal en {pred_id}: Liquidación anterior a Generación.")
            except Exception as e:
                errors.append(f"Error de formato de fecha en {pred_id}: {e}")
                
    if not errors:
        print(f"Verificación completada: {len(files)} expedientes íntegros.")
        log_event("INTEGRITY_CHECK", "SUCCESS", extra_info=f"{len(files)} valid records")
    else:
        print(f"!!! SE DETECTARON {len(errors)} FALLOS DE INTEGRIDAD !!!")
        for err in errors:
            print(f"- {err}")
        log_event("INTEGRITY_CHECK", "WARNING", extra_info=f"{len(errors)} errors found")

if __name__ == "__main__":
    run_integrity_check()
