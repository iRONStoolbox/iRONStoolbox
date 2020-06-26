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

from Data_management.Read_data import read_csv_data

### Function to test ###
from Weather_forecast.Bias_correction import linear_scaling

### Observed data ###
# File path
path_obs_data = 'iRONS/Notebooks/B - Implementation/Inputs'
#path_obs_data = ''
name_obs_file = 'hist_clim_data.csv'
# Read files
dates_obs,Temp_obs = read_csv_data(path_obs_data,name_obs_file,'Temp')
dates_obs,Rain_obs = read_csv_data(path_obs_data,name_obs_file,'Rain')

### Forecast data ###
origin_centre = 'ECMWF' # forecast originating centre
file_format = 'netcdf'
path_fore_data = 'iRONS/Notebooks/B - Implementation/Inputs/'+origin_centre+' forecasts '+file_format
name_fore_file_end = "_1d_7m_"+origin_centre+"_Temp_Evap_Rain.nc"

dates_fore = pd.date_range(start = '2015-12-01', end = '2015-12-31', freq = 'D')
Rain_fore  = np.ones(dates_fore.size)
Temp_fore  = np.zeros(dates_fore.size)

### Run the function to test: Precipitation bias correction ###
Rain_fore_corr = linear_scaling(path_fore_data,name_fore_file_end,
                                dates_fore,Rain_fore,
                                dates_obs,Rain_obs,
                                'Rain')

### Run the function to test: Temperature bias correction ###
Temp_fore_corr = linear_scaling(path_fore_data,name_fore_file_end,
                                dates_fore,Temp_fore,
                                dates_obs,Temp_obs,
                                'Temp')

### Testing functions ###
def test_Rain_fore_corr():
    # Expected output
    Rain_fore_corr_expect = np.ones([len(dates_fore)])*2.1405371204414 + [0]
    # Test 
    assert_array_equal(Rain_fore_corr,Rain_fore_corr_expect)
    
### Testing functions ###
def test_Temp_fore_corr():
    # Expected output
    Temp_fore_corr_expect = np.ones([len(dates_fore)])*-0.670478360150061
    # Test 
    assert_array_equal(Temp_fore_corr,Temp_fore_corr_expect)
