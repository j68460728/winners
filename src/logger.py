import os
import datetime
from prospective_pipeline import ALGO_VERSION

LOGS_DIR = "logs"

def log_event(process_name, result, prediction_id="N/A", extra_info=""):
    os.makedirs(LOGS_DIR, exist_ok=True)
    utc_now = datetime.datetime.now(datetime.UTC).isoformat()
    log_file = os.path.join(LOGS_DIR, "system.log")
    
    # Format: UTC | ID | Versión | Proceso | Resultado | Extra
    log_entry = f"{utc_now} | {prediction_id} | {ALGO_VERSION} | {process_name} | {result} | {extra_info}\n"
    
    with open(log_file, "a") as f:
        f.write(log_entry)
        
if __name__ == "__main__":
    log_event("LOGGER_INIT", "SUCCESS", extra_info="Logger system initialized.")
