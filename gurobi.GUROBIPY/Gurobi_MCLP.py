# -*- coding: utf-8 -*-
'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing a Maximum Cover Location Problem problem in 
#        Python/Gurobi[gurobipy]
# Change dimensions of Cij and the Facility Constraint for varying
#        spatial extents
# The dimensions of the problem are SERVICExCLIENT (rowXcolumn)
#        unlike equation formulation CLIENTxSERVICE (rowXcolumn)

import numpy as np
import gurobipy as gbp
import time
np.random.seed(352)
t1 = time.time()

#           1. Read In (or Create) Data
'''
# Cost Vector
Cij = [0, 13, 8, 15, 13, 0, 12, 11, 8, 12, 0, 10, 15, 11, 10, 0]
# Demand
#Hi = np.array([1000, 1200, 1100, 1250])
'''
# Cost Vector
#Cij = list(np.random.randint(100, 1000, 25))
Cij = np.random.randint(2, 
                                10, 
                                4*4)

# Demand
#Hi = np.random.randint(1, 100, 5)


# Client Weights
Hi = np.random.randint(2, 
                        10, 
                        4)


HiSum = np.sum(Hi)
# Create Aij: Determine Aij (nodes within S)
# S --> 1 = served; 0 = unserved
S = 7.
Aij = []
for i in Cij:
    if i <= S:
        outtext = 1
    else:
        outtext = 0
    Aij.append(outtext)
Cij = np.array(Cij)
Cij = Cij.reshape(4,4)
Aij = np.array(Aij)
Aij = Aij.reshape(4,4)

client_nodes = range(len(Cij[0]))

#     2. Create Model, Set MIP Focus, Add Variables, & Update Model
m = gbp.Model(" -- MCLP -- ")
# Set MIP Focus to 2 for optimality
gbp.setParam('MIPFocus', 2)
# Add Client Decision Variables
client_var = []
for orig in client_nodes:
    client_var.append(m.addVar(vtype=gbp.GRB.BINARY,
                                ub = 1,
                                name='x'+str(orig+1)))
# Add Service Decision Variables
serv_var = []
for dest in client_nodes:
    serv_var.append(m.addVar(vtype=gbp.GRB.BINARY,
                                ub = 1,
                                name='y'+str(dest+1)))
# Update Model Variables
m.update()       

#     4. Set Objective Function
m.setObjective(gbp.quicksum(Hi[orig] * client_var[orig] 
                            for orig in client_nodes), 
                            gbp.GRB.MAXIMIZE)

#    5. Add Constraints 
#Add Coverage Constraints
for orig in client_nodes:
        m.addConstr(gbp.quicksum(Aij[orig][dest]*serv_var[dest] 
                                for dest in client_nodes) - client_var[orig] >= 0,
                                'Coverage_Constraint_%d' % orig)
# Add Facility Constraint  --> [p ≤ 2]
m.addConstr(gbp.quicksum(serv_var[dest] for dest in client_nodes) <= 1, 
                        "Facility_Constraint")
                        
#     6. Optimize and Print Results
m.optimize()
t2 = time.time()-t1
print '*****************************************************************************************'
selected = []
for v in m.getVars():
    if v.x > 0 and 'x' not in v.varName:
        var = '%s' % v.VarName
        selected.append(v.x)
        print '    |                                                           ', var
print '    | Selected Facility Locations ----------------------------  ^^^^ '
print '    | Coverage (S) ------------------------------------------- ', S
print '    | Candidate Facilities [p] ------------------------------- ', len(selected)
val = int(m.objVal)
print '    | Objective Value(clients covered in S/total clients) ---- ', val, '/', HiSum
print '    | Percentage of clients served --------------------------- ', round(float(val)/float(HiSum)*100, 4), '%'
print '    | Real Time to Optimize (sec.) --------------------------- ', t2
print '*****************************************************************************************'
print '\nJames Gaboardi, 2015'
m.write("path.lp")