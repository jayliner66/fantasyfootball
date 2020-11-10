import pandas as pd
import numpy as np

fanduel_file = "fanduel/2020/FanDuel_2020_Week_10.csv"
fantasypros_dir = "fantasypros/2020/Week 10/FantasyPros_2020_Week_10_"
kept_categories = ['Nickname', 'Salary', 'Team', 'Injury Indicator']
abnormal_teams = ['BAL', 'IND', 'TEN', 'NE', 'CHI', 'MIN']
bye_teams = []

# aliases = pd.read_csv("aliases.csv").set_index('ID').T.to_dict('list')
fanduel_data = pd.read_csv(fanduel_file)

qb = fanduel_data.loc[fanduel_data['Position'] == 'QB']
rb = fanduel_data.loc[fanduel_data['Position'] == 'RB']
wr = fanduel_data.loc[fanduel_data['Position'] == 'WR']
te = fanduel_data.loc[fanduel_data['Position'] == 'TE']
dst = fanduel_data.loc[fanduel_data['Position'] == 'D']

qb = qb[kept_categories]
qb.reset_index(drop = True, inplace = True)
qb['PROJ. FPTS'] = np.nan
rb = rb[kept_categories]
rb.reset_index(drop = True, inplace = True)
rb['PROJ. FPTS'] = np.nan
wr = wr[kept_categories]
wr.reset_index(drop = True, inplace = True)
wr['PROJ. FPTS'] = np.nan
te = te[kept_categories]
te.reset_index(drop = True, inplace = True)
te['PROJ. FPTS'] = np.nan
dst = dst[kept_categories]
dst.reset_index(drop = True, inplace = True)
dst['PROJ. FPTS'] = np.nan

print(qb)
# Use to determine aliases needed
# for pos_pair in [(qb,'QB'),(rb,'RB'),(wr,'WR'),(te,'TE'),(dst, 'DST')]:
#     fantasy_pros_data = pd.read_csv(fantasypros_dir+pos_pair[1]+'_Rankings.csv')
#     for index, row in fantasy_pros_data.iterrows():
#         if not any(pos_pair[0]['Nickname'] == row['PLAYER NAME']) and row['TEAM'] not in abnormal_teams:
#             print(pos_pair[1], row['PLAYER NAME'], row['TEAM'])