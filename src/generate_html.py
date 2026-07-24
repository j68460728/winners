import json
import os
from datetime import datetime

def generate_html():
    state_path = "docs/dashboard_state.json"
    if not os.path.exists(state_path):
        print("Error: No se encontró dashboard_state.json")
        return
        
    with open(state_path, "r") as f:
        state = json.load(f)
        
    exp = state.get("estado_experimento", {})
    op = state.get("estado_operativo", {})
    fin = state.get("estado_financiero", {})
    integ = state.get("integridad", {})
    obs = state.get("observatorio", {})
    
    fuente = obs.get("estado_fuente", {})
    obs_dia = obs.get("observacion_dia", {})
    prox = obs.get("proximos_partidos", [])
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Winners - Observatorio de Datos</title>
    <style>
        body {{
            font-family: 'Courier New', Courier, monospace;
            background-color: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: auto;
            background: #fff;
            padding: 20px;
            border-top: 5px solid #2c3e50;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        .section {{
            margin-bottom: 30px;
            padding: 15px;
            border: 1px solid #ddd;
            background: #fafafa;
        }}
        .section-title {{
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 5px;
            margin-top: 0;
        }}
        .metric-box {{
            display: inline-block;
            width: 30%;
            margin-bottom: 15px;
            vertical-align: top;
        }}
        .metric-value {{
            font-size: 1.5em;
            font-weight: bold;
        }}
        .pass {{ color: green; font-weight: bold; }}
        .fail {{ color: red; font-weight: bold; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background: #eaeaea;
        }}
        .timestamp {{
            font-size: 0.8em;
            color: #666;
            text-align: right;
            margin-top: -30px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Winners v1.0.0</h1>
        <div class="timestamp">Última actualización: {state.get("timestamp_utc")}</div>
        
        <!-- SECCIÓN 1: ESTADO DEL EXPERIMENTO -->
        <div class="section">
            <h2 class="section-title">1. Estado del Experimento</h2>
            <p><strong>Salud:</strong> <span class="{'pass' if integ.get('status') == 'PASS' else 'fail'}">{integ.get('message')}</span></p>
            
            <div class="metric-box">
                <div>Evidence Age</div>
                <div class="metric-value">{exp.get("evidence_age_days")} días</div>
            </div>
            <div class="metric-box">
                <div>Apuestas Liquidadas</div>
                <div class="metric-value">{op.get("predicciones_liquidadas")}</div>
            </div>
            <div class="metric-box">
                <div>Pendientes</div>
                <div class="metric-value">{op.get("predicciones_pendientes")}</div>
            </div>
            
            <div class="metric-box">
                <div>Yield (ROI)</div>
                <div class="metric-value">{fin.get("yield_pct"):.2f}%</div>
            </div>
            <div class="metric-box">
                <div>Beneficio</div>
                <div class="metric-value">{fin.get("beneficio_uds"):.2f} uds</div>
            </div>
            <div class="metric-box">
                <div>Max Drawdown</div>
                <div class="metric-value">{fin.get("max_drawdown_uds"):.2f} uds</div>
            </div>
        </div>
        
        <!-- SECCIÓN 2: ESTADO DE LA FUENTE -->
        <div class="section">
            <h2 class="section-title">2. Estado de la Fuente de Datos</h2>
            <p><strong>Última consulta UTC:</strong> {fuente.get("ultima_consulta_utc")}</p>
            <table>
                <tr>
                    <th>Archivo Descargado</th>
                    <th>Estado</th>
                    <th>Registros Totales</th>
                    <th>Última Fecha Encontrada</th>
                </tr>
                <tr>
                    <td>fixtures.csv</td>
                    <td>{fuente.get("estado_main")}</td>
                    <td>{fuente.get("registros_main")}</td>
                    <td>{fuente.get("ultima_fecha_main")}</td>
                </tr>
                <tr>
                    <td>new_league_fixtures.csv</td>
                    <td>{fuente.get("estado_extra")}</td>
                    <td>{fuente.get("registros_extra")}</td>
                    <td>{fuente.get("ultima_fecha_extra")}</td>
                </tr>
            </table>
            <p><strong>Total Competiciones Detectadas:</strong> {fuente.get("total_competiciones")}</p>
        </div>
        
        <!-- SECCIÓN 3: OBSERVACIÓN DEL DÍA -->
        <div class="section">
            <h2 class="section-title">3. Observación del Día (Ligas Activas)</h2>
            <p>Ligas detectadas en el servidor, ordenadas por volumen de partidos:</p>
            <table>
                <tr>
                    <th>Competición</th>
                    <th>Total Partidos Extraídos</th>
                </tr>
"""
    for liga in obs_dia.get("ligas_activas", []):
        html += f"""
                <tr>
                    <td>{liga.get("competicion")}</td>
                    <td>{liga.get("partidos")}</td>
                </tr>"""
                
    html += f"""
            </table>
            
            <h3>Partidos del Día (HOY)</h3>
"""
    hoy = obs_dia.get("partidos_hoy", [])
    if not hoy:
        html += "<p>No se encontraron partidos programados para el día de hoy en la fuente de datos.</p>"
    else:
        html += """
            <table>
                <tr>
                    <th>Competición</th>
                    <th>Hora</th>
                    <th>Local</th>
                    <th>Visitante</th>
                </tr>"""
        for p in hoy:
            html += f"""
                <tr>
                    <td>{p.get("competicion")}</td>
                    <td>{p.get("hora")}</td>
                    <td>{p.get("local")}</td>
                    <td>{p.get("visitante")}</td>
                </tr>"""
        html += "</table>"
        
    html += f"""
        </div>
        
        <!-- SECCIÓN 4: PRÓXIMOS PARTIDOS -->
        <div class="section">
            <h2 class="section-title">4. Próximos Partidos (48 horas)</h2>
"""
    if not prox:
        html += "<p>No hay partidos programados en las próximas 48 horas.</p>"
    else:
        html += """
            <table>
                <tr>
                    <th>Fecha</th>
                    <th>Competición</th>
                    <th>Hora</th>
                    <th>Local</th>
                    <th>Visitante</th>
                </tr>"""
        for p in prox:
            html += f"""
                <tr>
                    <td>{p.get("fecha")}</td>
                    <td>{p.get("competicion")}</td>
                    <td>{p.get("hora")}</td>
                    <td>{p.get("local")}</td>
                    <td>{p.get("visitante")}</td>
                </tr>"""
        html += "</table>"
        
    html += """
        </div>
    </div>
</body>
</html>
"""

    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("HTML generado exitosamente en docs/index.html")

if __name__ == "__main__":
    generate_html()
