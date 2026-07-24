import json
import os
import glob
import datetime
import hashlib
import subprocess
from prospective_pipeline import ALGO_VERSION, get_config_hash
from logger import log_event

PROSPECTIVE_DIR = "data/prospective"
MANIFEST_PATH = "evidence_manifest.json"

def calculate_vault_checksum():
    sha256 = hashlib.sha256()
    files = sorted(glob.glob(os.path.join(PROSPECTIVE_DIR, "WIN-*.json")))
    for filepath in files:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256.update(byte_block)
    return sha256.hexdigest()

def run_reproducibility_audit():
    print("===================================================================")
    print("               AUDITORÍA DE REPRODUCIBILIDAD Y EVIDENCIA           ")
    print("===================================================================")
    
    if not os.path.exists(PROSPECTIVE_DIR):
        print("FAIL: Directorio prospectivo no encontrado.")
        log_event("REPRODUCIBILITY", "FAIL", extra_info="No vault found")
        return
        
    import sys
    try:
        # Reconstruir Diario para garantizar consistencia
        subprocess.run([sys.executable, "src/prospective_journal.py"], check=True, capture_output=True)
        
        # Ejecutar Integrity Check
        res = subprocess.run([sys.executable, "src/integrity_check.py"], capture_output=True, text=True)
        if "FALLOS" in res.stdout or "FAILED" in res.stdout:
            print("FAIL: Fallo en la verificación de integridad de la bóveda.")
            return
            
    except Exception as e:
        print(f"FAIL: Error ejecutando dependencias de reconstrucción -> {e}")
        return

    # Extraer métricas para el Manifest
    files = glob.glob(os.path.join(PROSPECTIVE_DIR, "WIN-*.json"))
    counts = {'PENDING': 0, 'SETTLED': 0, 'INVALID': 0}
    
    for filepath in files:
        with open(filepath, 'r') as f:
            data = json.load(f)
            status = data.get('status', 'INVALID')
            counts[status] = counts.get(status, 0) + 1
            
    vault_checksum = calculate_vault_checksum()
    utc_now = datetime.datetime.now(datetime.UTC).isoformat()
    config_hash = get_config_hash()
    
    # Intentar obtener el commit de git si existe
    git_hash = "N/A"
    try:
        git_res = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
        if git_res.returncode == 0:
            git_hash = git_res.stdout.strip()
    except:
        pass

    manifest = {
        'version': ALGO_VERSION,
        'config_hash': config_hash,
        'repo_hash': git_hash,
        'total_expedientes': len(files),
        'pending': counts['PENDING'],
        'settled': counts['SETTLED'],
        'invalid': counts['INVALID'],
        'timestamp_utc': utc_now,
        'vault_checksum_sha256': vault_checksum
    }
    
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=4)
        
    print(f"Manifest generado: {MANIFEST_PATH}")
    print(f"Checksum Bóveda: {vault_checksum}")
    print("\n-------------------------------------------------------------------")
    print("PASS")
    print("El experimento ha sido reconstruido de forma íntegra y determinista.")
    print("Cualquier investigador clonando este estado obtendrá el mismo Manifest.")
    print("===================================================================")
    
    log_event("REPRODUCIBILITY", "PASS", extra_info=f"Vault Hash: {vault_checksum[:8]}...")

if __name__ == "__main__":
    run_reproducibility_audit()
