'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing a Capacitated p-center facility location problem
#        in Python/cplex.CPLEX

import numpy as np
import cplex as cp
import time
t1 = time.time()

#     1. Read In Data
# Weights Vector
Dij = np.array ([0, 13, 8, 15, 13, 0, 12, 11, 8, 12, 0, 10, 15, 11, 10, 0])
Dij = Dij.reshape(4, 4)
# called below in the Capacity Constraint --->  qi = [1000, 1200, 1400, 1350]
# called below in the Capacity Constraint --->  Qi = [0, 6000, 0, 0]
rows, cols = Dij.shape
client_nodes = range(len(Dij[0]))
service_nodes = range(len(Dij))
# Indices & Variable Names
nodes = len(Dij)
Nodes = range(len(Dij))
all_nodes = len(Dij) * len(Dij)
ALL_nodes = range(all_nodes)
W = 'W'
x = 'x'
cli_var = []
for i in Nodes:
    for j in Nodes:
        temp = x + str(i+1) + '_' + str(j+1)
        cli_var.append(temp)
client_var = np.array(cli_var)
client_var = client_var.reshape(4,4)
print 'Client Variables\n' + str(cli_var)
y = 'y'
fac_var = []
for i in Nodes:
    temp = y + str(i+1)
    fac_var.append(temp)
facility_var = np.array(fac_var)
facility_var = facility_var.reshape(4,1)
print 'Facility Variables\n' + str(fac_var)

#     2. Create Model and Add Variables
# Create Model
m = cp.Cplex()
# Problem Name
m.set_problem_name('\n -- Capacitated P-Center -- ')
print m.get_problem_name()
# Problem Type  ==>  Linear Programming
m.set_problem_type(m.problem_type.LP)
# Set MIP Emphasis to '2' --> Optimal
m.parameters.emphasis.mip.set(2)
print m.parameters.get_changed()
print '\nProblem Type\n    ' + str(m.problem_type[m.get_problem_type()])
# Objective Function Sense  ==>  Minimize
m.objective.set_sense(m.objective.sense.minimize)
print 'Objective Sense\n    ' + str(m.objective.sense[m.objective.get_sense()])
# Add Maximized Minimized Average Time Variable
m.variables.add(names = [W],
                obj = [1],
                lb = [0],
                types = ['C'])
# Add Client Decision Variables
m.variables.add(names = [cli_var[i] for i in ALL_nodes], 
                        lb = [0] * all_nodes, 
                        ub = [1] * all_nodes, 
                        types = ['B'] * all_nodes)
# Add Service Decision Variable
m.variables.add(names = [fac_var[i] for i in Nodes],
                        lb = [0] * nodes, 
                        ub = [1] * nodes, 
                        types = ['B'] * nodes)
                        
#    3. Add Constraints
# Add Assignment Constraints
for orig in Nodes:       
    assignment_constraints = cp.SparsePair(ind = [client_var[orig][dest] 
                                            for dest in Nodes],                           
                                            val = [1] * nodes)
    m.linear_constraints.add(lin_expr = [assignment_constraints],                 
                                senses = ['E'], 
                                rhs = [1]);
# Add Facility Constraint
facility_constraint = cp.SparsePair(ind = fac_var, 
                                    val = [1.0]*nodes)
m.linear_constraints.add(lin_expr = [facility_constraint],
                                senses = ['E'],
                                rhs = [1])
# Add Opening Constraint
cli_var_open = []
for i in Nodes:
    for j in Nodes:
        temp = x + str(j+1) + '_' + str(i+1)
        cli_var_open.append(temp)
fac_var_open = []
for i in Nodes:
    for j in Nodes:
        temp = y + str(i+1)
        fac_var_open.append(temp)
l = []
for i in ALL_nodes:
    l.append([cli_var_open[i]]+[fac_var_open[i]])
for i in l:
    opening_constraint = cp.SparsePair(ind = i, val = [-1.0, 1.0])
    m.linear_constraints.add(lin_expr = [opening_constraint], senses = ['G'], rhs = [0])
# Add Maximized Minimized Average Time Constraint       
cli_var_max = []
for i in Nodes:
    cli_var_max.append([])
    for j in Nodes:
        temp = x + str(i+1) + '_' + str(j+1)
        cli_var_max[i].append(temp)
l2 = []
for orig in Nodes:
    l2.append([cli_var_max[orig][dest] for dest in Nodes] + [W])
l3 = []
for orig in Nodes:
    l3.append([Dij[orig][dest] for dest in Nodes] + [-1])
for orig in Nodes:
    max_constraints = cp.SparsePair(ind = l2[orig], val = l3[orig])
    m.linear_constraints.add(lin_expr = [max_constraints],                 
                                senses = ['L'], 
                                rhs = [0]);
# Add Capacity Constraint  
cli_var_cap = []
for i in Nodes:
    cli_var_cap.append([])
    for j in Nodes:
        temp = x + str(j+1) + '_' + str(i+1)
        cli_var_cap[i].append(temp)
    temp = y + str(i+1)
    cli_var_cap[i].append(temp)
qi = [1000, 1200, 1400, 1350]
Qi = [0, -6000, 0, 0]
qi_cap = []
for i in Nodes:
    qi_cap.append(qi)
l4 = []
for orig in Nodes:
    l4.append([qi_cap[orig][dest] for dest in Nodes] + [Qi[orig]])
for orig in Nodes:
    max_constraints = cp.SparsePair(ind = cli_var_cap[orig], val = l4[orig])
    m.linear_constraints.add(lin_expr = [max_constraints],                 
                                senses = ['L'], 
                                rhs = [0]);

#    4. Optimize and Print Results
m.solve()
solution = m.solution
# solution.get_status() returns an integer code
print 'Solution status = ' , solution.get_status(), ':',
print solution.status[solution.get_status()]
# Display solution.
print 'Total cost = ' , solution.get_objective_value()
print 'Determination Time = ', m.get_dettime(), 'ticks'
print 'Real Time          = ', time.time()-t1, 'sec.'
print '****************************'
for f in fac_var:
    if (solution.get_values(f) >
        m.parameters.mip.tolerances.integrality.get()):
        print '    Facility %s is open' % f
    else:
        print '    Facility %s is closed' % f      
print '****************************'
print '\n-----\nJames Gaboardi, 2015'
m.write('path.lp')