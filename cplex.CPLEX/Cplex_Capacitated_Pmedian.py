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
    S. L. Hakimi. 
    1964. 
    Optimum Locations of Switching Centers and 
                    the Absolute Centers and Medians of a Graph. 
    Operations Research. 
    12 (3):450-459.
'''

# Building and Optimizing a p-Median facility location problem
#        in Python/cplex.CPLEX

import numpy as np
import cplex as cp
import time
np.random.seed(352)

def Cplex_pMedian_Capacitated(dij, qi, Qy, p_facilities):
    
    t1 = time.time()
    
    dij = Cost_Matrix.reshape(client_vector,service_vector)    
    
    # Indices & Variable Names
    client_nodes = range(len(dij))
    service_nodes = range(len(dij[0]))

    all_nodes_len = len(dij) * len(dij[0])
    ALL_nodes_range = range(all_nodes_len)

    m = cp.Cplex()                                      # Create model
    m.parameters.emphasis.mip.set(2)                    # Set MIP emphasis ==> Optimal
    m.set_problem_type(m.problem_type.LP)               # Set problem type
    m.objective.set_sense(m.objective.sense.minimize)   # Objective        ==>  Minimize

    client_var = []
    for orig in client_nodes:
            client_var.append([])
            for dest in service_nodes:
                client_var[orig].append('x'+str(orig+1)+'_'+str(dest+1))

    fac_var = []
    for dest in service_nodes:
            fac_var.append([])
            fac_var[dest].append('y' + str(dest+1))

    # Add Client Decision Variables
    m.variables.add(names = [client_var[i][j] for i in client_nodes 
                                              for j in service_nodes],
                            obj = [dij[i][j] for i in client_nodes 
                                             for j in service_nodes], 
                            lb = [0] * all_nodes_len, 
                            ub = [1] * all_nodes_len, 
                            types = ['B'] * all_nodes_len)
    
    # Add Service Decision Variable
    m.variables.add(names = [fac_var[j][0] for j in service_nodes],
                            lb = [0] * len(dij[0]), 
                            ub = [1] * len(dij[0]), 
                            types = ['B'] * len(dij[0]))

    # Add Assignment Constraints
    for orig in client_nodes:       
        assignment_constraints = ([client_var[orig][dest] 
                                                for dest in service_nodes],                           
                                                [1] * len(dij[0]))
        m.linear_constraints.add(lin_expr = [assignment_constraints],                 
                                    senses = ['E'], 
                                    rhs = [1])
    # Add Facility Constraint
    facility_constraint = cp.SparsePair(ind = [fac_var[j][0] for j in service_nodes], 
                                        val = [1.0] * len(dij[0]))
    m.linear_constraints.add(lin_expr = [facility_constraint],
                                    senses = ['E'],
                                    rhs = [p_facilities])
    
    # Add Opening Constraints
    OC = [[client_var[i][j]] + [fac_var[j][0]] for i in client_nodes 
                                               for j in service_nodes]
    for oc in OC:
        opening_constraints = [oc, [-1.0, 1.0]]
        m.linear_constraints.add(lin_expr = [opening_constraints], 
                                    senses = ['G'], 
                                    rhs = [0])
    # Add Capacity Constraints                
    for dest in service_nodes:       
        capacity_constraints = ([client_var[orig][dest] for orig in client_nodes],                           
                                 [qi[orig] for orig in client_nodes])
        m.linear_constraints.add(lin_expr = [capacity_constraints],                 
                                    senses = ['L'], 
                                    rhs = [Qy[dest]])
    
    # Optimize and Print Results
    m.solve()
    t2 = round(time.time()-t1, 5)
    m.write('path.lp')
    solution = m.solution
    print '*******************************************************************'
    for f in fac_var:
        if solution.get_values(f[0]) > 0 :
            print 'Facility %s is open' % f[0]
    print '*******************************************************************'
    print 'Solution status    = ' , solution.get_status(), ':',\
                                     solution.status[solution.get_status()]
    print 'Facilities [p]     = ' , p_facilities
    print 'Total Cost         = ' , round(solution.get_objective_value(),5)
    print 'Total Clients      = ' , qi.sum()
    print 'Total Capacity     = ' , Qy.sum()
    print 'Real Time          = ' , t2, 'sec.'        
    print 'Matrix Shape       = ' , dij.shape
    print '*******************************************************************'
    print '\n -- The p-Median Problem -- CPLEX'
    print ' James Gaboardi, 2016'

############################################################################################################  
    
# Data can be read-in or simulated
client_vector =  10             # Density of clients
service_vector = 4              # Density of service facilities
P = candidate_facilities = 2

# Client Weights
Client_Weights = np.random.randint(5, 
                                   10, 
                                   client_vector)

# Capacity
Capacity = np.random.randint(50, 
                             65, 
                             service_vector)

# Cost Matrix of random floats 
Cost_Matrix = np.random.uniform(10, 
                                30, 
                                client_vector*service_vector)

# Call Function
Cplex_pMedian_Capacitated(dij=Cost_Matrix,
                qi=Client_Weights,
                Qy=Capacity,
                p_facilities=P)
'''
James Gaboardi, 2016
'''