'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing a p-Center facility location problem in
#        Python/cplex.CPLEX

import numpy as np
import cplex as cp
import time
t1 = time.time()

#     1. Read In Data
# Cost Matrix
#Cij = np.fromfile('/path/Cij.txt', dtype=float, sep='\n')
#Cij = Cij.reshape(4,4)
Cij = [[  0.,  13.,   8.,  15.],
 [ 13.,   0.,  12.,  11.],
 [  8.,  12.,   0.,  10.],
 [ 15.,  11.,  10.,   0.]]
# Indices & Variable Names
nodes = len(Cij)
Nodes = range(len(Cij))
all_nodes = len(Cij) * len(Cij)
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
#print 'Client Variables\n' + str(cli_var)
y = 'y'
fac_var = []
for i in Nodes:
    temp = y + str(i+1)
    fac_var.append(temp)
facility_var = np.array(fac_var)
facility_var = facility_var.reshape(4,1)
#print 'Facility Variables\n' + str(fac_var)

#     2. Create Model and Add Variables
# Create Model
m = cp.Cplex()
# Problem Name
m.set_problem_name('\n -- P-Center -- ')
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
    l3.append([Cij[orig][dest] for dest in Nodes] + [-1])
for orig in Nodes:
    max_constraints = cp.SparsePair(ind = l2[orig], val = l3[orig])
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