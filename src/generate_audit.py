import pandas as pd
import urllib.request
import io
import ssl
import sys

ssl._create_default_https_context = ssl._create_unverified_context

def get_data():
    league_name = '2.Bundesliga'
    league_code = 'D2'
    window_size = 5
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
            
            cols = ['League', 'Season', 'Date', 'HomeTeam', 'AwayTeam', 'FTR'] + odds_h + odds_a
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

def generate_audit():
    df = get_data()
    seasons = sorted(df['Season'].unique())
    test_seasons = ['2122', '2223', '2324']
    
    config = {'code': 'D2', 'window': 5, 'top_pct': 0.20, 'bottom_pct': 0.30}
    
    audit_rows = []
    
    for t_season in test_seasons:
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
        
        # Rankings (1 to N)
        rank_map = {team: rank+1 for rank, team in enumerate(tot_sorted.index)}
        
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
                
                mkt_pick = 'H' if match['Odds_H'] <= match['Odds_A'] else 'A'
                mkt_odds = match['Odds_H'] if mkt_pick == 'H' else match['Odds_A']
                won_mkt = (res == mkt_pick)
                mkt_prof = (mkt_odds - 1.0) if won_mkt else -1.0
                
                if winners_pick != mkt_pick:
                    h_rank = rank_map.get(h_t, 'N/A')
                    a_rank = rank_map.get(a_t, 'N/A')
                    
                    mkt_prob = 1.0 / mkt_odds
                    win_prob = 1.0 / winners_odds
                    prob_diff = mkt_prob - win_prob
                    
                    if res == winners_pick:
                        classification = "Mercado sobrevaloró favorito"
                    elif res == mkt_pick:
                        classification = "Mercado infravaloró favorito"
                    else:
                        classification = "Indeterminada"
                    
                    audit_rows.append({
                        'Fecha': match.get('Date', 'N/A'),
                        'Partido': f"{h_t} vs {a_t}",
                        'Ranking_H': h_rank,
                        'Ranking_A': a_rank,
                        'Cuota_H': round(match['Odds_H'], 2),
                        'Cuota_A': round(match['Odds_A'], 2),
                        'Pick_Mercado': mkt_pick,
                        'Pick_Winners': winners_pick,
                        'Resultado': res,
                        'Win_Prof': round(win_prof, 2),
                        'Mkt_Prof': round(mkt_prof, 2),
                        'Diff_Prob': round(prob_diff, 3),
                        'Clasificacion': classification
                    })
                    
    df_audit = pd.DataFrame(audit_rows)
    
    with open('/home/coderman/.gemini/antigravity-ide/brain/7c6be1f5-f2f1-40a1-b584-bf7d42c08371/2bundesliga_discrepancies.md', 'w') as f:
        f.write("# Auditoría Cruda: 11 Discrepancias en 2.Bundesliga\n\n")
        f.write("Este documento contiene el registro individual de todas las apuestas donde Winners contradijo al favorito implícito del mercado en la 2.Bundesliga.\n\n")
        f.write("| Fecha | Partido | Rank H | Rank A | Cuota H | Cuota A | Pick Mkt | Pick Win | Res | Prof Win | Prof Mkt | Diff Prob | Clasificación |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
        for _, row in df_audit.iterrows():
            f.write(f"| {row['Fecha']} | {row['Partido']} | {row['Ranking_H']} | {row['Ranking_A']} | {row['Cuota_H']} | {row['Cuota_A']} | {row['Pick_Mercado']} | {row['Pick_Winners']} | {row['Resultado']} | {row['Win_Prof']:+0.2f} | {row['Mkt_Prof']:+0.2f} | {row['Diff_Prob']:+0.3f} | {row['Clasificacion']} |\n")

if __name__ == "__main__":
    generate_audit()
