import os
import tarfile
import datetime
import hashlib
from logger import log_event

BACKUP_DIR = "data/backups"
TARGETS = ["data/prospective", "logs"]

def run_backup():
    print("Iniciando Snapshot de Backup...")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    date_str = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"backup_winners_{date_str}.tar.gz")
    
    try:
        with tarfile.open(backup_file, "w:gz") as tar:
            for target in TARGETS:
                if os.path.exists(target):
                    tar.add(target, arcname=os.path.basename(target))
                    
        # Calcular Checksum
        sha256_hash = hashlib.sha256()
        with open(backup_file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
                
        checksum = sha256_hash.hexdigest()
        
        checksum_file = backup_file + ".sha256"
        with open(checksum_file, "w") as f:
            f.write(checksum + "\n")
            
        print(f"Backup creado exitosamente: {backup_file}")
        print(f"Checksum SHA256: {checksum}")
        log_event("BACKUP", "SUCCESS", extra_info=f"File: {backup_file} Hash: {checksum[:8]}...")
        
    except Exception as e:
        print(f"Fallo al crear backup: {e}")
        log_event("BACKUP", "FAILED", extra_info=str(e))

if __name__ == "__main__":
    run_backup()
