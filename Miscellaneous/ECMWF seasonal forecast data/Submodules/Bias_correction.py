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
#import matplotlib.pyplot as plt
from netCDF4 import Dataset
from netCDF4 import date2num
import datetime
import os.path

def Bias_correction(provider, year, month,day,horizon):
    
    PET_obs = []
    PET_ctrl = []
    Rain_obs = []
    Rain_ctrl = []
    Temp_obs = []
    Temp_ctrl = []
    
    for y in np.arange(1981,year):
    
        if provider == 'ECMWF':
            if os.path.exists(provider+"//"+str(y)+str(month).zfill(2)+str(1).zfill(2)+"_1d_7m_"+provider+"_Temp_Evap_Rain.nc"):
                output = Dataset(provider+"//"+str(y)+str(month).zfill(2)+str(1).zfill(2)+"_1d_7m_"+provider+"_Temp_Evap_Rain.nc", "r")
            elif os.path.exists("..//"+provider+"//"+str(y)+str(month).zfill(2)+str(1).zfill(2)+"_1d_7m_"+provider+"_Temp_Evap_Rain.nc"):
                output = Dataset("..//"+provider+"//"+str(y)+str(month).zfill(2)+str(1).zfill(2)+"_1d_7m_"+provider+"_Temp_Evap_Rain.nc", "r")
        elif provider == 'UKMO':
            if os.path.exists(provider+"//"+str(y)+str(month).zfill(2)+str(1).zfill(2)+"_1d_7m_"+provider+"_sys_12_Temp_Evap_Rain.nc"):
                output = Dataset(provider+"//"+str(y)+str(month).zfill(2)+str(1).zfill(2)+"_1d_7m_"+provider+"_sys_12_Temp_Evap_Rain.nc", "r")
            elif os.path.exists("..//"+provider+"//"+str(y)+str(month).zfill(2)+str(1).zfill(2)+"_1d_7m_"+provider+"_sys_12_Temp_Evap_Rain.nc"):
                output = Dataset("..//"+provider+"//"+str(y)+str(month).zfill(2)+str(1).zfill(2)+"_1d_7m_"+provider+"_sys_12_Temp_Evap_Rain.nc", "r")        
        
        temperature=output.variables['t2m'][:] # in degK
        evaporation=output.variables['e'][:]*1000
        precipitation=output.variables['tp'][:]*1000
        
        temp_ensemble = temperature.mean(3)
        temp_ensemble = temp_ensemble.mean(2)-273.15 # in degC
        
        cum_evap_ensemble = -evaporation.mean(3)
        cum_evap_ensemble = cum_evap_ensemble.mean(2)
        evap_ensemble = np.zeros(np.shape(cum_evap_ensemble))
        for i in np.arange(len(cum_evap_ensemble[0,:])):
            for j in np.arange(len(cum_evap_ensemble[:,0])-1):
                evap_ensemble[j+1,i] = np.maximum(cum_evap_ensemble[j+1,i]-cum_evap_ensemble[j,i],0)
        
        cum_precip_ensemble = precipitation.mean(3)
        cum_precip_ensemble = cum_precip_ensemble.mean(2)
        precip_ensemble = np.zeros(np.shape(cum_precip_ensemble))
        for i in np.arange(len(cum_precip_ensemble[0,:])):
            for j in np.arange(len(cum_precip_ensemble[:,0])-1):
                precip_ensemble[j+1,i] = np.maximum(cum_precip_ensemble[j+1,i]-cum_precip_ensemble[j,i],0)
        
        day_ini = int(date2num(datetime.datetime(y, month, day, 0, 0),'days since 1900-01-01'))

        day_end = day_ini+horizon*7 # day_ini + horizon weeks * 7 days/week
        
        Rain_ens = precip_ensemble[0:day_end-day_ini]
        Temp_ens = temp_ensemble[0:day_end-day_ini]
        PET_ens  = evap_ensemble[0:day_end-day_ini] # The forecast has negative PET values while the observed are positive
        
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
            
        # Observed data
        PET_obs = np.append(PET_obs,PET[np.where(bf_day==day_ini)[0][0]:np.where(bf_day==day_end)[0][0]],axis = 0)
        Rain_obs = np.append(Rain_obs,Rain[np.where(bf_day==day_ini)[0][0]:np.where(bf_day==day_end)[0][0]],axis = 0)
        Temp_obs = np.append(Temp_obs,Temp[np.where(bf_day==day_ini)[0][0]:np.where(bf_day==day_end)[0][0]],axis = 0)
        
        # Control data (average of the forecast members)
