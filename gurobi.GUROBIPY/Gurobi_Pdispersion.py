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
import gurobipy as gbp
import time
np.random.seed(352)

def GbpPDisp(dij, p_facilities, total_facilities):
    
    t1 = time.time()
    
    service_nodes = range(len(dij))
    # Max Value in dij
    M = np.amax(dij)
    
    #     2. Create Model, Set MIP Focus, Add Variables, & Update Model
    mPDP = gbp.Model(" -- p-Dispersion -- ")
    # Set MIP Focus to 2 for optimality
    gbp.setParam('MIPFocus', 2)
    
    #     3. Add Variables
    # Add Decision Variables
    serv_var = []
    for dest in service_nodes:
        serv_var.append(mPDP.addVar(vtype=gbp.GRB.BINARY,
                                    lb = 0,
                                    ub = 1,
                                    name='y'+str(dest+1)))
    # Add Maximized Minimum Variable
    D = mPDP.addVar(vtype=gbp.GRB.CONTINUOUS,
                                    lb = 0,
                                    ub = gbp.GRB.INFINITY,
                                    name='D')
    
    # Update Model Variables
    mPDP.update()       
    
    #     4. Set Objective Function
    mPDP.setObjective(D, gbp.GRB.MAXIMIZE)
    
    #     5. Add Constriants
    # Add Facility Constraint  [p=2]
    mPDP.addConstr(gbp.quicksum(serv_var[dest] for dest in service_nodes) == p_facilities)                        
    
    # Add Inter-Facility Distance Constraints   n(n-1)/2
    for orig in service_nodes:
        for dest in service_nodes:
            if dest > orig:
                mPDP.addConstr(
                dij[orig][dest] + M*2 -M*serv_var[orig] -M*serv_var[dest] -D >= 0)
            else:
                pass
    
   
    #     6. Optimize and Print Results
    mPDP.optimize()
    mPDP.write('path.lp')
    t2 = round(time.time()-t1, 3)/60
    print '\n**********************************************************************'
    selected = []
    for v in mPDP.getVars():
        if 'D' in v.VarName:
            pass
        elif v.x > 0:
            var = '%s' % v.VarName
            selected.append(var)
            print '    |                                            ', var
    print '    | Selected Facility Locations -------------  ^^^^ '
    print '    | Candidate Facilities [p] ---------------- ', len(selected)
    print '    | Largest Value in dij (M) ---------------- ', M
    print '    | Objective Value (D) --------------------- ', mPDP.objVal
    print '    | Matrix Dimensions ----------------------- ', dij.shape
    print '    | Real Time to Solve (minutes)------------- ', t2
    print '**********************************************************************'
    print '    -- The p-Dispersion Problem Gurobi -- '
    print '\n    -- James Gaboardi, 2016 -- '
###################################################
# Data can be read-in or simulated

#  Total Number of Facilities  
Service = matrix_vector = 200       # matrix_vector * matrix_vector for total facilities

P = candidate_facilities = 2

# Cost Matrix
Cost_Matrix = np.random.randint(3, 
                                50, 
                                matrix_vector*matrix_vector)
Cost_Matrix = Cost_Matrix.reshape(matrix_vector,matrix_vector)

# Call Function   
GbpPDisp(
        dij=Cost_Matrix, 
        p_facilities=P, 
        total_facilities=Service)

'''
James Gaboardi, 2015
'''
