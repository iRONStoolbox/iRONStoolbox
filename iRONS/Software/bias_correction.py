# -*- coding: utf-8 -*-
"""
This module contains functions to bias correct forecast data
The functions included are:
    linear_scaling

This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi and at 
Bristol University (2020).

Licence: MIT
"""

import numpy as np
#import sys
# Tools
#sys.path.append('../../Toolbox')
from irons.Software.read_data import read_netcdf_data

def linear_scaling(folder_path,file_name_end,
                   dates_fore,data_fore,
                   dates_obs,data_obs,
                   weather_variable):
    
    """ This function uses the linear scaling approach for bias correction 
    of forecast data. A bias monthly correction factor is calculated 
    considering the ratio (between the observed and the forecast 
    (ensemble mean) values. The correction factor obtained is then applied 
    as a multiplicative (rain and evaporation) or additive (temperature) 
    factor to correct raw daily forecast value.  A different factor is 
    calculated and applied for each month and each year of the evaluation 
    period.
    
    inputs = (folder_path,file_name_end,
              dates_fore,data_fore,
              dates_obs,data_obs,
              weather_variable)
    
    outputs = data_fore_corr
    
    folder_path      = path to the folder containing the forecast file
    file_name_end    = end of the file name
    dates_fore       = dates of the forecast values
    data_fore        = forecast values
    dates_obs        = dates of the observed/historical values
    data_obs         = observed values
    weather_variable = weather variable to bias correct:
        'Temp'       = temperature
        'e'          = evaporation
        'Rain'       = Rainfall
    
    data_fore_corr   = bias corrected forecast values
    
    References: 
        
    Crochemore, L., Ramos, M.-H., and Pappenberger, F.: Bias correcting 
    precipitation forecasts to improve the skill of seasonal streamflow 
    forecasts, Hydrol. Earth Syst. Sci., 20, 3601–3618
    
    """
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
    
            # Temperature

            if weather_variable == 'Temp':
                dates_ctrl, data_ctrl = read_netcdf_data(folder_path,
                                                         str(y)+str(fore_ini_month).zfill(2)+str(1).zfill(2)+file_name_end,
                                                         't2m')
                ID_ctrl = np.where((dates_ctrl.year>=clim_ini_year) & (dates_ctrl.month==m))[0]
                data_ctrl_ens = data_ctrl.mean(3).mean(2).mean(1)-273.15 # in degC
                data_ctrl_all = np.append(data_ctrl_all,
                                      np.reshape(data_ctrl_ens[ID_ctrl],
                                                 [np.size(data_ctrl_ens[ID_ctrl]),1]))
    
            # Evaporation
            elif weather_variable == 'e':
                dates_ctrl, data_ctrl = read_netcdf_data(folder_path,
                                                         str(y)+str(fore_ini_month).zfill(2)+str(1).zfill(2)+file_name_end,
                                                         'e')
                ID_ctrl = np.where((dates_ctrl.year>=clim_ini_year) & (dates_ctrl.month==m))[0]
                data_ctrl_cum = -data_ctrl.mean(3).mean(2).mean(1)*1000 # in mm
                data_ctrl_ens = np.zeros(np.shape(data_ctrl_cum))
                for j in np.arange(len(data_ctrl_cum[:])-1):
                    data_ctrl_ens[j+1] = np.maximum(data_ctrl_cum[j+1]-data_ctrl_cum[j],0)
                data_ctrl_all = np.append(data_ctrl_all,
                                         np.reshape(data_ctrl_ens[ID_ctrl],
                                                    [np.size(data_ctrl_ens[ID_ctrl]),1]))
            # Rainfall
            elif weather_variable == 'Rain':
                dates_ctrl, data_ctrl = read_netcdf_data(folder_path,
                                                         str(y)+str(fore_ini_month).zfill(2)+str(1).zfill(2)+file_name_end,
                                                         'tp')
                ID_ctrl = np.where((dates_ctrl.year>=clim_ini_year) & (dates_ctrl.month==m))[0]
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
        if weather_variable == 'Temp': # Additive factor
            data_bias_corr_factor = data_obs_mean - data_ctrl_mean
            data_bias_corr = data_scen + data_bias_corr_factor
            data_fore_corr[ID_scen] = data_bias_corr
        else: # Multiplicative factor
            data_bias_corr_factor = data_obs_mean / data_ctrl_mean
            data_bias_corr = data_scen*data_bias_corr_factor
            data_fore_corr[ID_scen] = data_bias_corr
            
    return data_fore_corr
