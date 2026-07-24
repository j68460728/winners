import json
import os
import glob
import pandas as pd

PROSPECTIVE_DIR = "data/prospective"
JOURNAL_PATH = "data/prospective/journal.md"

def build_journal():
    print("Reconstruyendo Diario Acumulativo...")
    
    if not os.path.exists(PROSPECTIVE_DIR):
        print("No hay directorio prospectivo.")
        return
        
    all_files = glob.glob(os.path.join(PROSPECTIVE_DIR, "WIN-*.json"))
    
    records = []
    
    for filepath in all_files:
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        if data.get('status') == 'INVALID':
            continue
            
        rec = {
            'ID': data['prediction_id'],
            'Fecha_Generacion': data['metadata']['timestamp_utc'],
            'Partido': f"{data['match']['home_team']} vs {data['match']['away_team']}",
            'Liga': data['match']['league'],
            'Pick': data['prediction']['winners_pick'],
            'Cuota': data['prediction']['winners_odds'],
            'Estado': data['status']
        }
        
        if data['status'] == 'SETTLED':
            rec['Resultado'] = data['settlement']['result']
            rec['Beneficio'] = data['settlement']['profit']
        else:
            rec['Resultado'] = 'N/A'
            rec['Beneficio'] = 0.0
            
        records.append(rec)
        
    if not records:
        print("No hay registros válidos para el diario.")
        return
        
    df = pd.DataFrame(records)
    df['Fecha_Generacion'] = pd.to_datetime(df['Fecha_Generacion'])
    df = df.sort_values(by='Fecha_Generacion')
    
    # Calcular capital acumulativo
    df['Beneficio_Acumulado'] = df['Beneficio'].cumsum()
    
    # Calcular Max Drawdown
    cum_max = df['Beneficio_Acumulado'].cummax()
    df['Drawdown'] = cum_max - df['Beneficio_Acumulado']
    max_dd = df['Drawdown'].max()
    
    df_settled = df[df['Estado'] == 'SETTLED']
    total_bets = len(df_settled)
    total_profit = df['Beneficio_Acumulado'].iloc[-1]
    yield_pct = (total_profit / total_bets * 100) if total_bets > 0 else 0.0
    
    # Métricas de Evidence Age
    import datetime
    now_utc = datetime.datetime.now(datetime.UTC)
    first_prediction_date = df['Fecha_Generacion'].iloc[0]
    days_since_first = (now_utc - first_prediction_date).days
    monitored_leagues = df['Liga'].nunique()
    
    # Generar la vista del diario
    with open(JOURNAL_PATH, 'w') as f:
        f.write("# Diario Acumulativo de Laboratorio: Winners v1.0.0\n\n")
        f.write("> **IMPORTANTE:** Este documento es una reconstrucción 100% determinista. Los archivos JSON individuales son la única fuente de verdad.\n\n")
        
        f.write("## ⏳ Evidence Age (Madurez del Experimento)\n")
        f.write(f"- **Días de Recolección Prospectiva:** {days_since_first} días\n")
        f.write(f"- **Predicciones Liquidadas (Muestra N):** {total_bets}\n")
        f.write(f"- **Ligas Monitorizadas:** {monitored_leagues}\n\n")
        
        f.write("## 📊 Métricas Globales (Solo apuestas liquidadas)\n")
        f.write(f"- **Beneficio Neto (Bankroll):** {total_profit:+.2f} uds\n")
        f.write(f"- **Yield (ROI):** {yield_pct:+.2f}%\n")
        f.write(f"- **Máximo Drawdown:** {max_dd:.2f} uds\n\n")
        
        f.write("## Registro Histórico\n\n")
        f.write("| ID Predicción | Fecha Generación (UTC) | Liga | Partido | Pick | Cuota | Estado | Res | Beneficio | Bankroll | Drawdown |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
        
        for _, row in df.iterrows():
            f.write(f"| {row['ID']} | {row['Fecha_Generacion'].strftime('%Y-%m-%d %H:%M:%S')} | {row['Liga']} | {row['Partido']} | {row['Pick']} | {row['Cuota']:.2f} | {row['Estado']} | {row['Resultado']} | {row['Beneficio']:+0.2f} | {row['Beneficio_Acumulado']:+0.2f} | {row['Drawdown']:.2f} |\n")
            
    print(f"Diario reconstruido con éxito en: {JOURNAL_PATH}")

if __name__ == "__main__":
    build_journal()