#        PET_ctrl = np.append(PET_ctrl,np.mean(PET_ens,axis=1),axis = 0)
#        Rain_ctrl = np.append(Rain_ctrl,np.mean(Rain_ens,axis=1),axis = 0)
#        Temp_ctrl = np.append(Temp_ctrl,np.mean(Temp_ens,axis=1),axis = 0)
        
        # Control data (all forecast members)
        PET_ctrl = np.append(PET_ctrl,np.reshape(PET_ens,(np.size(PET_ens),)),axis = 0)
        Rain_ctrl = np.append(Rain_ctrl,np.reshape(Rain_ens,(np.size(Rain_ens),)),axis = 0)
        Temp_ctrl = np.append(Temp_ctrl,np.reshape(Temp_ens,(np.size(Temp_ens),)),axis = 0)
        
    PET_ens_md = np.zeros(np.shape(PET_ens))
    Rain_ens_md = np.zeros(np.shape(Rain_ens))
    Temp_ens_md = np.zeros(np.shape(Temp_ens))
    
    PET_ens_qm = np.zeros(np.shape(PET_ens))
    Rain_ens_qm = np.zeros(np.shape(Rain_ens))
    Temp_ens_qm = np.zeros(np.shape(Temp_ens))
      
    # In[] Bias correction - Quantile mapping
    # Quantile mapping
    def quan_map(vals):
        """ CDF mapping for bias correction """
        """ note that values exceeding the range of the training set"""
        """ are set to -999 at the moment - possibly could leave unchanged?"""
        # calculate exact CDF values using linear interpolation
        #
        cdf1=np.interp(vals,xbins,cdfmod,left=0.0,right=999.0)
        # now use interpol again to invert the obsCDF, hence reversed x,y
        corrected=np.interp(cdf1,cdfobs,xbins,left=0.0,right=-999.0)
        return corrected
    cdfn=10
    
    # PET
    # sort the arrays
    PET_obs_sort=np.sort(PET_obs)
    PET_for_sort=np.sort(PET_ctrl)
    # calculate the global max and bins.
    global_max=max(np.amax(PET_obs_sort),np.amax(PET_for_sort))
    wide=global_max/cdfn
    xbins=np.arange(0.0,global_max+wide,wide)
    # create PDF
    pdfobs,bins=np.histogram(PET_obs_sort,bins=xbins)
    pdfmod,bins=np.histogram(PET_for_sort,bins=xbins)
    # create CDF with zero in first entry.
    cdfobs=np.insert(np.cumsum(pdfobs),0,0.0)/np.size(Rain_obs)
    cdfmod=np.insert(np.cumsum(pdfmod),0,0.0)/np.size(Rain_ctrl)
    
    # Bias correct each member of the ensemble
    for i in np.arange(np.shape(PET_ens)[1]):
        PET_ens_md[:,i] = PET_ens[:,i]*np.mean(PET_obs)/np.mean(PET_ctrl)
        PET_ens_qm[:,i] = quan_map(PET_ens[:,i])
    
    # Rainfall
    # sort the arrays
    Rain_obs_sort=np.sort(Rain_obs)
    Rain_for_sort=np.sort(Rain_ctrl)
    # calculate the global max and bins.
    global_max=max(np.amax(Rain_obs_sort),np.amax(Rain_for_sort))
    wide=global_max/cdfn
    xbins=np.arange(0.0,global_max+wide,wide)
    # create PDF
    pdfobs,bins=np.histogram(Rain_obs_sort,bins=xbins)
    pdfmod,bins=np.histogram(Rain_for_sort,bins=xbins)
    # create CDF with zero in first entry.
    cdfobs=np.insert(np.cumsum(pdfobs),0,0.0)/np.size(Rain_obs)
    cdfmod=np.insert(np.cumsum(pdfmod),0,0.0)/np.size(Rain_ctrl)
    
    # Bias correct each member of the ensemble
    for i in np.arange(np.shape(Rain_ens)[1]):
        Rain_ens_md[:,i] = Rain_ens[:,i]*np.mean(Rain_obs)/np.mean(Rain_ctrl)
        Rain_ens_qm[:,i] = quan_map(Rain_ens[:,i])
        
    # Temperature
    # sort the arrays
    Temp_obs_sort=np.sort(Temp_obs)
    Temp_for_sort=np.sort(Temp_ctrl)
    # calculate the global max and bins.
    global_max=max(np.amax(Temp_obs_sort),np.amax(Temp_for_sort))
    wide=global_max/cdfn
    xbins=np.arange(0.0,global_max+wide,wide)
    # create PDF
    pdfobs,bins=np.histogram(Temp_obs_sort,bins=xbins)
    pdfmod,bins=np.histogram(Temp_for_sort,bins=xbins)
    # create CDF with zero in first entry.
    cdfobs=np.insert(np.cumsum(pdfobs),0,0.0)/np.size(Rain_obs)
    cdfmod=np.insert(np.cumsum(pdfmod),0,0.0)/np.size(Rain_ctrl)
    
    # Bias correct each member of the ensemble
    for i in np.arange(np.shape(Temp_ens)[1]):
        Temp_ens_md[:,i] = Temp_ens[:,i]*np.mean(Temp_obs)/np.mean(Temp_ctrl)
        Temp_ens_qm[:,i] = quan_map(Temp_ens[:,i])
        
    return PET_ens_md, Rain_ens_md, Temp_ens_md,PET_ens_qm, Rain_ens_qm, Temp_ens_qm