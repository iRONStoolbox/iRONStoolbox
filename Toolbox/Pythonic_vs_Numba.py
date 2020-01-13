# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 19:45:26 2019

@author: andro
"""

import numpy as np
import time
import numba

rows = 12*30*24*60
cols = 100

matrix = np.abs(np.random.randn(rows,cols))
cum_hydro = np.cumsum(matrix,axis=0)

def instant_hydro(x):
    result = x*np.nan
    result[1:] = x[1:] - np.roll(x, shift = 1, axis = 0)[1:]
    
    return result

@numba.njit()
def instant_hydro_numba(x):
    result = x*np.nan
    for col in range(cols):
        site_hydro = x[:,col]
        for row in range(rows-1):
            result[row+1,col] = site_hydro[row+1] - site_hydro[row]
    
    return result

time_start = time.clock()
result = instant_hydro(cum_hydro)
time_elapsed = (time.clock() - time_start)

time_start_numba = time.clock()
result_numba = instant_hydro_numba(cum_hydro)
time_elapsed_numba = (time.clock() - time_start_numba)