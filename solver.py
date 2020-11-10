from processing import qb, rb, wr, te, dst
from pulp import *

prob = LpProblem("Lineup Optimization",LpMaximize)

players = []
players += list(qb["Nickname"])

qb_dict = {}
rb_dict = {}
wr_dict = {}
te_dict = {}
flex_dict = {}
dst_dict = {}

player = [str(i) for i in range(data.shape[0])]
point = {str(i): data['Points'][i] for i in range(data.shape[0])} 
cost = {str(i): data['Cost'][i] for i in range(data.shape[0])}
gk = {str(i): 1 if data['Position'][i] == 'GK' else 0 for i in range(data.shape[0])}
defe = {str(i): 1 if data['Position'][i] == 'DEF' else 0 for i in range(data.shape[0])}
mid = {str(i): 1 if data['Position'][i] == 'MID' else 0 for i in range(data.shape[0])}
stri = {str(i): 1 if data['Position'][i] == 'STR' else 0 for i in range(data.shape[0])}
xi = {str(i): 1 for i in range(data.shape[0])}

prob = LpProblem("Fantasy Football",LpMaximize)
player_vars = LpVariable.dicts("Players",player,0,1,LpBinary)

# objective function
prob += lpSum([point[i]*player_vars[i] for i in player]), "Total Cost"

# constraint
prob += lpSum([player_vars[i] for i in player]) == 11, "Total 11 Players"
prob += lpSum([cost[i] * player_vars[i] for i in player]) <= 100.0, "Total Cost"
prob += lpSum([gk[i] * player_vars[i] for i in player]) == 1, "Only 1 GK"
prob += lpSum([defe[i] * player_vars[i] for i in player]) <= 4, "Less than 4 DEF"
prob += lpSum([mid[i] * player_vars[i] for i in player]) <= 5, "Less than 5 MID"
prob += lpSum([stri[i] * player_vars[i] for i in player]) <= 3, "Less than 3 STR"

# solve
status = prob.solve()