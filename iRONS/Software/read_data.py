# -*- coding: utf-8 -*-
"""
These modules extract the data from either a CSV (comma separated variables) or 
a NetCDF file.

This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi and at 
Bristol University (2020).

Licence: MIT
"""
import pandas as pd
import numpy as np
from netCDF4 import Dataset

def read_csv_data(folder_path,file_name,column_name = None):
    """
    This module extracts the data from a CSV (comma separated variables) file
    """

    data = pd.read_csv(folder_path+"/"+file_name)
    ### Dates ###
    # the next day at 00:00 we need to substract one day (-24h) 
    # to reflect that the first data member corresponds to the first 
    # day and not to the next day at 00:00
    date = pd.to_datetime(np.array(data['Date']),
                           format = '%d/%m/%Y')

    # Each element of args is the name of weather variable
    if isinstance(column_name,(str)):
        outputs = np.array(data[column_name])
    else:
        outputs = np.array(data[data.columns[1:]])
        
    return date,outputs

def read_netcdf_data(folder_path,file_name,variable_name):

    """
    This module extracts the data from a NetCDF file
    """
    
    data = Dataset(folder_path+"//"+file_name, "r")
    ### Dates ###
    # the next day at 00:00 we need to substract one day (-24h) 
    # to reflect that the first data member corresponds to the first 
    # day and not to the next day at 00:00
    date = pd.to_datetime(data['time'][:]-24, 
                            unit='h', # hourly
                            origin = pd.Timestamp('01-01-1900'))

    # Each element of args is the name of weather variable
    outputs = np.array(data.variables[variable_name][:])
        
    return date,outputs