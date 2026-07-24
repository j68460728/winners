import pandas as pd
import urllib.request
import io
import ssl
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context

# --- CONFIGURACIÓN CONGELADA (VERSIÓN 1.0) ---
STATIC_CONFIG = {
    'Premier': {'code': 'E0', 'window': 5, 'top_pct': 0.20, 'bottom_pct': 0.30},
    '2.Bundesliga': {'code': 'D2', 'window': 5, 'top_pct': 0.20, 'bottom_pct': 0.30}
}
TEST_SEASONS = ['2122', '2223', '2324']
# ---------------------------------------------

def download_auditor_data(league_name, league_code, window_size):
    # Necesitamos las Test Seasons + Window Size históricas
    # Para Test = 2122, con V5, necesitamos desde 1617
    seasons = ['1617', '1718', '1819', '1920', '2021', '2122', '2223', '2324']
    all_data = []
    
    odds_h = ['B365H', 'BWH', 'IWH', 'PSH', 'WHH', 'VCH', 'AvgH']
    odds_a = ['B365A', 'BWA', 'IWA', 'PSA', 'WHA', 'VCA', 'AvgA']
    
    for season in seasons:
        url = f"https://www.football-data.co.uk/mmz4281/{season}/{league_code}.csv"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            df = pd.read_csv(io.StringIO(response.read().decode('utf-8', errors='ignore')))
            df['League'] = league_name
            df['Season'] = season
            
            cols = ['League', 'Season', 'HomeTeam', 'AwayTeam', 'FTR'] + odds_h + odds_a
            df = df[[c for c in cols if c in df.columns]]
            df = df.dropna(subset=['FTR'])
            
            avail_h = [c for c in odds_h if c in df.columns]
            avail_a = [c for c in odds_a if c in df.columns]
            df['Odds_H'] = df[avail_h].mean(axis=1, skipna=True)
            df['Odds_A'] = df[avail_a].mean(axis=1, skipna=True)
            
            df = df.dropna(subset=['Odds_H', 'Odds_A'])
            all_data.append(df)
        except Exception:
            pass
            
    return pd.concat(all_data, ignore_index=True)

def audit_league(league, config):
    df = download_auditor_data(league, config['code'], config['window'])
    seasons = sorted(df['Season'].unique())
    
    bets_log = []
    
    for t_season in TEST_SEASONS:
        if t_season not in seasons: continue
        idx = seasons.index(t_season)
        if idx < config['window']: continue
            
        df_hist = df[df['Season'].isin(seasons[idx-config['window']:idx])]
        df_tar = df[df['Season'] == t_season].copy()
        
        home_pts = df_hist.groupby('HomeTeam')['FTR'].apply(lambda x: (x == 'H').sum() * 3 + (x == 'D').sum()).reset_index()
        home_pts.columns = ['Team', 'Pts']
        away_pts = df_hist.groupby('AwayTeam')['FTR'].apply(lambda x: (x == 'A').sum() * 3 + (x == 'D').sum()).reset_index()
        away_pts.columns = ['Team', 'Pts']
        total_pts = pd.concat([home_pts, away_pts]).groupby('Team')['Pts'].sum()
        
        n_teams = len(total_pts)
        if n_teams == 0: continue
        
        tot_sorted = total_pts.sort_values(ascending=False)
        top_teams = tot_sorted.head(max(1, int(n_teams * config['top_pct']))).index.tolist()
        bot_teams = tot_sorted.tail(max(1, int(n_teams * config['bottom_pct']))).index.tolist()
        
        for _, match in df_tar.iterrows():
            h_t, a_t = match['HomeTeam'], match['AwayTeam']
            res = match['FTR']
            
            bet_placed = False
            winners_pick = None
            winners_odds = None
            won_winners = False
            
            if h_t in top_teams and a_t in bot_teams:
                bet_placed, winners_pick, winners_odds, won_winners = True, 'H', match['Odds_H'], (res == 'H')
            elif a_t in top_teams and h_t in bot_teams:
                bet_placed, winners_pick, winners_odds, won_winners = True, 'A', match['Odds_A'], (res == 'A')
                
            if bet_placed and pd.notna(winners_odds):
                win_prof = (winners_odds - 1.0) if won_winners else -1.0
                
                # Benchmark Implícito (Menor cuota)
                mkt_pick = 'H' if match['Odds_H'] <= match['Odds_A'] else 'A'
                mkt_odds = match['Odds_H'] if mkt_pick == 'H' else match['Odds_A']
                won_mkt = (res == mkt_pick)
                mkt_prof = (mkt_odds - 1.0) if won_mkt else -1.0
                
                bets_log.append({
                    'season': t_season,
                    'match': f"{h_t} vs {a_t}",
                    'winners_pick': winners_pick,
                    'mkt_pick': mkt_pick,
                    'result': res,
                    'winners_odds': winners_odds,
                    'mkt_odds': mkt_odds,
                    'winners_profit': win_prof,
                    'mkt_profit': mkt_prof,
                    'discrepancy': (winners_pick != mkt_pick)
                })
                
    return pd.DataFrame(bets_log)

