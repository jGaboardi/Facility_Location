#!/usr/bin/env python

import cplex as cp
import numpy as np
import time
#import pulp
t1 = time.time()

#P_Center = pulp.LpProblem("P-Center Problem", pulp.LpMinimize)

#m = pulp.cplex.Cplex()
m = cp.Cplex()                                      # Create model
m.parameters.emphasis.mip.set(2)                    # Set MIP emphasis to '2' --> Optimal
m.set_problem_type(m.problem_type.LP)               # Set problem type
m.objective.set_sense(m.objective.sense.minimize)   # Objective Function Sense  ==>  Minimize

np.random.seed(352)

# Cost Matrix
Cij = np.random.uniform(1, 10, 9)
Cij = Cij.reshape(3,3)
client_nodes = range(len(Cij))
service_nodes = range(len(Cij[0]))
all_nodes_len = len(Cij) * len(Cij[0])
ALL_nodes_range = range(all_nodes_len)

# Variable Indices
W = 'W'

client_var = []
for orig in client_nodes:
        client_var.append([])
        for dest in service_nodes:
            client_var[orig].append('x'+str(orig+1)+'_'+str(dest+1))

fac_var = []
for dest in service_nodes:
        fac_var.append([])
        fac_var[dest].append('y' + str(dest+1))


# Add Maximized Minimized Average Time Variable
m.variables.add(names = W,
                obj = [1],
                lb = [0],
                ub = [cp.infinity],
                types = ['C'])
# Add Client Decision Variables
m.variables.add(names = [client_var[i][j] for i in client_nodes for j in service_nodes], 
                        lb = [0] * all_nodes_len, 
                        ub = [1] * all_nodes_len, 
                        types = ['B'] * all_nodes_len)
# Add Service Decision Variable
m.variables.add(names = [fac_var[j][0] for j in service_nodes],
                        lb = [0] * len(Cij[0]), 
                        ub = [1] * len(Cij[0]), 
                        types = ['B'] * len(Cij[0]))


#    3. Add Constraints
# Add Assignment Constraints
for orig in client_nodes:       
    assignment_constraints = cp.SparsePair(ind = [client_var[orig][dest] 
                                            for dest in service_nodes],                           
                                            val = [1] * len(Cij[0]))
    m.linear_constraints.add(lin_expr = [assignment_constraints],                 
                                senses = ['E'], 
                                rhs = [1]);
# Add Facility Constraint
facility_constraint = cp.SparsePair(ind = [fac_var[j][0] for j in service_nodes], 
                                    val = [1.0] * len(Cij[0]))
m.linear_constraints.add(lin_expr = [facility_constraint],
                                senses = ['E'],
                                rhs = [1])
# Add Opening Constraint
OC = [[client_var[i][j]] + [fac_var[j][0]] for i in client_nodes for j in service_nodes]
for oc in OC:
    #print oc
    opening_constraints = cp.SparsePair(ind = oc, val = [-1.0, 1.0])
    m.linear_constraints.add(lin_expr = [opening_constraints], 
                                senses = ['G'], 
                                rhs = [0])
# Add Maximized Minimized Average Time Constraint
MC = [[],[]]
for i in client_nodes:
    MC[0].append([client_var[i][j] for j in service_nodes] + [W])
    MC[1].append([Cij[i][j] for j in service_nodes] + [-1])
#print MC
#val = []
#for i in client_nodes:
#    val.append([Cij[i][j] for j in service_nodes] + [-1])
#print val
for i in client_nodes:   
    #max_constraints = cp.SparsePair(ind = MC[i],                           
    #                                val = val[i])
    max_constraints = [MC[0][i], MC[1][i]]                            
    #print max_constraints
    m.linear_constraints.add(lin_expr = [max_constraints],                 
                                senses = ['L'], 
                                rhs = [0]);



m.write('/Users/jgaboardi/Desktop/pathCENTER.lp')
m.solve()
t2 = time.time()-t1
solution = m.solution

# Display solution.
print '****************************'
for f in fac_var:
    if solution.get_values(f[0]) > 0 :
        print 'Facility %s is open' % f[0]
print 'Solution status    = ' , solution.get_status(), ':', solution.status[solution.get_status()]
print 'Total cost         = ' , solution.get_objective_value()
print 'Determination Time = ', m.get_dettime(), 'ticks'
print 'Real Time          = ', t2/60, 'min.'        
print 'Matrix Size        = ', Cij.shape
print '****************************'
print '\n-----\nJames Gaboardi, 2016'