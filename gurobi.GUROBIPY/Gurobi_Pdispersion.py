'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing a p-Dispersion facility location problem in 
#        Python/Gurobi[gurobipy]
#
# Maximizing the minimum distance bewteen facilities (generally noxious)

# Terminology & General Background for Facility Location and Summation Notation:

#   *   The objective of the p-Dispersion Facility Location Problem is to 
#        maximize the minimum distance bewteen facilities (generally noxious).

#   *   [i] - a specific origin
#   *   [j] - a specifc destination
#   *   [n] - the set of origins
#   *   [m] - the set of destinations
#   *   [dij] - matrix of travel costs between nodes
#   *   [M] - largest value in dij
#   *   [D] - Maximized minimum distance between facilities
#   *	[yi] - each service facility
#   *   [p] - the number of facilities to be sited


#    1. Imports and Data Creation
# Imports
import pysal as ps
import numpy as np
import gurobipy as gbp
# Distance Matrix --> 20x20
dij = np.random.randint(100, 1000, 400)
dij = dij.reshape(20,20)
# Service Nodes
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
                                ub = 1,
                                name='y'+str(dest+1)))
# Add Maximized Minimum Variable
D = mPDP.addVar(vtype=gbp.GRB.CONTINUOUS,
            name='D')
# Update Model Variables
mPDP.update()       

#     4. Set Objective Function
mPDP.setObjective(D, gbp.GRB.MAXIMIZE)

#     5. Add Constriants
# Add Facility Constraint  [p=2]
mPDP.addConstr(gbp.quicksum(serv_var[dest] for dest in service_nodes) == 2,
                    'Facility_Constraint')                        
# Add Inter-Facility Distance Constraints   n(n-1)/2
counter=0
for orig in service_nodes:
    for dest in service_nodes:
        if dest > orig:
            counter = counter+1
            mPDP.addConstr(
            dij[orig][dest]+M*2-M*serv_var[orig]-M*serv_var[dest]-D>=0,
                    'Inter-Fac_Dist_Constraint_%i' % counter)
        else:
            pass

#     6. Optimize and Print Results
mPDP.optimize()
mPDP.write('/path.lp')
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
print '**********************************************************************'
print '\nJames Gaboardi, 2015'