# -*- coding: utf-8 -*-
#p-Maxian Facility Location Problem

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


#   Terminology & General Background for Facility Location and 
#        Summation Notation:

#   *        The objective of the p-Maxianian Facility Location Problem is to 
#            maximize the total weighted travel cost between service facilities
#            and clients while siting p facilitied.

#   *   [i] - a specific origin
#   *   [j] - a specifc destination
#   *   [n] - the set of origins
#   *   [m] - the set of destinations
#   *   [Ai] - weight at each node (usually population)
#   *   [Cij] - travel costs between nodes
#   *   [Sij] - weighted travel costs [(Ai)(Cij)]
#   *   [Z] - the sum of the weighted travel costs between all origins and 
#                    destinations multiplied by the decision variables 
#   *   [x#_#] - the decision variable in # row, # column position in the matrix
#   *	[y#] - service facility in the # row
#   *   [p] - the number of facilities to be sited


#    1. IMPORTS
# Other imports may be necessary for matrix creation and manipulation 
import numpy as np


#    2. DEFINED FUNCTIONS
# Objective Function 
# The objective of this function is to maximize the total weighted travel 
#    cost along the network.
# *** Maximize(Z)
def get_objective_function_p_maxian(Sij):
    outtext = ' obj: '
    for i in range(rows):
        temp = ''
        for j in range(cols):
            temp += str(Sij[i,j]) + ' x' + str(i+1) + '_' + str(j+1) + ' + '
        outtext += temp + ' \n'
    outtext = outtext[:-4] + ' \n'
    return outtext

# Assignment Constraints
# This indicates a client can only be served by one facility.
# Each column in the matrix must equal 1.
def get_assignment_constraints(rows):
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
def get_opening_constraints_p_maxian(Sij):
    counter = 5
    outtext = ''
    for i in range(1, rows+1):
        for j in range(1, cols+1):
            counter = counter + 1 
            outtext += ' c' + str(counter) + ':  - x' + str(j) + '_' + str(i) + ' + ' + 'y' + str(i) +  ' >= 0\n'
    return outtext

# Facility Constraint
# Indicate how many facilties will be sited in 'outtext' below.
# *** '= 1\n' indicates 1 facility
def get_p_facilities(rows):
    outtext = ''
    for i in range(1, rows+1):
        temp = ''
        temp += 'y' + str(i)
        outtext += temp + ' + '
    outtext = ' c31:  ' + outtext[:-2] + '= 1\n'
    return outtext

# Declaration of Bounds
def get_bounds_allocation(Sij):
    outtext = ''
    for i in range(rows):
        temp = ''
        for j in range(cols):
            temp += ' 0 <= x' + str(i+1) + '_' + str(j+1) + ' <= 1\n'
        outtext += temp    
    return outtext

def get_bounds_facility(Sij):
    outtext = ''
    for i in range(rows):
        outtext += ' 0 <= y' + str(i+1) + ' <= 1\n'
    return outtext

# Declaration of Decision Variables (form can be: Binary, Integer, etc.)
# In this case decision variables are binary.
def get_allocation_decision_variables_p_maxian(Sij):
    outtext = ''
    for i in range(1, rows+1):
        temp = ''
        for j in range(1, cols+1):
            temp += ' x' + str(i) + '_' + str(j) + ' '
        outtext += temp
    return outtext
    
def get_facility_decision_variables_p_maxian(rows):  
    outtext = ''
    for i in range (1, rows+1):
        outtext += ' y' + str(i) + ' '
    return outtext
 
    
#    3. DATA Creation & VARIABLE DECLARATION
Ai = np.random.randint(1, 20, 5)
Ai = Ai.reshape(5, 1)
Cij = np.random.randint(1, 50, 25)
Cij = Cij.reshape(5, 5)
Sij = Ai * Cij
rows, cols = Sij.shape

#    4. START TEXT FOR .lp FILE
# Declaration of Objective Function
text = "p-Maxian Facility Location Problem\n"
text += "'''\n"
text += 'Maximize\n'          
text += get_objective_function_p_maxian(Sij)
# Declaration of Constraints
text += 'Subject To\n'                    
text += get_assignment_constraints(rows)
text += get_opening_constraints_p_maxian(Sij)
text += get_p_facilities(rows)
# Declaration of Bounds
text += 'Bounds\n' 
text += get_bounds_allocation(Sij)
text += get_bounds_facility(Sij)
# Declaration of Decision Variables form: Binaries
text += 'Binaries\n'
text += get_allocation_decision_variables_p_maxian(Sij)
text += get_facility_decision_variables_p_maxian(rows)
text += '\n'
text += 'End\n'
text += "'''\n"
text += "© James Gaboardi, 2015"                


#   5. CREATE & WRITE .lp FILE TO DISK
# Fill path name  --  File name must not have spaces.
outfile = open('LP.lp', 'w')
outfile.write(text)
outfile.close()