import json
import os
from datetime import datetime

def generate_html():
    state_path = "docs/dashboard_state.json"
    if not os.path.exists(state_path):
        print("Error: No se encontró dashboard_state.json")
        return
        
    with open(state_path, "r") as f:
        data = json.load(f)
        
    exp = data.get("estado_experimento", {})
    op = data.get("estado_operativo", {})
    fin = data.get("estado_financiero", {})
    integ = data.get("integridad", {})
    last = op.get("ultima_observacion", {})
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Winners - Dashboard Operativo</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #121212;
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        h1, h2 {{
            color: #ffffff;
            border-bottom: 1px solid #333;
            padding-bottom: 5px;
        }}
        .block {{
            background: #1e1e1e;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #4CAF50;
        }}
        .block.fin {{ border-left-color: #2196F3; }}
        .block.op {{ border-left-color: #FFC107; }}
        .block.alert {{ border-left-color: #F44336; }}
        
        .stat-row {{
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid #333;
            padding: 8px 0;
        }}
        .stat-row:last-child {{ border-bottom: none; }}
        .label {{ font-weight: bold; color: #aaaaaa; }}
        .value {{ font-family: monospace; font-size: 1.1em; color: #ffffff; }}
        .update-time {{
            text-align: center;
            font-size: 0.9em;
            color: #888;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Winners v1.0.0</h1>
        
        <!-- ESTADO DEL EXPERIMENTO -->
        <div class="block">
            <h2>1. Estado del Experimento</h2>
            <div class="stat-row">
                <span class="label">Evidence Age:</span>
                <span class="value">{exp.get('evidence_age_days', 0)} días</span>
            </div>
            <div class="stat-row">
                <span class="label">Versiones de Algoritmo:</span>
                <span class="value">{', '.join(exp.get('versiones_algoritmo', []))}</span>
            </div>
            <div class="stat-row">
                <span class="label">Ligas Monitorizadas:</span>
                <span class="value">{exp.get('ligas_monitorizadas', 0)}</span>
            </div>
            <div class="stat-row">
                <span class="label">Integridad Estructural:</span>
                <span class="value">{integ.get('message', 'UNKNOWN')}</span>
            </div>
        </div>

        <!-- ESTADO OPERATIVO -->
        <div class="block op">
            <h2>2. Estado Operativo</h2>
            <div class="stat-row">
                <span class="label">Expedientes PENDING:</span>
                <span class="value">{op.get('predicciones_pendientes', 0)}</span>
            </div>
            <div class="stat-row">
                <span class="label">Expedientes SETTLED:</span>
                <span class="value">{op.get('predicciones_liquidadas', 0)}</span>
            </div>
            <div class="stat-row">
                <span class="label">Expedientes INVALID:</span>
                <span class="value">{op.get('predicciones_invalidas', 0)}</span>
            </div>
            <br>
            <div class="stat-row">
                <span class="label">Última Observación (Fecha):</span>
                <span class="value">{last.get('timestamp_utc', 'N/A')}</span>
            </div>
            <div class="stat-row">
                <span class="label">Última Observación (Estado):</span>
                <span class="value">{last.get('status', 'N/A')}</span>
            </div>
        </div>

        <!-- ESTADO FINANCIERO -->
        <div class="block fin">
            <h2>3. Estado Financiero</h2>
            <div class="stat-row">
                <span class="label">Apuestas Totales:</span>
                <span class="value">{fin.get('apuestas_totales', 0)}</span>
            </div>
            <div class="stat-row">
                <span class="label">Bankroll (Beneficio):</span>
                <span class="value">{fin.get('beneficio_uds', 0):+.2f} uds</span>
            </div>
            <div class="stat-row">
                <span class="label">Yield (ROI):</span>
                <span class="value">{fin.get('yield_pct', 0):+.2f}%</span>
            </div>
            <div class="stat-row">
                <span class="label">Max Drawdown:</span>
                <span class="value">{fin.get('max_drawdown_uds', 0):.2f} uds</span>
            </div>
        </div>
        
        <div class="update-time">
            Página generada estáticamente el: {data.get('timestamp_utc')}
        </div>
    </div>
</body>
</html>
"""
    
    with open("docs/index.html", "w") as f:
        f.write(html)
    print("Dashboard HTML generado exitosamente en docs/index.html")

if __name__ == "__main__":
    generate_html()
