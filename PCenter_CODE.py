#p-Center Facility Location Problem
#This script creates a linear programming file to be read into an optimizer.
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
#	66 --> 'c##' needs to changed depending on data and constraint number based on .lp file
#	66 --> '= ##\n' needs to changed for the number of facilities to be sited
#	71 --> 'c##' needs to changed depending on data and constraint number based on .lp file
#	83 --> 'c##' needs to changed depending on data and constraint number based on .lp file

#   Terminology & General Background for Facility Location and Summation Notation:

#   *        The objective of the p-center Facility Location Problem is to minimize the maximum cost 
#            of travel between service facilities and clients on a network.

#   *   [i] - a specific origin
#   *   [j] - a specifc destination
#   *   [n] - the set of origins
#   *   [m] - the set of destinations
#   *   [Cij] - travel costs between nodes
#   *   [W] - the maximum travel costs between service facilties and clients 
#   *   [x#_#] - the decision variable in # row, # column position in the matrix
#   *	[y#] - service facility in the # row
#   *   [p] - the number of facilities to be sited


#    1. IMPORTS
# Other imports may be necessary for matrix creation and manipulation 
import numpy as np


#    2. DEFINED FUNCTIONS
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
            temp += 'x' + str(j) + '_' + str(i) + ' + '
        outtext += temp[:-2] + '= 1\n'
    return outtext

# Facility Constraint
# *** '= 1\n' indicates 1 facility  
def get_p_facilities(rows):
    outtext = ''
    for i in range(1, rows+1):
        temp = ''
        temp += 'y' + str(i)
        outtext += temp + ' + '
	outtext = ' c##:  ' + outtext[:-2] + '= #\n'
    return outtext

# Opening Constraints
def get_opening_constraints_p_center(Cij):
    counter = 151
    outtext = ''
    for i in range(1, rows+1):
        for j in range(1, cols+1):
            counter = counter + 1 
            outtext += ' c' + str(counter) + ':  - x' + str(i) + '_' + str(j) + ' + ' + 'y' + str(i) +  ' >= 0\n'
    return outtext

# Maximum Cost Constraints
# This indicates that the maximum travel cost from any client to service facility is greater than the travel cost from client to client.
# This code chunk works by summing the columns not rows
def get_max_cost(rows):
    counter = 1501
    outtext = ''
    for j in range(cols):
        counter = counter + 1
        temp = ' c' + str(counter) + ':  '
        for i in range(rows):
            temp += str(Cij[i,j]) + ' x' + str(i+1) + '_' + str(j+1) + ' + '
        outtext += temp[:-2] + '- W <= 0\n'
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

# Declaration of Decision Variable (form can be: Binary, Integer, etc.)
# In this case decision variables are binary.
# *** 0 for no sited facility, 1 for a sited facilty
def get_decision_variables_p_center(Cij):
    outtext = ' '
    for i in range(1, rows+1):
        temp = ''
        for j in range(1, cols+1):
            temp += 'x' + str(i) + '_' + str(j) + ' '
        outtext += temp
    return outtext
    
def get_facility_decision_variables_p_center(rows):  
    outtext = ''
    for i in range (1, rows+1):
        outtext += 'y' + str(i) + ' '
    #outtext += temp
    return outtext    


#    3. DATA READS & VARIABLE DECLARATION
'''
########## Cost Matrix
########## Cij -->  [ 0, 13, 8, 15, 
##########			 13, 0, 12, 11, 
##########			  8, 12, 0, 10, 
##########			 15, 11, 10, 0]
########## Read Cij in as a vector text file.
'''

Cij = np.fromfile('path/Cij.txt', dtype=float, sep='\n')
Cij = Cij.reshape(#, #)
rows,cols = Cij.shape


#    4. START TEXT FOR .lp FILE
# Declaration of Objective Function
text = "p-Center Facility Location Problem\n"
text += "'''\n"
text += 'Minimize\n'
text += ' obj: W\n'
# Declaration of Constraints
text += 'Subject To\n'                    
text += get_assignment_constraints(rows)
text += get_p_facilities(rows)
text += get_opening_constraints_p_center(Cij)
text += get_max_cost(rows)
# Declaration of Bounds
text += 'Bounds\n'
text += get_bounds_allocation(Cij)
text += get_bounds_facility(Cij)
# Declaration of Decision Variables form: Binaries
text += 'Binaries\n'
text += get_decision_variables_p_center(Cij)
text += get_facility_decision_variables_p_center(rows)
text += '\n'
text += 'End\n'
text += "'''\n"
text += "© James Gaboardi, 2015"
                

#   5. CREATE & WRITE .lp FILE TO DISK
# Fill path name  --  File name must not have spaces.
outfile = open('path/name.lp', 'w')
outfile.write(text)
outfile.close()