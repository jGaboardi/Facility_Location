'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing a Set Cover Location Problem problem in 
#        Python/Gurobi[gurobipy]
# Change dimensions of Cij and the Facility Constraint for varying
#        spatial extents
# The dimensions of the problem are SERVICExCLIENT (rowXcolumn)
#        unlike equation formulation CLIENTxSERVICE (rowXcolumn)

import numpy as np
import gurobipy as gbp
import time
t1 = time.time()

#           1. Read In (or Create) Data
'''
# Cost Vector
Cij = [0, 13, 8, 15, 13, 0, 12, 11, 8, 12, 0, 10, 15, 11, 10, 0]
'''
# Cost Vector
Cij = list(np.random.randint(100, 1000, 25))

# Create Aij: Determine Aij (nodes within S)
# S --> 1 = served; 0 = unserved
S = 500
Aij = []
for i in Cij:
    if i <= S:
        outtext = 1
    else:
        outtext = 0
    Aij.append(outtext)
Cij = np.array(Cij)
Cij = Cij.reshape(5,5)
rows, cols = Cij.shape
Aij = np.array(Aij)
Aij = Aij.reshape(5,5)
client_nodes = range(len(Cij[0]))

#     2. Create Model, Set MIP Focus, Add Variables, & Update Model
m = gbp.Model(" -- SCLP -- ")
# Set MIP Focus to 2 for optimality
gbp.setParam('MIPFocus', 2)
# Add Client Decision Variables
client_var = []
for orig in client_nodes:
    client_var.append(m.addVar(vtype=gbp.GRB.BINARY,
                                ub = 1,
                                name='x'+str(orig+1)))
# Update Model Variables
m.update()       

#     4. Set Objective Function
m.setObjective(gbp.quicksum(client_var[orig] 
                            for orig in client_nodes), 
                            gbp.GRB.MINIMIZE)

#    5. Add Constraints 
#Add Coverage Constraints
for orig in client_nodes:
        m.addConstr(gbp.quicksum(Aij[orig][dest]*client_var[dest] 
                                for dest in client_nodes) >= 1,
                                'Coverage_Constraint_%d' % orig)

#     6. Optimize and Print Results
m.optimize()
t2 = time.time()-t1
print '**********************************************************************'
selected = []
for v in m.getVars():
    if v.x > 0:
        var = '%s' % v.VarName
        selected.append(v.x)
        print '    |                                                                   ', var
print '    | Selected Facility Locations -------------------------------------  ^^^^ '
print '    | Coverage (S) ---------------------------------------------------- ', S
print '    | Client Nodes ---------------------------------------------------- ', len(client_nodes)
print '    | Candidate Facilities needed for 100% coverage of client nodes --- ', len(selected)
print '    | Real Time to Optimize (sec.) ------------------------------------ ', t2
print '*****************************************************************************************'
print '\nJames Gaboardi, 2015'
m.write("path.lp")