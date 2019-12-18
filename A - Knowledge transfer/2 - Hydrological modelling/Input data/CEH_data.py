# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 16:56:38 2018

@author: ap18525
"""

def CEH_data(year0, month0, months):

    from netCDF4 import Dataset
    import numpy as np
    
    import os

    if os.path.isdir('CHESS//'):
        file_path = 'CHESS//'
    elif os.path.isdir('Input data//CHESS//'):
        file_path = 'Input data//CHESS//'
        
    year = year0
    month = month0
    dates=[]
    for i in range(months):
        
        dates.append(int(str(year)+str(month).zfill(2))) 
        month = month+1
        if month>12:
            month=1
            year = year +1
        
#    dates = np.concatenate((np.arange(200901,200913,1), np.arange(201001,201013,1), np.arange(201101,201113,1), np.arange(201201,201213,1)), axis=0)

    CEH_date=np.empty(0)
    Temp_value=np.empty(0)
    PET_value=np.empty(0)
    Rain_value=np.empty(0)
    
    for i in dates:
        
        Temp_filename = 'chess_tas_'+str(i)+'.nc'
        PET_filename = 'chess_pet_wwg_'+str(i)+'.nc'
        Rain_filename = 'chess_precip_'+str(i)+'.nc'
        
        Temp_data = Dataset(file_path+Temp_filename)
        PET_data = Dataset(file_path+PET_filename)
        Rain_data = Dataset(file_path+Rain_filename)
        
        CEH_time=PET_data.variables['time'][:] + 22280 # Time in days since 1961-01-01 into days since 01/01/1900
        
        Temp=Temp_data.variables['tas'][:] -273.15 # degK into degC
        PET=PET_data.variables['pet'][:] #  in mm
        Rain=Rain_data.variables['precip'][:] * 86400 # kg m-2 s-1 into mm

        CEH_date = np.append(CEH_date,CEH_time[:])
        Temp_value = np.append(Temp_value,Temp[:,132,298]) # Coordinates
        PET_value = np.append(PET_value,PET[:,132,298]) # Coordinates
        Rain_value = np.append(Rain_value,Rain[:,132,298]) # Coordinates
    
    return(CEH_date, Temp_value, PET_value, Rain_value)