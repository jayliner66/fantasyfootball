import pandas as pd
import numpy as np
import random

year = '2020'
week = '13'
consensus = True
drop_injured = True
drop_questionable = True
random_dropout = 0

fanduel_file = "fanduel/"+year+"/FanDuel_"+year+"_Week_"+week+".csv"
fantasypros_consensus_dir = "fantasypros_consensus/"+year+"/Week "+week+"/FantasyPros_Fantasy_Football_Projections_"
fantasypros_dir = "fantasypros/"+year+"/Week "+week+"/FantasyPros_"+year+"_Week_"+week+"_"
compiled_dir = "compiled_data/"+year+"/Week "+week+"/"
fantasypros_categories = ['PLAYER NAME', 'TEAM', 'PROJ. FPTS']
fanduel_categories = ['Salary', 'Injury Indicator']
abnormal_teams = ['DEN','KC','WAS','PIT','BUF','SF','DAL','BAL']
bye_teams = []

if consensus:
    qb = pd.read_csv(fantasypros_consensus_dir+"QB.csv")
    rb = pd.read_csv(fantasypros_consensus_dir+"RB.csv")
    wr = pd.read_csv(fantasypros_consensus_dir+"WR.csv")
    te = pd.read_csv(fantasypros_consensus_dir+"TE.csv")
    dst = pd.read_csv(fantasypros_consensus_dir+"DST.csv")
else:
    qb = pd.read_csv(fantasypros_dir+'QB_Rankings.csv')
    rb = pd.read_csv(fantasypros_dir+'RB_Rankings.csv')
    wr = pd.read_csv(fantasypros_dir+'WR_Rankings.csv')
    te = pd.read_csv(fantasypros_dir+'TE_Rankings.csv')
    dst = pd.read_csv(fantasypros_dir+'DST_Rankings.csv')

if consensus:
    qb.rename(columns={"Player": "PLAYER NAME", "Team": "TEAM", "FPTS": "PROJ. FPTS"}, inplace = True)
    rb.rename(columns={"Player": "PLAYER NAME", "Team": "TEAM", "FPTS": "PROJ. FPTS"}, inplace = True)
    wr.rename(columns={"Player": "PLAYER NAME", "Team": "TEAM", "FPTS": "PROJ. FPTS"}, inplace = True)
    te.rename(columns={"Player": "PLAYER NAME", "Team": "TEAM", "FPTS": "PROJ. FPTS"}, inplace = True)
    dst.rename(columns={"Player": "PLAYER NAME", "Team": "TEAM", "FPTS": "PROJ. FPTS"}, inplace = True)

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

# # Use to determine aliases needed
# for pos_pair in [(qb,'QB'),(rb,'RB'),(wr,'WR'),(te,'TE'),(dst, 'D')]:
#     fanduel_pos_data = fanduel_data.loc[fanduel_data['Position'] == pos_pair[1]]
#     for index, row in pos_pair[0].iterrows():
#         if not any(fanduel_pos_data['Nickname'] == row['PLAYER NAME']) and row['TEAM'] not in abnormal_teams:
#             print(pos_pair[1], row['PLAYER NAME'], row['TEAM'])

if drop_injured or drop_questionable:
    fanduel_data.drop(fanduel_data.loc[fanduel_data['Injury Indicator']=='D'].index, inplace=True)
    fanduel_data.drop(fanduel_data.loc[fanduel_data['Injury Indicator']=='O'].index, inplace=True)
    fanduel_data.drop(fanduel_data.loc[fanduel_data['Injury Indicator']=='NA'].index, inplace=True)
    fanduel_data.drop(fanduel_data.loc[fanduel_data['Injury Indicator']=='IR'].index, inplace=True)
if drop_questionable:
    fanduel_data.drop(fanduel_data.loc[fanduel_data['Injury Indicator']=='Q'].index, inplace=True)

for pos_pair in [(qb,'QB'),(rb,'RB'),(wr,'WR'),(te,'TE'),(dst, 'D')]:
    fanduel_pos_data = fanduel_data.loc[fanduel_data['Position'] == pos_pair[1]]
    for index, row in pos_pair[0].iterrows():
        complete_break = False
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
            try:
                search_index = fanduel_pos_data.index[fanduel_pos_data['Nickname'] == search_name].tolist()[0]
                pos_pair[0].at[index, category] = fanduel_pos_data.loc[search_index][category]
            except:
                pos_pair[0].drop(index, inplace = True)
                complete_break = True
                break
        if random.random() < random_dropout and not complete_break:
            pos_pair[0].drop(index, inplace = True)
    pos_pair[0].reset_index(drop = True, inplace = True)
    if random_dropout == 0:
        if consensus:
            pos_pair[0].to_csv(compiled_dir+pos_pair[1]+'_consensus.csv', index = False, header=True)
        else:
            pos_pair[0].to_csv(compiled_dir+pos_pair[1]+'.csv', index = False, header=True)

overall = pd.concat([qb, rb, wr, te, dst])
overall.reset_index(drop = True, inplace = True)
for i in range(overall.shape[0]):
    if overall.loc[i]["PROJ. FPTS"] == '-':
        overall.at[i, "PROJ. FPTS"] = 0.0

if not drop_injured and not drop_questionable and random_dropout == 0:
    if consensus:
        overall.to_csv(compiled_dir+'OVERALL_consensus.csv', index = False, header=True)
    else:
        overall.to_csv(compiled_dir+'OVERALL.csv', index = False, header=True)