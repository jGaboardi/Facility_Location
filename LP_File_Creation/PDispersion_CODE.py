# -*- coding: utf-8 -*-
# p-Dispersion Facility Location Problem
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


#  Terminology & General Background for Facility Location and 
#                    Summation Notation:

#   *        The objective of the p-Dispersion Facility Location Problem 
#                    is to maximize the minimum distance bewteen 
#                    facilities (generally noxious).

#   *   [i] - a specific origin
#   *   [j] - a specifc destination
#   *   [n] - the set of origins
#   *   [m] - the set of destinations
#   *   [dij] - matrix of travel costs between nodes
#   *   [M] - largest value in dij
#   *   [D] - Maximized minimum distance between facilities
#   *	[yi] - each service facility
#   *   [p] - the number of facilities to be sited

#    1. IMPORTS
# Other imports may be necessary for matrix creation and manipulation 
import numpy as np


#    2. DEFINED FUNCTIONS
# Facility Constraint
# *** '= 1\n' indicates 1 facility  
def get_p_facilities(cols):
    outtext = ''
    for i in range(1, cols+1):
        temp = ''
        temp += 'y' + str(i)
        outtext += temp + ' + '
	outtext = ' c1:  ' + outtext[:-2] + '= 2\n'
    return outtext

# Inter-Facility Distance Constraints   n(n-1)/2