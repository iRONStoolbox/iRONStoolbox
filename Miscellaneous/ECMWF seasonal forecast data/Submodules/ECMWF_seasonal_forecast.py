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
from netCDF4 import Dataset
from netCDF4 import num2date,date2num
import datetime
from Submodules.TUW_WimClat_Sim import TUW_WimClat # TUW hydrological model

def ECMWF_seasonal_forecast(provider, year, month,day,horizon,area):

    output = Dataset(provider+"//"+str(year)+str(month).zfill(2)+str(1).zfill(2)+"_1d_7m_"+provider+"_Temp_Evap_Rain.nc", "r")

    dates = num2date(output['time'][:]-24,units=output['time'].units) # the data is given every 24 h, so the it always starts the next day at 00:00
    # we need to substract one day (-24h) to reflect that the first data member corresponds to the first day and not to the next day at 00:00

# =============================================================================
#     for i in output.variables:
#         print(output.variables[i].dimensions)
#         
#     print(output.dimensions)
#     print("number of dimensions ="+str(len(output.dimensions)))
#     for key in output.dimensions:
#         print("dimension["+key+"] = "+str(len(output.dimensions[key])))
# =============================================================================
    
    #Attributes
#    gattrs=output.ncattrs()
 #   ngattrs=len(gattrs)
# =============================================================================
#     print("number of global attributes="+str(ngattrs))
#     
#     for key in gattrs:
#         print("global attribute["+key+"]="+str(str(getattr(output,key))))
# =============================================================================
        
#    vars=output.variables
#    nvars=len(vars)
#    print("number of variables ="+str(nvars))
    
#    for var in vars:
#        print("-------variable '"+var+"'--------")
#        print("shape="+str(vars[var].shape)) #dimensions of the variable; shape is a tuple
#        vdims=vars[var].dimensions
#        for vd in vdims:
#            print("dimensions["+vd+"]="+str(len(output.dimensions[vd]))) #print the length
            
    # Dimension and attributes of each variable
#        vattrs=vars[var].ncattrs()
#        print("number of attributes="+str(len(vattrs)))
#        for vat in vattrs:
#            print("attribute["+vat+"]="+str(getattr(vars[var],vat)))
    
    temperature=output.variables['t2m'][:] # in degK
    evaporation=output.variables['e'][:]*1000
    precipitation=output.variables['tp'][:]*1000
    
    temp_ensemble = temperature.mean(3)
    temp_ensemble = temp_ensemble.mean(2)-273.15 # in degC
    
    cum_evap_ensemble = evaporation.mean(3)
    cum_evap_ensemble = cum_evap_ensemble.mean(2)
    evap_ensemble = np.zeros(np.shape(cum_evap_ensemble))
    for i in np.arange(len(cum_evap_ensemble[0,:])):
        for j in np.arange(len(cum_evap_ensemble[:,0])-1):
            evap_ensemble[j+1,i] = cum_evap_ensemble[j+1,i]-cum_evap_ensemble[j,i]
    
    cum_precip_ensemble = precipitation.mean(3)
    cum_precip_ensemble = cum_precip_ensemble.mean(2)
    precip_ensemble = np.zeros(np.shape(cum_precip_ensemble))
    for i in np.arange(len(cum_precip_ensemble[0,:])):
        for j in np.arange(len(cum_precip_ensemble[:,0])-1):
            precip_ensemble[j+1,i] = cum_precip_ensemble[j+1,i]-cum_precip_ensemble[j,i]
    
    day0 = int(date2num(datetime.datetime(year, month, day, 0, 0),'days since 1900-01-01'))
    yday0 = datetime.datetime(year, month, day, 0, 0).weekday() # 
    
    if yday0 >3:
        day_ini = day0 + (7-yday0)
    else:
        day_ini = day0 - yday0
    if num2date(day_ini,'days since 1900-01-01').month < month:
        day_ini = day_ini + 7 # Next Monday instead of the previous one
    elif num2date(day_ini,'days since 1900-01-01').month > month:
        day_ini = day_ini - 7 # Last Monday instead of the next one
    
    day_end = day_ini+horizon*7 # day_ini + horizon weeks * 7 days/week
    
    days = np.arange(day_ini,day_end+1,1)

    Rain_ens = precip_ensemble[0:day_end-day_ini]
    Temp_ens = temp_ensemble[0:day_end-day_ini]
    PET_ens = evap_ensemble[0:day_end-day_ini]
    
    I_sf = Rain_ens*0 + np.nan
    
    # Climate data 1968-2018
    filename = 'Data//ClimdataWim.csv'

    bf_date_str = np.genfromtxt(filename, delimiter = ',',skip_header=1,usecols=0,dtype='str')
    bf_date = [datetime.datetime.strptime(bf_date_str[i], '%d/%m/%Y') for i in range(len(bf_date_str))]
    bf_day = date2num(bf_date,'days since 1900-01-01').astype('int')
    weather_data = np.genfromtxt(filename, delimiter = ',',skip_header=1)
    PET = weather_data[0:,1]
    Rain = weather_data[0:,2]
    Temp = weather_data[0:,3]

    # Warm-up
    inic = [50,2.5,2.5,0]
    wu_ini = int(date2num(datetime.datetime(1968, 1, 1, 0, 0),'days since 1900-01-01'))
    wu_end = day_ini
    I_wu,STATES_wu,FLUXES_wu =TUW_WimClat(Rain[np.where(bf_day==wu_ini)[0][0]:np.where(bf_day==wu_end)[0][0]],Temp[np.where(bf_day==wu_ini)[0][0]:np.where(bf_day==wu_end)[0][0]],PET[np.where(bf_day==wu_ini)[0][0]:np.where(bf_day==wu_end)[0][0]],inic,area,1)
    
    sf_inic = [STATES_wu[0][-1],STATES_wu[1][-1],STATES_wu[2][-1],STATES_wu[3][-1]]
    
    for i in range(np.size(Rain_ens, axis = 1)):
        HBV_I_sf,STATES_sf,FLUXES_sf =TUW_WimClat(Rain_ens[:,i],Temp_ens[:,i],PET_ens[:,i],sf_inic,area,1)
        I_sf[:,i]=HBV_I_sf
    I_sf_ens = I_sf
    
    dates = num2date(days,'days since 1900-01-01')
    dates_w = dates[0]
    I_sf_ens_w = [np.zeros(np.shape(I_sf_ens)[1])]
    Rain_ens_w = [np.zeros(np.shape(Rain_ens)[1])]
    Temp_ens_w = [np.zeros(np.shape(Temp_ens)[1])]
    PET_ens_w = [np.zeros(np.shape(PET_ens)[1])]
    for i in np.arange(1,horizon+1,1):
        dates_w = np.append(dates_w,[dates[i*7]])
        I_sf_ens_w = np.append(I_sf_ens_w,[np.sum(I_sf_ens[(i-1)*7:i*7,:],axis =0)],axis = 0)
        Rain_ens_w = np.append(Rain_ens_w,[np.sum(Rain_ens[(i-1)*7:i*7,:],axis =0)],axis = 0)
        Temp_ens_w = np.append(Temp_ens_w,[np.sum(Temp_ens[(i-1)*7:i*7,:],axis =0)],axis = 0)
        PET_ens_w = np.append(PET_ens_w,[np.sum(PET_ens[(i-1)*7:i*7,:],axis =0)],axis = 0)
        
    return dates_w, I_sf_ens_w,Rain_ens_w,Temp_ens_w,PET_ens_w