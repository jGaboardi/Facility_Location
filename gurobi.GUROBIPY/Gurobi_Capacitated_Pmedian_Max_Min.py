'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing a Capacitated P-median Facility Location problem in
#        Python/Gurobi[gurobipy]
#   Maximum [Qy]and Minimum [Mi] Capacity Constraints Used
#       


import numpy as np
import gurobipy as gbp
import time
t1 = time.time()

#           1. Create Data
# Weights Array
Dij = np.random.randint(100, 1000, 49)
Dij = Dij.reshape(7,7)
# Demand
qi = np.random.randint(1, 100, 7)
# Demand Sum
qiSum = np.sum(qi)
# Max Capacity
Qy = np.random.randint(200, 300, 7)
# Min Capacity
Mi = np.random.randint(100, 200, 7)

rows, cols = Dij.shape
client_nodes = range(rows)
service_nodes = range(cols)

#       2. Create Model, Set MIP Focus, Add Variables, & Update Model
mCPMP = gbp.Model(' -- Capacitated P-Median -- ')
# Set MIP Focus to 2 for optimality
gbp.setParam('MIPFocus', 2)
# Add Client Decision Variables
client_var = []
for orig in client_nodes:
    client_var.append([])
    for dest in service_nodes:
        client_var[orig].append(mCPMP.addVar(vtype=gbp.GRB.BINARY, 
                                            obj=Dij[orig][dest], 
                                            name='x'+str(orig+1)+'_'+
                                            str(dest+1)))
# Add Service Decision Variables
serv_var = []
for dest in service_nodes:
    serv_var.append([])
    serv_var[dest].append(mCPMP.addVar(vtype=gbp.GRB.BINARY, 
                                    name='y'+str(dest+1)))

    # Update Model Variables
mCPMP.update()       

#       3. Set Objective Function
mCPMP.setObjective(gbp.quicksum(Dij[orig][dest]*client_var[orig][dest] 
                        for orig in client_nodes for dest in service_nodes),
                        gbp.GRB.MINIMIZE)

#       4. Add Constraints
#Add Assignment Constraints
for orig in client_nodes:
    mCPMP.addConstr(gbp.quicksum(client_var[orig][dest] 
                        for dest in service_nodes) == 1)
# Add Opening Constraints
for dest in service_nodes:
    for orig in client_nodes:
        mCPMP.addConstr((serv_var[dest] - client_var[orig][dest] >= 0))
# Add Facility Constraint
mCPMP.addConstr(gbp.quicksum(serv_var[dest][0] 
                        for dest in service_nodes) == 2)
# Add Max Capacity Constraints
for dest in service_nodes:
    mCPMP.addConstr(gbp.quicksum(qi[orig]*client_var[orig][dest]
                        for orig in client_nodes) - 
                        Qy[dest]*serv_var[dest][0] <= 0)
# Add Min Capacity Constraints
for dest in service_nodes:
    mCPMP.addConstr(gbp.quicksum(qi[orig]*client_var[orig][dest]
                        for orig in client_nodes) - 
                        Mi[dest]*serv_var[dest][0] >= 0)

#       5. Optimize and Print Results
mCPMP.optimize()
t2 = time.time()-t1
print '**********************************************************************'
selected = []
for v in mCPMP.getVars():
    if 'x' in v.VarName:
        pass
    elif v.x > 0:
        var = '%s' % v.VarName
        selected.append(var)
        print '    |                                            ', var
print '    | Selected Facility Locations --------------  ^^^^ '
print '    | Candidate Facilities [p] ----------------- ', len(selected)
val = mCPMP.objVal
print '    | Objective Value -------------------------- ', val
avg = float(mCPMP.objVal)/float(qiSum)


print '    | Avg. Value / Client ---------------------- ', avg
print '    | Real Time to Optimize (sec.) ------------- ', t2
print '**********************************************************************'
print '\nJames Gaboardi, 2015'
mCPMP.write('path.lp')