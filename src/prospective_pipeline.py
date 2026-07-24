import pandas as pd
import urllib.request
import io
import ssl
import json
import datetime
import hashlib
import os

ssl._create_default_https_context = ssl._create_unverified_context

ALGO_VERSION = "1.0.0"
STATIC_CONFIG = {
    'Premier': {'code': 'E0', 'window': 5, 'top_pct': 0.20, 'bottom_pct': 0.30},
    '2.Bundesliga': {'code': 'D2', 'window': 5, 'top_pct': 0.20, 'bottom_pct': 0.30}
}
PROVIDER = "football-data.co.uk"
DATASET_VERSION = "fixtures.csv (Live)"
PROSPECTIVE_DIR = "data/prospective"

def get_config_hash():
    config_str = json.dumps(STATIC_CONFIG, sort_keys=True)
    return hashlib.sha256(config_str.encode()).hexdigest()

def get_hierarchy(league_code, window_size):
    seasons = ['1920', '2021', '2122', '2223', '2324']
    all_hist = []
    for season in seasons:
        url = f"https://www.football-data.co.uk/mmz4281/{season}/{league_code}.csv"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            df = pd.read_csv(io.StringIO(response.read().decode('utf-8', errors='ignore')))
            all_hist.append(df)
        except:
            pass
            
    if not all_hist: return []
    df_hist = pd.concat(all_hist, ignore_index=True)
    df_hist = df_hist.dropna(subset=['FTR'])
    
    home_pts = df_hist.groupby('HomeTeam')['FTR'].apply(lambda x: (x == 'H').sum() * 3 + (x == 'D').sum()).reset_index()
    home_pts.columns = ['Team', 'Pts']
    away_pts = df_hist.groupby('AwayTeam')['FTR'].apply(lambda x: (x == 'A').sum() * 3 + (x == 'D').sum()).reset_index()
    away_pts.columns = ['Team', 'Pts']
    
    total_pts = pd.concat([home_pts, away_pts]).groupby('Team')['Pts'].sum().sort_values(ascending=False)
    return total_pts

def run_prospective_pipeline():
    os.makedirs(PROSPECTIVE_DIR, exist_ok=True)
    
    print("Descargando fixtures futuros...")
    url = "https://www.football-data.co.uk/fixtures.csv"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        df_fix = pd.read_csv(io.StringIO(response.read().decode('utf-8', errors='ignore')))
    except Exception as e:
        print(f"Error descargando fixtures: {e}")
        return
        
    utc_now = datetime.datetime.now(datetime.UTC).isoformat()
    date_str = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d")
    
    odds_h = ['B365H', 'BWH', 'IWH', 'PSH', 'WHH', 'VCH', 'AvgH']
    odds_a = ['B365A', 'BWA', 'IWA', 'PSA', 'WHA', 'VCA', 'AvgA']
    
    prediction_count = 1
    
    for league, config in STATIC_CONFIG.items():
        hierarchy = get_hierarchy(config['code'], config['window'])
        if len(hierarchy) == 0: continue
            
        n_teams = len(hierarchy)
        top_teams = hierarchy.head(max(1, int(n_teams * config['top_pct']))).index.tolist()
        bot_teams = hierarchy.tail(max(1, int(n_teams * config['bottom_pct']))).index.tolist()
        
        df_league_fix = df_fix[df_fix['Div'] == config['code']].copy()
        
        avail_h = [c for c in odds_h if c in df_league_fix.columns]
        avail_a = [c for c in odds_a if c in df_league_fix.columns]
        
        for _, match in df_league_fix.iterrows():
            h_t, a_t = match['HomeTeam'], match['AwayTeam']
            
            m_odds_h = match[avail_h].mean(skipna=True) if avail_h else None
            m_odds_a = match[avail_a].mean(skipna=True) if avail_a else None
            
            if pd.isna(m_odds_h) or pd.isna(m_odds_a):
                continue
                
            bet_placed = False
            winners_pick = None
            winners_odds = None
            
            if h_t in top_teams and a_t in bot_teams:
                bet_placed, winners_pick, winners_odds = True, 'H', m_odds_h
            elif a_t in top_teams and h_t in bot_teams:
                bet_placed, winners_pick, winners_odds = True, 'A', m_odds_a
                
            if bet_placed:
                mkt_pick = 'H' if m_odds_h <= m_odds_a else 'A'
                mkt_odds = m_odds_h if mkt_pick == 'H' else m_odds_a
                
                prediction_id = f"WIN-{date_str}-{prediction_count:05d}"
                
                log_data = {
                    'prediction_id': prediction_id,
                    'status': 'PENDING',
                    'metadata': {
                        'timestamp_utc': utc_now,
                        'algo_version': ALGO_VERSION,
                        'config_hash': get_config_hash(),
                        'data_provider': PROVIDER,
                        'dataset_version': DATASET_VERSION,
                        'repo_commit': 'N/A'
                    },
                    'match': {
                        'league': league,
                        'date': str(match['Date']),
                        'home_team': h_t,
                        'away_team': a_t
                    },
                    'prediction': {
                        'winners_pick': winners_pick,
                        'mkt_pick': mkt_pick,
                        'winners_odds': float(winners_odds),
                        'mkt_odds': float(mkt_odds)
                    },
                    'settlement': {}
                }
                
                filepath = os.path.join(PROSPECTIVE_DIR, f"{prediction_id}.json")
                with open(filepath, 'w') as f:
                    json.dump(log_data, f, indent=4)
                    
                prediction_count += 1
                print(f"Generada predicción irreversible: {prediction_id}")
                
    # Guardar estado de la última observación
    last_run_data = {
        "timestamp_utc": utc_now,
        "source": PROVIDER,
        "leagues_inspected": len(STATIC_CONFIG),
        "matches_found": (prediction_count - 1),
        "status": "Observación completada correctamente."
    }
    with open(os.path.join(PROSPECTIVE_DIR, "last_run.json"), "w") as f:
        json.dump(last_run_data, f, indent=4)
        
if __name__ == "__main__":
    run_prospective_pipeline()
