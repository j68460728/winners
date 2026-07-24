import json
import glob
import os
import datetime
from logger import log_event
import pandas as pd
import requests
import io

PROSPECTIVE_DIR = "data/prospective"
URL_MAIN = "https://www.football-data.co.uk/fixtures.csv"
URL_EXTRA = "https://www.football-data.co.uk/new_league_fixtures.csv"

def get_url_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(io.BytesIO(response.content))
        
        # Estandarizar columnas para el observatorio
        if 'Date' in df.columns:
            df['ParsedDate'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
        else:
            df['ParsedDate'] = pd.NaT
            
        if 'Div' in df.columns: 
            df['LeagueCol'] = df['Div']
        elif 'League' in df.columns: 
            if 'Country' in df.columns:
                df['LeagueCol'] = df['Country'] + ' - ' + df['League']
            else:
                df['LeagueCol'] = df['League']
        else: 
            df['LeagueCol'] = 'Unknown'
            
        if 'HomeTeam' in df.columns: df['HomeCol'] = df['HomeTeam']
        elif 'Home' in df.columns: df['HomeCol'] = df['Home']
        else: df['HomeCol'] = 'Unknown'
            
        if 'AwayTeam' in df.columns: df['AwayCol'] = df['AwayTeam']
        elif 'Away' in df.columns: df['AwayCol'] = df['Away']
        else: df['AwayCol'] = 'Unknown'
            
        if 'Time' not in df.columns:
            df['Time'] = 'N/A'
            df['Time_Local'] = 'N/A'
        else:
            df['Time'] = df['Time'].fillna('N/A')
            def convert_time(row):
                if pd.isna(row['ParsedDate']) or row['Time'] == 'N/A':
                    return 'N/A'
                try:
                    dt_str = row['ParsedDate'].strftime('%Y-%m-%d') + ' ' + str(row['Time'])
                    dt_london = pd.to_datetime(dt_str).tz_localize('Europe/London')
                    dt_bogota = dt_london.tz_convert('America/Bogota')
                    return dt_bogota.strftime('%H:%M')
                except:
                    return 'N/A'
            df['Time_Local'] = df.apply(convert_time, axis=1)
            
        return df, "OK"
    except Exception as e:
        return pd.DataFrame(), f"ERROR: {str(e)}"

def audit_data_source():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    today = now_utc.date()
    tomorrow = today + datetime.timedelta(days=1)
    day_after = today + datetime.timedelta(days=2)
    
    print(f"\n--- AUDITANDO FUENTE DE DATOS ---")
    df_main, status_main = get_url_data(URL_MAIN)
    df_extra, status_extra = get_url_data(URL_EXTRA)
    print(f"fixtures.csv: {status_main} | {len(df_main)} registros")
    print(f"new_league_fixtures.csv: {status_extra} | {len(df_extra)} registros")
    
    max_date_main = df_main['ParsedDate'].dropna().max().strftime('%Y-%m-%d') if not df_main.empty and not df_main['ParsedDate'].dropna().empty else "N/A"
    max_date_extra = df_extra['ParsedDate'].dropna().max().strftime('%Y-%m-%d') if not df_extra.empty and not df_extra['ParsedDate'].dropna().empty else "N/A"
    
    dfs = []
    if not df_main.empty: dfs.append(df_main)
    if not df_extra.empty: dfs.append(df_extra)
    
    if dfs:
        df_all = pd.concat(dfs, ignore_index=True)
    else:
        df_all = pd.DataFrame(columns=['ParsedDate', 'LeagueCol', 'Time', 'HomeCol', 'AwayCol'])
        
    ligas_activas_counts = df_all['LeagueCol'].value_counts()
    
    # Ordenar por número de partidos de mayor a menor
    ligas_activas = [{"competicion": str(k), "partidos": int(v)} for k, v in ligas_activas_counts.items() if str(k) != 'Unknown']
    ligas_activas = sorted(ligas_activas, key=lambda x: x['partidos'], reverse=True)
    
    df_today = df_all[df_all['ParsedDate'].dt.date == today]
    partidos_hoy = []
    for _, row in df_today.iterrows():
        partidos_hoy.append({
            "competicion": str(row['LeagueCol']),
            "hora": str(row['Time']) if pd.notna(row['Time']) else "N/A",
            "hora_local": str(row['Time_Local']) if 'Time_Local' in row and pd.notna(row['Time_Local']) else "N/A",
            "local": str(row['HomeCol']),
            "visitante": str(row['AwayCol'])
        })
        
    df_next = df_all[(df_all['ParsedDate'].dt.date > today) & (df_all['ParsedDate'].dt.date <= day_after)]
    df_next = df_next.sort_values(by=['ParsedDate', 'Time'])
    proximos_partidos = []
    for _, row in df_next.iterrows():
        proximos_partidos.append({
            "fecha": row['ParsedDate'].strftime('%Y-%m-%d'),
            "competicion": str(row['LeagueCol']),
            "hora": str(row['Time']) if pd.notna(row['Time']) else "N/A",
            "hora_local": str(row['Time_Local']) if 'Time_Local' in row and pd.notna(row['Time_Local']) else "N/A",
            "local": str(row['HomeCol']),
            "visitante": str(row['AwayCol'])
        })
        
    return {
        "estado_fuente": {
            "ultima_consulta_utc": now_utc.isoformat(),
            "archivos_descargados": ["fixtures.csv", "new_league_fixtures.csv"],
            "registros_main": len(df_main),
            "registros_extra": len(df_extra),
            "total_registros": len(df_all),
            "total_competiciones": len(ligas_activas),
            "ultima_fecha_main": max_date_main,
            "ultima_fecha_extra": max_date_extra,
            "estado_main": status_main,
            "estado_extra": status_extra
        },
        "observacion_dia": {
            "ligas_activas": ligas_activas,
            "partidos_hoy": partidos_hoy
        },
        "proximos_partidos": proximos_partidos
    }

def build_dashboard():
    print("===================================================================")
    print("                     DASHBOARD DE OBSERVABILIDAD                   ")
    print("===================================================================")
    
    # 1. Auditoría de la Fuente (Aislamiento Operacional)
    observatorio_data = audit_data_source()
    
    # 2. Experimento Winners
    status_counts = {'PENDING': 0, 'SETTLED': 0, 'INVALID': 0}
    leagues_seen = set()
    algo_versions = set()
    config_hashes = set()
    total_profit = 0.0
    profit_history = []
    league_stats = {}
    first_date = None
    alerts = []
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    
    if os.path.exists(PROSPECTIVE_DIR):
        files = glob.glob(os.path.join(PROSPECTIVE_DIR, "WIN-*.json"))
        for filepath in sorted(files):
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            status = data.get('status', 'INVALID')
            status_counts[status] = status_counts.get(status, 0) + 1
            
            meta = data.get('metadata', {})
            algo_versions.add(meta.get('algo_version', 'UNKNOWN'))
            config_hashes.add(meta.get('config_hash', 'UNKNOWN'))
            
            gen_date = datetime.datetime.fromisoformat(meta.get('timestamp_utc', now_utc.isoformat()))
            if first_date is None or gen_date < first_date:
                first_date = gen_date
                
            league = data.get('match', {}).get('league', 'UNKNOWN')
            leagues_seen.add(league)
            
            if league not in league_stats:
                league_stats[league] = {'bets': 0, 'profit': 0.0}
                
            if status == 'INVALID':
                alerts.append(f"ALERTA: Archivo inválido detectado ({data.get('prediction_id')})")
            if status == 'PENDING':
                days_old = (now_utc - gen_date).days
                if days_old > 7:
                    alerts.append(f"ALERTA: Predicción pendiente demasiado antigua ({days_old} días) - {data.get('prediction_id')}")
                    
            if status == 'SETTLED':
                prof = data.get('settlement', {}).get('profit', 0.0)
                total_profit += prof
                profit_history.append(total_profit)
                league_stats[league]['bets'] += 1
                league_stats[league]['profit'] += prof
    else:
        print("Directorio prospectivo no encontrado. Se asume estado inicial vacío.")
        
    max_dd = 0.0
    if profit_history:
        peak = profit_history[0]
        for p in profit_history:
            if p > peak: peak = p
            dd = peak - p
            if dd > max_dd: max_dd = dd
            
    total_bets = status_counts['SETTLED']
    yield_pct = (total_profit / total_bets * 100) if total_bets > 0 else 0.0
    evidence_age = (now_utc - first_date).days if first_date else 0
    
    if len(config_hashes) > 1:
        alerts.append("ALERTA CRÍTICA: Múltiples hashes de configuración detectados.")
        
    last_run_path = os.path.join(PROSPECTIVE_DIR, "last_run.json")
    last_run = {}
    if os.path.exists(last_run_path):
        with open(last_run_path, "r") as f:
            last_run = json.load(f)
            
    # Ensamblar JSON
    dashboard_state = {
        "timestamp_utc": now_utc.isoformat(),
        "estado_experimento": {
            "evidence_age_days": evidence_age,
            "versiones_algoritmo": list(algo_versions),
            "hashes_config": list(config_hashes),
            "ligas_monitorizadas": len(leagues_seen)
        },
        "estado_operativo": {
            "predicciones_pendientes": status_counts.get('PENDING', 0),
            "predicciones_liquidadas": status_counts.get('SETTLED', 0),
            "predicciones_invalidas": status_counts.get('INVALID', 0),
            "ultima_observacion": last_run
        },
        "estado_financiero": {
            "apuestas_totales": total_bets,
            "beneficio_uds": round(total_profit, 2),
            "yield_pct": round(yield_pct, 2),
            "max_drawdown_uds": round(max_dd, 2)
        },
        "integridad": {
            "status": "PASS" if not alerts else "FAIL",
            "message": "ESTADO SALUDABLE" if not alerts else "ALERTAS ACTIVAS",
            "alerts": alerts
        },
        "observatorio": observatorio_data
    }
    
    os.makedirs("docs", exist_ok=True)
    with open("docs/dashboard_state.json", "w") as f:
        json.dump(dashboard_state, f, indent=4)
        
    print(f"\nGeneración de dashboard_state.json completada exitosamente.")
    log_event("DASHBOARD_RUN", "SUCCESS")
    print("===================================================================")

if __name__ == "__main__":
    build_dashboard()
