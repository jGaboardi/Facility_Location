# -*- coding: utf-8 -*-
# Anti Cover 2 Facility Location Problem
# This script creates a linear programming file to be read into an optimizer.
'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''
# Developed by:  James D. Gaboardi, MSGIS
#                08/2015
#                © James Gaboardi


# The ACLP2 maximizes the number of service facilities to be sited
#       while minimum separation distance is constrained.

#    1. Imports
# Other imports may be necessary for matrix creation and manipulation
import numpy as np


#    2. Defined Functions
# Objective Function
def anti_cover_2_objective_function():
    outtext = ' obj: '
    for i in range(1, cols + 1):
        temp = ''
        temp += 'x'+str(i)
        outtext += temp + ' + '
    outtext = outtext[:-2]
    return outtext

#Add Adjacency Pairwise Constraints
def adjacency_pairwise_constraints():    
    outtext = ''
    temp = ''
    for i in range(rows):
        for j in range(cols):
            if i != j and Dij[i][j] < r:
                temp += 'x'+str(i) + ' + '+ 'x' + str(j) + ' <= 1\n'
            else:
                pass
        outtext += temp
    return outtext
    
'''    
    for orig in service_nodes:
        for dest in service_nodes:
            if orig != dest and Dij[orig][dest] < r:
                m.addConstr((serv_var[orig] + serv_var[dest]  <= 1))    
            else:
                pass
'''


# Declaration of Binaries
def anti_cover_2_binaries():
    outtext = ''
    for i in range(1, rows + 1):
        temp = ''
        temp += ' x' + str(i) 
        outtext += temp 
    return outtext

# Declaration of Bounds
def get_bounds_facility():
    outtext = ''
    for i in range(rows):
        outtext += ' 0 <= x' + str(i+1) + ' <= 1\n' 
    return outtext

#    3. DATA Creation & VARIABLE DECLARATION
# Cost Matrix
Dij = np.random.randint(1, 20, 16)
Dij = Dij.reshape(4,4)
# Minimum Separation Distance
r = 6
service_nodes = range(len(Dij))
rows, cols = Dij.shape


#    4. START TEXT FOR .lp FILE
# Declaration of Objective Function
text = "Anti Cover 2 Location Problem\n"
text += "'''\n"
text += 'Maximize\n'
text += anti_cover_2_objective_function()
text += '\n'
# Declaration of Constraints
text += 'Subject To\n'
text += adjacency_pairwise_constraints()
text += '\n'
# Declaration of Bounds
text += 'Bounds\n'
text += get_bounds_facility()
text += '\n'
# Declaration of Decision Variables form: Binaries
text += 'Binaries\n'
text += anti_cover_2_binaries()
text += '\n'
text += 'End\n'
text += "'''\n"
text += "© James Gaboardi, 2015"


#   5. CREATE & WRITE .lp FILE TO DISK
# Fill path name  --  File name must not have spaces.
outfile = open('LP.lp', 'w')
outfile.write(text)
outfile.close()