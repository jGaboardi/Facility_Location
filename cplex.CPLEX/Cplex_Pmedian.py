'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing a p-median facility location problem
#        in Python/cplex.CPLEX

import numpy as np
import cplex as cp
import time
t1 = time.time()

#     1. Read In Data
# Weights Vector
#Ai = np.fromfile('path/Ai.txt', dtype=int, sep='\n')
#Ai = Ai.reshape(4,1)
# Cost Matrix
#Cij = np.fromfile('path/Cij.txt', dtype=float, sep='\n')
#Cij = Cij.reshape(4,4)
# Cost Coefficients for Decision Variables
#Sij = Ai * Cij
#Sij =  [[    0, 13000,  8000, 15000],
#         [15600,     0, 14400, 13200],
#         [ 8800, 13200,     0, 11000],
#         [18750, 13750, 12500,     0]]

# CREATE
# Cost Matrix
Cij = np.random.randint(100, 1000, 50000)
Cij = Cij.reshape(500,100)
# Weights Matrix
Ai = np.random.randint(1, 100, 500)
Ai = Ai.reshape(len(Ai), 1)
# Demand Sum
AiSum = np.sum(Ai)
# Weighted Cost Coefficients for Decision Variables
Sij = Ai * Cij

# Indices & Variable Names
client_nodes = range(len(Sij))
service_nodes = range(len(Sij[0]))

#Nodes = range(len(Sij))
all_nodes = len(Sij) * len(Sij[0])
ALL_nodes = range(all_nodes)

x = 'x'
cli_var = []
for i in client_nodes:
    for j in service_nodes:
        temp = x + str(i+1) + '_' + str(j+1)
        cli_var.append(temp)
client_var = np.array(cli_var)
client_var = client_var.reshape(len(Sij),len(Sij[0]))

y = 'y'
fac_var = []
for i in service_nodes:
    temp = y + str(i+1)
    fac_var.append(temp)
facility_var = np.array(fac_var)
facility_var = facility_var.reshape(1,len(Sij[0]))


#     2. Create Model and Add Variables
# Create Model
m = cp.Cplex()
# Problem Name
m.set_problem_name('\n -- P-Median -- ')
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
# Add Client Decision Variables
m.variables.add(names = [cli_var[i] for i in ALL_nodes],
                        obj = [Sij[i][j] for i in client_nodes for j in service_nodes], 
                        lb = [0] * all_nodes, 
                        ub = [1] * all_nodes, 
                        types = ['B'] * all_nodes)
# Add Service Decision Variable
m.variables.add(names = [fac_var[j] for j in service_nodes],
                        lb = [0] * len(Sij[0]), 
                        ub = [1] * len(Sij[0]), 
                        types = ['B'] * len(Sij[0]))

#    3. Add Constraints
# Add Assignment Constraints
for orig in client_nodes:       
    assignment_constraints = cp.SparsePair(ind = [client_var[orig][dest] 
                                            for dest in service_nodes],                           
                                            val = [1] * len(Sij[0]))
    m.linear_constraints.add(lin_expr = [assignment_constraints],                 
                                senses = ['E'], 
                                rhs = [1]);
# Add Facility Constraint
facility_constraint = cp.SparsePair(ind = fac_var, 
                                    val = [1.0] * len(Sij[0]))
m.linear_constraints.add(lin_expr = [facility_constraint],
                                senses = ['E'],
                                rhs = [1])
# Add Opening Constraint
cli_var_open = []
for i in client_nodes:
    for j in service_nodes:
        temp = x + str(i+1) + '_' + str(j+1)
        cli_var_open.append(temp)
fac_var_open = []
for i in client_nodes:
    for j in service_nodes:
        temp = y + str(j+1)
        fac_var_open.append(temp)
l = []
for i in ALL_nodes:
    l.append([cli_var_open[i]]+[fac_var_open[i]])
for i in l:
    opening_constraint = cp.SparsePair(ind = i, val = [-1.0, 1.0])
    m.linear_constraints.add(lin_expr = [opening_constraint], 
                                senses = ['G'], 
                                rhs = [0])
                                
#    4. Optimize and Print Results
m.solve()
m.write('/Users/jgaboardi/Desktop/LPpath.lp')
solution = m.solution
# solution.get_status() returns an integer code
print 'Solution status = ' , solution.get_status(), ':',
# the following line prints the corresponding string
print solution.status[solution.get_status()]
# Display solution.
print 'Total cost = ' , solution.get_objective_value()
print 'Determination Time = ', m.get_dettime(), 'ticks'
print 'Real Time to Optimize (sec.): *', time.time()-t1
print '****************************'
for f in fac_var:
    if (solution.get_values(f) >
        m.parameters.mip.tolerances.integrality.get()):
        print '    Facility %s is open' % f
    else:
        print '    Facility %s is closed' % f           
print '****************************'
print '\n-----\nJames Gaboardi, 2015'
