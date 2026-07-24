import json
import os
import glob
import urllib.request
import io
import pandas as pd
import datetime
import hashlib
from prospective_pipeline import get_config_hash, STATIC_CONFIG

PROSPECTIVE_DIR = "data/prospective"

def download_latest_results(league_code):
    # Utilizamos la temporada actual, asumiendo 2425 (para el ejemplo) 
    # En producción deberíamos inferirla o probar varias
    url = f"https://www.football-data.co.uk/mmz4281/2425/{league_code}.csv"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        return pd.read_csv(io.StringIO(response.read().decode('utf-8', errors='ignore')))
    except:
        return pd.DataFrame()

def run_settler():
    print("Iniciando Liquidador Automático (Settler)...")
    
    if not os.path.exists(PROSPECTIVE_DIR):
        print("No hay directorio prospectivo.")
        return
        
    pending_files = glob.glob(os.path.join(PROSPECTIVE_DIR, "WIN-*.json"))
    
    if not pending_files:
        print("No hay archivos para auditar.")
        return
        
    # Cache results per league
    results_cache = {}
    
    current_hash = get_config_hash()
    utc_now = datetime.datetime.now(datetime.UTC).isoformat()
    
    for filepath in pending_files:
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        if data.get('status') != 'PENDING':
            continue
            
        # 1. Integrity Check
        metadata = data.get('metadata', {})
        if metadata.get('config_hash') != current_hash:
            data['status'] = 'INVALID'
            data['settlement'] = {'reason': 'Config Hash mismatch. Integrity failed.'}
            with open(filepath, 'w') as f: json.dump(data, f, indent=4)
            print(f"Predicción {data['prediction_id']} invalidada por falla de integridad.")
            continue
            
        # Podríamos verificar timestamp vs inicio del partido si tuviéramos la hora del kickoff
        # Asumiremos integridad temporal por ahora.
        
        match_info = data['match']
        league = match_info['league']
        league_code = STATIC_CONFIG[league]['code']
        
        if league_code not in results_cache:
            results_cache[league_code] = download_latest_results(league_code)
            
        df_res = results_cache[league_code]
        if df_res.empty: continue
            
        # Buscar el partido (por fecha y equipos)
        # La fecha en fixtures a veces varía un día respecto a results, usamos equipos.
        h_t = match_info['home_team']
        a_t = match_info['away_team']
        
        match_row = df_res[(df_res['HomeTeam'] == h_t) & (df_res['AwayTeam'] == a_t)]
        
        if not match_row.empty:
            # Se jugó
            ftr = match_row.iloc[-1]['FTR']
            
            winners_pick = data['prediction']['winners_pick']
            winners_odds = data['prediction']['winners_odds']
            
            won = (ftr == winners_pick)
            profit = (winners_odds - 1.0) if won else -1.0
            
            data['status'] = 'SETTLED'
            data['settlement'] = {
                'result': ftr,
                'profit': round(profit, 2),
                'settlement_timestamp_utc': utc_now,
                'source': 'football-data.co.uk (historical CSV)'
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
                
            print(f"Predicción {data['prediction_id']} liquidada. Profit: {profit:+.2f} uds.")
            
if __name__ == "__main__":
    run_settler()
