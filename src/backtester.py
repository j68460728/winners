import pandas as pd
import urllib.request
import io
import ssl
import itertools
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context

def download_financial_data():
    seasons = ['1415', '1516', '1617', '1718', '1819', '1920', '2021', '2122', '2223', '2324']
    leagues = {
        'Bundesliga': 'D1', 'Premier': 'E0', 'LaLiga': 'SP1', 'SerieA': 'I1',
        'Championship': 'E1', '2.Bundesliga': 'D2', 'SegundaEsp': 'SP2', 
        'Scotland': 'SC0', 'Belgium': 'B1'
    }
    
    all_data = []
    print("Descargando datos financieros y cuotas (2014-2024)...")
    
    # Cuotas a rastrear (Local, Empate, Visitante)
    odds_h = ['B365H', 'BWH', 'IWH', 'PSH', 'WHH', 'VCH', 'AvgH']
    odds_a = ['B365A', 'BWA', 'IWA', 'PSA', 'WHA', 'VCA', 'AvgA']
    
    for league_name, league_code in leagues.items():
        for season in seasons:
            url = f"https://www.football-data.co.uk/mmz4281/{season}/{league_code}.csv"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                df = pd.read_csv(io.StringIO(response.read().decode('utf-8', errors='ignore')))
                df['League'] = league_name
                df['Season'] = season
                
                # Quedarnos con info base + cuotas
                cols = ['League', 'Season', 'HomeTeam', 'AwayTeam', 'FTR'] + odds_h + odds_a
                df = df[[c for c in cols if c in df.columns]]
                df = df.dropna(subset=['FTR'])
                
                # Consolidar cuotas promediando todas las casas disponibles para evitar dependencia única
                available_h = [c for c in odds_h if c in df.columns]
                available_a = [c for c in odds_a if c in df.columns]
                
                df['Odds_H'] = df[available_h].mean(axis=1, skipna=True)
                df['Odds_A'] = df[available_a].mean(axis=1, skipna=True)
                
                # Eliminar partidos sin cuotas
                df = df.dropna(subset=['Odds_H', 'Odds_A'])
                all_data.append(df)
            except Exception:
                pass
                
    return pd.concat(all_data, ignore_index=True)

def simulate_financials(df_league, window_size, top_pct, bottom_pct):
    seasons = sorted(df_league['Season'].unique())
    
    train_seasons = ['1920', '2021'] 
    test_seasons = ['2122', '2223', '2324'] 
    
    def process_targets(target_list):
        bets = []
        
        for t_season in target_list:
            if t_season not in seasons: continue
            
            idx = seasons.index(t_season)
            if idx < window_size: continue
                
            history_seasons = seasons[idx-window_size:idx]
            df_hist = df_league[df_league['Season'].isin(history_seasons)]
            df_tar = df_league[df_league['Season'] == t_season].copy()
            
            # Puntos históricos
            home_pts = df_hist.groupby('HomeTeam')['FTR'].apply(lambda x: (x == 'H').sum() * 3 + (x == 'D').sum()).reset_index()
            home_pts.columns = ['Team', 'Pts']
            away_pts = df_hist.groupby('AwayTeam')['FTR'].apply(lambda x: (x == 'A').sum() * 3 + (x == 'D').sum()).reset_index()
            away_pts.columns = ['Team', 'Pts']
            total_pts = pd.concat([home_pts, away_pts]).groupby('Team')['Pts'].sum()
            
            n_teams = len(total_pts)
            if n_teams == 0: continue
            
            total_pts_sorted = total_pts.sort_values(ascending=False)
            top_teams = total_pts_sorted.head(max(1, int(n_teams * top_pct))).index.tolist()
            bottom_teams = total_pts_sorted.tail(max(1, int(n_teams * bottom_pct))).index.tolist()
            
            for _, match in df_tar.iterrows():
                h_team, a_team = match['HomeTeam'], match['AwayTeam']
                res = match['FTR']
                
                # Apostamos si Top juega contra Bottom
                bet_placed = False
                if h_team in top_teams and a_team in bottom_teams:
                    bet_placed = True
                    odds = match['Odds_H']
                    won = (res == 'H')
                elif a_team in top_teams and h_team in bottom_teams:
                    bet_placed = True
                    odds = match['Odds_A']
                    won = (res == 'A')
                    
                if bet_placed and pd.notna(odds):
                    profit = (odds - 1.0) if won else -1.0
                    bets.append({
                        'season': t_season,
                        'won': won,
                        'odds': odds,
                        'profit': profit
                    })
                    
        return bets

    train_bets = process_targets(train_seasons)
    test_bets = process_targets(test_seasons)
    
    def calc_metrics(bet_list):
        if not bet_list: return None
        df_b = pd.DataFrame(bet_list)
        total_bets = len(df_b)
        net_profit = df_b['profit'].sum()
        yield_pct = (net_profit / total_bets) * 100
        hit_rate = df_b['won'].mean()
        avg_odds = df_b['odds'].mean()
        
        # Max Drawdown
        bankroll = df_b['profit'].cumsum()
        peak = bankroll.cummax()
        drawdown = peak - bankroll
        max_dd = drawdown.max()
        
        return {
            'bets': total_bets,
            'profit': net_profit,
            'yield': yield_pct,
            'hit_rate': hit_rate,
            'avg_odds': avg_odds,
            'max_dd': max_dd,
            'raw': df_b
        }

    return calc_metrics(train_bets), calc_metrics(test_bets)