def perform_bootstrap(df_bets, iterations=10000):
    profits = df_bets['winners_profit'].values
    n = len(profits)
    
    bs_yields = []
    for _ in range(iterations):
        sample = np.random.choice(profits, size=n, replace=True)
        bs_yield = (np.sum(sample) / n) * 100
        bs_yields.append(bs_yield)
        
    bs_yields = np.array(bs_yields)
    
    return {
        'mean': np.mean(bs_yields),
        'median': np.median(bs_yields),
        'std': np.std(bs_yields),
        'p5': np.percentile(bs_yields, 5),
        'p25': np.percentile(bs_yields, 25),
        'p50': np.percentile(bs_yields, 50),
        'p75': np.percentile(bs_yields, 75),
        'p95': np.percentile(bs_yields, 95),
        'prob_gt_0': np.mean(bs_yields > 0) * 100,
        'prob_gt_5': np.mean(bs_yields > 5) * 100,
        'prob_gt_10': np.mean(bs_yields > 10) * 100
    }

def print_audit_report(league, df_bets):
    print(f"\n================================================================================")
    print(f"                 AUDITORÍA CUANTITATIVA: {league.upper()}")
    print(f"================================================================================")
    
    # 1. Estabilidad Temporal
    print("\n[1] ESTABILIDAD TEMPORAL")
    print(f"{'Año':<8} | {'Apuestas':<10} | {'Yield Winners':<15} | {'Yield Mercado':<15} | {'Max DD':<10}")
    print("-" * 75)
    for s in TEST_SEASONS:
        df_s = df_bets[df_bets['season'] == s]
        if len(df_s) == 0: continue
        w_yield = (df_s['winners_profit'].sum() / len(df_s)) * 100
        m_yield = (df_s['mkt_profit'].sum() / len(df_s)) * 100
        cum = df_s['winners_profit'].cumsum()
        mdd = (cum.cummax() - cum).max()
        print(f"{s:<8} | {len(df_s):<10} | {w_yield:>+14.2f}% | {m_yield:>+14.2f}% | {mdd:>9.2f}u")
        
    # 2. Análisis Bootstrap
    bs_metrics = perform_bootstrap(df_bets)
    print("\n[2] DISTRIBUCIÓN BOOTSTRAP (N=10,000)")
    print(f"Media Yield:      {bs_metrics['mean']:+.2f}%")
    print(f"Mediana Yield:    {bs_metrics['median']:+.2f}%")
    print(f"Desviación Std:   {bs_metrics['std']:.2f}%")
    print(f"Percentiles:      P5: {bs_metrics['p5']:+.2f}% | P25: {bs_metrics['p25']:+.2f}% | P75: {bs_metrics['p75']:+.2f}% | P95: {bs_metrics['p95']:+.2f}%")
    print(f"P(ROI > 0%):      {bs_metrics['prob_gt_0']:.1f}%")
    print(f"P(ROI > 5%):      {bs_metrics['prob_gt_5']:.1f}%")
    print(f"P(ROI > 10%):     {bs_metrics['prob_gt_10']:.1f}%")
    
    # 3. Benchmark Discrepancias
    discrepancias = df_bets[df_bets['discrepancy']]
    print(f"\n[3] DISCREPANCIAS CONTRA EL FAVORITO IMPLÍCITO DEL MERCADO")
    print(f"Total de discrepancias encontradas: {len(discrepancias)} de {len(df_bets)} apuestas.")
    if len(discrepancias) > 0:
        win_prof_d = discrepancias['winners_profit'].sum()
        mkt_prof_d = discrepancias['mkt_profit'].sum()
        print(f"En partidos donde Winners contradijo al mercado:")
        print(f"  Beneficio Winners: {win_prof_d:+.2f} uds")
        print(f"  Beneficio Mercado: {mkt_prof_d:+.2f} uds")
        print("\nDetalle de discrepancias:")
        print(f"{'Partido':<25} | {'Win Pick':<10} | {'Mkt Pick':<10} | {'Res':<5} | {'Win Prof':<10} | {'Mkt Prof':<10}")
        print("-" * 80)
        for _, row in discrepancias.iterrows():
            print(f"{row['match']:<25} | {row['winners_pick']:<10} | {row['mkt_pick']:<10} | {row['result']:<5} | {row['winners_profit']:>+10.2f} | {row['mkt_profit']:>+10.2f}")

if __name__ == "__main__":
    for league, config in STATIC_CONFIG.items():
        df_bets = audit_league(league, config)
        if len(df_bets) > 0:
            print_audit_report(league, df_bets)
