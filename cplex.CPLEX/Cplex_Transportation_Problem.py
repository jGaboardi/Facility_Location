'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''
# Building and Optimizing The Transportation Problem in
#        Python/cplex.CPLEX
# Change dimensions of Cij and the Facility Constraint for varying
#        spatial extents

import numpy as np
import cplex as cp
import time
t1 = time.time()

#     1. Read In Data
Cij = np.array([4,5,4,10,6,3,3,5,8])
Cij = Cij.reshape(3,3)
rows, cols = Cij.shape
Si = np.array([100,130,140])
Si = Si.reshape(3,1)
Dj = np.array([150,100,120])
Dj = Dj.reshape(3,1)
client_nodes = range(len(Cij))

# Indices & Variable Names
nodes = len(Cij)
Nodes = range(len(Cij))
all_nodes = len(Cij) * len(Cij)
ALL_nodes = range(all_nodes)
x = 'x'
cli_var = []
for i in Nodes:
    for j in Nodes:
        temp = x + str(i+1) + '_' + str(j+1)
        cli_var.append(temp)
client_var = np.array(cli_var)
client_var = client_var.reshape(3,3)

#     2. Create Model and Add Variables
# Create Model
m = cp.Cplex()
# Problem Name
m.set_problem_name('\n -- The Transportation Problem -- ')
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
                        obj = [Cij[i][j] for i in Nodes for j in Nodes],
                        types = ['C'] * all_nodes)

#    3. Add Constraints 
#Add Supply Constraints
for orig in Nodes:       
    supply_constraints = cp.SparsePair(ind = [client_var[dest][orig] 
                                            for dest in Nodes],                           
                                            val = [1] * nodes)
    m.linear_constraints.add(lin_expr = [supply_constraints],                 
                                senses = ['E'], 
                                rhs = Si[orig]);

#Add Demand Constraints
for orig in Nodes:       
    demand_constraints = cp.SparsePair(ind = [client_var[orig][dest] 
                                            for dest in Nodes],                           
                                            val = [1] * nodes)
    m.linear_constraints.add(lin_expr = [demand_constraints],                 
                                senses = ['E'], 
                                rhs = Dj[orig]);

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
for f in cli_var:
    if (solution.get_values(f) >
        m.parameters.mip.tolerances.integrality.get()):
        print '    Facility %s is open and ships' % f, solution.get_values(f), 'units'  
    else:
        print '    Facility %s is closed' % f     
print '\n-----\nJames Gaboardi, 2015'
m.write('/path.lp')