'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing a Set Cover Location Problem problem in 
#        Python/cplex.CPLEX

import numpy as np
import cplex as cp
import time
np.random.seed(352)

def Cplex_SetCover(Cij, S):
    t1 = time.time()
    
    # 
    Aij = []
    print Aij
    for i in Cij:
        for j in Cij:
            if j <= S:
                outtext = 1
            else:
                outtext = 0
            Aij.append(outtext)
    
    Cij = np.array(Cij)
    Cij = Cij.reshape(4,4)
    rows, cols = Cij.shape
    
    Aij = np.array(Aij)
    Aij = Aij.reshape(4,4)
    
    client_nodes = range(len(Cij[0]))

    # Indices & Variable Names
    nodes = len(Cij)
    Nodes = range(len(Cij))
    all_nodes = len(Cij) * len(Cij)
    ALL_nodes = range(all_nodes)
    x = 'x'
    cli_var = []
    for i in Nodes:
        for j in Nodes:
            temp = x + str(j+1)
            cli_var.append(temp)
    client_var = np.array(cli_var)
    client_var = client_var.reshape(4,4)
    results_var = []
    for i in Nodes:
        temp = x + str(i+1)
        results_var.append(temp)

    #     2. Create Model and Add Variables
    # Create Model
    m = cp.Cplex()
    # Problem Name
    m.set_problem_name('\n -- Set Cover Location Problem -- ')
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
    m.variables.add(names = [cli_var[i] for i in Nodes],  
                            obj = [1] * nodes,
                            lb = [0] * nodes, 
                            ub = [1] * nodes, 
                            types = ['B'] * nodes)

    #    3. Add Constraints 
    #Add Coverage Constraints
    for orig in Nodes:       
        coverage_constraints = cp.SparsePair(ind = [client_var[orig][dest] 
                                                for dest in Nodes],                           
                                                val = [Aij[orig][dest]for dest in Nodes])
        m.linear_constraints.add(lin_expr = [coverage_constraints],                 
                                    senses = ['G'], 
                                    rhs = [1]);

    #    4. Optimize and Print Results
    m.solve()
    solution = m.solution
    
    
    
    print 'Total cost = ' , solution.get_objective_value()
    print 'Determination Time = ', m.get_dettime(), 'ticks'
    print 'Real Time to Optimize (sec.): *', time.time()-t1
    print '****************************'
    for f in results_var:
        if (solution.get_values(f) >
            m.parameters.mip.tolerances.integrality.get()):
            print '    Facility %s is open' % f
        else:
            print '    Facility %s is closed' % f        
    print '****************************'
    print '\n-----\nJames Gaboardi, 2015'
    m.write('/path.lp')
    
########################################################   

 # Cost Matrix
Sites = 8

Cost_Matrix = np.random.uniform(1, 10, Sites*Sites)
Cost_Matrix = Cost_Matrix.reshape(Sites,Sites)
print Cost_Matrix
Minimum_Distance = 4

Cplex_SetCover(Cij=Cost_Matrix, S=Minimum_Distance)    
