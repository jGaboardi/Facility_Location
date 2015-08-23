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
#   *   [Cij] - travel costs between nodes
#   *   [D] - the maximum travel costs between service facilities and clients 
#   *   [x#_#] - the decision variable in # row, # column position in the matrix
#   *	[y#] - service facility in the # row
#   *   [p] - the number of facilities to be sited


#    1. IMPORTS
# Other imports may be necessary for matrix creation and manipulation 
import numpy as np


#    2. DEFINED FUNCTIONS
