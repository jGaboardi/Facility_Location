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
    M. J. Kuby. 
    1988. 
    Programming models for facility dispersion: the p-dispersion 
            and maxisum dispersion problems. 
    Mathematical and Computer Modelling. 
    10 (4):316-329.
'''

# Maximizing the minimum distance bewteen facilities (generally noxious)

# Terminology & General Background for Facility Location and Summation Notation:

#   *   [i][j] - matrix dimensions
#   *   [dij] - matrix of travel costs between nodes
#   *   [M] - largest value in dij
#   *   [D] - Maximized minimum distance between facilities
#   *	[yi] - each service facility
#   *   [p] - the number of facilities to be sited


# Imports
import numpy as np
import cplex as cp
import time
np.random.seed(352)

def CplexPDisp(dij, p_facilities, total_facilities):
    
    t1 = time.time()
    
    m = cp.Cplex()                                      # Create model
    m.parameters.emphasis.mip.set(2)                    # Set MIP emphasis to '2' --> Optimal
    m.set_problem_type(m.problem_type.LP)               # Set problem type
    m.objective.set_sense(m.objective.sense.maximize)   # Objective Function Sense  ==>  Maximize

    # Service Nodes
    service_nodes = range(total_facilities)
    all_nodes_len = total_facilities * total_facilities
    ALL_nodes_range = range(all_nodes_len)
    
    # Max Value in dij
    M = np.amax(dij)
    
    #  Add Variables        
    fac_var = []
    for dest in service_nodes:
        fac_var.append([])
        fac_var[dest].append('y' + str(dest+1))
    
    # Add Maximized Minimum Variable
    D = 'D'
    m.variables.add(names = D,
                        obj = [1],
                        lb = [0],
                        ub = [cp.infinity],
                        types = ['C'])
    
    # Add Facility Decision Variables
    m.variables.add(names = [fac_var[j][0] for j in service_nodes],
                        lb = [0] * total_facilities, 
                        ub = [1] * total_facilities, 
                        types = ['B'] * total_facilities)
    
    # Add Facility Constraint
    facility_constraint = cp.SparsePair(ind = [fac_var[j][0] for j in service_nodes], 
                                    val = [1.0] * total_facilities)
    m.linear_constraints.add(lin_expr = [facility_constraint],
                                senses = ['E'],
                                rhs = [p_facilities])
    
    # Add Inter-Facility Distance Constraints   n(n-1)/2
    ind_val_rhs = [[],[],[]]
    for orig in service_nodes:
        for dest in service_nodes:
            if dest > orig:
                ind_val_rhs[0].append([fac_var[orig][0]] + [fac_var[dest][0]] + [D])
                ind_val_rhs[1].append([-M] + [-M] + [-1.0])
                ind_val_rhs[2].append(-2*M - dij[orig][dest])
            else:
                pass

    for i in range(len(ind_val_rhs[0])):
        #print i
        inter_facility_constraints = ind_val_rhs[0][i], ind_val_rhs[1][i]
        m.linear_constraints.add(lin_expr = [inter_facility_constraints],                 
                                senses = ['G'], 
                                rhs = [ind_val_rhs[2][i]])

    #     6. Optimize and Print Results
    
    m.write('/Users/jgaboardi/Desktop/pathCPLEX.lp')
    m.solve()
    solution = m.solution
    t2 = round(time.time()-t1, 3)/60
        
    print '\n**********************************************************************'
    selected = []
    for f in fac_var:
        if solution.get_values(f[0]) > 0 :
            selected.append(f)
            print ' Facility %s is open' % f[0],'                            ', f
    print '**********************************************************************'
    print 'Largest Value in dij (M)     = ', M
    print 'Objective Value (D)          = ', solution.get_objective_value()
    print 'Matrix Dimensions            = ', dij.shape
    print 'Real Time to Solve (minutes) = ', t2
    print 'Solution status              = ' , solution.get_status(), ':', solution.status[solution.get_status()]
    print '****************************'
    print '    -- The p-Dispersion Problem CPLEX -- '
    print '\n    -- James Gaboardi, 2016 -- '
##########################################################################
# Data can be read-in or simulated

#  Total Number of Facilities  
Service = matrix_vector = 200       # matrix_vector * matrix_vector for total facilities

# Candidate Facilities
P = candidate_facilities = 2

# Cost Matrix
Cost_Matrix = np.random.randint(3, 
                                50, 
                                matrix_vector*matrix_vector)
Cost_Matrix = Cost_Matrix.reshape(matrix_vector,matrix_vector)

# Call Function   
CplexPDisp(
            dij=Cost_Matrix, 
            p_facilities=P, 
            total_facilities=Service)


'''
James Gaboardi, 2016
'''
