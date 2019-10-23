# -*- coding: utf-8 -*-
"""
"""
# Import libraries
import numpy as np
from netCDF4 import num2date,date2num
import datetime

from Submodules.TUW_WimClat_Sim import TUW_WimClat # TUW hydrological model

def Generated_weather(year_day0,horizon,area):
    
    # Climate data 1981-2018
    filename = 'Data//GeneratedRainWim.csv' # 1000 members
    Rain_data = np.genfromtxt(filename, delimiter = ',',skip_header=1)
    Rain_gen = Rain_data[:,1:]
    
    filename = 'Data//GeneratedPETWim.csv' # 1000 members
    PET_data = np.genfromtxt(filename, delimiter = ',',skip_header=1)
    PET_gen = PET_data[:,1:]
    
    filename = 'Data//GeneratedTempWim.csv' # 1000 members
    Temp_data = np.genfromtxt(filename, delimiter = ',',skip_header=1)
    Temp_gen = Temp_data[:,1:]
    
    I_gen = Rain_gen*0
    
    inic = [200,30,50,0]
    
    for i in range(np.size(Rain_gen, axis = 1)):
        I,STATES,FLUXES =TUW_WimClat(Rain_gen[:,i],Temp_gen[:,i],PET_gen[:,i],inic,area,1)
        inic = [STATES[0][-1],STATES[1][-1],STATES[2][-1],STATES[3][-1]]
        I_gen[:,i]=I
    
    Rain_gen = np.append(Rain_gen[:,0:-1],Rain_gen[:,1:],axis = 0)
    PET_gen = np.append(PET_gen[:,0:-1],PET_gen[:,1:],axis = 0)
    Temp_gen = np.append(Temp_gen[:,0:-1],Temp_gen[:,1:],axis = 0)
    I_gen = np.append(I_gen[:,0:-1],I_gen[:,1:],axis = 0)
    
    I_gen_w = [np.zeros(np.shape(I_gen)[1])]
    Rain_gen_w = [np.zeros(np.shape(Rain_gen)[1])]
    Temp_gen_w = [np.zeros(np.shape(Temp_gen)[1])]
    PET_gen_w = [np.zeros(np.shape(PET_gen)[1])]
    for i in np.arange(1,horizon+1,1):
        I_gen_w = np.append(I_gen_w,[np.sum(I_gen[(i-1)*7:i*7,:],axis =0)],axis = 0)
        Rain_gen_w = np.append(Rain_gen_w,[np.sum(Rain_gen[(i-1)*7:i*7,:],axis =0)],axis = 0)
        Temp_gen_w = np.append(Temp_gen_w,[np.sum(Temp_gen[(i-1)*7:i*7,:],axis =0)],axis = 0)
        PET_gen_w = np.append(PET_gen_w,[np.sum(PET_gen[(i-1)*7:i*7,:],axis =0)],axis = 0)
       
    return I_gen_w, Rain_gen_w, Temp_gen_w, PET_gen_w