'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing an Uncapacitated Fixed Charge 
#    facility location problem in Python/Gurobi[gurobipy]
'''
Adapted from:

Daskin, M. S. 
    1995 
    Network and Discrete Location: Models, Algorithms, and Applications
    Hoboken, NJ, USA
    John Wiley & Sons, Inc.

'''

import numpy as np
import gurobipy as gbp
import time
t1 = time.time()

def GbpCFLP():
    #     1. Read In (or Create) Data
    # CREATE
    # Distance Matrix
    dij = np.random.randint(10, 20, 25)
    dij = dij.reshape(5,5)
    # Demand Matrix
    hi = np.random.randint(25, 50, 5)
    #hi = hi.reshape(len(hi),1)
    # Demand Sum
    hiSum = np.sum(hi)
    # Cost per mile
    c = 1.25
    # Capacity
    kj = np.random.randint(100, 150, 5)
    kjSum = np.sum(kj)
    # Fixed Facility Cost
    Fj = np.random.randint(75, 100, 50)
    Fj = Fj.reshape(1,len(Fj))
    FjSum = np.sum(Fj)
    # Weighted Cost Coefficients for Decision Variables
    Sij = hi * dij
    
    client_nodes = range(len(Sij))
    service_nodes = range(len(Sij[0]))
    
    #       2. Create Model, Set MIP Focus, Add Variables, & Update Model
    mCFLP = gbp.Model(' -- UFLP -- ')
    # Set MIP Focus to 2 for optimality
    gbp.setParam('MIPFocus', 2)
    # Add Client Decision Variables
    client_var = []
    for orig in client_nodes:
        client_var.append([])
        for dest in service_nodes:
            client_var[orig].append(mCFLP.addVar(vtype=gbp.GRB.BINARY, 
                                                obj=dij[orig][dest],
                                                name='x'+str(orig+1)+'_'+str(dest+1)))
    # Add Service Decision Variables
    serv_var = []
    for dest in service_nodes:
        serv_var.append([])
        serv_var[dest].append(mCFLP.addVar(vtype=gbp.GRB.BINARY, 
                                        name='y'+str(dest+1)))
    # Update Model Variables
    mCFLP.update()       
    
    #       3. Set Objective Function
    mCFLP.setObjective(gbp.quicksum((Fj[0][dest]*serv_var[dest][0] + 
                            c * Sij[orig][dest]*client_var[orig][dest] 
                            for orig in client_nodes for dest in service_nodes)), 
                            gbp.GRB.MINIMIZE)
    
    #       4. Add Constraints
    #Add Assignment Constraints
    for orig in client_nodes:
        mCFLP.addConstr(gbp.quicksum(client_var[orig][dest] 
                            for dest in service_nodes) == 1)
    # Add Opening Constraints
    for dest in service_nodes:
        for orig in client_nodes:
            mCFLP.addConstr(serv_var[dest] - client_var[orig][dest] >= 0)
    
    # Add Capacity Constraint
    for dest in service_nodes:
        mCFLP.addConstr(gbp.quicksum(hi[dest]*client_var[orig][dest] 
                                        for orig in client_nodes) - 
                                        kj[dest]*serv_var[dest][0] <= 0)
    
    #       5. Optimize and Print Results
    try:
        mCFLP.optimize()
    except Exception as e:
        print '   ################################################################'
        print ' < ISSUE : ', e, ' >'
        print '   ################################################################'
    t2 = time.time()-t1
    print '**********************************************************************'
    selected = []
    for v in mCFLP.getVars():
        if 'x' in v.VarName:
            pass
        elif v.x > 0:
            var = '%s' % v.VarName
            selected.append(var)
            print '    |                                            ', var
    print '    | Selected Facility Locations --------------  ^^^^ '
    print '    | Candidate Facilities [p] ----------------- ', len(selected)
    print '    | Cost per miles [c] ----------------------- ', c
    val = mCFLP.objVal
    print '    | Objective Value (Total Facility Cost) ---- ', val
    print '    | Total Demand ----------------------------- ', hiSum
    print '    | Total Capacity --------------------------- ', kjSum
    print '    | Total Potential Fixed Cost --------------- ', FjSum
    avgh = float(mCFLP.objVal)/float(hiSum)
    print '    | Avg. Cost / Demand ----------------------- ', avgh
    avgF = float(mCFLP.objVal)/len(selected)
    print '    | Avg. Cost / Facility --------------------- ', avgF
    print '    | Real Time to Optimize (sec.) ------------- ', t2
    print '**********************************************************************'
    print 'Capacitated Fixed Charge Location Problem'
    mCFLP.write('path.lp')


try:
    GbpCFLP()
    print '\nJames Gaboardi, 2015'
except Exception as e:
    print '   ################################################################'
    print ' < ISSUE : ', e, ' >'
    print '   ################################################################'