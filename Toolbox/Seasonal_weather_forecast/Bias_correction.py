# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:40:00 2019

@author: ap18525
"""

import numpy as np
import sys
# Tools
sys.path.append('../../Toolbox')
from Data_management.Read_data import read_netcdf_data

def linear_scaling(folder_path,file_name_end,
        dates_fore,data_fore,dates_obs,data_obs,weather_variable):
    
    clim_ini_year = dates_obs[0].year+1 # Initial climatology year
    
    fore_ini_year = dates_fore[0].year # Initial forecast year
    fore_ini_month = dates_fore[0].month # Initial forecast month
    fore_end_month = dates_fore[-1].month # Final forecast month
    
    if dates_fore[0].month>dates_fore[-1].month:
        num_months = fore_end_month - fore_ini_month + 1 + 12
    else:
        num_months = fore_end_month - fore_ini_month + 1
    
    data_fore_corr = np.zeros(np.shape(data_fore))
    
    for i in np.arange(0,num_months):
        if dates_fore[0].month+i<=12:
            m = fore_ini_month+i
        else:
            m = fore_ini_month+i-12
        data_ctrl_all = []
    
        # Mean observed weather data for a given month in all the climatology years
        ID_obs = np.where((dates_obs.year>=clim_ini_year) & (dates_obs.year<fore_ini_year) & (dates_obs.month==m))[0]
        data_obs_all  = data_obs[ID_obs]
        data_obs_mean = np.mean(data_obs_all[1:])
    
        # Control data for a given month in all the climatology years
        for y in np.arange(clim_ini_year,fore_ini_year):
    
            #Control/reference data
            dates_ctrl, data_ctrl = read_netcdf_data(folder_path,str(y)+str(fore_ini_month).zfill(2)+str(1).zfill(2)+file_name_end,
                                                     weather_variable)
    
            ID_ctrl = np.where((dates_ctrl.year>=clim_ini_year) & (dates_ctrl.month==m))[0]
    
            # Temperature
            if weather_variable == 't2m':
                data_ctrl_ens = data_ctrl.mean(3).mean(2).mean(1)-273.15 # in degC
                data_ctrl_all = np.append(data_ctrl_all,
                                      np.reshape(data_ctrl_ens[ID_ctrl],
                                                 [np.size(data_ctrl_ens[ID_ctrl]),1]))
    
    
            elif weather_variable == 'e':
                data_ctrl_cum = -data_ctrl.mean(3).mean(2).mean(1)*1000 # in mm
                data_ctrl_ens = np.zeros(np.shape(data_ctrl_cum))
                for j in np.arange(len(data_ctrl_cum[:])-1):
                    data_ctrl_ens[j+1] = np.maximum(data_ctrl_cum[j+1]-data_ctrl_cum[j],0)
                data_ctrl_all = np.append(data_ctrl_all,
                                         np.reshape(data_ctrl_ens[ID_ctrl],
                                                    [np.size(data_ctrl_ens[ID_ctrl]),1]))
    
            elif weather_variable == 'tp':
                data_ctrl_cum = data_ctrl.mean(3).mean(2).mean(1)*1000 # in mm 
                data_ctrl_ens = np.zeros(np.shape(data_ctrl_cum))
                for j in np.arange(len(data_ctrl_cum[:])-1):
                    data_ctrl_ens[j+1] = np.maximum(data_ctrl_cum[j+1]-data_ctrl_cum[j],0)
                data_ctrl_all = np.append(data_ctrl_all,
                                          np.reshape(data_ctrl_ens[ID_ctrl],
                                                     [np.size(data_ctrl_ens[ID_ctrl]),1]))
    
        # Define the raw forecast data for a given month
        ID_scen = np.where((dates_fore.year>=clim_ini_year) & (dates_fore.month==m))[0]
        data_scen = data_fore[ID_scen]
    
        # Mean control data
        data_ctrl_mean = np.mean(data_ctrl_all)
    
        # Bias correction factor for a given month
        if weather_variable == 't2m':
            data_bias_corr_factor = data_obs_mean - data_ctrl_mean
            data_bias_corr = data_scen + data_bias_corr_factor
            data_fore_corr[ID_scen] = data_bias_corr
        else:
            data_bias_corr_factor = data_obs_mean / data_ctrl_mean
            data_bias_corr = data_scen*data_bias_corr_factor
            data_fore_corr[ID_scen] = data_bias_corr
            
    return data_fore_corr
