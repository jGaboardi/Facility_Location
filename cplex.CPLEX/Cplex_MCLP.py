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
    Church, R. L.
    C. ReVelle.
    1974.
    The Maximal Covering Location Problem. 
    Papers of the Regional Science Association.
    32:101-18.
'''
# Building and Optimizing a Maximum Cover Location Problem problem in 
#        Python/cplex.CPLEX

import numpy as np
import cplex as cp
import time
np.random.seed(352)

def Cplex_MaxCover(ai, Cij, p_facilities, S) :
    
    t1 = time.time()
    
    m = cp.Cplex()                                      # Create model
    m.parameters.emphasis.mip.set(2)                    # Set MIP emphasis ==> Optimal
    m.set_problem_type(m.problem_type.LP)               # Set problem type
    m.objective.set_sense(m.objective.sense.maximize)   # Objective        ==>  Minimize
    
    Cij = Cost_Matrix.reshape(client_vector,service_vector)    
    ai = Client_Weights.reshape(client_vector, 1)
    
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
       
    # Indices & Variable Names
    client_nodes = range(len(Cij))
    service_nodes = range(len(Cij[0]))

    all_nodes_len = len(Cij) * len(Cij[0])
    ALL_nodes_range = range(all_nodes_len)

    # Index for Serialized Variables      
    matrix_variable = [['x' + str(orig+100001) for orig in nodes_range]] * nodes_length      
    print matrix_variable 
    facility_variable = []
    for dest in service_nodes:
            facility_variable.append([])
            facility_variable[dest].append('y' + str(dest+1))

    # Add Client Decision Variables
    m.variables.add(names = [matrix_variable[0][i] for i in nodes_range],
                            obj = [ai[i][0] for i in nodes_range],
                            lb = [0] * nodes_length, 
                            ub = [1] * nodes_length, 
                            types = ['B'] * nodes_length)

    # Add Service Decision Variable
    m.variables.add(names = [facility_variable[j][0] for j in service_nodes],
                            lb = [0] * len(Cij[0]), 
                            ub = [1] * len(Cij[0]), 
                            types = ['B'] * len(Cij[0]))

    #Add Coverage Constraints
    for orig in nodes_range:
        coverage_constraints = ([matrix_variable[orig][dest] for dest in nodes_range]+
                                                [facility_variable[orig][0]],                           
                                                [Aij[orig][dest]for dest in nodes_range]+[1])
        m.linear_constraints.add(lin_expr = [coverage_constraints],                 
                                    senses = ['G'], 
                                    rhs = [0])
           
    # Add Facility Constraint
    facility_constraint = ([facility_variable[j][0] for j in service_nodes], 
                                        [1.0] * len(Cij[0]))
    m.linear_constraints.add(lin_expr = [facility_constraint],
                                    senses = ['L'],
                                    rhs = [p_facilities])

     # Optimize and Print Results
    m.solve()
    t2 = round(time.time()-t1, 5)
    m.write('path.lp')
    solution = m.solution
    print '*******************************************************************'
    for f in facility_variable:
        if solution.get_values(f[0]) > 0 :
            print 'Facility %s is open' % f[0]
    print '*******************************************************************'
    print 'Solution status                 = ' , solution.get_status(), ':',\
                                                solution.status[solution.get_status()]
    print 'Facilities [p]                  = ' , p_facilities
    print 'Minimum Distance for Cover (S)  = ' , S
    print 'Total Cost                      = ' , round(solution.get_objective_value(),5)
    print 'Total Clients                   = ' , ai.sum()
    print 'Real Time                       = ' , t2, 'sec.'        
    print 'Matrix Shape                    = ' , Cij.shape
    print '*******************************************************************'
    print '\n -- The Maximal Cover Location Problem -- CPLEX'
    print '          -- James Gaboardi, 2016 -- '

############################################################################################################  


# Data can be read-in or simulated
client_vector =  4             # Density of clients
service_vector = 4             # Density of service facilities
P = candidate_facilities = 1
Minimum_Distance =7.

# Client Weights
Client_Weights = np.random.randint(2, 
                                   10, 
                                   client_vector)

# Cost Matrix of random floats 
Cost_Matrix = np.random.randint(2, 
                                10, 
                                client_vector*service_vector)

# Call Function
Cplex_MaxCover(ai=Client_Weights,
                Cij=Cost_Matrix, 
                p_facilities=P,
                S=Minimum_Distance)
'''
James Gaboardi, 2016
'''