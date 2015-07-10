# -*- coding: utf-8 -*-
'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''
# Building and Optimizing The Transportation Problem in
#        Python/Gurobi[gurobipy]
# Supply MUST equal Demand

import numpy as np
import gurobipy as gbp
import time
t1 = time.time()

#           1. Read In (or Create) Data
'''
# Cost Matrix
Cij = np.array([4,5,4,10,6,3,3,5,8])
Cij = Cij.reshape(3,3)
# Supply
Si = np.array([100,130,140])
Si = Si.reshape(3,1)
# Demand
Dj = np.array([150,100,120])
'''
# Cost Matrix
# 500x500
Cij = np.random.randint(100, 10000, 250000)
Cij = Cij.reshape(500,500)
# Supply
Si = np.random.randint(50, 200, 500)
Si = Si.reshape(500,1)
SiSum = np.sum(Si)
# Demand
Dj = np.sort(Si, axis=None)
DjSum = np.sum(Dj)
client_nodes = range(len(Cij))

#       2. Create Model, Set MIP Focus, Add Variables, & Update Model
m = gbp.Model(' -- The Transportation Problem -- ')
# Set MIP Focus to 2 for optimality
gbp.setParam('MIPFocus', 2)
client_var = []
for orig in client_nodes:
    client_var.append([])
    for dest in client_nodes:
        client_var[orig].append(m.addVar(vtype=gbp.GRB.CONTINUOUS, 
                                        obj=Cij[orig][dest], 
                                        name='x'+str(orig+1)+'_'+str(dest+1)))
# Update Model Variables
m.update()       

#       3. Set Objective Function
m.setObjective(gbp.quicksum(Cij[orig][dest]*client_var[orig][dest] 
                        for orig in client_nodes for dest in client_nodes), 
                        gbp.GRB.MINIMIZE)
                        
#       4. Add Constraints
# Add Supply Constraints
for orig in client_nodes:
     m.addConstr(gbp.quicksum(client_var[dest][orig] 
                        for dest in client_nodes) - Si[orig] == 0, 
                        'Supply_Constraint_%d' % orig)
# Add Demand Constraints
for orig in client_nodes:
     m.addConstr(gbp.quicksum(client_var[orig][dest] 
                        for dest in client_nodes) - Dj[orig] == 0, 
                        'Demand_Constraint_%d' % orig)

#       5. Optimize and Print Results
m.optimize()
t2 = time.time()-t1
print '*****************************************************************************************'
print '    | From SUPPLY Facility to DEMAND Facility x(Si)_(Dj) shipping # of units  '
print '    |                                         ↓↓        ↓↓     ↓↓'
selected = []
for v in m.getVars():
    if v.x > 0:
        var = '%s' % v.VarName
        value = '%i' % v.x
        selected.append(v.x)
        print '    |                                       ', var, '____ Units: ' ,value
print '    | Selected Facility Locations ---------  ^^^^^^^^^^^^^^^^^^^^^^^ '
print '    | Candidate Facilities [p] ------------ ', len(selected)
print '    | Supply Sum -------------------------- ', SiSum
print '    | Demand Sum -------------------------- ', DjSum
val = m.objVal
print '    | Objective Value --------------------- ', int(val)
print '    | Real Time to Optimize (sec.) -------- ', t2
print '*****************************************************************************************'
print '\nJames Gaboardi, 2015'
m.write('path.lp')