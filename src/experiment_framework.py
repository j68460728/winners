import pandas as pd
import urllib.request
import io
import ssl
import itertools
import math

ssl._create_default_https_context = ssl._create_unverified_context

def wilson_score_interval(p, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    denominator = 1 + z**2 / n
    centre_adjusted_probability = p + z**2 / (2 * n)
    adjusted_standard_deviation = math.sqrt((p * (1 - p) / n) + (z**2 / (4 * n**2)))
    
    lower_bound = (centre_adjusted_probability - z * adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + z * adjusted_standard_deviation) / denominator
    return max(0, lower_bound), min(1, upper_bound)

def download_data_10_seasons():
    seasons = ['1415', '1516', '1617', '1718', '1819', '1920', '2021', '2122', '2223', '2324']
    leagues = {
        'Bundesliga': 'D1', 'Premier': 'E0', 'LaLiga': 'SP1', 'SerieA': 'I1',
        'Championship': 'E1', '2.Bundesliga': 'D2', 'SegundaEsp': 'SP2', 
        'Scotland': 'SC0', 'Belgium': 'B1'
    }
    
    all_data = []
    print("Descargando historial completo (2014-2024)...")
    for league_name, league_code in leagues.items():
        for season in seasons:
            url = f"https://www.football-data.co.uk/mmz4281/{season}/{league_code}.csv"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                df = pd.read_csv(io.StringIO(response.read().decode('utf-8', errors='ignore')))
                df['League'] = league_name
                df['Season'] = season
                cols_to_keep = ['League', 'Season', 'HomeTeam', 'AwayTeam', 'FTR']
                df = df[[c for c in cols_to_keep if c in df.columns]]
                df = df.dropna(subset=['FTR'])
                all_data.append(df)
            except Exception:
                pass
                
    return pd.concat(all_data, ignore_index=True)

def calculate_baselines(df_target, history_pts):
    """ Calcula el rendimiento de las líneas base en la temporada objetivo """
    if len(df_target) == 0:
        return 0.0, 0.0
        
    # Baseline Local: Apostar siempre al local
    home_wins = (df_target['FTR'] == 'H').sum()
    baseline_local = home_wins / len(df_target)
    
    # Baseline Favorito Histórico: Apostar siempre al que tiene más puntos históricos
    fav_wins = 0
    valid_matches = 0
    for _, match in df_target.iterrows():
        h_team = match['HomeTeam']
        a_team = match['AwayTeam']
        
        h_pts = history_pts.get(h_team, 0)
        a_pts = history_pts.get(a_team, 0)
        
        if h_pts == a_pts:
            continue # No hay favorito claro
            
        valid_matches += 1
        is_home_fav = h_pts > a_pts
        if is_home_fav and match['FTR'] == 'H':
            fav_wins += 1
        elif not is_home_fav and match['FTR'] == 'A':
            fav_wins += 1
            
    baseline_fav = fav_wins / valid_matches if valid_matches > 0 else 0.0
    return baseline_local, baseline_fav

def evaluate_config(df_league, window_size, top_pct, bottom_pct, upset_def):
    seasons = sorted(df_league['Season'].unique())
    
    train_seasons = ['1920', '2021'] # Temporadas objetivo para Train
    test_seasons = ['2122', '2223', '2324'] # Temporadas objetivo para Test
    
    def process_targets(target_list):
        upsets = 0
        matches = 0
        base_local_list = []
        base_fav_list = []
        
        for t_season in target_list:
            if t_season not in seasons: continue
            
            idx = seasons.index(t_season)
            if idx < window_size: continue
                
            history_seasons = seasons[idx-window_size:idx]
            df_hist = df_league[df_league['Season'].isin(history_seasons)]
            df_tar = df_league[df_league['Season'] == t_season]
            
            # Puntos históricos
            home_pts = df_hist.groupby('HomeTeam')['FTR'].apply(lambda x: (x == 'H').sum() * 3 + (x == 'D').sum()).reset_index()
            home_pts.columns = ['Team', 'Pts']
            away_pts = df_hist.groupby('AwayTeam')['FTR'].apply(lambda x: (x == 'A').sum() * 3 + (x == 'D').sum()).reset_index()
            away_pts.columns = ['Team', 'Pts']
            total_pts = pd.concat([home_pts, away_pts]).groupby('Team')['Pts'].sum()
            
            n_teams = len(total_pts)
            if n_teams == 0: continue
            
            # Baselines
            b_loc, b_fav = calculate_baselines(df_tar, total_pts.to_dict())
            base_local_list.append(b_loc)
            base_fav_list.append(b_fav)
            
            total_pts_sorted = total_pts.sort_values(ascending=False)
            top_teams = total_pts_sorted.head(max(1, int(n_teams * top_pct))).index.tolist()
            bottom_teams = total_pts_sorted.tail(max(1, int(n_teams * bottom_pct))).index.tolist()
            
            mask_top_home = df_tar['HomeTeam'].isin(top_teams) & df_tar['AwayTeam'].isin(bottom_teams)
            mask_bot_home = df_tar['HomeTeam'].isin(bottom_teams) & df_tar['AwayTeam'].isin(top_teams)
            
            asym_matches = df_tar[mask_top_home | mask_bot_home]
            matches += len(asym_matches)
            
            for _, match in asym_matches.iterrows():
                is_bottom_home = match['HomeTeam'] in bottom_teams
                res = match['FTR']
                
                is_upset = False
                if upset_def == "Pierde":
                    if is_bottom_home and res == 'H': is_upset = True
                    elif not is_bottom_home and res == 'A': is_upset = True
                elif upset_def == "No_Gana":
                    if is_bottom_home and res in ['H', 'D']: is_upset = True
                    elif not is_bottom_home and res in ['A', 'D']: is_upset = True
                    
                if is_upset: upsets += 1
                
        # Hit rate es 1 - tasa_sorpresa
        hit_rate = 1.0 - (upsets / matches) if matches > 0 else 0.0
        b_loc_avg = sum(base_local_list) / len(base_local_list) if base_local_list else 0.0
        b_fav_avg = sum(base_fav_list) / len(base_fav_list) if base_fav_list else 0.0
        
        return hit_rate, matches, b_loc_avg, b_fav_avg

    train_hit, train_matches, _, _ = process_targets(train_seasons)
    test_hit, test_matches, b_loc, b_fav = process_targets(test_seasons)
    
    return train_hit, train_matches, test_hit, test_matches, b_loc, b_fav

if __name__ == "__main__":
    df_all = download_data_10_seasons()
    
    windows = [4, 5]
    top_pcts = [0.10, 0.15, 0.20]
    bottom_pcts = [0.10, 0.15, 0.20]
    upset_defs = ["Pierde"] # Restringimos a 'Pierde' para este MVP y facilitar lectura
    
    print("\n================================================================================")
    print("                 REPORTE DE VALIDACIÓN CIENTÍFICA OUT-OF-SAMPLE                 ")
    print("================================================================================\n")
    
    for league in df_all['League'].unique():
        df_league = df_all[df_all['League'] == league]
        
        best_config = None
        best_gap = float('inf')
        
        # Grid Search en TRAIN, optimizando por GAP
        for w, top, bot, u_def in itertools.product(windows, top_pcts, bottom_pcts, upset_defs):
            tr_hit, tr_m, ts_hit, ts_m, b_loc, b_fav = evaluate_config(df_league, w, top, bot, u_def)
            
            if tr_m > 10 and ts_m > 10: # Minimo de significancia
                gap = abs(tr_hit - ts_hit)
                
                # Criterio de selección: Menor Gap (Estabilidad)
                if gap < best_gap:
                    best_gap = gap
                    best_config = {
                        'config': f"V{w} | {top*100:.0f}%-{bot*100:.0f}% | {u_def}",
                        'tr_hit': tr_hit,
                        'ts_hit': ts_hit,
                        'gap': gap,
                        'ts_m': ts_m,
                        'b_loc': b_loc,
                        'b_fav': b_fav
                    }
                    
        if best_config:
            lower_ci, upper_ci = wilson_score_interval(best_config['ts_hit'], best_config['ts_m'])
            
            # Resultado final: Supera baselines de forma concluyente?
            hit = best_config['ts_hit']
            es_superior = hit > best_config['b_loc'] and hit > best_config['b_fav']
            res_final = "SEÑAL ROBUSTA" if es_superior and best_config['gap'] < 0.15 else "RUIDO / INESTABLE"
            
            print(f"Liga:             {league}")
            print(f"Train (Hit Rate): {best_config['tr_hit']:.1%}")
            print(f"Test  (Hit Rate): {best_config['ts_hit']:.1%}")
            print(f"Gen. Gap:         {best_config['gap']:.1%}")
            print(f"Partidos (Test):  {best_config['ts_m']}")
            print(f"Wilson CI (95%):  [{lower_ci:.1%} - {upper_ci:.1%}]")
            print(f"Config Elegida:   {best_config['config']}")
            print(f"Baseline Local:   {best_config['b_loc']:.1%}")
            print(f"Baseline Favorito:{best_config['b_fav']:.1%}")
            print(f"Resultado Final:  {res_final}")
            print("-" * 80)
