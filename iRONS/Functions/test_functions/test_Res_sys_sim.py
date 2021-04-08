# -*- coding: utf-8 -*-
"""
This is a function to test the Bias_correction function
This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi and at 
Bristol University (2020).
"""
import pandas as pd
import numpy as np
from numpy.testing import assert_array_equal

if __name__ == '__main__':
    import sys
    sys.path.append("..") # Adds higher directory to python modules path.
    ### Function to test ###
    from Reservoir_system_simulation.Res_sys_sim import Res_sys_sim
else:
    ### Function to test ###
    from irons.Functions.Reservoir_system_simulation.Res_sys_sim import Res_sys_sim
    
### Inputs ###
N = 10
dates = pd.date_range('2018-01-01', periods=N, freq='W')
I = np.ones([N,1])*10
e = np.ones([N,1])*1
s_0 = 20
s_min = 5
s_max = 100
env_min = 2
d = np.ones([N,1])*9

Qreg = {'releases' : [],
        'inflows'  : [],
        'rel_inf'  : []}
    
env, spill, Qreg_rel, Qreg_inf, s, E = Res_sys_sim(dates, I, e, s_0, s_min, s_max, env_min, d, Qreg)


### Testing functions ###
# Regulated releases
def test_Qreg_rel():
    # Expected output
    Qreg_rel_expect = np.array([9.,9.,9.,9.,9.,9.,9.,8.,7.,7.]).transpose()
    # Test 
    assert_array_equal(Qreg_rel,Qreg_rel_expect)
    
# Storage
def test_s():
    # Expected output
    s_expect = np.array([20.,18.,16.,14.,12.,10.,8.,6.,5.,5.,5.]).transpose()
    # Test 
    assert_array_equal(s,s_expect)

# Spillage   
def test_spill():
    I = np.ones([N,1])*50
    env, spill, Qreg_rel, Qreg_inf, s, E = Res_sys_sim(dates, I, e, s_0, s_min, s_max, env_min, d, Qreg)
    # Expected output
    spill_expect = np.array([0.,0.,34.,38.,38.,38.,38.,38.,38.,38.]).transpose()
    # Test 
    assert_array_equal(spill,spill_expect)