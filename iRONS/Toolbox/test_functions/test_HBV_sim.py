# -*- coding: utf-8 -*-
"""
This is a function to test the HBV model
@author: Andres Peñuela
"""

import numpy as np
from numpy.testing import assert_array_almost_equal

if __name__ == '__main__':
    import sys
    sys.path.append("..") # Adds higher directory to python modules path.

### Function to test ###
from Inflow_simulation.HBV_sim import HBV_sim
# Test inptus
P = np.array([10, 20, 15])
ept = np.array([2, 5, 6])   
param = np.array([3.5, 50, 50, 3.5, 0.65, 1000, 50, 1 ,0.5 , 0.05, 50, 3.5]) 
Case = 1 
ini = np.array([200,50,50]) 
area = 10
# Run the function to test
Q,STATES,FLUXES  = HBV_sim(P,ept,param,Case,ini,area)

### Testing functions ###
def test_Q():
    # Expected output
    Q_expect = np.array([1000., 2100., 0.         ])
    # Test 
    assert_array_almost_equal(Q,Q_expect)
    
def test_STATES():
    # Expected output
    STATES_expect = [np.array([200. , 0.   , 19.96      , 34.27462518]),
                     np.array([50.  , 210. , 0.         , 0.60291782 ]),
                     np.array([50.  , 0.   , 0.         , 0.         ])]
    # Test
    assert_array_almost_equal(STATES,STATES_expect)

def test_FLUXES():
    # Expected output
    FLUXES_expect = [np.array([0.   , 0.04 , 0.082457   ]),
                     np.array([210. , 0.   , 0.60291782 ]),
                     np.array([0.   , 0.   , 0.         ]),
                     np.array([500. , 2100., 0.         ]),
                     np.array([500. , 0.   , 0.         ])]
    # Test
    assert_array_almost_equal(FLUXES,FLUXES_expect)
