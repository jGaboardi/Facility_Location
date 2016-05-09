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
Adapted from:   
    Minieka, E.
    1970. 
    The m-Center Problem. 
    SIAM Review. 
    12:38–39.
'''

import cplex as cp
import numpy as np
import time
np.random.seed(352)

def Cplex_pCenter(Cij, p):
    t1 = time.time()

    m = cp.Cplex()                                      # Create model
    m.parameters.emphasis.mip.set(2)                    # Set MIP emphasis to Optimal
    m.set_problem_type(m.problem_type.LP)               # Set problem type
    m.objective.set_sense(m.objective.sense.minimize)   # Objective Function ==>  Minimize

    # Cost Matrix
    client_nodes = range(len(Cij))
    service_nodes = range(len(Cij[0]))
    all_nodes_len = len(Cij) * len(Cij[0])
    ALL_nodes_range = range(all_nodes_len)

    # Variable Indices
    W = 'W'
    client_variable = []
    for orig in client_nodes:
            client_variable.append([])
            for dest in service_nodes:
                client_variable[orig].append('x'+str(orig+1)+'_'+str(dest+1))
    facility_variable = []
    for dest in service_nodes:
            facility_variable.append([])
            facility_variable[dest].append('y' + str(dest+1))


    # Add Maximized Minimized Average Time Variable
    m.variables.add(names = W,
                    obj = [1],
                    lb = [0],
                    ub = [cp.infinity],
                    types = ['C'])
    # Add Client Decision Variables
    m.variables.add(names = [client_variable[i][j] for i in client_nodes 
                                                   for j in service_nodes], 
                            lb = [0] * all_nodes_len, 
                            ub = [1] * all_nodes_len, 
                            types = ['B'] * all_nodes_len)
    # Add Service Decision Variable
    m.variables.add(names = [facility_variable[j][0] for j in service_nodes],
                            lb = [0] * len(Cij[0]), 
                            ub = [1] * len(Cij[0]), 
                            types = ['B'] * len(Cij[0]))

    # Add Assignment Constraints
    for orig in client_nodes:       
        assignment_constraints = ([client_variable[orig][dest] 
                                                for dest in service_nodes],                           
                                                [1] * len(Cij[0]))
        m.linear_constraints.add(lin_expr = [assignment_constraints],                 
                                    senses = ['E'], 
                                    rhs = [1]);
    # Add Facility Constraint
    facility_constraint = ([facility_variable[j][0] for j in service_nodes], 
                                        [1.0] * len(Cij[0]))
    m.linear_constraints.add(lin_expr = [facility_constraint],
                                    senses = ['E'],
                                    rhs = [p])
    # Add Opening Constraint
    OC = [[client_variable[i][j]] + [facility_variable[j][0]] 
                                    for i in client_nodes 
                                    for j in service_nodes]
    for oc in OC:
        opening_constraints = (oc, [-1.0, 1.0])
        m.linear_constraints.add(lin_expr = [opening_constraints], 
                                    senses = ['G'], 
                                    rhs = [0])
    # Add Maximized Minimized Average Time Constraint
    MC = [[],[]]
    for i in client_nodes:
        MC[0].append([client_variable[i][j] for j in service_nodes] + [W])
        MC[1].append([Cij[i][j] for j in service_nodes] + [-1])
    for i in client_nodes:   
        max_constraints = [MC[0][i], MC[1][i]]                            
        m.linear_constraints.add(lin_expr = [max_constraints],                 
                                    senses = ['L'], 
                                    rhs = [0])
                                    
    # Optimize
    m.solve()
    m.write('path.lp')
    t2 = time.time()-t1
    solution = m.solution

    # Display solution.
    print '\n\n****************************************************************'
    for each_facility in facility_variable:
        if solution.get_values(each_facility[0]) > 0 :
            print 'Facility %s is open' % each_facility[0]
    print '****************************************************************'
    print 'Solution status       = ', solution.get_status(), ':', \
                                                    solution.status[solution.get_status()]
    print 'Total cost            = ', solution.get_objective_value()
    print 'Candidate Facilities  = ', p
    print 'Real Time             = ', t2/60, 'min.'        
    print 'Matrix Size           = ', Cij.shape
    print '****************************************************************'
    print '    -- The p-Center Problem CPLEX -- '
    print '    --    James Gaboardi, 2016    -- '
########################################################   

 # Cost Matrix
Cost_Matrix = np.random.uniform(1, 10, 9)
Cost_Matrix = Cost_Matrix.reshape(3,3)

p_facilities = 1

Cplex_pCenter(Cij=Cost_Matrix, p=p_facilities)