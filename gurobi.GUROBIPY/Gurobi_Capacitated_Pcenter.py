'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing a Capacitated p-Center facility location problem in 
#        Python/Gurobi[gurobipy]
# Change dimensions of Dij and the Facility Constraint for varying 
#        spatial extents
# The dimension of the problem are SERVICExCLIENT (rowXcolumn) 
#        unlike equation formulation CLIENTxSERVICE (rowXcolumn)

import numpy as np
import gurobipy as gbp
import time
t1 = time.time()

#           1. Read In (or Create) Data
'''
# Cost Matrix
Dij = np.array ([0, 13, 8, 15, 13, 0, 12, 11, 8, 12, 0, 10, 15, 11, 10, 0])
Dij = Dij.reshape(4, 4)
qi = np.array([1000, 1200, 1400, 1350])
Qi = [0, 6000, 0, 0]
'''
Dij = np.random.randint(100, 1000, 25)
Dij = Dij.reshape(5,5)
qi = np.random.randint(1, 100, 5)
#qiSum = np.sum(qi)
Qi = np.random.randint(200, 300, 5)

client_nodes = range(len(Dij[0]))
service_nodes = range(len(Dij))







#     2. Create Model, Set MIP Focus, Add Variables, & Update Model
m = gbp.Model(" -- Capacitated P-Center -- ")
# Set MIP Focus to 2 for optimality
gbp.setParam('MIPFocus', 2)
# Add Client Decision Variables
client_var = []
for orig in service_nodes:
    client_var.append([])
    for dest in client_nodes:
        client_var[orig].append(m.addVar(vtype=gbp.GRB.BINARY, 
                                            obj=Dij[orig][dest], 
                                            name='x'+str(orig+1)+'_'+
                                            str(dest+1)))
# Add Service Decision Variables
serv_var = []
for dest in service_nodes:
    serv_var.append([])
    serv_var[dest].append(m.addVar(vtype=gbp.GRB.BINARY, 
                                    name='y'+str(dest+1)))
# Add Minimized Maximum Average Variable
W = m.addVar(vtype=gbp.GRB.CONTINUOUS,
            name='W')
# Update Model Variables
m.update()       

#     4. Set Objective Function
m.setObjective(W, gbp.GRB.MINIMIZE)

#    5. Add Constraints 
#Add Assignment Constraints
for orig in client_nodes:
    m.addConstr(gbp.quicksum(client_var[dest][orig] 
                        for dest in service_nodes) == 1, 
                        "Assignment_Constraint_%d" % orig)
# Add Opening Constraints
for dest in service_nodes:
    for orig in client_nodes:
        m.addConstr((serv_var[dest] - client_var[dest][orig] >= 0), 
                        "Opening_Constraint_%d_%d" % (dest, orig))
# Add Facility Constraint
m.addConstr(gbp.quicksum(serv_var[dest][0] for dest in service_nodes) == 1, 
                        "Facility_Constraint")
# Add Minimized Maximum Time Constraint
for orig in client_nodes:
    m.addConstr(gbp.quicksum(Dij[dest][orig]*client_var[dest][orig]
                        for dest in service_nodes) - W <= 0,
                        "Max_Time_Constraint_%d" % orig)
# Add Capacity Constraints
for dest in service_nodes:
    m.addConstr(gbp.quicksum(qi[dest]*client_var[dest][orig] 
                        for orig in client_nodes) - 
                        Qi[dest]*serv_var[dest][0] <= 0,
                        'Capacity_Constraint_%d_%d' % (dest, orig))

#     5. Optimize and Print Results
m.optimize()
print "Selected Facility Locations:"
selected = []
for v in m.getVars():
    if 'x' in v.VarName:
        pass
    elif 'W' in v.VarName:
        pass
    elif v.x > 0:
        selected.append(v.x)
        print('            Variable %s = %g' % (v.varName, v.x))
print 'Candidate Facilities          *', len(selected)
print('Rounded Objective (min):      * %g' % m.objVal)
print "Real Time to Optimize (sec.): *", time.time()-t1
print "\n-----\nJames Gaboardi, 2015"
m.write("path.lp")