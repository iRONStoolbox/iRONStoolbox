# -*- coding: utf-8 -*-
"""
This is a function to test the cum2inst function
@author: Andres Peñuela
"""

import numpy as np
from numpy.testing import assert_array_almost_equal

if __name__ == '__main__':
    import sys
    sys.path.append("..") # Adds higher directory to python modules path.

### Function to test ###
from Data_management.cum2inst import cum2inst
# Test inputs
cum_rain = np.array([[10], [20], [20]]) # Cumulative rain
# Run the function to test
ins_rain = cum2inst(cum_rain)

### Testing functions ###
def test_cum2inst():
    # Expected output
    ins_rain_expect = np.array([[10], [10], [0]])
    # Test 
    assert_array_almost_equal(ins_rain,ins_rain_expect)