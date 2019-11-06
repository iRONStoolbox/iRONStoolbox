# -*- coding: utf-8 -*-
"""
v3: option to select the time step(daily, weekly or monthly)
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
import os.path
if os.path.exists("Submodules"):
    from Submodules.TUW_WimClat_Sim import TUW_WimClat # TUW hydrological model
else:
    from TUW_WimClat_Sim import TUW_WimClat # TUW hydrological model

def Seasonal_forecast_v3(provider, year0, month0,day,horizon,area,tstep,bias='No BC'):
    
    area = np.array([area])
    
    data = np.load(provider+"//Bias corrected - "+bias+"//"+str(year0)+str(month0).zfill(2)+str(1).zfill(2)+"_1d_7m_"+provider+"_Temp_Evap_Rain.npy")

    temp_ensemble = data[:,:,1]
    
    evap_ensemble = data[:,:,2]
    
    precip_ensemble = data[:,:,3]
    
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

    Rain_ens = precip_ensemble[0:day_end-day_ini+1] 
    Temp_ens = temp_ensemble[0:day_end-day_ini+1] 
    PET_ens = - evap_ensemble[0:day_end-day_ini+1] 

    # Climate data 1968-2018
    if os.path.exists('Data//ClimdataWim.csv'):
        filename = 'Data//ClimdataWim.csv'
    elif os.path.exists('..//Data//ClimdataWim.csv'):
        filename = '..//Data//ClimdataWim.csv'

    bf_date_str = np.genfromtxt(filename, delimiter = ',',skip_header=1,usecols=0,dtype='str')
    bf_date = [datetime.datetime.strptime(bf_date_str[i], '%d/%m/%Y') for i in range(len(bf_date_str))]
    bf_day = date2num(bf_date,'days since 1900-01-01').astype('int')
    weather_data = np.genfromtxt(filename, delimiter = ',',skip_header=1)
    PET = weather_data[0:,1]
    Rain = weather_data[0:,2]
    Temp = weather_data[0:,3]
    
    # In[] Warm-up
    inic = np.array([50,2.5,2.5,0])
    wu_ini = int(date2num(datetime.datetime(1968, 1, 1, 0, 0),'days since 1900-01-01'))
    wu_end = day_ini
    PET_wu = PET[np.where(bf_day==wu_ini)[0][0]:np.where(bf_day==wu_end)[0][0]]
    Rain_wu = Rain[np.where(bf_day==wu_ini)[0][0]:np.where(bf_day==wu_end)[0][0]]
    Temp_wu = Temp[np.where(bf_day==wu_ini)[0][0]:np.where(bf_day==wu_end)[0][0]]
    I_wu,SM_wu,UZ_wu,LZ_wu,SWE_wu,EA_wu,R_wu,RL_wu,I0_wu,I1_wu,I2_wu,SW_wu,MT_wu =TUW_WimClat(Rain_wu,Temp_wu,PET_wu,inic,area)
    sf_inic = np.array([SM_wu[-1],UZ_wu[-1],LZ_wu[-1],SWE_wu[-1]])
    
    I_sf = Rain_ens*0 + np.nan
    
    for i in range(np.size(Rain_ens, axis = 1)):
    
        HBV_I_sf,SM_sf,UZ_sf,LZ_sf,SWE_sf,EA_sf,R_sf,RL_sf,I0_sf,I1_sf,I2_sf,SW_sf,MT_sf =TUW_WimClat(Rain_ens[:,i],Temp_ens[:,i],PET_ens[:,i],sf_inic,area)
        I_sf[:,i]=HBV_I_sf
    
    I_sf_ens = I_sf
    
    dates = num2date(days,'days since 1900-01-01')
    Dates_out = dates[0]

    I_sf_ens_out = [np.zeros(np.shape(I_sf_ens)[1])]
    Rain_ens_out = [np.zeros(np.shape(Rain_ens)[1])]
    Temp_ens_out = [np.zeros(np.shape(Temp_ens)[1])]
    PET_ens_out = [np.zeros(np.shape(PET_ens)[1])]
    count = 0
    for i in np.arange(1,horizon+1,1):
        if tstep == 'daily':
            Dates_out    = dates
            I_sf_ens_out = I_sf_ens
            Rain_ens_out = Rain_ens
            Temp_ens_out = Temp_ens
            PET_ens_out  = PET_ens
        elif tstep == 'weekly':
            delta1 = 7
            count += delta1
            Dates_out    = np.append(Dates_out,[dates[count]])
            I_sf_ens_out = np.append(I_sf_ens_out,[np.sum(I_sf_ens[count - delta1:count,:],axis =0)],axis = 0)
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
            I_sf_ens_out = np.append(I_sf_ens_out,[np.sum(I_sf_ens[count - delta1:count,:],axis =0)],axis = 0)
            Rain_ens_out = np.append(Rain_ens_out,[np.sum(Rain_ens[count - delta1:count,:],axis =0)],axis = 0)
            Temp_ens_out = np.append(Temp_ens_out,[np.mean(Temp_ens[count - delta1:count,:],axis =0)],axis = 0)
            PET_ens_out  = np.append(PET_ens_out,[np.sum(PET_ens[count - delta1:count,:],axis =0)],axis = 0)
        
    return Dates_out, I_sf_ens_out,Rain_ens_out,Temp_ens_out,PET_ens_out