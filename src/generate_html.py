import json
import os
import datetime
import shutil
import difflib

LEAGUE_STYLES = {
    "E0": {"name": "Premier League", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "color": "#e90052", "country": "Inglaterra"},
    "E1": {"name": "Championship", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "color": "#00f0ff", "country": "Inglaterra"},
    "E2": {"name": "League One", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "color": "#00f0ff", "country": "Inglaterra"},
    "E3": {"name": "League Two", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "color": "#00f0ff", "country": "Inglaterra"},
    "EC": {"name": "National League", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "color": "#00f0ff", "country": "Inglaterra"},
    "SP1": {"name": "La Liga", "flag": "🇪🇸", "color": "#ff4b44", "country": "España"},
    "SP2": {"name": "Segunda División", "flag": "🇪🇸", "color": "#ff4b44", "country": "España"},
    "D1": {"name": "Bundesliga", "flag": "🇩🇪", "color": "#d20515", "country": "Alemania"},
    "D2": {"name": "2. Bundesliga", "flag": "🇩🇪", "color": "#d20515", "country": "Alemania"},
    "I1": {"name": "Serie A", "flag": "🇮🇹", "color": "#008fd7", "country": "Italia"},
    "I2": {"name": "Serie B", "flag": "🇮🇹", "color": "#008fd7", "country": "Italia"},
    "F1": {"name": "Ligue 1", "flag": "🇫🇷", "color": "#da251d", "country": "Francia"},
    "F2": {"name": "Ligue 2", "flag": "🇫🇷", "color": "#da251d", "country": "Francia"},
    "B1": {"name": "Pro League", "flag": "🇧🇪", "color": "#e20613", "country": "Bélgica"},
    "P1": {"name": "Primeira Liga", "flag": "🇵🇹", "color": "#00902c", "country": "Portugal"},
    "N1": {"name": "Eredivisie", "flag": "🇳🇱", "color": "#ff4f00", "country": "Países Bajos"},
    "T1": {"name": "Süper Lig", "flag": "🇹🇷", "color": "#e30a17", "country": "Turquía"},
    "G1": {"name": "Super League", "flag": "🇬🇷", "color": "#0d5eaf", "country": "Grecia"},
    "SC0": {"name": "Premiership", "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "color": "#005eb8", "country": "Escocia"},
    "SC1": {"name": "Championship", "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "color": "#005eb8", "country": "Escocia"},
    "Argentina - Liga Profesional": {"name": "Liga Profesional", "flag": "🇦🇷", "color": "#75aadb", "country": "Argentina"},
    "Brazil - Serie A": {"name": "Serie A", "flag": "🇧🇷", "color": "#009c3b", "country": "Brasil"},
    "Brazil - Serie B": {"name": "Serie B", "flag": "🇧🇷", "color": "#009c3b", "country": "Brasil"},
    "Switzerland - Super League": {"name": "Super League", "flag": "🇨🇭", "color": "#ff0000", "country": "Suiza"},
    "China - Super League": {"name": "Super League", "flag": "🇨🇳", "color": "#ff0000", "country": "China"},
    "Denmark - Superliga": {"name": "Superliga", "flag": "🇩🇰", "color": "#c60c30", "country": "Dinamarca"},
    "Finland - Veikkausliiga": {"name": "Veikkausliiga", "flag": "🇫🇮", "color": "#002f6c", "country": "Finlandia"},
    "Ireland - Premier Division": {"name": "Premier Division", "flag": "🇮🇪", "color": "#169b62", "country": "Irlanda"},
    "Mexico - Liga MX": {"name": "Liga MX", "flag": "🇲🇽", "color": "#006847", "country": "México"},
    "Norway - Eliteserien": {"name": "Eliteserien", "flag": "🇳🇴", "color": "#ef2b2d", "country": "Noruega"},
    "Poland - Ekstraklasa": {"name": "Ekstraklasa", "flag": "🇵🇱", "color": "#dc143c", "country": "Polonia"},
    "Romania - Superliga": {"name": "Superliga", "flag": "🇷🇴", "color": "#fce100", "country": "Rumania"},
    "Sweden - Allsvenskan": {"name": "Allsvenskan", "flag": "🇸🇪", "color": "#006aa7", "country": "Suecia"},
    "USA - MLS": {"name": "MLS", "flag": "🇺🇸", "color": "#001f5b", "country": "Estados Unidos"},
    "Japan - J-League": {"name": "J-League", "flag": "🇯🇵", "color": "#bc002d", "country": "Japón"},
    "Unknown": {"name": "Desconocida", "flag": "🌍", "color": "#8b949e", "country": "Mundial"}
}

def get_league_style(league_code):
    return LEAGUE_STYLES.get(league_code, {"name": league_code, "flag": "🌍", "color": "#388bfd", "country": "Mundial"})

def get_safe_filename(name):
    return name.replace("/", "_").replace("\\", "_")

def sync_logos(active_teams):
    """
    Sincroniza los escudos de los equipos desde FootballAssets hacia docs/assets/clubs/
    utilizando team_mapping.json y fuzzy matching.
    """
    assets_dir = "FootballAssets/football-logos/logos/clubs"
    dest_dir = "docs/assets/clubs"
    mapping_file = "docs/team_mapping.json"
    
    os.makedirs(dest_dir, exist_ok=True)
    
    # Cargar aliases
    aliases = {}
    alias_path = "docs/team_aliases.json"
    if os.path.exists(alias_path):
        with open(alias_path, "r", encoding="utf-8") as f:
            try:
                aliases = json.load(f)
            except:
                pass

    # Cargar mapeo existente
    mapping = {}
    if os.path.exists(mapping_file):
        try:
            with open(mapping_file, "r", encoding="utf-8") as f:
                mapping = json.load(f)
        except:
            pass
            
    # Indexar todos los logos disponibles en FootballAssets
    available_logos = {} # name -> path
    if os.path.exists(assets_dir):
        for root, dirs, files in os.walk(assets_dir):
            for file in files:
                if file.endswith((".png", ".svg")):
                    name = os.path.splitext(file)[0]
                    available_logos[name] = os.path.join(root, file)
                    
    logo_names = list(available_logos.keys())
    mapping_updated = False
    
    for original_team in active_teams:
        team = aliases.get(original_team, original_team)
        
        if team in mapping and mapping[team] != "":
            # Ya está mapeado, asegurarse que exista en dest_dir
            source_path = mapping[team]
            safe_team = get_safe_filename(team)
            dest_path = os.path.join(dest_dir, f"{safe_team}.png") # always save as safe_team.png
            
            should_copy = False
            if not os.path.exists(dest_path):
                should_copy = True
            elif os.path.exists(source_path):
                # Check if file size differs to override cached images
                if os.path.getsize(dest_path) != os.path.getsize(source_path):
                    should_copy = True
                    
            if should_copy and os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
            continue
            
        if not logo_names:
            continue
            
        # Intentar coincidencia exacta
        if team in available_logos:
            mapping[team] = available_logos[team]
            mapping_updated = True
            safe_team = get_safe_filename(team)
            dest_path = os.path.join(dest_dir, f"{safe_team}.png")
            shutil.copy2(available_logos[team], dest_path)
            continue
            
        # Intentar coincidencia parcial (fuzzy) case-insensitive
        team_lower = team.lower()
        logo_names_lower = [n.lower() for n in logo_names]
        matches = difflib.get_close_matches(team_lower, logo_names_lower, n=1, cutoff=0.6)
        
        if matches:
            best_match_lower = matches[0]
            best_match = next(n for n in logo_names if n.lower() == best_match_lower)
            mapping[team] = available_logos[best_match]
            mapping_updated = True
            safe_team = get_safe_filename(team)
            dest_path = os.path.join(dest_dir, f"{safe_team}.png")
            shutil.copy2(available_logos[best_match], dest_path)
        else:
            # Marcarlo como vacío para no buscarlo una y otra vez (o que el usuario lo llene manual)
            mapping[team] = ""
            mapping_updated = True
            
    if mapping_updated:
        with open(mapping_file, "w", encoding="utf-8") as f:
            json.dump(mapping, f, indent=4, ensure_ascii=False)

def get_team_html(team_name):
    # Asume que si el escudo existe en docs/assets/clubs/team_name.png, se muestra
    import json
    alias_path = "docs/team_aliases.json"
    if os.path.exists(alias_path):
        try:
            with open(alias_path, "r", encoding="utf-8") as f:
                aliases = json.load(f)
                team_name = aliases.get(team_name, team_name)
        except:
            pass

    safe_team = get_safe_filename(team_name)
    logo_path = f"assets/clubs/{safe_team}.png"
    if os.path.exists(f"docs/{logo_path}"):
        return f'<img src="{logo_path}" alt="{team_name}" width="20" height="20" style="vertical-align: middle; margin-right: 8px;"><strong>{team_name}</strong>'
    return f'<strong>{team_name}</strong>'

def generate_html():
    state_path = "docs/dashboard_state.json"
    if not os.path.exists(state_path):
        print("Error: No se encontró dashboard_state.json")
        return
        
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)
        
    exp = state.get("estado_experimento", {})
    op = state.get("estado_operativo", {})
    fin = state.get("estado_financiero", {})
    integ = state.get("integridad", {})
    obs = state.get("observatorio", {})
    
    fuente = obs.get("estado_fuente", {})
    obs_dia = obs.get("observacion_dia", {})
    prox = obs.get("proximos_partidos", [])
    
    # 1. Obtener equipos activos y sincronizar logos
    hoy = obs_dia.get("partidos_hoy", [])
    active_teams = set()
    for p in hoy:
        active_teams.add(p.get("local"))
        active_teams.add(p.get("visitante"))
    for p in prox:
        active_teams.add(p.get("local"))
        active_teams.add(p.get("visitante"))
        
    sync_logos(active_teams)
    
    # Calculate some summary values
    partidos_hoy_count = len(hoy)
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
        dt = datetime.datetime.fromisoformat(timestamp)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        colombia_tz = datetime.timezone(datetime.timedelta(hours=-5))
        dt_local = dt.astimezone(colombia_tz)
        timestamp_formatted = dt_local.strftime("%Y-%m-%d %H:%M:%S (Hora)")
    except Exception as e:
        timestamp_formatted = timestamp
        
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Winners - Observatorio de Datos</title>
    <style>
        :root {{
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --text-main: #c9d1d9;
            --text-muted: #8b949e;
            --primary-blue: #58a6ff;
            --success-green: #3fb950;
            --warning-yellow: #d29922;
            --danger-red: #f85149;
            --border-color: #30363d;
            --shadow: 0 4px 12px rgba(0,0,0,0.5);
            --border-radius: 12px;
            --font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            --table-header-bg: #21262d;
            --table-row-even: #0d1117;
            --table-row-hover: #1f242c;
            --empty-state-bg: #1c2128;
            --badge-success-bg: rgba(46, 160, 67, 0.15);
            --badge-success-text: #3fb950;
            --badge-warning-bg: rgba(210, 153, 34, 0.15);
            --badge-warning-text: #d29922;
            --badge-error-bg: rgba(248, 81, 73, 0.15);
            --badge-error-text: #f85149;
            --badge-info-bg: rgba(56, 139, 253, 0.15);
            --badge-info-text: #58a6ff;
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
            color: var(--text-main);
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
            background-color: var(--table-header-bg);
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
        }}
        
        tr:nth-child(even) {{
            background-color: var(--table-row-even);
        }}
        
        tr:hover {{
            background-color: var(--table-row-hover);
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
        
        .league-badge {{
            display: inline-flex;
            align-items: center;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            gap: 10px;
            background-color: transparent;
        }}
        
        .league-name {{
            font-weight: 600;
            color: var(--text-main);
        }}
        
        .league-flag {{
            font-size: 1.2rem;
        }}
        
        .badge-success {{ background-color: var(--badge-success-bg); color: var(--badge-success-text); }}
        .badge-warning {{ background-color: var(--badge-warning-bg); color: var(--badge-warning-text); }}
        .badge-error {{ background-color: var(--badge-error-bg); color: var(--badge-error-text); }}
        .badge-info {{ background-color: var(--badge-info-bg); color: var(--badge-info-text); }}
        
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
            background-color: var(--empty-state-bg);
            border-radius: 8px;
            border: 1px solid var(--border-color);
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
                    <span class="metric-value">📅 <span style="font-size: 1.1rem; color: var(--primary-blue);">{timestamp_formatted}</span></span>
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
                📅 <strong>Última consulta al proveedor:</strong> {timestamp_formatted}
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
                            <th>País</th>
                            <th>Total Partidos Extraídos</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    for liga in obs_dia.get("ligas_activas", []):
        l_code = liga.get("competicion")
        l_style = get_league_style(l_code)
        html += f"""
                        <tr>
                            <td>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <img src="assets/leagues/{get_safe_filename(l_code)}.png" alt=" " onerror="this.onerror=null; this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🏆</text></svg>';" style="height: 20px; width: auto;">
                                    <span style="font-weight: 500;">{l_style['name']}</span>
                                </div>
                            </td>
                            <td>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span>{l_style['flag']}</span>
                                    <span style="color: var(--text-color);">{l_style['country']}</span>
                                </div>
                            </td>
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
    if not hoy:
        html += '<div class="empty-state">No se encontraron partidos programados para el día de hoy en la fuente de datos.</div>'
    else:
        html += """
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Competición</th>
                            <th>País</th>
                            <th>Hora</th>
                            <th>Local</th>
                            <th>Visitante</th>
                        </tr>
                    </thead>
                    <tbody>"""
        for p in hoy:
            l_style = get_league_style(p.get("competicion"))
            local_html = get_team_html(p.get("local"))
            visit_html = get_team_html(p.get("visitante"))
            html += f"""
                        <tr>
                            <td>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <img src="assets/leagues/{get_safe_filename(p.get('competicion'))}.png" alt=" " onerror="this.onerror=null; this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🏆</text></svg>';" style="height: 20px; width: auto;">
                                    <span style="font-weight: 500;">{l_style['name']}</span>
                                </div>
                            </td>
                            <td>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span>{l_style['flag']}</span>
                                    <span style="color: var(--text-color); font-size: 0.9rem;">{l_style['country']}</span>
                                </div>
                            </td>
                            <td><span style="color: var(--primary-blue); font-weight: 600;">{p.get("hora_local", "N/A")}</span></td>
                            <td>{local_html}</td>
                            <td>{visit_html}</td>
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
                            <th>País</th>
                            <th>Hora</th>
                            <th>Local</th>
                            <th>Visitante</th>
                        </tr>
                    </thead>
                    <tbody>"""
        for p in prox:
            l_style = get_league_style(p.get("competicion"))
            local_html = get_team_html(p.get("local"))
            visit_html = get_team_html(p.get("visitante"))
            html += f"""
                        <tr>
                            <td>{p.get("fecha")}</td>
                            <td>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <img src="assets/leagues/{get_safe_filename(p.get('competicion'))}.png" alt=" " onerror="this.onerror=null; this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🏆</text></svg>';" style="height: 20px; width: auto;">
                                    <span style="font-weight: 500;">{l_style['name']}</span>
                                </div>
                            </td>
                            <td>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span>{l_style['flag']}</span>
                                    <span style="color: var(--text-color); font-size: 0.9rem;">{l_style['country']}</span>
                                </div>
                            </td>
                            <td><span style="color: var(--primary-blue); font-weight: 600;">{p.get("hora_local", "N/A")}</span></td>
                            <td>{local_html}</td>
                            <td>{visit_html}</td>
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
