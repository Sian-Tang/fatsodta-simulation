# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 08:35:16 2022

@author: Micha
"""

import networkx as nx
import gurobipy as gpy
import webbrowser
import sys
from collections import defaultdict
import itertools

# Zeithorizont
T = range(25) #TODO: Anpassen
# Supersenke
CSS = ["Super"]

# Graph G
G = nx.DiGraph()                        # intialize empty graph G

fatsodta_nodes = [
    ("Q1", {'type': 'source', 'total_cap': -1, 'agents': []}),
    ("Q2", {'type': 'source', 'total_cap': -1, 'agents': []}),
    ("Q3", {'type': 'source', 'total_cap': -1, 'agents': []}),
    ("C1", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C2", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C3", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C4", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C5", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C6", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C7", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C8", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C9", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C10", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C11", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C12", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C13", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C14", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C15", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C16", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C17", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C18", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C19", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C20", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C21", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C22", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C23", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C24", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C25", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C26", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C27", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C28", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C29", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C30", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C31", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C32", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C33", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("S1", {'type': 'sink', 'total_cap': -1, 'agents': []}),
    ("S2", {'type': 'sink', 'total_cap': -1, 'agents': []}),
    ("S3", {'type': 'sink', 'total_cap': -1, 'agents': []}),
    ("Super", {'type': 'sink', 'total_cap': -1, 'agents': []})
]
G.add_nodes_from(fatsodta_nodes)

case = "limited" #"semilimited","limited" #TODO: Anpassen
if case == "unlimited":
    flow = 10
elif case == "semilimited":
    flow = 5
elif case == "limited":
    flow = 3

limited     = 1
semilimited = 5
unlimited   = 10

semilimited_list = [
    ("C2","C4"),
    ("C11","C14"),
    ("C30","C10")]

limited_list = [
    ("C11","C13"),
    ("C15","C16"),
    ("C17","C22"),
    ("C23","C1")]

fatsodta_edges = [
    ("Q1","C1", {'flow': -1}),
    ("C1","C2", {'flow': unlimited}),
    ("C2","C3", {'flow': unlimited}),
    ("C2","C4", {'flow': semilimited}),         #- semilimited
    ("C3","C5", {'flow': unlimited}),
    ("C4","C9", {'flow': unlimited}),
    ("C5","C6", {'flow': unlimited}),
    ("C6","C7", {'flow': unlimited}),
    ("C7","C8", {'flow': unlimited}),
    ("C8","C9", {'flow': unlimited}),
    ("C9","C10", {'flow': unlimited}),
    ("C10","C11", {'flow': unlimited}),
    ("C11","C12", {'flow': unlimited}),
    ("C11","C13", {'flow': limited}),           ## limited
    ("C11","C14", {'flow': semilimited}),       #- semilimited
    ("C12","C15", {'flow': unlimited}),
    ("C13","C18", {'flow': unlimited}),
    ("C14","C31", {'flow': unlimited}),
    ("C15","C16", {'flow': limited}),           ## limited
    ("C15","C17", {'flow': unlimited}),
    ("C16","C20", {'flow': unlimited}),
    ("C17","C21", {'flow': unlimited}),
    ("C17","C22", {'flow': limited}),           ## limited
    ("C18","C19", {'flow': unlimited}),
    ("C19","C22", {'flow': unlimited}),
    ("C20","S1", {'flow': unlimited}),
    ("C21","S2", {'flow': -1}),
    ("C22","S3", {'flow': -1}),
    ("C23","C1", {'flow': limited}),            ## limited
    ("C23","C24", {'flow': unlimited}),
    ("C24","C25", {'flow': unlimited}),
    ("C25","C26", {'flow': unlimited}),
    ("C26","C27", {'flow': unlimited}),
    ("C27","C28", {'flow': unlimited}),
    ("C28","C29", {'flow': unlimited}),
    ("C29","C30", {'flow': unlimited}),
    ("C30","C10", {'flow': semilimited}),       #- semilimited
    ("C30","C14", {'flow': unlimited}),
    ("C31","C32", {'flow': unlimited}),
    ("C32","C33", {'flow': unlimited}),
    ("C33","C19", {'flow': unlimited}),
    ("Q2","C23", {'flow': -1}),
    ("Q3","C12", {'flow': -1}),
    ("S1","Super", {'flow': -1}),
    ("S2","Super", {'flow': -1}),
    ("S3","Super", {'flow': -1})
]


G.add_edges_from(fatsodta_edges)

#Nachfolgerzellen
Suc = dict()

for node in fatsodta_nodes:
    Suc[node[0]] = []

for edge in fatsodta_edges:
    Suc[edge[0]].append(edge[1])

# Suc = {
#        "Q1": ["A2"],
#        "Q2": ["A8"],
#        "A1": ["A4"],
#        "A2": ["A1", "A5"],
#        "A3": ["A2"],
#        "A4": ["A7", "S2"],
#        "A5": ["A4", "A6", "A8"],
#        "A6": ["A3", "S1"],
#        "A7": ["A8"],
#        "A8": ["A9"],
#        "A9": ["A6"],
#        "S1": ["Super"],
#        "S2": ["Super"],
#        "Super": []
#        }

#%% Konstruktion der Vorgängerzellen
Pre = dict()
for c in Suc.keys():
    Pre[c] = []
for k, v in Suc.items():
    for j in v:
        Pre[j].append(k)

#%% Konstruktion der benötigten Mengen
undefined = []
CR,CG,CS = [],[],[]
EG,ER,ES = [],[],[]
for g in Suc.keys():
    numberofsucessors = len(Suc[g])
    numberofpredecessors = len(Pre[g])
    if numberofsucessors > 1:
        CG.append(g) #CD in normalem SODTA
        for h in Suc[g]:
            EG.append((g,h)) #EM entsprechend
    elif numberofsucessors == 1:
# If "Supersink" is the only sucessor cell add cell to sink cells CS
        if Suc[g][0] in CSS:
            CS.append(g)
            for h in Suc[g]:
                ES.append((g,h))
        else:
# If there is exactly one sucessor and  one predecessor cell add cell to
# ordinary cells CO
            if numberofpredecessors == 1:
                CG.append(g) #CO in normalen SODTA
                for h in Suc[g]:
                    EG.append((g,h)) #EO entsprechend
# If there is only one sucessor and no predecessor cell add cell to source
# cells CR
            elif numberofpredecessors == 0:
                CR.append(g)
                for h in Suc[g]:
                    ER.append((g,h))
# If there is only one sucessor and more than one predecessor cell add cell
# to merging cells CM
            elif numberofpredecessors > 0:
                CG.append(g) #CM in normalem SODTA
                for h in Suc[g]:
                    EG.append((g,h)) #EM entsprechend
# Warning for undefined cells which are not the supersink
    else:
        if g not in CSS:
            undefined.append(g)
            print("WARNING UNDEFINED CELLS! CHECK CELL",g)

# Konstruktion Mengen C, E
C = CR+CG+CS+CSS
E = ER+EG+ES

#%%
#Konstruktion der OD-Paare
OD = []
for i in CR:
    for j in CS:
       OD.append((i,j))


#%% Konstruktion N,Q
N = dict()
Q = dict()
for node in fatsodta_nodes:
    for t in T:
        if node[1]["total_cap"] >= 0:
            N[node[0],t] = node[1]["total_cap"]

for node in fatsodta_nodes: # TODO:
    for t in T:
        Q[node[0],t] = 10 #

# for t in T:
#     # Q["C4",t] = 5
#     # Q["C13",t] = 1
#     # Q["C16",t] = 1
#     # Q["C17",t] = 5
#     Q["C21",t] = 1


# for t in range(3):
#     Q["C12",t] = 1
#TODO: Anpassen
# for t in list(range(3,len(T),4))+list(range(4,len(T),4)):
#     Q["C16",t] = 0



#%% Konstruktion Arrivaltime + Zeitfenster
tArr = round(max(T)/2) #### TODO: Anpassen
eps = tArr #### TODO: Anpassen
TW = range(tArr-eps,tArr+eps)

# d = dict()
# for (o,d) in OD:
#     d[(o,d),tArr] = 20

demand = defaultdict(lambda: 0) #TODO: Anpassen
for od in OD:
    demand[(od[0],od[1],tArr)] = 10
demand[("Q3","S2",tArr)] = 30

#---------------------- MODELL ---------------------
#%%
FATSODTA = gpy.Model()

#%% Entscheidungsvariablen
x = FATSODTA.addVars(OD,C,T, lb = 0, vtype=gpy.GRB.CONTINUOUS, name="x")
y = FATSODTA.addVars(OD,E,T, lb = 0, vtype=gpy.GRB.CONTINUOUS, name="y")
accS = FATSODTA.addVars(CS, lb=0, vtype = gpy.GRB.CONTINUOUS, name="accS")
accSuper = FATSODTA.addVar(lb = 0, vtype = gpy.GRB.CONTINUOUS, name="accSuper")

#%% Zielfunktion (1a)
FATSODTA.setObjective(gpy.quicksum(x[o,d,i,t] for t in T for i in CG+CR for (o,d) in OD),
                      gpy.GRB.MINIMIZE)
# FATSODTA.setObjective(gpy.quicksum(x[o,d,i,t] for t in T for i in CG+CR+CS for (o,d) in OD),
#                       gpy.GRB.MINIMIZE)

#%% Flusserhaltung (1b)
FATSODTA.addConstrs((x[o,d,i,t] == x[o,d,i,t-1]
                    + (gpy.quicksum(y[o,d,k,i,t-1] for k in Pre[i])
                       - gpy.quicksum(y[o,d,i,j,t-1] for j in Suc[i]))
                    for (o,d) in OD for i in C for t in T if t >0),
                    name = "Flow")

#%% MaxAusfluss bzgl Zellinhalt (1c)
FATSODTA.addConstrs((gpy.quicksum(y[o,d,i,j,t] for j in Suc[i]) <= x[o,d,i,t]
                     for i in CG+CR+CS for (o,d) in OD for t in T),
                    name= "Max_Out(Cont)")

#%% MaxZellenKapazität (1d)
FATSODTA.addConstrs((gpy.quicksum(y[o,d,i,j,t] for (o,d) in OD for i in Pre[j]) +
                     gpy.quicksum(x[o,d,j,t] for (o,d) in OD) <=
                     N[j,t] for j in CG for t in T),
                    name = "Max_Cell_Cap")

#%% MaxAusfluss bzgl Ausflusskapazität TODO: So ok?
# FATSODTA.addConstrs((gpy.quicksum(y[o,d,i,j,t] for (o,d) in OD for j in Suc[i]) <=
#                      Q[i,t] for i in CG for t in T),
#                     name = "Max_Out(Q)")

#%% MaxEinfluss bzgl Einflusskapazität
FATSODTA.addConstrs((gpy.quicksum(y[o,d,i,j,t] for (o,d) in OD for i in Pre[j]) <=
                     Q[i,t] for j in CG for t in T),
                    name = "Max_In(Q)")

#%% Netzwerk bei t = 0
FATSODTA.addConstrs((x[o,d,i,0] == 0 for (o,d) in OD for i in CG+CS+CSS),
                    name = "x(t=0)")

FATSODTA.addConstrs((y[o,d,i,j,0] == 0 for (o,d) in OD for (i,j) in E),
                    name = "y(t=0)")

#%% Ankunftszeit
FATSODTA.addConstrs((gpy.quicksum(y[o,d,i,j,t] for (i,j) in ES for t in TW) ==
                     demand[o,d,tArr] for (o,d) in OD),
                    name = "demand")

#%% Abfahrtsort #### TODO: In Modellbeschreibung aufnehmen
FATSODTA.addConstrs((x[o,d,i,t] == 0 for (o,d) in OD for i in CR if i != o for t in T),
                    name="Abfahrtsort")

FATSODTA.addConstrs(((x[o,d,i,t] == 0) for (o,d) in OD for i in CS if i != d for t in T),
                    name = "Senkenrestriktion")

FATSODTA.addConstrs((accS[i] == gpy.quicksum(x[o,d,i,t] for t in T for (o,d) in OD) for i in CS), name = "AccS")


FATSODTA.addConstr(accSuper == gpy.quicksum(x[o,d,"Super",len(T)-1] for (o,d) in OD))

# FATSODTA.write("FATSODTA-Exp-Mod.lp")
# webbrowser.open("FATSODTA-Exp-Mod.lp")

## Sian
# limited
FATSODTA.addConstrs((y["Q3","S1","Q3","C12",t] <= 1 for t in T), name = "q3,c12=1")
FATSODTA.addConstrs((y["Q2",d,"C23","C1",t] <= 1 for d in ["S1","S2","S3"] for t in T), name = "c23,c1=1")
FATSODTA.addConstrs((y[o,d,"C15","C16",t] <= 1 for (o,d) in itertools.product(["Q1","Q2","Q3"],["S1"]) for t in T), name = "c15,c16=1")
FATSODTA.addConstrs((y[o,d,"C17","C22",t] <= 1 for (o,d) in itertools.product(["Q1","Q2"],["S3"]) for t in T), name = "c17,c22=1")
FATSODTA.addConstrs((y[o,d,"C11","C13",t] <= 1 for (o,d) in itertools.product(["Q1","Q2"],["S3"]) for t in T), name = "c11,c13=1")
#semilimited
FATSODTA.addConstrs((y[o,d,"C15","C17",t] <= 5 for (o,d) in itertools.product(["Q1","Q2","Q3"],["S2","S3"]) for t in T), name = "c15,c17=5")
FATSODTA.addConstrs((y[o,d,"C2","C4",t] <= 5 for (o,d) in itertools.product(["Q1","Q2"],["S1","S2","S3"]) for t in T), name = "c2,c4=5")
FATSODTA.addConstrs((y[o,d,"C30","C10",t] <= 5 for (o,d) in itertools.product(["Q2"],["S1","S2","S3"]) for t in T), name = "c30,c10=5")
FATSODTA.addConstrs((y[o,d,"C11","C14",t] <= 5 for (o,d) in itertools.product(["Q1","Q2"],["S3"]) for t in T), name = "c11,c14=5")

#--------------------------------------



FATSODTA.optimize()
FATSODTA.write("FATSODTA-Solve.sol")
# webbrowser.open("FATSODTA-Solve.sol")

for v in FATSODTA.getVars():
    if v.X != 0:
        print("%s %f" % (v.Varname, v.X))
