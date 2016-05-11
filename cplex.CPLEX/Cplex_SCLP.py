#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''
'''
Originally Published:
    Toregas, C.
    ReVelle, Charles.
    1972.
    Optimal Location Under Time or Distance Constraints.
    Papers of the Regional Science Association.
    28(1):133 - 144. 
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
                Aij.append(1)
            else:
                Aij.append(0)
    Aij = np.array(Aij)
    Aij = Aij.reshape(Cij.shape)

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
     
    #Add Coverage Constraints
    for orig in nodes_range:       
        coverage_constraints = ([matrix_variable[orig][dest] for dest in nodes_range],                           
                                                [Aij[orig][dest]for dest in nodes_range])
        m.linear_constraints.add(lin_expr = [coverage_constraints],                 
                                    senses = ['G'], 
                                    rhs = [1])

    #  Optimize and Print Results
    m.solve()
    t2 = time.time()-t1
    solution = m.solution

    print 'Total cost = ' , solution.get_objective_value()
    print 'Determination Time = ', m.get_dettime(), 'ticks'
    print 'Real Time to Optimize (sec.): *', time.time()-t1
    print '*******************************************************'
    Open_Facilities = []
    for f in matrix_variable[0]:
        if solution.get_values(f) > 0 :
            print 'Facility %s is open' % f
            Open_Facilities.append(f[0])
        else:
            print 'Facility %s is closed' % f       
    print '*******************************************************'
    print 'Density of Facilities to Cover All Demand = ', len(Open_Facilities)
    print 'Minimum Distance for Cover (S)            = ', S
    print 'Solution Time (minutes)                   = ', round(t2/60, 5)
    print '*******************************************************'
    print '    -- The Set Cover Location Problem CPLEX -- '
    print '    --         James Gaboardi, 2016         -- '
    m.write('path.lp')
    
########################################################   

 # Cost Matrix
Sites = 20

Cost_Matrix = np.random.uniform(1, 20, Sites*Sites)
Cost_Matrix = Cost_Matrix.reshape(Sites,Sites)

Minimum_Distance =7.

Cplex_SetCover(Cij=Cost_Matrix, S=Minimum_Distance)    
'''
James Gaboardi, 2016
'''