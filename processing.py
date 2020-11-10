import pandas as pd
import numpy as np

year = '2020'
week = '10'

fanduel_file = "fanduel/"+year+"/FanDuel_"+year+"_Week_"+week+".csv"
fantasypros_dir = "fantasypros/"+year+"/Week "+week+"/FantasyPros_"+year+"_Week_"+week+"_"
compiled_dir = "compiled_data/"+year+"/Week "+week+"/"
fantasypros_categories = ['PLAYER NAME', 'TEAM', 'PROJ. FPTS']
fanduel_categories = ['Salary', 'Injury Indicator']
abnormal_teams = ['BAL', 'IND', 'TEN', 'NE', 'CHI', 'MIN']
bye_teams = []

qb = pd.read_csv(fantasypros_dir+'QB_Rankings.csv')
rb = pd.read_csv(fantasypros_dir+'RB_Rankings.csv')
wr = pd.read_csv(fantasypros_dir+'WR_Rankings.csv')
te = pd.read_csv(fantasypros_dir+'TE_Rankings.csv')
dst = pd.read_csv(fantasypros_dir+'DST_Rankings.csv')

qb = qb[fantasypros_categories]
qb["Position"] = 'QB'
qb["Salary"] = np.nan
qb["Injury Indicator"] = ''
rb = rb[fantasypros_categories]
rb["Position"] = 'RB'
rb["Salary"] = np.nan
rb["Injury Indicator"] = ''
wr = wr[fantasypros_categories]
wr["Position"] = 'WR'
wr["Salary"] = np.nan
wr["Injury Indicator"] = ''
te = te[fantasypros_categories]
te["Position"] = 'TE'
te["Salary"] = np.nan
te["Injury Indicator"] = ''
dst = dst[fantasypros_categories]
dst["Position"] = 'DST'
dst["Salary"] = np.nan
dst["Injury Indicator"] = ''

aliases = pd.read_csv("aliases.csv")
fantasypros_to_fanduel = aliases.set_index("FantasyPros name").T.to_dict()
# print(fantasypros_to_fanduel)
fanduel_data = pd.read_csv(fanduel_file)

# Use to determine aliases needed
# for pos_pair in [(qb,'QB'),(rb,'RB'),(wr,'WR'),(te,'TE'),(dst, 'D')]:
#     fanduel_pos_data = fanduel_data.loc[fanduel_data['Position'] == pos_pair[1]]
#     for index, row in pos_pair[0].iterrows():
#         if not any(fanduel_pos_data['Nickname'] == row['PLAYER NAME']) and row['TEAM'] not in abnormal_teams:
#             print(pos_pair[1], row['PLAYER NAME'], row['TEAM'])

for pos_pair in [(qb,'QB'),(rb,'RB'),(wr,'WR'),(te,'TE'),(dst, 'D')]:
    fanduel_pos_data = fanduel_data.loc[fanduel_data['Position'] == pos_pair[1]]
    for index, row in pos_pair[0].iterrows():
        search_name = row['PLAYER NAME']
        if not any(fanduel_pos_data['Nickname'] == row['PLAYER NAME']):
            if row['TEAM'] in abnormal_teams:
                pos_pair[0].drop(index, inplace = True)
                continue
            elif search_name in fantasypros_to_fanduel:
                search_name = fantasypros_to_fanduel[search_name]['FanDuel name']
            else:
                pos_pair[0].drop(index, inplace = True)
                continue
        for category in fanduel_categories:
            search_index = fanduel_pos_data.index[fanduel_pos_data['Nickname'] == search_name].tolist()[0]
            pos_pair[0].at[index, category] = fanduel_pos_data.loc[search_index][category]
    pos_pair[0].reset_index(drop = True, inplace = True)
    pos_pair[0].to_csv(compiled_dir+pos_pair[1]+'.csv', index = False, header=True)

overall = pd.concat([qb, rb, wr, te, dst])
overall.to_csv(compiled_dir+'OVERALL.csv', index = False, header=True)