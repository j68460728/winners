import pandas as pd
import urllib.request
import io
import ssl
import sys
import itertools

ssl._create_default_https_context = ssl._create_unverified_context

def download_data_10_seasons():
    """Descarga 10 temporadas para evitar sesgos por ventana corta"""
    seasons = ['1415', '1516', '1617', '1718', '1819', '1920', '2021', '2122', '2223', '2324']
    leagues = {
        'Bundesliga': 'D1', 
        'Premier League': 'E0', 
        'La Liga': 'SP1', 
        'Serie A': 'I1'
    }
    
    all_data = []
    print("Descargando 10 temporadas (2014-2024)...")
    for league_name, league_code in leagues.items():
        for season in seasons:
            url = f"https://www.football-data.co.uk/mmz4281/{season}/{league_code}.csv"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                df = pd.read_csv(io.StringIO(response.read().decode('utf-8', errors='ignore')))
                df['League'] = league_name
                df['Season'] = season
                
                cols_to_keep = ['League', 'Season', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
                df = df[[c for c in cols_to_keep if c in df.columns]]
                all_data.append(df)
            except Exception as e:
                pass # Ignoramos silenciosamente si alguna no existe para mantener el script limpio
                
    return pd.concat(all_data, ignore_index=True)

def evaluate_parameters(df_league, window_size, top_pct, bottom_pct, upset_def):
    """
    Evalúa la tasa de sorpresas corrigiendo el data leakage:
    Utiliza 'window_size' temporadas para construir jerarquía, 
    y evalúa SOLO en la temporada siguiente.
    """
    seasons = sorted(df_league['Season'].unique())
    
    total_asymmetric_matches = 0
    total_upsets = 0
    
    # Deslizamos la ventana en el tiempo
    for i in range(window_size, len(seasons)):
        target_season = seasons[i]
        history_seasons = seasons[i-window_size:i]
        
        df_history = df_league[df_league['Season'].isin(history_seasons)]
        df_target = df_league[df_league['Season'] == target_season]
        
        # 1. Puntos históricos en la ventana (Sin ver el futuro)
        home_pts = df_history.groupby('HomeTeam')['FTR'].apply(lambda x: (x == 'H').sum() * 3 + (x == 'D').sum()).reset_index()
        home_pts.columns = ['Team', 'Pts']
        away_pts = df_history.groupby('AwayTeam')['FTR'].apply(lambda x: (x == 'A').sum() * 3 + (x == 'D').sum()).reset_index()
        away_pts.columns = ['Team', 'Pts']
        
        total_pts = pd.concat([home_pts, away_pts]).groupby('Team')['Pts'].sum().sort_values(ascending=False)
        
        n_teams = len(total_pts)
        if n_teams == 0: continue
            
        top_n = max(1, int(n_teams * top_pct))
        bottom_n = max(1, int(n_teams * bottom_pct))
        
        top_teams = total_pts.head(top_n).index.tolist()
        bottom_teams = total_pts.tail(bottom_n).index.tolist()
        
        # 2. Filtrar enfrentamientos asimétricos en la temporada TARGET
        mask_top_home = df_target['HomeTeam'].isin(top_teams) & df_target['AwayTeam'].isin(bottom_teams)
        mask_bot_home = df_target['HomeTeam'].isin(bottom_teams) & df_target['AwayTeam'].isin(top_teams)
        
        asym_matches = df_target[mask_top_home | mask_bot_home]
        if len(asym_matches) == 0: continue
            
        total_asymmetric_matches += len(asym_matches)
        
        # 3. Contar sorpresas según la definición
        for _, match in asym_matches.iterrows():
            is_bottom_home = match['HomeTeam'] in bottom_teams
            result = match['FTR']
            
            is_upset = False
            if upset_def == "Pierde": # Sorpresa agresiva: Favorito pierde
                if is_bottom_home and result == 'H': is_upset = True
                elif not is_bottom_home and result == 'A': is_upset = True
            elif upset_def == "No_Gana": # Sorpresa leve: Favorito empata o pierde
                if is_bottom_home and result in ['H', 'D']: is_upset = True
                elif not is_bottom_home and result in ['A', 'D']: is_upset = True
                
            if is_upset:
                total_upsets += 1
                
    if total_asymmetric_matches == 0:
        return 0.0, 0
        
    return total_upsets / total_asymmetric_matches, total_asymmetric_matches

if __name__ == "__main__":
    print("Iniciando Batería de Experimentos (Controlando Fuga de Información)...")
    
    try:
        import pandas as pd
    except ImportError:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
        import pandas as pd
        
    df_all = download_data_10_seasons()
    
    # Parámetros del Grid Search
    windows = [3, 5]                  # Ventana de 3 o 5 temporadas para construir jerarquía
    top_pcts = [0.10, 0.20]           # Top 10% vs Top 20%
    bottom_pcts = [0.10, 0.20]        # Bottom 10% vs Bottom 20%
    upset_defs = ["Pierde", "No_Gana"]# Definición de fracaso del favorito
    
    results = []
    
    print("\n--- EJECUTANDO GRID SEARCH ---")
    for league in df_all['League'].unique():
        df_league = df_all[df_all['League'] == league]
        
        for w, top, bot, u_def in itertools.product(windows, top_pcts, bottom_pcts, upset_defs):
            tasa, matches = evaluate_parameters(df_league, w, top, bot, u_def)
            if matches > 15: # Evitar muestras sin significancia estadística
                results.append({
                    'Liga': league,
                    'Ventana': w,
                    'Top%': f"{top*100:.0f}%",
                    'Bot%': f"{bot*100:.0f}%",
                    'Def_Sorpresa': u_def,
                    'Tasa': tasa,
                    'Partidos': matches
                })
                
    df_results = pd.DataFrame(results)
    
    print("\n--- MEJORES DESCUBRIMIENTOS POR LIGA (Tasa de Sorpresas más baja) ---")
    for league in df_results['Liga'].unique():
        df_l = df_results[df_results['Liga'] == league]
        best = df_l.sort_values('Tasa').iloc[0]
        print(f"Liga: {league:15} | Tasa Sorpresa: {best['Tasa']:.1%} | Partidos: {best['Partidos']}")
        print(f"      (Ventana: {best['Ventana']} temp | Enfrentamiento: {best['Top%']} vs {best['Bot%']} | Definición Sorpresa: Favorito {best['Def_Sorpresa']})")
        print("-" * 80)
