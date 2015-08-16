'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing an Uncapacitated Fixed Charge 
#    facility location problem in Python/Gurobi[gurobipy]
'''
Adapted from:

Daskin, Mark
    2008
    What You Should Know About Location Modeling
    Naval Research Logistics
    55:2
    283-294
'''

import numpy as np
import gurobipy as gbp
import time
t1 = time.time()

#     1. Read In (or Create) Data
# CREATE
# Distance Matrix
dij = np.random.randint(10, 20, 9)
dij = dij.reshape(3,3)
# Weights Matrix
hi = np.random.randint(1, 5, 3)
hi = hi.reshape(len(hi),1)
# Cost per mile
c = 1.25
# Demand Sum
hiSum = np.sum(hi)
# Fixed Facility Cost
Fj = np.random.randint(6, 10, 3)
Fj = Fj.reshape(1,len(Fj))
FjSum = np.sum(Fj)
# Weighted Cost Coefficients for Decision Variables
Sij = hi * dij

client_nodes = range(len(Sij))
service_nodes = range(len(Sij[0]))

#       2. Create Model, Set MIP Focus, Add Variables, & Update Model
m = gbp.Model(' -- UFLP -- ')
# Set MIP Focus to 2 for optimality
gbp.setParam('MIPFocus', 2)
# Add Client Decision Variables
client_var = []
for orig in client_nodes:
    client_var.append([])
    for dest in service_nodes:
        client_var[orig].append(m.addVar(vtype=gbp.GRB.BINARY, 
                                            obj=dij[orig][dest], 
                                            name='x'+str(orig+1)+'_'+str(dest+1)))
# Add Service Decision Variables
serv_var = []
for dest in service_nodes:
    serv_var.append([])
    serv_var[dest].append(m.addVar(vtype=gbp.GRB.BINARY, 
                                    name='y'+str(dest+1)))
# Update Model Variables
m.update()       

#       3. Set Objective Function
m.setObjective(gbp.quicksum((Fj[0][dest]*serv_var[dest][0] + 
                        c * Sij[orig][dest]*client_var[orig][dest] 
                        for orig in client_nodes for dest in service_nodes)), 
                        gbp.GRB.MINIMIZE)

#       4. Add Constraints
#Add Assignment Constraints
for orig in client_nodes:
    m.addConstr(gbp.quicksum(client_var[orig][dest] 
                        for dest in service_nodes) == 1)
# Add Opening Constraints
for dest in service_nodes:
    for orig in client_nodes:
        m.addConstr(serv_var[dest] - client_var[orig][dest] >= 0)

#       5. Optimize and Print Results
m.optimize()
t2 = time.time()-t1
print '**********************************************************************'
selected = []
for v in m.getVars():
    if 'x' in v.VarName:
        pass
    elif v.x > 0:
        var = '%s' % v.VarName
        selected.append(var)
        print '    |                                            ', var
print '    | Selected Facility Locations --------------  ^^^^ '
print '    | Candidate Facilities [p] ----------------- ', len(selected)
print '    | Cost per miles [c] ----------------------- ', c
val = m.objVal
print '    | Objective Value (Total Facility Cost) ---- ', val
print '    | Total Demand ----------------------------- ', hiSum
print '    | Total Potential Fixed Cost --------------- ', FjSum
avgh = float(m.objVal)/float(hiSum)
print '    | Avg. Cost / Demand ----------------------- ', avgh
avgF = float(m.objVal)/len(selected)
print '    | Avg. Cost / Facility --------------------- ', avgF
print '    | Real Time to Optimize (sec.) ------------- ', t2
print '**********************************************************************'
print 'Uncapacitated Fixed Charge Location Problem'
print '\nJames Gaboardi, 2015'
m.write('path.lp')