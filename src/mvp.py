import pandas as pd
import urllib.request
import io
import ssl
import sys

# Ignorar verificación SSL para evitar problemas de certificados con la fuente de datos
ssl._create_default_https_context = ssl._create_unverified_context

def download_data():
    # Descargaremos 5 temporadas de 4 grandes ligas desde football-data.co.uk
    seasons = ['1920', '2021', '2122', '2223', '2324']
    leagues = {
        'Bundesliga': 'D1', 
        'Premier League': 'E0', 
        'La Liga': 'SP1', 
        'Serie A': 'I1'
    }
    
    all_data = []
    for league_name, league_code in leagues.items():
        for season in seasons:
            url = f"https://www.football-data.co.uk/mmz4281/{season}/{league_code}.csv"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                # Leemos el CSV saltando líneas con errores si las hay
                df = pd.read_csv(io.StringIO(response.read().decode('utf-8', errors='ignore')))
                df['League'] = league_name
                df['Season'] = season
                
                # Nos quedamos con las columnas esenciales (HomeTeam, AwayTeam, FTHG, FTAG, FTR)
                cols_to_keep = ['League', 'Season', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
                df = df[[c for c in cols_to_keep if c in df.columns]]
                all_data.append(df)
            except Exception as e:
                print(f"Error descargando {league_name} {season}: {e}")
                
    return pd.concat(all_data, ignore_index=True)

def certificar_liga(df_liga, umbral_sorpresa=0.20):
    """
    Función MVP para certificar una liga.
    1. Calcula puntos históricos de la ventana.
    2. Define Dominantes (Top 20%) e Inferiores (Bottom 20%).
    3. Calcula tasa de sorpresas en enfrentamientos directos.
    """
    # 1. Puntos históricos
    home_pts = df_liga.groupby('HomeTeam')['FTR'].apply(lambda x: (x == 'H').sum() * 3 + (x == 'D').sum()).reset_index()
    home_pts.columns = ['Team', 'Pts']
    
    away_pts = df_liga.groupby('AwayTeam')['FTR'].apply(lambda x: (x == 'A').sum() * 3 + (x == 'D').sum()).reset_index()
    away_pts.columns = ['Team', 'Pts']
    
    total_pts = pd.concat([home_pts, away_pts]).groupby('Team')['Pts'].sum().sort_values(ascending=False)
    
    # 2. Identificar Top 20% y Bottom 20%
    n_teams = len(total_pts)
    top_n = max(1, int(n_teams * 0.2))
    bottom_n = max(1, int(n_teams * 0.2))
    
    top_teams = total_pts.head(top_n).index.tolist()
    bottom_teams = total_pts.tail(bottom_n).index.tolist()
    
    # 3. Extraer solo enfrentamientos directos (Top vs Bottom)
    mask_top_home = df_liga['HomeTeam'].isin(top_teams) & df_liga['AwayTeam'].isin(bottom_teams)
    mask_bot_home = df_liga['HomeTeam'].isin(bottom_teams) & df_liga['AwayTeam'].isin(top_teams)
    
    asymmetric_matches = df_liga[mask_top_home | mask_bot_home]
    
    if len(asymmetric_matches) == 0:
        return False, 0.0, 0, top_teams, bottom_teams
        
    # 4. Calcular tasa de sorpresas (Cuando el Inferior gana)
    upsets = 0
    for _, match in asymmetric_matches.iterrows():
        if match['HomeTeam'] in bottom_teams and match['FTR'] == 'H':
            upsets += 1
        elif match['AwayTeam'] in bottom_teams and match['FTR'] == 'A':
            upsets += 1
            
    tasa_sorpresa = upsets / len(asymmetric_matches)
    certificada = tasa_sorpresa <= umbral_sorpresa
    
    return certificada, tasa_sorpresa, len(asymmetric_matches), top_teams, bottom_teams

if __name__ == "__main__":
    print("Iniciando Pipeline de Certificación (MVP)...")
    try:
        import pandas as pd
    except ImportError:
        print("Instalando pandas...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
        import pandas as pd

    print("Descargando evidencia histórica (últimas 5 temporadas)...")
    df_all = download_data()
    
    print("\n=======================================================")
    print("      RESULTADOS DEL PIPELINE DE CERTIFICACIÓN         ")
    print("      Umbral de tolerancia a sorpresas: <= 20%         ")
    print("=======================================================\n")
    
    for league in df_all['League'].unique():
        df_liga = df_all[df_all['League'] == league]
        certificada, tasa, n_partidos, tops, bots = certificar_liga(df_liga, umbral_sorpresa=0.20)
        
        estado = "[ CERTIFICADA ]" if certificada else "[ NO CERTIFICADA ]"
        print(f"LIGA: {league}")
        print(f"ESTADO: {estado}")
        print(f"Tasa de sorpresas: {tasa:.1%} ({n_partidos} partidos analizados Top vs Bottom)")
        print(f"Dominantes: {', '.join(tops)}")
        print(f"Inferiores: {', '.join(bots)}")
        print("-" * 55)
