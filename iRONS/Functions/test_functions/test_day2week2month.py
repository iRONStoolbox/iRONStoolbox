# -*- coding: utf-8 -*-
"""
This is a function to test the day2week2month functions

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
    from Data_management.day2week2month import day2week
else:
    ### Function to test ###
    from irons.Functions.Data_management.day2week2month import day2week
    
# Test inputs
N = 3 # 3 weeks
dates = pd.date_range(start = '2020-06-09', end = '2020-07-09', freq = 'D')
data  = np.ones(dates.size+1)
# Run the function to test
dates_week,data_week,data_cum_week = day2week(N,dates,data)

### Testing functions ###
def test_dates_week():
    # Expected output
    dates_week_expect = pd.to_datetime(np.array(['2020-06-15','2020-06-22','2020-06-29','2020-07-06']))
    # Test 
    assert_array_equal(dates_week,dates_week_expect)
    
### Testing functions ###
def test_data_week():
    # Expected output
    data_week_expect = np.array([[0],[7],[7],[7]])
    # Test 
    assert_array_equal(data_week,data_week_expect)
    
### Testing functions ###
def test_data_cum_week():
    # Expected output
    data_cum_week_expect = np.array([[0],[7],[14],[21]])
    # Test 
    assert_array_equal(data_cum_week,data_cum_week_expect)