import os
import shutil
import zipfile
import re
import hashlib
import time

ACRONYMS = {"FC", "CF", "RB", "SV", "AC", "CD", "PSV", "AZ", "RC", "US", "SSC", "IFK", "AIK", "LP", "SC", "AFC", "RSC"}

def get_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def get_hash_from_bytes(data):
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()

def clean_name(filename):
    name = os.path.splitext(filename)[0]
    
    # 1. Remove .football-logos.cc
    name = name.replace(".football-logos.cc", "")
    
    # 2. Remove resolutions
    name = re.sub(r'[_|-]?\d+x\d+', '', name)
    
    # 3. Strip country prefixes
    if '_' in name:
        name = name.split('_')[-1]
        
    # 4. Replace hyphens with spaces
    name = name.replace("-", " ")
    
    # 5. Clean spaces and Title Case
    name = ' '.join(name.split())
    name = name.title()
    
    # 6. Fix common acronyms using exact word match
    words = name.split()
    for i, word in enumerate(words):
        if word.upper() in ACRONYMS:
            words[i] = word.upper()
    name = " ".join(words)
    
    return name

def main():
    start_time = time.time()
    
    base_dir = "FootballAssets/football-logos"
    legacy_1 = os.path.join(base_dir, "logos_legacy_1")
    legacy_2 = os.path.join(base_dir, "logos_legacy_2")
    out_dir = os.path.join(base_dir, "logos", "clubs")
    conflicts_dir = os.path.join(base_dir, "logos", "conflicts")
    
    # Reset directories to ensure fully clean and idempotent run
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    if os.path.exists(conflicts_dir):
        shutil.rmtree(conflicts_dir)
        
    os.makedirs(out_dir, exist_ok=True)
    
    stats = {
        "procesadas": 0,
        "copiadas": 0,
        "descartadas": 0,
        "duplicadas": 0,
        "conflictos": 0,
        "zips": 0,
        "corruptos": 0,
        "modificados": 0
    }
    
    registry = {}
    conflict_log = []
    
    def register_file(std_name, data, source_info):
        stats["procesadas"] += 1
        file_hash = get_hash_from_bytes(data)
        
        if std_name not in registry:
            registry[std_name] = []
            
        for existing_path, existing_hash in registry[std_name]:
            if file_hash == existing_hash:
                stats["duplicadas"] += 1
                return None
                
        # Conflict detection
        if len(registry[std_name]) > 0:
            stats["conflictos"] += 1
            # Ensure conflicts dir exists for this team
            team_conflict_dir = os.path.join(conflicts_dir, std_name)
            os.makedirs(team_conflict_dir, exist_ok=True)
            
            # Use original filename for uniqueness in conflict folder
            # Source info might be "archive.zip -> filename.png"
            clean_source_name = source_info.split('->')[-1].strip().split('/')[-1]
            if not clean_source_name.endswith('.png'):
                clean_source_name += '.png'
            
            # If this name is already taken in the conflict dir, append a number
            final_path = os.path.join(team_conflict_dir, clean_source_name)
            idx = 1
            while os.path.exists(final_path):
                base, ext = os.path.splitext(clean_source_name)
                final_path = os.path.join(team_conflict_dir, f"{base}_{idx}{ext}")
                idx += 1
                
            conflict_log.append(f"- **Conflicto Aisaldo:** `{std_name}` de `{source_info}` guardado en `{final_path}`")
            
            with open(final_path, 'wb') as f:
                f.write(data)
            
            registry[std_name].append((final_path, file_hash))
            return None # Do not count as "copiadas" to master
            
        else:
            final_path = os.path.join(out_dir, f"{std_name}.png")
            registry[std_name].append((final_path, file_hash))
            
            with open(final_path, 'wb') as f:
                f.write(data)
            
            stats["copiadas"] += 1
            if std_name != source_info.split('/')[-1]:
                stats["modificados"] += 1
                
            return std_name

    # Process legacy 1
    if os.path.exists(legacy_1):
        for root, dirs, files in os.walk(legacy_1):
            for file in files:
                if not file.lower().endswith(('.png', '.svg')):
                    continue
                path = os.path.join(root, file)
                std_name = clean_name(file)
                try:
                    with open(path, 'rb') as f:
                        data = f.read()
                    register_file(std_name, data, path)
                except Exception as e:
                    stats["corruptos"] += 1

    # Process legacy 2 (ZIPs)
    if os.path.exists(legacy_2):
        for file in os.listdir(legacy_2):
            if file.lower().endswith('.zip'):
                stats["zips"] += 1
                zip_path = os.path.join(legacy_2, file)
                try:
                    with zipfile.ZipFile(zip_path, 'r') as z:
                        # Group by standardized name
                        teams_files = {}
                        for zinfo in z.infolist():
                            if zinfo.is_dir() or not zinfo.filename.lower().endswith('.png'):
                                continue
                                
                            filename = os.path.basename(zinfo.filename)
                            std_name = clean_name(filename)
                            
                            # Parse resolution from path (e.g., "512x512/team.png")
                            res = 0
                            match = re.search(r'(\d+)x\d+', zinfo.filename)
                            if match:
                                res = int(match.group(1))
                                
                            if std_name not in teams_files:
                                teams_files[std_name] = []
                            teams_files[std_name].append((res, zinfo))
                            
                        # Extract the highest resolution for each team
                        for std_name, files_list in teams_files.items():
                            files_list.sort(key=lambda x: x[0], reverse=True)
                            best_file = files_list[0][1]
                            
                            data = z.read(best_file)
                            register_file(std_name, data, f"{file} -> {best_file.filename}")
                except Exception as e:
                    stats["corruptos"] += 1

    elapsed = time.time() - start_time
    
    # Generar Reporte
    report = f"""# Reporte de Migración de Escudos

**Fecha de Ejecución:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**Tiempo de Ejecución:** {elapsed:.2f} segundos

## 📊 Auditoría Final
- **Número total de escudos disponibles en master:** {stats['copiadas']}
- **Número de clubes únicos procesados:** {len(registry)}
- **Archivos ZIP procesados:** {stats['zips']}

## 📈 Estadísticas de Procesamiento
- **Imágenes analizadas (procesadas):** {stats['procesadas']}
- **Imágenes guardadas (copiadas):** {stats['copiadas']}
- **Imágenes duplicadas (mismo hash, descartadas):** {stats['duplicadas']}
- **Conflictos (distinto hash, mismo nombre):** {stats['conflictos']}
- **Nombres estandarizados/modificados:** {stats['modificados']}
- **Archivos corruptos/ilegibles:** {stats['corruptos']}

## ⚠️ Registro de Conflictos
"""
    if conflict_log:
        report += "\\n".join(conflict_log)
    else:
        report += "No se encontraron conflictos. Todos los duplicados eran idénticos byte a byte."
        
    report += "\\n\\n*Nota: Los directorios `logos_legacy_1` y `logos_legacy_2` se han mantenido intactos para preservar la trazabilidad total.*"

    with open("migration_report.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"Migración completada. Procesados {stats['procesadas']} archivos. Ver migration_report.md para más detalles.")

if __name__ == "__main__":
    main()
