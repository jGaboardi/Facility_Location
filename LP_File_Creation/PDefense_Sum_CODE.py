# -*- coding: utf-8 -*-
#The p-Defense-Sum Facility Location Problem
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

# Maximizing the total distance bewteen facilities (generally noxious)

#    1. IMPORTS
# Other imports may be necessary for matrix creation and manipulation 
import numpy as np


#    2. DEFINED FUNCTIONS
def get_objective_function_p_def_sum():
    outtext = ' obj: '
    for i in range(rows):
        temp = ''
        temp += str(Cij[i][0]) + ' y' + str(i+1) + ' + '
        outtext += temp #+ ' \n'
    outtext = outtext[:-3] + ' \n'
    return outtext

# Facility Constraint
# *** '= 1\n' indicates 1 facility  
def get_p_facilities():
    outtext = ''
    for i in range(rows):
        temp = ''
        temp += 'y' + str(i+1)
        outtext += temp + ' + '
    outtext = ' c1:  ' + outtext[:-2] + '= 2\n'
    return outtext

# Declaration of Bounds
def get_bounds_facility():
    outtext = ''
    for i in range(rows):
        outtext += ' 0 <= y' + str(i+1) + ' <= 1\n'
    return outtext

# Declaration of Decision Variable (form can be: Binary, Integer, etc.)
# In this case decision variables are binary.
# *** 0 for no sited facility, 1 for a sited facilty
def get_facility_decision_variables():  
    outtext = ''
    for i in range(rows):
        outtext += 'y' + str(i+1) + ' '
    return outtext 
    
#    3. DATA READS & VARIABLE DECLARATION
Cij = np.random.randint(1,20,16)
Cij = Cij.reshape(16,1)
rows,cols = Cij.shape


#    4. START TEXT FOR .lp FILE
# Declaration of Objective Function
text = "p-Defense-Sum Facility Location Problem\n"
text += "'''\n"
text += 'Maximize\n'
text += get_objective_function_p_def_sum()
# Declaration of Constraints
text += 'Subject To\n'                    
text += get_p_facilities()
# Declaration of Bounds
text += 'Bounds\n'
text += get_bounds_facility()
# Declaration of Decision Variables form: Binaries
text += 'Binaries\n'
text += get_facility_decision_variables()
text += '\n'
text += 'End\n'
text += "'''\n"
text += "© James Gaboardi, 2015"
                

#   5. CREATE & WRITE .lp FILE TO DISK
# Fill path name  --  File name must not have spaces.
outfile = open('LP.lp', 'w')
outfile.write(text)
outfile.close()