from processing import overall, consensus, compiled_dir, drop_injured, drop_questionable, random_dropout
from pulp import *
import pandas as pd
import random

overall["PROJ. FPTS"] = overall["PROJ. FPTS"].astype(float)
players = range(len(list(overall["PLAYER NAME"])))
projections = list(overall["PROJ. FPTS"])
salaries = list(overall["Salary"])

qb_dict = {i: 1 if overall.loc[i]["Position"]=="QB" else 0 for i in range(len(players))}
rb_dict = {i: 1 if overall.loc[i]["Position"]=="RB" else 0 for i in range(len(players))}
wr_dict = {i: 1 if overall.loc[i]["Position"]=="WR" else 0 for i in range(len(players))}
te_dict = {i: 1 if overall.loc[i]["Position"]=="TE" else 0 for i in range(len(players))}
flex_dict = {i: 1 if overall.loc[i]["Position"] in ["RB", "WR", "TE"] else 0 for i in range(len(players))}
dst_dict = {i: 1 if overall.loc[i]["Position"]=="DST" else 0 for i in range(len(players))}

prob = LpProblem("Fantasy Football",LpMaximize)
player_vars = LpVariable.dicts("Players",players,0,1,LpBinary)

# objective function
prob += lpSum([projections[i]*player_vars[i] for i in players]), "Total Projection"

# constraint
prob += lpSum([salaries[i] * player_vars[i] for i in players]) <= 60000, "Total Salary"
prob += lpSum([qb_dict[i] * player_vars[i] for i in players]) == 1, "Exactly 1 QB"
prob += lpSum([rb_dict[i] * player_vars[i] for i in players]) >= 2, "At least 2 RBs"
prob += lpSum([wr_dict[i] * player_vars[i] for i in players]) >= 3, "At least 3 WRs"
prob += lpSum([te_dict[i] * player_vars[i] for i in players]) >= 1, "At least 1 TE"
prob += lpSum([flex_dict[i] * player_vars[i] for i in players]) == 7, "Exactly 7 RB/WR/TEs"
prob += lpSum([dst_dict[i] * player_vars[i] for i in players]) == 1, "Exactly 1 D/ST"

# solve
prob.solve()
winning_players = {'QB': [], 'RB': [], 'WR': [], 'TE': [], 'DST': []}
players_list = []

for i in prob.variables():
    if i.varValue == 1:
        row = overall.loc[[int(str(i.name)[8:])]]
        winning_players[row.iloc[0]["Position"]].append(row)

winning_players['RB'].sort(key=lambda row : -row.iloc[0]["PROJ. FPTS"])
winning_players['WR'].sort(key=lambda row : -row.iloc[0]["PROJ. FPTS"])
winning_players['TE'].sort(key=lambda row : -row.iloc[0]["PROJ. FPTS"])

players_list += winning_players['QB']
players_list += winning_players['RB'][:2]
players_list += winning_players['WR'][:3]
players_list += winning_players['TE'][:1]
if len(winning_players['RB'])==3:
    players_list.append(winning_players['RB'][2])
elif len(winning_players['WR'])==4:
    players_list.append(winning_players['WR'][3])
else:
    players_list.append(winning_players['TE'][1])
players_list += winning_players['DST']

result = pd.concat(players_list)
result.reset_index(drop = True, inplace = True)
total_projection = result.sum(axis = 0)["PROJ. FPTS"]
total_salary = result.sum(axis = 0)["Salary"]
result.at[9, "PLAYER NAME"] = "Total"
result.at[9, "PROJ. FPTS"] = total_projection
result.at[9, "Salary"] = total_salary

file_number = random.randint(10000, 99999)
if consensus:
    if drop_questionable:
        if random_dropout == 0:
            result.to_csv(compiled_dir+'lineup_consensus_noQues.csv', index = False, header=True)
        else:
            result.to_csv(compiled_dir+str(random_dropout)+'_'+str(file_number)+'_lineup_con_noQ.csv', index = False, header=True)
    elif drop_injured:
        if random_dropout == 0:
            result.to_csv(compiled_dir+'lineup_consensus_noInj.csv', index = False, header=True)
        else:
            result.to_csv(compiled_dir+str(random_dropout)+'_'+str(file_number)+'_lineup_con_noI.csv', index = False, header=True)
    else:
        result.to_csv(compiled_dir+'lineup_consensus.csv', index = False, header=True)
else:
    if drop_questionable:
        result.to_csv(compiled_dir+'lineup_noQues.csv', index = False, header=True)
    elif drop_injured:
        result.to_csv(compiled_dir+'lineup_noInj.csv', index = False, header=True)
    else:
        result.to_csv(compiled_dir+'lineup.csv', index = False, header=True)