# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:40:06 2018

@author: ap18525
"""

import numpy as np
from netCDF4 import num2date,date2num
import datetime
from calendar import monthrange
import os.path

if os.path.exists("Submodules"):
    from Submodules.TUW_WimClat_Sim import TUW_WimClat # TUW hydrological model
else:
    from TUW_WimClat_Sim import TUW_WimClat # TUW hydrological model

def Observed_inflow_data(year0,month0,day,horizon,area,tstep):
    
    # Climate data 1968-2018
    if os.path.exists('Data//ClimdataWim.csv'):
        filename = 'Data//ClimdataWim.csv'
    elif os.path.exists('..//Data//ClimdataWim.csv'):
        filename = '..//Data//ClimdataWim.csv'
        
    date_str = np.genfromtxt(filename, delimiter = ',',skip_header=1,usecols=0,dtype='str')
    date = [datetime.datetime.strptime(date_str[i], '%d/%m/%Y') for i in range(len(date_str))]
    date_num = date2num(date,'days since 1900-01-01').astype('int')
    weather_data = np.genfromtxt(filename, delimiter = ',',skip_header=1)
    PET = weather_data[:,1]
    Rain = weather_data[:,2]
    Temp = weather_data[:,3]
        
    inic = np.array([50,2.5,2.5,0])
    
    I_data,SM,UZ,LZ,SWE,EA,R,RL,I0,I1,I2,SW,MT =TUW_WimClat(Rain,Temp,PET,inic,area)
    
    if month0 == 2 and day == 29:
        day0 = int(date2num(datetime.datetime(year0, month0, 28, 0, 0),'days since 1900-01-01'))
    else:
        day0 = int(date2num(datetime.datetime(year0, month0, day, 0, 0),'days since 1900-01-01'))
    
    if tstep == 'daily':
        day_ini = day0
        day_end = day_ini+horizon
    elif tstep == 'monthly':
        day_ini = day0
        if month0+horizon>12:
            day_end = int(date2num(datetime.datetime(year0+1, month0+horizon-12, day, 0, 0),'days since 1900-01-01'))
        else:
            day_end = int(date2num(datetime.datetime(year0, month0+horizon, day, 0, 0),'days since 1900-01-01'))
    elif tstep == 'weekly':
        wday0 = datetime.datetime(year0, month0, day, 0, 0).weekday() # 
    
        if wday0 >3:
            day_ini = day0 + (7-wday0)
        else:
            day_ini = day0 - wday0
        if num2date(day_ini,'days since 1900-01-01').month == 12 and month0 == 1:
            day_ini = day_ini + 7 # Next Monday instead of the previous one
        elif num2date(day_ini,'days since 1900-01-01').month < month0:
            day_ini = day_ini + 7 # Next Monday instead of the previous one
        elif num2date(day_ini,'days since 1900-01-01').month > month0:
            day_ini = day_ini - 7 # Last Monday instead of the next one
        
        day_end = day_ini+horizon*7 # day_ini + horizon weeks * 7 days/week
    
    days = np.arange(day_ini,day_end+1,1)
    
    dates = num2date(days,'days since 1900-01-01')
    I = I_data[np.where(date_num==day_ini)[0][0]:np.where(date_num==day_end)[0][0]]
    P = Rain[np.where(date_num==day_ini)[0][0]:np.where(date_num==day_end)[0][0]]
    T = Temp[np.where(date_num==day_ini)[0][0]:np.where(date_num==day_end)[0][0]]
    E = PET[np.where(date_num==day_ini)[0][0]:np.where(date_num==day_end)[0][0]]
    
    Dates_out = dates[0]
    I_out = [0]
    P_out = [0]
    T_out = [0]
    E_out = [0]
    count = 0
    for i in np.arange(1,horizon+1,1):
        if tstep == 'daily':
            Dates_out    = dates
            I_out = I
            P_out = P
            T_out = T
            E_out  = E
        elif tstep == 'weekly':
            delta1 = 7
            count += delta1
            Dates_out    = np.append(Dates_out,[dates[count]])
            I_out = np.append(I_out,[np.sum(I[count - delta1:count],axis =0)],axis = 0)
            P_out = np.append(P_out,[np.sum(P[count - delta1:count],axis =0)],axis = 0)
            T_out = np.append(T_out,[np.mean(T[count - delta1:count],axis =0)],axis = 0)
            E_out  = np.append(E_out,[np.sum(E[count - delta1:count],axis =0)],axis = 0)
        elif tstep == 'monthly':
            if month0+i-1>12:
                delta1 = monthrange(year0+1, month0+i-12-1)[1]
            else:
                delta1 = monthrange(year0, month0+i-1)[1]
            count += delta1
            Dates_out    = np.append(Dates_out,[dates[count]])
            I_out = np.append(I_out,[np.sum(I[count - delta1:count],axis =0)],axis = 0)
            P_out = np.append(P_out,[np.sum(P[count - delta1:count],axis =0)],axis = 0)
            T_out = np.append(T_out,[np.mean(T[count - delta1:count],axis =0)],axis = 0)
            E_out  = np.append(E_out,[np.sum(E[count - delta1:count],axis =0)],axis = 0)

    return Dates_out, I_out, P_out, T_out, E_out
