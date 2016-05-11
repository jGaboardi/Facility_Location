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
t1 = time.time()

def Cplex_MaxCover(ai, Cij, p_facilities):


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



Hi = [1000, 1200, 1100, 1250]


client_nodes = range(len(Cij[0]))

# Indices & Variable Names
nodes = len(Cij)
Nodes = range(len(Cij))

    
    t1 = time.time()
    
    Cij = Cost_Matrix.reshape(client_vector,service_vector)    
    ai = Client_Weights.reshape(client_vector, 1)
    Sij = Cij * ai

    # Indices & Variable Names
    client_nodes = range(len(Sij))
    service_nodes = range(len(Sij[0]))

    all_nodes_len = len(Sij) * len(Sij[0])
    ALL_nodes_range = range(all_nodes_len)

    m = cp.Cplex()                                      # Create model
    m.parameters.emphasis.mip.set(2)                    # Set MIP emphasis ==> Optimal
    m.set_problem_type(m.problem_type.LP)               # Set problem type
    m.objective.set_sense(m.objective.sense.minimize)   # Objective        ==>  Minimize

    client_variable = []
    for orig in client_nodes:
            client_variable.append([])
            for dest in service_nodes:
                client_variable[orig].append('x'+str(orig+1)+'_'+str(dest+1))

    facility_variable = []
    for dest in service_nodes:
            facility_variable.append([])
            facility_variable[dest].append('y' + str(dest+1))

    # Add Client Decision Variables
    m.variables.add(names = [client_variable[i][j] for i in client_nodes 
                                                   for j in service_nodes],
                            obj = [Sij[i][j] for i in client_nodes 
                                             for j in service_nodes], 
                            lb = [0] * all_nodes_len, 
                            ub = [1] * all_nodes_len, 
                            types = ['B'] * all_nodes_len)
    # Add Service Decision Variable
    m.variables.add(names = [facility_variable[j][0] for j in service_nodes],
                            lb = [0] * len(Sij[0]), 
                            ub = [1] * len(Sij[0]), 
                            types = ['B'] * len(Sij[0]))




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
        print 'Solution status    = ' , solution.get_status(), ':',\
                                         solution.status[solution.get_status()]
        print 'Facilities [p]     = ' , p_facilities
        print 'Total Cost         = ' , round(solution.get_objective_value(),5)
        print 'Total Clients      = ' , ai.sum()
        print 'Real Time          = ' , t2, 'sec.'        
        print 'Matrix Shape       = ' , Sij.shape
        print '*******************************************************************'
        print '\n -- The Maximal Cover Location Problem -- CPLEX'
        print '          -- James Gaboardi, 2016 -- '

############################################################################################################  


# Data can be read-in or simulated
client_vector =  4             # Density of clients
service_vector = 3             # Density of service facilities
P = candidate_facilities = 1
Minimum_Distance =7.

# Client Weights
Client_Weights = np.random.randint(2, 
                                   20, 
                                   client_vector)

# Cost Matrix of random floats 
Cost_Matrix = np.random.uniform(10, 
                                30, 
                                client_vector*service_vector)

# Call Function
Cplex_pMedian(ai=Client_Weights,
                Cij=Cost_Matrix, 
                p_facilities=P,
                S=Minimum_Distance)
'''
James Gaboardi, 2016
'''