# -*- coding: utf-8 -*-
#The Transportation Problem
#This script creates a linear programming file to be read into an optimizer.
'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''
# Developed by:  James D. Gaboardi, MSGIS
#                05/2015
#                © James Gaboardi


#   Terminology & General Background for Facility Location and Summation Notation:

#   *        The objective of The Transportation Problem is to minimize the cost of shipping from supply nodes to 
#            demand nodes.

#   *   [i] - a specific origin -- supply node
#   *   [j] - a specifc destination  -- demand node
#   *   [n] - the set of origins
#   *   [m] - the set of destinations
#   *   [Si] - supply at i
#   *   [Dj] - demand at j
#   *   [Cij] - unit cost of shipping from i to j
#   *   [x#_#] - the decision variable in # row, # column position in the matrix

#    1. IMPORTS
# Other imports may be necessary for matrix creation and manipulation 
import numpy as np


#    2. DEFINED FUNCTIONS
# Objective Function 
# The objective of this function is to minimize the cost of shipping from supply nodes to demand nodes.
def get_objective_function_trans_problem(Cij):
    outtext = ' obj: '
    for i in range(rows):
        temp = ''
        for j in range(cols):
            temp += str(Cij[i,j]) + 'x' + str(i+1) + '_' + str(j+1) + ' + '
        outtext += temp + ' \n      '
    outtext = outtext[:-11] + ' \n'
    return outtext

#Supply Constraint
def get_supply_constraint(Cij):
    counter = 0
    outtext = ''
    for i in range(rows):
        counter = counter + 1
        temp = ' c' + str(counter) + ':  '
        for j in range(cols):
            temp += 'x' + str(j+1) + '_' + str(i+1) + ' + '
        outtext += temp[:-2] + '= ' + str(Si[i,0]) + '\n'
    return outtext
    
#Demand Constraint
def get_demand_constraint(Cij):
    counter = 4
    outtext = ''
    for j in range(cols):
        counter = counter + 1
        temp = ' c' + str(counter) + ':  '
        for i in range(rows):
            temp += 'x' + str(j+1) + '_' + str(i+1) + ' + '
        outtext += temp[:-2] + '= ' + str(Dj[0,j]) + '\n'
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

def get_bounds_trans(Cij):
    outtext = ''
    for i in range(rows):
        for j in range(cols):
            outtext += ' x' + str(i+1) + '_' + str(j+1) + ' >= 0\n'
    return outtext

# Declaration of Decision Variables (form can be: Binary, Integer, etc.)
# In this case decision variables are General.
def get_shipped_decision_variables_trans(Cij):
    outtext = ''
    for i in range(1, rows+1):
        temp = ''
        for j in range(1, cols+1):
            temp += ' x' + str(i) + '_' + str(j) + '\n'
        outtext += temp
    return outtext
    
    
#    3. DATA READS & VARIABLE DECLARATION
Cij = np.array([4,5,4,10,6,3,3,5,8])
Cij = Cij.reshape(3,3)
rows, cols = Cij.shape
Si = np.array([100,130,140])
Si = Si.reshape(3,1)
Dj = np.array([150,100,120])
Dj = Dj.reshape(1,3)


#    4. START TEXT FOR .lp FILE
# Declaration of Objective Function
text = "The Transportation Problem\n"
text += "'''\n"
text += 'Minimize\n'          
text += get_objective_function_trans_problem(Cij)
text += '\n'
# Declaration of Constraints
text += 'Subject To\n'
text += get_supply_constraint(Cij)
text += '\n'
text += get_demand_constraint(Cij)
text += '\n'
# Declaration of Bounds
text += 'Bounds\n' 
text += get_bounds_trans(Cij)
text += '\n'
# Declaration of Decision Variables form: Generals
text += 'Generals\n'
text += get_shipped_decision_variables_trans(Cij)
text += '\n'
text += 'End\n'
text += "'''\n"
text += "© James Gaboardi, 2015"                


#   5. CREATE & WRITE .lp FILE TO DISK
# Fill path name  --  File name must not have spaces.
outfile = open('/path/name.lp', 'w')
outfile.write(text)
outfile.close()