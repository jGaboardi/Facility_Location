'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing a p-median facility location problem in Python/Gurobi[gurobipy]
# Change dimiensions of Cij and the Facility Constraint for varying spatial extents
# The dimension of the problem are SERVICExCLIENT unlike equation formulation

import numpy as np
import gurobipy as gbp
import time
t1 = time.time()

#     1. Read In Data
# Weights Vector
Ai = np.fromfile('path.txt', dtype=int, sep='\n')
Ai = Ai.reshape(1,len(Ai))
# Cost Matrix
Cij = np.fromfile('path.txt', dtype=float, sep='\n')
Cij = Cij.reshape(71,750)
# Cost Coefficients for Decision Variables
Sij = Ai * Cij
Sij = list(Sij)
client_nodes = range(len(Sij[0]))
service_nodes = range(len(Sij))

#       2. Create Model, Set MIP Focus, Add Variables, & Update Model
m = gbp.Model(' -- P-Median -- ')
# Set MIP Focus to 2 for optimality
gbp.setParam('MIPFocus', 2)
# Add Client Decision Variables
client_var = []
for orig in service_nodes:
    client_var.append([])
    for dest in client_nodes:
        client_var[orig].append(m.addVar(vtype=gbp.GRB.BINARY, 
                                            obj=Sij[orig][dest], 
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
m.setObjective(gbp.quicksum(Sij[orig][dest]*client_var[orig][dest] 
                        for orig in service_nodes for dest in client_nodes), 
                        gbp.GRB.MINIMIZE)

#       4. Add Constraints
#Add Assignment Constraints
for orig in client_nodes:
    m.addConstr(gbp.quicksum(client_var[dest][orig] 
                        for dest in service_nodes) == 1, 
                        'Assignment_Constraint_%d' % orig)
# Add Opening Constraints
for dest in service_nodes:
    for orig in client_nodes:
        m.addConstr((serv_var[dest] - client_var[dest][orig] >= 0), 
                        'Opening_Constraint_%d_%d' % (dest, orig))
# Add Facility Constraint
m.addConstr(gbp.quicksum(serv_var[dest][0] for dest in service_nodes) == 36,
                        'Facility_Constraint')

#       5. Optimize and Print Results
m.optimize()
print 'Selected Facility Locations:'
selected = []
for v in m.getVars():
    if 'x' in v.VarName:
        pass
    elif v.x > 0:
        selected.append(v.x)
        print('            Variable %s = %g' % (v.varName, v.x))
print 'Candidate Facilities          *', len(selected)
print('Rounded Objective (min):      * %g' % m.objVal)
print 'Real Time to Optimize (sec.): *', time.time()-t1
print '\n-----\nJames Gaboardi, 2015'

m.write('path.lp')