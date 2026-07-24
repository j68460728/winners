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
    
    # Calculate some summary values
    partidos_hoy_count = len(obs_dia.get("partidos_hoy", []))
    partidos_prox_count = len(prox)
    winners_actividad = "Sí" if op.get("predicciones_pendientes", 0) > 0 or op.get("predicciones_liquidadas", 0) > 0 else "No"
    
    estado_proveedor = "Operativo" if fuente.get("estado_main") == "OK" and fuente.get("estado_extra") == "OK" else "Error"
    prov_icon = "🟢" if estado_proveedor == "Operativo" else "🔴"
    
    integ_status = integ.get("status")
    if integ_status == "PASS":
        wf_icon = "🟢"
        wf_text = "Saludable"
    else:
        wf_icon = "🔴"
        wf_text = "Alertas Activas"
        
    timestamp = state.get("timestamp_utc", "")
    try:
        dt = datetime.fromisoformat(timestamp)
        timestamp_formatted = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except:
        timestamp_formatted = timestamp
        
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Winners - Observatorio de Datos</title>
    <style>
        :root {{
            --bg-color: #f0f2f5;
            --card-bg: #ffffff;
            --text-main: #1d1d1f;
            --text-muted: #86868b;
            --primary-blue: #0066cc;
            --success-green: #34c759;
            --warning-yellow: #ffcc00;
            --danger-red: #ff3b30;
            --border-color: #e5e5ea;
            --shadow: 0 4px 12px rgba(0,0,0,0.05);
            --border-radius: 12px;
            --font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        
        body {{
            font-family: var(--font-family);
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
            line-height: 1.5;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 20px 0;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin: 0 0 10px 0;
            color: var(--text-main);
            letter-spacing: -0.5px;
        }}
        
        .header h2 {{
            font-size: 1.5rem;
            margin: 0 0 15px 0;
            color: var(--primary-blue);
            font-weight: 500;
        }}
        
        .header p {{
            color: var(--text-muted);
            font-size: 0.95rem;
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .card {{
            background: var(--card-bg);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid var(--border-color);
        }}
        
        .card-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin: 0 0 20px 0;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        
        .metric {{
            display: flex;
            flex-direction: column;
        }}
        
        .metric-label {{
            font-size: 0.85rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        
        .metric-value {{
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        
        th {{
            background-color: #f9f9f9;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
        }}
        
        tr:nth-child(even) {{
            background-color: #fafafa;
        }}
        
        tr:hover {{
            background-color: #f1f1f1;
        }}
        
        .status-badge {{
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            gap: 6px;
        }}
        
        .badge-success {{ background-color: #e3f8e9; color: #1e7e34; }}
        .badge-warning {{ background-color: #fff8e1; color: #f57f17; }}
        .badge-error {{ background-color: #fceceb; color: #d32f2f; }}
        .badge-info {{ background-color: #e3f2fd; color: #1976d2; }}
        
        .footer {{
            text-align: center;
            padding: 30px 0;
            color: var(--text-muted);
            font-size: 0.85rem;
            border-top: 1px solid var(--border-color);
            margin-top: 40px;
        }}
        
        .empty-state {{
            padding: 30px;
            text-align: center;
            color: var(--text-muted);
            font-style: italic;
            background-color: #f9f9f9;
            border-radius: 8px;
        }}
        
        @media (max-width: 768px) {{
            .summary-grid {{
                grid-template-columns: 1fr;
            }}
            .card {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <header class="header">
            <h1>Winners v1.0.0</h1>
            <h2>Observatorio de Datos Prospectivo</h2>
            <p>Información operacional en tiempo real. La evidencia predictiva permanece completamente aislada de esta vista.</p>
        </header>

        <!-- RESUMEN EJECUTIVO -->
        <div class="card">
            <h3 class="card-title">📊 Resumen Ejecutivo</h3>
            <div class="summary-grid">
                <div class="metric">
                    <span class="metric-label">Estado del Proveedor</span>
                    <span class="metric-value">{prov_icon} {estado_proveedor}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Última Actualización</span>
                    <span class="metric-value">📅 {timestamp_formatted}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Partidos de Hoy</span>
                    <span class="metric-value">⚽ {partidos_hoy_count}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Próximas 48 Horas</span>
                    <span class="metric-value">⚽ {partidos_prox_count}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Actividad Winners</span>
                    <span class="metric-value">🔵 {winners_actividad}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Estado del Workflow</span>
                    <span class="metric-value">{wf_icon} {wf_text}</span>
                </div>
            </div>
        </div>

        <!-- ESTADO DEL EXPERIMENTO -->
        <div class="card">
            <h3 class="card-title">🤖 Estado del Experimento</h3>
            <div class="summary-grid">
                <div class="metric">
                    <span class="metric-label">Salud del Sistema</span>
                    <span class="metric-value">
                        <span class="status-badge {'badge-success' if integ_status == 'PASS' else 'badge-error'}">
                            {wf_icon} {integ.get('message')}
                        </span>
                    </span>
                </div>
                <div class="metric">
                    <span class="metric-label">Edad de la Evidencia</span>
                    <span class="metric-value">📅 {exp.get('evidence_age_days')} días</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Apuestas Liquidadas</span>
                    <span class="metric-value">🏆 {op.get('predicciones_liquidadas')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Apuestas Pendientes</span>
                    <span class="metric-value">⚪ {op.get('predicciones_pendientes')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Yield (ROI)</span>
                    <span class="metric-value">🔵 {fin.get('yield_pct'):.2f}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Beneficio Total</span>
                    <span class="metric-value">🔵 {fin.get('beneficio_uds'):.2f} uds</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Máximo Drawdown</span>
                    <span class="metric-value">⚪ {fin.get('max_drawdown_uds'):.2f} uds</span>
                </div>
            </div>
        </div>

        <!-- ESTADO DE LA FUENTE -->
        <div class="card">
            <h3 class="card-title">📡 Estado de la Fuente de Datos</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 20px;">
                📅 <strong>Última consulta al proveedor:</strong> {fuente.get("ultima_consulta_utc")}
            </p>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Archivo Descargado</th>
                            <th>Estado</th>
                            <th>Registros Totales</th>
                            <th>Última Fecha Encontrada</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>fixtures.csv</td>
                            <td><span class="status-badge {'badge-success' if fuente.get('estado_main') == 'OK' else 'badge-error'}">{'🟢' if fuente.get('estado_main') == 'OK' else '🔴'} {fuente.get('estado_main')}</span></td>
                            <td>{fuente.get('registros_main')}</td>
                            <td>{fuente.get('ultima_fecha_main')}</td>
                        </tr>
                        <tr>
                            <td>new_league_fixtures.csv</td>
                            <td><span class="status-badge {'badge-success' if fuente.get('estado_extra') == 'OK' else 'badge-error'}">{'🟢' if fuente.get('estado_extra') == 'OK' else '🔴'} {fuente.get('estado_extra')}</span></td>
                            <td>{fuente.get('registros_extra')}</td>
                            <td>{fuente.get('ultima_fecha_extra')}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <p style="margin-top: 15px; font-weight: 500;">
                🏆 Total Competiciones Detectadas: {fuente.get("total_competiciones")}
            </p>
        </div>

        <!-- LIGAS ACTIVAS -->
        <div class="card">
            <h3 class="card-title">🏆 Ligas Activas</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 20px;">
                Competiciones detectadas en el servidor, ordenadas por volumen de partidos programados.
            </p>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Competición</th>
                            <th>Total Partidos Extraídos</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    for liga in obs_dia.get("ligas_activas", []):
        html += f"""
                        <tr>
                            <td>{liga.get("competicion")}</td>
                            <td>{liga.get("partidos")}</td>
                        </tr>"""
                        
    html += f"""
                    </tbody>
                </table>
            </div>
        </div>

        <!-- PARTIDOS DEL DÍA -->
        <div class="card">
            <h3 class="card-title">⚽ Partidos del Día (Hoy)</h3>
"""
    hoy = obs_dia.get("partidos_hoy", [])
    if not hoy:
        html += '<div class="empty-state">No se encontraron partidos programados para el día de hoy en la fuente de datos.</div>'
    else:
        html += """
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Competición</th>
                            <th>Hora</th>
                            <th>Local</th>
                            <th>Visitante</th>
                        </tr>
                    </thead>
                    <tbody>"""
        for p in hoy:
            html += f"""
                        <tr>
                            <td><span class="status-badge badge-info">{p.get("competicion")}</span></td>
                            <td>{p.get("hora")}</td>
                            <td><strong>{p.get("local")}</strong></td>
                            <td><strong>{p.get("visitante")}</strong></td>
                        </tr>"""
        html += """
                    </tbody>
                </table>
            </div>"""
            
    html += f"""
        </div>

        <!-- PRÓXIMAS 48 HORAS -->
        <div class="card">
            <h3 class="card-title">📅 Próximos Partidos (48 horas)</h3>
"""
    if not prox:
        html += '<div class="empty-state">No hay partidos programados en las próximas 48 horas.</div>'
    else:
        html += """
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Fecha</th>
                            <th>Competición</th>
                            <th>Hora</th>
                            <th>Local</th>
                            <th>Visitante</th>
                        </tr>
                    </thead>
                    <tbody>"""
        for p in prox:
            html += f"""
                        <tr>
                            <td>{p.get("fecha")}</td>
                            <td><span class="status-badge badge-info">{p.get("competicion")}</span></td>
                            <td>{p.get("hora")}</td>
                            <td><strong>{p.get("local")}</strong></td>
                            <td><strong>{p.get("visitante")}</strong></td>
                        </tr>"""
        html += """
                    </tbody>
                </table>
            </div>"""
            
    html += """
        </div>

        <!-- FOOTER -->
        <footer class="footer">
            <p><strong>Sistema:</strong> Winners v1.0.0 | <strong>Proveedor:</strong> football-data.co.uk</p>
            <p>Generado el 📅 """ + timestamp_formatted + """</p>
            <p style="margin-top: 10px; opacity: 0.7;">Repositorio GitHub - Observatorio Estático</p>
        </footer>
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
