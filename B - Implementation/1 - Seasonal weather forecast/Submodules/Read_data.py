# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 12:59:29 2019

@author: ap18525
"""
import pandas as pd
import numpy as np
from netCDF4 import Dataset

def read_csv_data(folder_path,file_name,weather_variable):
    data = pd.read_csv(folder_path+"//"+file_name)
    ### Dates ###
    # the next day at 00:00 we need to substract one day (-24h) 
    # to reflect that the first data member corresponds to the first 
    # day and not to the next day at 00:00
    dates = pd.to_datetime(np.array(data['Date']),
                           format = '%d/%m/%Y')

    # Each element of args is the name of weather variable
    outputs = np.array(data[weather_variable])
        
    return dates,outputs

def read_netcdf_data(folder_path,file_name,weather_variable):
    data = Dataset(folder_path+"//"+file_name, "r")
    ### Dates ###
    # the next day at 00:00 we need to substract one day (-24h) 
    # to reflect that the first data member corresponds to the first 
    # day and not to the next day at 00:00
    dates = pd.to_datetime(data['time'][:]-24, 
                            unit='h', # hourly
                            origin = pd.Timestamp('01-01-1900'))

    # Each element of args is the name of weather variable
    outputs = np.array(data.variables[weather_variable][:])
        
    return dates,outputs
        