# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 12:26:03 2019

@author: ap18525
"""

import numpy as np
import numba

# Function to transform cumulative data into instantaneous data
@numba.jit(nopython=True) # to speed-up the function
def cum2inst(cum_data):
    inst_data = np.zeros(cum_data.shape)
    for i in np.arange(len(cum_data[0,:])):
        for j in np.arange(len(cum_data[:,0])-1):
            inst_data[j+1,i] = np.maximum(cum_data[j+1,i]-cum_data[j,i],0)
    inst_data[0,:] = cum_data[0,:]
    return inst_data
    