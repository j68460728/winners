import json
import glob
import os
import datetime
from logger import log_event

PROSPECTIVE_DIR = "data/prospective"

def build_dashboard():
    print("===================================================================")
    print("                     DASHBOARD DE OBSERVABILIDAD                   ")
    print("===================================================================")
    
    if not os.path.exists(PROSPECTIVE_DIR):
        print("Directorio prospectivo no encontrado.")
        return
        
    files = glob.glob(os.path.join(PROSPECTIVE_DIR, "WIN-*.json"))
    
    status_counts = {'PENDING': 0, 'SETTLED': 0, 'INVALID': 0}
    leagues_seen = set()
    algo_versions = set()
    config_hashes = set()
    
    total_profit = 0.0
    profit_history = []
    
    league_stats = {}
    
    first_date = None
    alerts = []
    
    now_utc = datetime.datetime.now(datetime.UTC)
    
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
            
        # Alertas de Calidad
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
            
    # Calcular Max Drawdown y ROI general
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
        
    print(f"\n--- ESTADO DEL EXPERIMENTO ---")
    print(f"Evidence Age:          {evidence_age} días")
    print(f"Versiones Algoritmo:   {', '.join(algo_versions)}")
    print(f"Hashes Config:         {', '.join(config_hashes)}")
    print(f"Ligas Monitorizadas:   {len(leagues_seen)}")
    
    print(f"\n--- ESTADO OPERATIVO ---")
    print(f"Predicciones Pendientes: {status_counts['PENDING']}")
    print(f"Predicciones Liquidadas: {status_counts['SETTLED']}")
    print(f"Predicciones Inválidas:  {status_counts['INVALID']}")
    
    print(f"\n--- RENDIMIENTO ACUMULADO ---")
    print(f"Apuestas Totales:      {total_bets}")
    print(f"Beneficio (Bankroll):  {total_profit:+.2f} uds")
    print(f"Yield (ROI):           {yield_pct:+.2f}%")
    print(f"Máximo Drawdown:       {max_dd:.2f} uds")
    
    print(f"\n--- DISTRIBUCIÓN POR LIGA ---")
    for l, stats in league_stats.items():
        if stats['bets'] > 0:
            l_yield = (stats['profit'] / stats['bets']) * 100
            print(f"{l:<15}: {stats['bets']} apuestas | {stats['profit']:+.2f} uds | Yield: {l_yield:+.2f}%")
            
    print(f"\n--- CALIDAD DEL EXPERIMENTO ---")
    if not alerts:
        integrity_status = "ESTADO SALUDABLE: No hay anomalías estructurales."
        print(integrity_status)
    else:
        integrity_status = "ALERTAS ACTIVAS"
        for alert in alerts:
            print(alert)
            
    # Última observación
    last_run_path = os.path.join(PROSPECTIVE_DIR, "last_run.json")
    last_run = {}
    if os.path.exists(last_run_path):
        with open(last_run_path, "r") as f:
            last_run = json.load(f)
        print(f"\n--- ÚLTIMA OBSERVACIÓN ---")
        print(f"Fecha UTC:              {last_run.get('timestamp_utc')}")
        print(f"Fuente:                 {last_run.get('source')}")
        print(f"Ligas inspeccionadas:   {last_run.get('leagues_inspected')}")
        print(f"Partidos encontrados:   {last_run.get('matches_found')}")
        print(f"Estado:                 {last_run.get('status')}")
            
    log_event("DASHBOARD_RUN", "SUCCESS")
    print("\n===================================================================")
    
    # Exportar estado oficial como JSON
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
            "message": integrity_status,
            "alerts": alerts
        }
    }
    
    os.makedirs("docs", exist_ok=True)
    with open("docs/dashboard_state.json", "w") as f:
        json.dump(dashboard_state, f, indent=4)

if __name__ == "__main__":
    build_dashboard()
