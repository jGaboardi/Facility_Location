# -*- coding: utf-8 -*-
# Maximum Cover Facility Location Problem
# This script creates a linear programming file to be read into an optimizer.
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


##### **Attention** **Adjust the following**
#####	Line 60 --> S = # needs to changed for the definition of 'S'

#   Terminology & General Background for Facility Location and Summation Notation:

#   *        The objective of the Maximum Cover Facility Location Problem is to site a fixed number of facilties
#            to achieve maximum coverage of demand within S.

#   *   [i] - a specific origin
#   *   [j] - a specifc destination
#   *   [n] - the set of origins
#   *   [m] - the set of destinations
#   *   [Hi] - demand at each node
#   *   [Aij] - binary matrix of nodes within S
#   *   [Cij] - travel costs between nodes
#   *   [Dij] - distnace from i to j
#   *   [S] - defined distance from node
#   *   [x#_#] - the decision variable in # row, # column position in the matrix
#   *	[y#] - service facility in the # row


#    1. Imports
# Other imports may be necessary for matrix creation and manipulation
import numpy as np


#    2. Defined Functions
# The objective of this function is to cover the maximum amount of demand while siting (p) facilities.
def maximum_cover_objective_function(rows2):
    outtext = ' obj: '
    for i in range(rows2):
        for j in range(cols2):
            temp = ''
            temp += str(Hi[i,j]) + 'x' + str(i+1) + ' + '
            outtext += temp #+ ' \n'
    outtext = outtext[:-3] + ' \n'
    return outtext
    
# Aij and Service Constraints
# Step 1: Determine Aij (nodes within S coverage area)
# S defined in line 60  --> 1 = served; 0 = unserved
def Served_Nodes(rows):
    outtext = ''
    S = 8
    Aij = []
    for i in Cij:
        for j in i:
            if j <= S:
                outtext = 1
            else:
                outtext = 0
            Aij.append(outtext)
    Aij = np.array(Aij)
    Aij = Aij.reshape(4,4)
    rows, cols = Aij.shape
# Step 2:
# Create Constraints
# Covering Constraint 
    counter = 0
    counter2 = 0
    outtext1 = ''
    for i in range(rows):
        counter = counter + 1
        counter2 = counter2 + 1
        temp = ' c' + str(counter) + ':  '
        for j in range(cols):
            temp += str(Aij[i,j]) + 'y' + str(j+1) + ' + '
        outtext1 += temp[:-2] + '- x' + str(counter2) + ' >= 0\n'
    return outtext1

# Facility Constraint
# Indicate how many facilties will be sited in 'outtext' below.
# *** '= 1\n' indicates 1 facility
def get_p_facilities(rows):
    outtext = ''
    for i in range(1, rows+1):
        temp = ''
        temp += 'y' + str(i)
        outtext += temp + ' + '
    outtext = ' c5:  ' + outtext[:-2] + '<= 2\n'
    return outtext

# Declaration of Bounds
def get_bounds_allocation(Cij):
    outtext = ''
    for i in range(rows):
        temp = ''
        for j in range(cols):
            temp += ' 0 <= x' + str(i+1) + '_' + str(j+1) + ' <= 1\n'
        outtext += temp    
    return outtext

def get_bounds_facility(Cij):
    outtext = ''
    for i in range(rows):
        outtext += ' 0 <= y' + str(i+1) + ' <= 1\n'
    return outtext
    
# Declaration of Binaries
def maximum_cover_allocation_binaries(cols):
    outtext = ''
    for i in range(1, rows + 1):
        temp = ''
        temp += ' x' + str(i) + '\n'
        outtext += temp #+ ' + '
    #outtext = outtext[:-2]
    return outtext

def get_facility_decision_variables_max_cover(rows):  
    outtext = ''
    for i in range (1, rows+1):
        outtext += ' y' + str(i) + '\n'
    return outtext


#    3. DATA READS & VARIABLE DECLARATION
'''
########## Cost Matrix Vector
########## Cij -->  [ 0, 13, 8, 15,
##########           13, 0, 12, 11,
##########            8, 12, 0, 10,
##########           15, 11, 10, 0]
########## Read Cij in as a vector text file.

########## Demand Matrix Vector
########## Hi -->  [1000,
##########          1200,
##########          1100,
##########          1250,]
########## Read Hi in as a vector text file.
'''
Hi = np.array([1000, 1200, 1100, 1250])
'''
Hi = np.fromfile('path/Hi.txt', dtype=int, sep='\n')
'''
Hi = Hi.reshape(4,1)
rows2, cols2 = Hi.shape
Cij = np.array([ 0, 13, 8, 15, 3, 0, 12, 11, 8, 12, 0, 10, 15, 11, 10, 0])
'''
Cij = np.fromfile('path/Cij.txt', dtype=int, sep='\n')
'''
Cij = Cij.reshape(4, 4)
rows, cols = Cij.shape


#    4. START TEXT FOR .lp FILE
# Declaration of Objective Function
text = "Maximum Cover Location Problem\n"
text += "'''\n"
text += 'Maximize\n'
text += maximum_cover_objective_function(rows)
text += '\n'
# Declaration of Constraints
text += 'Subject To\n'
text += Served_Nodes(rows)
text += '\n'
text += get_p_facilities(rows)
text += '\n'
# Declaration of Bounds
text += 'Bounds\n'
text += get_bounds_allocation(Cij)
text += '\n'
text += get_bounds_facility(Cij)
text += '\n'
# Declaration of Decision Variables form: Binaries
text += 'Binaries\n'
text += maximum_cover_allocation_binaries(rows)
text += '\n'
text += get_facility_decision_variables_max_cover(rows)
text += '\n'
text += 'End\n'
text += "'''\n"
text += "© James Gaboardi, 2015"


#   5. CREATE & WRITE .lp FILE TO DISK
# Fill path name  --  File name must not have spaces.
outfile = open('/path/name.lp', 'w')
outfile.write(text)
outfile.close()