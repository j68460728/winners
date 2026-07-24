import os
import urllib.request
from logger import log_event

CRITICAL_DIRS = ["data/prospective", "logs", "data/backups"]
ENDPOINTS = ["https://www.football-data.co.uk/fixtures.csv"]

def run_health_check():
    print("Iniciando Verificación de Salud Operacional...\n")
    
    status = "HEALTHY"
    messages = []
    
    # 1. Verificar Directorios y Permisos
    for d in CRITICAL_DIRS:
        if not os.path.exists(d):
            messages.append(f"CRITICAL: Falta el directorio {d}")
            status = "CRITICAL"
        elif not os.access(d, os.W_OK):
            messages.append(f"CRITICAL: Directorio {d} no tiene permisos de escritura.")
            status = "CRITICAL"
        else:
            messages.append(f"OK: Directorio {d} accesible y escribible.")
            
    # 2. Verificar Endpoints de Datos
    for url in ENDPOINTS:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=10)
            if response.getcode() == 200:
                messages.append(f"OK: Endpoint {url} alcanzable.")
            else:
                messages.append(f"WARNING: Endpoint {url} devolvió código {response.getcode()}.")
                if status == "HEALTHY": status = "WARNING"
        except Exception as e:
            messages.append(f"WARNING: Fallo al contactar {url} - {e}")
            if status == "HEALTHY": status = "WARNING"
            
    print(f"ESTADO GLOBAL: [{status}]")
    for msg in messages:
        print(f"  {msg}")
        
    log_event("HEALTH_CHECK", status, extra_info="Health check executed.")
    return status

if __name__ == "__main__":
    run_health_check()
