# -*- coding: utf-8 -*-
#Uncapacitated Fixed-charge Facility Location Problem

#This script creates a linear programming file to be read into an optimizer.
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

#   Terminology & General Background for 
#            Facility Location and Summation Notation:

#   *        The objective of the Uncapacitated Fixed-Charge Facility Location 
#                Problem is to minimize the cost to serve clients and the
#                number of facilities to serve clients.

#   *   [i] - a specific origin
#   *   [j] - a specifc destination
#   *   [n] - the set of origins
#   *   [m] - the set of destinations
#   *   [hi] - demand at each node (usually population)
#   *   [Fj] - cost to site a facility at each candidate location
#   *   [dij] - travel costs between nodes
#   *   [Sij] - weighted travel costs [(hi)(dij)]
#   *   [x#_#] - the decision variable in # row, # column position in the matrix
#   *	[y#] - service facility in the # row
#   *   [p] - the number of facilities to be sited


#    1. IMPORTS
# Other imports may be necessary for matrix creation and manipulation 
import numpy as np


#    2. DEFINED FUNCTIONS
# Objective Function 
# The objective of this function is to minimize the average travel cost along the network.
# *** Minimize(Z)
def get_objective_function_UFLP():
    outtext = ' obj: '
    for i in range(rows):
        temp1 = ''
        for j in range(cols):
            temp1 += str(c*Sij[i,j]) + ' x' + str(i+1) + '_' + str(j+1) + ' + '
        outtext += temp1 + ' \n'
    for j in range(cols):
        temp2 = ''
        temp2 += str(fj[j,0]) +  ' y' + str(j+1) + ' + '
        outtext += temp2
    outtext = outtext[:-4] + ' \n'
    return outtext

# Assignment Constraints
# This indicates a client can only be served by one facility.
# Each column in the matrix must equal 1.
def get_assignment_constraints():
    counter = 0
    outtext = ''
    for i in range(1,cols+1):
        counter = counter + 1
        temp = ' c' + str(counter) + ':  '
        for j in range(1,rows+1):
            temp += 'x' + str(i) + '_' + str(j) + ' + '
        outtext += temp[:-2] + '= 1\n'
    return outtext

# Opening Constraints
def get_opening_constraints_UFLP():
    counter = 5
    outtext = ''
    for i in range(1, rows+1):
        for j in range(1, cols+1):
            counter = counter + 1 
            outtext += ' c' + str(counter) + ':  - x' + str(j) + '_' + str(i) + ' + ' + 'y' + str(i) +  ' >= 0\n'
    return outtext

# Declaration of Bounds
def get_bounds_allocation():
    outtext = ''
    for i in range(rows):
        temp = ''
        for j in range(cols):
            temp += ' 0 <= x' + str(i+1) + '_' + str(j+1) + ' <= 1\n'
        outtext += temp    
    return outtext

def get_bounds_facility():
    outtext = ''
    for i in range(rows):
        outtext += ' 0 <= y' + str(i+1) + ' <= 1\n'
    return outtext

# Declaration of Decision Variables (form can be: Binary, Integer, etc.)
# In this case decision variables are binary.
def get_allocation_decision_variables_UFLP():
    outtext = ''
    for i in range(1, rows+1):
        temp = ''
        for j in range(1, cols+1):
            temp += ' x' + str(i) + '_' + str(j) + ' '
        outtext += temp
    return outtext
    
def get_facility_decision_variables_UFLP():  
    outtext = ''
    for i in range (1, rows+1):
        outtext += ' y' + str(i) + ' '
    return outtext
 
    
#    3. DATA Creation & VARIABLE DECLARATION
hi = np.random.randint(1, 20, 5)
hi = hi.reshape(5, 1)
fj = np.random.randint(30, 50, 5)
fj = fj.reshape(5, 1)
dij = np.random.randint(1, 50, 25)
dij = dij.reshape(5, 5)
c = 1.25
Sij = hi * dij
rows, cols = Sij.shape

#    4. START TEXT FOR .lp FILE
# Declaration of Objective Function
text = "Uncapacitated Fixed-Charge Facility Location Problem\n"
text += "'''\n"
text += 'Minimize\n'          
text += get_objective_function_UFLP()
# Declaration of Constraints
text += 'Subject To\n'                    
text += get_assignment_constraints()
text += get_opening_constraints_UFLP()
# Declaration of Bounds
text += 'Bounds\n' 
text += get_bounds_allocation()
text += get_bounds_facility()
# Declaration of Decision Variables form: Binaries
text += 'Binaries\n'
text += get_allocation_decision_variables_UFLP()
text += get_facility_decision_variables_UFLP()
text += '\n'
text += 'End\n'
text += "'''\n"
text += "© James Gaboardi, 2015"                


#   5. CREATE & WRITE .lp FILE TO DISK
# Fill path name  --  File name must not have spaces.
outfile = open('/Users/jgaboardi/Desktop/LP.lp', 'w')
outfile.write(text)
outfile.close()