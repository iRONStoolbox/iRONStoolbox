# -*- coding: utf-8 -*-
"""
This script extract the seasonal forecast data from the netcdf files and convert this data into Python arrays
To read and extract data from netcdf files the library netCDF4 needs to be installed. For this purpose type and execute this at the Anaconda Prompt:

    conda install -c anaconda netcdf4

Then either open you Python GUI, Spyder for example, or, if already open, restart the kernel
Now you are able to import the library
"""
# Import libraries
import numpy as np
from netCDF4 import num2date,date2num
import datetime
from calendar import monthrange

from Submodules.TUW_WimClat_Sim import TUW_WimClat # TUW hydrological model

def ESP_forecast(year0,month0,day,horizon,area,tstep):
    
    # Climate data 1981-2018
    filename = 'Data//ClimdataWim.csv' # 1968-2018

    date_str = np.genfromtxt(filename, delimiter = ',',skip_header=1,usecols=0,dtype='str')
    date = [datetime.datetime.strptime(date_str[i], '%d/%m/%Y') for i in range(len(date_str))]
    date_num = date2num(date,'days since 1900-01-01').astype('int')
    weather_data = np.genfromtxt(filename, delimiter = ',',skip_header=1)
    PET = weather_data[:,1]
    Rain = weather_data[:,2]
    Temp = weather_data[:,3]

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
    
    dates = date[np.where(date_num==day_ini)[0][0]:np.where(date_num==day_end)[0][0]]
    Rain_ens = np.zeros((day_end-day_ini,dates[0].year-1981))+np.nan
    Temp_ens = np.zeros((day_end-day_ini,dates[0].year-1981))+np.nan
    PET_ens = np.zeros((day_end-day_ini,dates[0].year-1981))+np.nan

    for i in range(dates[0].year-1981):
        if dates[0].month == 2 and dates[0].day == 29:
            d_ini = int(date2num(datetime.datetime(1981+i, dates[0].month, 28, 0, 0),'days since 1900-01-01'))
        else:
            d_ini = int(date2num(datetime.datetime(1981+i, dates[0].month, dates[0].day, 0, 0),'days since 1900-01-01'))

        Rain_ens[:,i] = Rain[np.where(date_num==d_ini)[0][0]:np.where(date_num==d_ini+day_end-day_ini)[0][0]]
        Temp_ens[:,i] = Temp[np.where(date_num==d_ini)[0][0]:np.where(date_num==d_ini+day_end-day_ini)[0][0]]
        PET_ens[:,i] = PET[np.where(date_num==d_ini)[0][0]:np.where(date_num==d_ini+day_end-day_ini)[0][0]]
            
    # Warm-up
    inic = np.array([50,2.5,2.5,0])
    wu_ini = int(date2num(datetime.datetime(1981, 1, 1, 0, 0),'days since 1900-01-01'))
    wu_end = day_ini
    I_wu,SM_wu,UZ_wu,LZ_wu,SWE_wu,EA_wu,R_wu,RL_wu,I0_wu,I1_wu,I2_wu,SW_wu,MT_wu =TUW_WimClat(Rain[np.where(date_num==wu_ini)[0][0]:np.where(date_num==wu_end)[0][0]],
        Temp[np.where(date_num==wu_ini)[0][0]:np.where(date_num==wu_end)[0][0]],PET[np.where(date_num==wu_ini)[0][0]:np.where(date_num==wu_end)[0][0]],inic,area)
    
    inic = np.array([SM_wu[-1],UZ_wu[-1],LZ_wu[-1],SWE_wu[-1]])
    
    I_ens = Rain_ens*0 + np.nan
    
    for i in range(np.size(Rain_ens, axis = 1)):
        I,SM,UZ,LZ,SWE,EA,R,RL,I0,I1,I2,SW,MT =TUW_WimClat(Rain_ens[:,i],Temp_ens[:,i],PET_ens[:,i],inic,area)
        I_ens[:,i]=I
     
    dates = num2date(days,'days since 1900-01-01')
    Dates_out = dates[0]
    I_ens_out = [np.zeros(np.shape(I_ens)[1])]
    Rain_ens_out = [np.zeros(np.shape(Rain_ens)[1])]
    Temp_ens_out = [np.zeros(np.shape(Temp_ens)[1])]
    PET_ens_out = [np.zeros(np.shape(PET_ens)[1])]
    
    count = 0    
    for i in np.arange(1,horizon+1,1):
        if tstep == 'daily':
            Dates_out    = dates
            I_ens_out = I_ens
            Rain_ens_out = Rain_ens
            Temp_ens_out = Temp_ens
            PET_ens_out  = PET_ens
        elif tstep == 'weekly':
            delta1 = 7
            count += delta1
            Dates_out    = np.append(Dates_out,[dates[count]])
            I_ens_out = np.append(I_ens_out,[np.sum(I_ens[count - delta1:count,:],axis =0)],axis = 0)
            Rain_ens_out = np.append(Rain_ens_out,[np.sum(Rain_ens[count - delta1:count,:],axis =0)],axis = 0)
            Temp_ens_out = np.append(Temp_ens_out,[np.mean(Temp_ens[count - delta1:count,:],axis =0)],axis = 0)
            PET_ens_out  = np.append(PET_ens_out,[np.sum(PET_ens[count - delta1:count,:],axis =0)],axis = 0)
        elif tstep == 'monthly':
            if month0+i-1>12:
                delta1 = monthrange(year0+1, month0+i-12-1)[1]
            else:
                delta1 = monthrange(year0, month0+i-1)[1]
            count += delta1
            Dates_out    = np.append(Dates_out,[dates[count]])
            I_ens_out = np.append(I_ens_out,[np.sum(I_ens[count - delta1:count,:],axis =0)],axis = 0)
            Rain_ens_out = np.append(Rain_ens_out,[np.sum(Rain_ens[count - delta1:count,:],axis =0)],axis = 0)
            Temp_ens_out = np.append(Temp_ens_out,[np.mean(Temp_ens[count - delta1:count,:],axis =0)],axis = 0)
            PET_ens_out  = np.append(PET_ens_out,[np.sum(PET_ens[count - delta1:count,:],axis =0)],axis = 0)
            
    return Dates_out, I_ens_out, Rain_ens_out, Temp_ens_out, PET_ens_out