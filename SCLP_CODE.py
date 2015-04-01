# -*- coding: utf-8 -*-
# Set Cover Facility Location Problem
# This script creates a linear programming file to be read into an optimizer.
'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''
# Developed by:  James D. Gaboardi, MSGIS
#                03/2015
#                © James Gaboardi


# **Attention** **Adjust the following**
#	57 --> S = # needs to changed for the definition of 'S'

#   Terminology & General Background for Facility Location and Summation Notation:

#   *        The objective of the Set Cover Facility Location Problem is to minimize the average cost
#            of travel (between service facilities and clients).

#   *   [i] - a specific origin
#   *   [j] - a specifc destination
#   *   [n] - the set of origins
#   *   [m] - the set of destinations
#   *   [Aij] - binary matrix of of nodes within S
#   *   [Cij] - travel costs between nodes
#   *   [Dij] - distnace from i to j
#   *   [S] - defined distance from node
#   *   [x#_#] - the decision variable in # row, # column position in the matrix
#   *	[y#] - service facility in the # row


#    1. Imports
# Other imports may be necessary for matrix creation and manipulation
import numpy as np


#    2. Defined Functions
# The objective of this function is to minimize the number of additional facilties needed for complete coverage.
def set_cover_objective_function(rows):
    outtext = ' obj: '
    for i in range(1, rows + 1):
        temp = ''
        temp += 'x'+str(i)
        outtext += temp + ' + '
    outtext = outtext[:-2]
    return outtext

# Aij and Service Constraints
# Step 1: Determine Aij (nodes within S)
# S defined in line &&&  --> 1 = served; 0 = unserved
def Served_Nodes(rows):
    outtext = ''
    S = 10
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
    counter = 0
    outtext1 = ''
    for i in range(rows):
        counter = counter + 1
        temp = ' c' + str(counter) + ':  '
        for j in range(cols):
            temp += str(Aij[i,j]) + 'x' + str(j+1) + ' + '
        outtext1 += temp[:-2] + '>= 1\n'
    return outtext1

#    Binaries
def set_cover_binaries(cols):
    outtext = ''
    for i in range(1, rows + 1):
        temp = ''
        temp += ' x' + str(i) + '\n'
        outtext += temp #+ ' + '
    #outtext = outtext[:-2]
    return outtext


#    3. DATA READS & VARIABLE DECLARATION
'''
########## Cost Matrix Vector
########## Cij -->  [ 0, 13, 8, 15,
##########           13, 0, 12, 11,
##########            8, 12, 0, 10,
##########           15, 11, 10, 0]
########## Read Cij in as a vector text file.
'''

Cij = np.array([ 0, 13, 8, 15, 3, 0, 12, 11, 8, 12, 0, 10, 15, 11, 10, 0])
'''
Cij = np.fromfile('path/Cij.txt', dtype=int, sep='\n')
'''
Cij = Cij.reshape(4, 4)
rows, cols = Cij.shape


#    4. START TEXT FOR .lp FILE
# Declaration of Objective Function
text = "Set Cover Location Problem\n"
text += "'''\n"
text += 'Minimize\n'
text += set_cover_objective_function(rows)
text += '\n\n'
# Declaration of Constraints
text += 'Subject To\n'
text += Served_Nodes(rows)
text += '\n'
# Declaration of Decision Variables form: Binaries
text += 'Binaries\n'
text += set_cover_binaries(rows)
text += '\n'
text += 'End\n'
text += "'''\n"
text += "© James Gaboardi, 2015"


#   5. CREATE & WRITE .lp FILE TO DISK
# Fill path name  --  File name must not have spaces.
outfile = open('/Users/jgaboardi/Desktop/test.lp', 'w')
outfile.write(text)
outfile.close()