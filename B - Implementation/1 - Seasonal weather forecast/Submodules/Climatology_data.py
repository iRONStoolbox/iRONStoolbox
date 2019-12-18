# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:40:06 2018

@author: ap18525
"""

import numpy as np
import matplotlib.dates as dates
import datetime
import os.path

if os.path.exists("Submodules"):
    from Submodules.TUW_WimClat_Sim import TUW_WimClat # TUW hydrological model
else:
    from TUW_WimClat_Sim import TUW_WimClat # TUW hydrological model

def Climatology_data(area,tstep,ini_year,end_year,file_path):
    
    if os.path.exists(file_path):
        filename = file_path
    elif os.path.exists('..//'+file_path):
        filename = '..//'+file_path
        
    date_str = np.genfromtxt(filename, delimiter = ',',skip_header=1,usecols=0,dtype='str')
    date = [datetime.datetime.strptime(date_str[i], '%d/%m/%Y') for i in range(len(date_str))]
    date_num = dates.date2num(date).astype('int')
    weather_data = np.genfromtxt(filename, delimiter = ',',skip_header=1)
    PET = weather_data[:,1]
    Rain = weather_data[:,2]
    Temp = weather_data[:,3]
        
    inic = np.array([50,2.5,2.5,0])
    
    I_data,SM,UZ,LZ,SWE,EA,R,RL,I0,I1,I2,SW,MT =TUW_WimClat(Rain,Temp,PET,inic,area)
    
    Rain_out = np.zeros(len(Rain))
    I_data_out = np.zeros(len(I_data))
    
    if tstep == 'daily':
        Rain_out = Rain
        I_data_out = I_data
    elif tstep == 'weekly':        

        for i in np.arange(7,len(Rain),1):
            Rain_out[i] = np.sum(Rain[i-7:i])
                
        for i in np.arange(7,len(I_data),1):
            I_data_out[i] = np.sum(I_data[i-7:i])

    elif tstep == 'monthly':
        
        for i in np.arange(30,len(Rain),1):
            Rain_out[i] = np.sum(Rain[i-30:i])
                
        for i in np.arange(30,len(I_data),1):
            I_data_out[i] = np.sum(I_data[i-30:i])
            
    y_ini = ini_year
    y_end = end_year
    
    PET_matrix = np.zeros((366+1,y_end-y_ini+1))+np.nan
    Rain_matrix = np.zeros((366+1,y_end-y_ini+1))+np.nan
    Rain_matrix_out = np.zeros((366+1,y_end-y_ini+1))+np.nan
    Temp_matrix = np.zeros((366+1,y_end-y_ini+1))+np.nan
    I_matrix = np.zeros((366+1,y_end-y_ini+1))+np.nan
    I_matrix_out = np.zeros((366+1,y_end-y_ini+1))+np.nan
    
    Rain_matrix[0,:] = np.arange(y_ini,y_end+1,1)
    Rain_matrix_out[0,:] = np.arange(y_ini,y_end+1,1)    
    I_matrix[0,:] = np.arange(y_ini,y_end+1,1)
    I_matrix_out[0,:] = np.arange(y_ini,y_end+1,1)

    count = 0
    for i in date_num:
        year = dates.num2date(i).year
        d0 = dates.date2num(datetime.datetime(year, 1, 1, 0, 0))
        n_col = np.where(I_matrix[0,:] == year)
        n_row = int(i-d0+1)
        PET_matrix[n_row,n_col] = PET[count]
        Rain_matrix[n_row,n_col] = Rain[count]
        Rain_matrix_out[n_row,n_col] = Rain_out[count]
        Temp_matrix[n_row,n_col] = Temp[count]
        I_matrix[n_row,n_col] = I_data[count]
        I_matrix_out[n_row,n_col] = I_data_out[count]
        count += 1
        
    I_max = np.concatenate((np.nanmax(I_matrix[1:-1,:], axis = 1),np.nanmax(I_matrix[1:-1,:], axis = 1)),axis=0)
    I_p95 = np.concatenate((np.nanpercentile(I_matrix[1:-1,:],95, axis =1),np.nanpercentile(I_matrix[1:-1,:],95, axis =1)),axis=0)
    I_p5 = np.concatenate((np.nanpercentile(I_matrix[1:-1,:],5, axis =1),np.nanpercentile(I_matrix[1:-1,:],5, axis =1)),axis=0)
    I_min = np.concatenate((np.nanmin(I_matrix[1:-1,:], axis = 1),np.nanmin(I_matrix[1:-1,:], axis = 1)),axis=0)
    
    outputs = (Rain_matrix_out,I_matrix_out,I_max,I_p95,I_p5,I_min)
    return outputs
