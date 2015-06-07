'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing a Maximum Cover Location Problem problem in 
#        Python/cplex.CPLEX

import numpy as np
import cplex as cp
import time
t1 = time.time()

#     1. Read In Data
# Cost Vector
Cij = [0, 13, 8, 15, 13, 0, 12, 11, 8, 12, 0, 10, 15, 11, 10, 0]
# Create Aij: Determine Aij (nodes within S)
# S --> 1 = served; 0 = unserved
S = 8
Aij = []
for i in Cij:
    if i <= S:
        outtext = 1
    else:
        outtext = 0
    Aij.append(outtext)
Cij = np.array(Cij)
Cij = Cij.reshape(4,4)
rows, cols = Cij.shape
Aij = np.array(Aij)
Aij = Aij.reshape(4,4)
Hi = [1000, 1200, 1100, 1250]
client_nodes = range(len(Cij[0]))

# Indices & Variable Names
nodes = len(Cij)
Nodes = range(len(Cij))
x = 'x'
cli_var = []
for i in Nodes:
    for j in Nodes:
        temp = x + str(j+1)
        cli_var.append(temp)
y = 'y'
fac_var = []
for i in Nodes:
    temp = y + str(i+1)
    fac_var.append(temp)

#     2. Create Model and Add Variables
# Create Model
m = cp.Cplex()
# Problem Name
m.set_problem_name('\n -- MCLP -- ')
print m.get_problem_name()
# Problem Type  ==>  Linear Programming
m.set_problem_type(m.problem_type.LP)
# Set MIP Emphasis to '2' --> Optimal
m.parameters.emphasis.mip.set(2)
print m.parameters.get_changed()
print '\nProblem Type\n    ' + str(m.problem_type[m.get_problem_type()])
# Objective Function Sense  ==>  Maximize
m.objective.set_sense(m.objective.sense.maximize)
print 'Objective Sense\n    ' + str(m.objective.sense[m.objective.get_sense()])
# Add Client Decision Variables
m.variables.add(names = [cli_var[i] for i in Nodes],  
                        obj = [Hi[i] for i in Nodes], 
                        types = ['B'] * nodes)
# Add Service Decision Variable
m.variables.add(names = [fac_var[i] for i in Nodes], 
                        types = ['B'] * nodes)

#    3. Add Constraints 
#Add Coverage Constraints
cli_var_cover = []
for i in Nodes:
    cli_var_cover.append([])
    for j in Nodes:
        temp = y + str(j+1)
        cli_var_cover[i].append(temp)
    temp = x + str(i+1)
    cli_var_cover[i].append(temp)
l = []
for orig in Nodes:
    l.append([Aij[orig][dest] for dest in Nodes] + [-1])
print l
for orig in Nodes:       
    coverage_constraints = cp.SparsePair(ind = cli_var_cover[orig],                           
                                            val = l[orig])
    m.linear_constraints.add(lin_expr = [coverage_constraints],                 
                                senses = ['G'], 
                                rhs = [0]);

# Add Facility Constraint
facility_constraint = cp.SparsePair(ind = fac_var, 
                                    val = [1.0]*nodes)
m.linear_constraints.add(lin_expr = [facility_constraint],
                                senses = ['L'],
                                rhs = [2])

#    4. Optimize and Print Results
m.solve()
solution = m.solution
# solution.get_status() returns an integer code
print 'Solution status = ' , solution.get_status(), ':',
# the following line prints the corresponding string
print solution.status[solution.get_status()]
# Display solution.
print 'Total cost = ' , solution.get_objective_value()
print 'Determination Time = ', m.get_dettime(), 'ticks'
print 'Real Time to Optimize (sec.): *', time.time()-t1
print '**************'
print "NOTE:  Selected Variables Are Not Displayed"   
print '\n-----\nJames Gaboardi, 2015'
m.write('/Users/jgaboardi/Desktop/CPLEX.lp')