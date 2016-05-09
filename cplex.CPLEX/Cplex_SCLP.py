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
    
    m = cp.Cplex()                                      # Create model
    m.set_problem_name('\n -- Set Cover Location Problem -- ')
    m.parameters.emphasis.mip.set(2)                    # Set MIP emphasis to Optimal
    m.set_problem_type(m.problem_type.LP)               # Set problem type
    m.objective.set_sense(m.objective.sense.minimize)   # Objective Function ==>  Minimize
    
    # Is the value of Cij within S?
    Aij = []
    for i in Cij:
        for j in i:
            if j <= S:
                outtext = 1
            else:
                outtext = 0
            Aij.append(outtext)
    rows, cols = Cij.shape
    
    Aij = np.array(Aij)
    Aij = Aij.reshape(rows,cols)

    # Indices & Variable Names
    nodes_length = len(Cij)
    nodes_range = range(len(Cij))
    
    # Index for Serialized Variables      
    matrix_variable = [['x' + str(orig+100001) for orig in nodes_range]] * nodes_length      
    
    # Add Client Decision Variables
    m.variables.add(names = [matrix_variable[0][i] for i in nodes_range],
                            obj = [1] * nodes_length,
                            lb = [0] * nodes_length, 
                            ub = [1] * nodes_length, 
                            types = ['B'] * nodes_length)

    
    #    3. Add Constraints 
    #Add Coverage Constraints
    for orig in nodes_range:       
        coverage_constraints = ([matrix_variable[orig][dest] for dest in nodes_range],                           
                                                [Aij[orig][dest]for dest in nodes_range])
        m.linear_constraints.add(lin_expr = [coverage_constraints],                 
                                    senses = ['G'], 
                                    rhs = [1])

    #    4. Optimize and Print Results
    m.solve()
    solution = m.solution
    

    print 'Total cost = ' , solution.get_objective_value()
    print 'Determination Time = ', m.get_dettime(), 'ticks'
    print 'Real Time to Optimize (sec.): *', time.time()-t1
    print '*********************************************'
    for f in matrix_variable[0]:
        if (solution.get_values(f) >
            m.parameters.mip.tolerances.integrality.get()):
            print '    Facility %s is open' % f
        else:
            print '    Facility %s is closed' % f        
    print '*********************************************'
    print '\n-----\nJames Gaboardi, 2015'
    m.write('path.lp')
    
########################################################   

 # Cost Matrix
Sites = 8

Cost_Matrix = np.random.uniform(1, 20, Sites*Sites)
Cost_Matrix = Cost_Matrix.reshape(Sites,Sites)

Minimum_Distance =7.

Cplex_SetCover(Cij=Cost_Matrix, S=Minimum_Distance)    
'''
James Gaboardi, 2016
'''