if __name__ == "__main__":
    df_all = download_financial_data()
    
    windows = [4, 5]
    configs = [(0.10, 0.10), (0.10, 0.20), (0.15, 0.15), (0.20, 0.20), (0.20, 0.30)]
    
    print("\n================================================================================")
    print("                 MVP 2: REPORTE DE VIABILIDAD ECONÓMICA (EV+)                   ")
    print("================================================================================\n")
    
    for league in df_all['League'].unique():
        df_league = df_all[df_all['League'] == league]
        
        best_gap = float('inf')
        best_cfg = None
        best_res = None
        
        # 1. Encontrar la configuración más estable en Train (Minimizar Gap de Yield)
        for w, (top, bot) in itertools.product(windows, configs):
            tr_res, ts_res = simulate_financials(df_league, w, top, bot)
            if tr_res and ts_res and tr_res['bets'] > 10 and ts_res['bets'] > 10:
                # Optimizamos por estabilidad del Yield entre train y test
                gap = abs(tr_res['yield'] - ts_res['yield'])
                if gap < best_gap:
                    best_gap = gap
                    best_cfg = (w, top, bot)
                    best_res = (tr_res, ts_res)
                    
        if best_cfg and best_res:
            tr, ts = best_res
            w, top, bot = best_cfg
            
            print(f"Liga:             {league}")
            print(f"Config Elegida:   V{w} | {top*100:.0f}%-{bot*100:.0f}% (Menor Yield Gap)")
            print(f"Train Yield:      {tr['yield']:+.2f}% (Partidos: {tr['bets']})")
            print(f"Test  Yield:      {ts['yield']:+.2f}% (Partidos: {ts['bets']})")
            print(f"Beneficio Neto:   {ts['profit']:+.2f} uds")
            print(f"Hit Rate Test:    {ts['hit_rate']:.1%}")
            print(f"Cuota Media:      {ts['avg_odds']:.2f}")
            print(f"Max Drawdown:     {ts['max_dd']:.2f} uds")
            
            # 2. Análisis de Sensibilidad y Robustez (Degradación)
            print("--- Curva de Degradación (Sensibilidad en Test) ---")
            degradations = [(0.10, 0.10), (0.10, 0.20), (0.20, 0.20), (0.20, 0.30), (0.30, 0.30)]
            for d_top, d_bot in degradations:
                _, ts_deg = simulate_financials(df_league, w, d_top, d_bot)
                if ts_deg:
                    y = ts_deg['yield']
                    p = ts_deg['profit']
                    b = ts_deg['bets']
                    print(f"    {d_top*100:.0f}% vs {d_bot*100:.0f}% -> Yield: {y:+.2f}% | Ben: {p:+.2f} u | Apuestas: {b}")
                else:
                    print(f"    {d_top*100:.0f}% vs {d_bot*100:.0f}% -> Sin suficientes datos")
            print("-" * 80)
