# -*- coding: utf-8 -*-
"""
This is a function to transform daily data into weekly

This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi and at 
Bristol University (2020).

Licence: MIT
"""
import numpy as np
import pandas as pd
from datetime import timedelta

def day2week(N,dates,data):
    
    if data.ndim == 1:
        data = data.reshape([data.shape[0],1])
    
    delta = 7 # days of a week
    # Initial day
    date0 = dates[0]
    # Day of the week of the initial day (Monday = 0,..., Sunday = 6)
    wday0 = date0.weekday()
    # We define the inital date according to the day of the week we would like to start with, in this case Monday
    if wday0 != 0:
        date_ini = date0 + timedelta(days = 7-wday0)
    else:
        date_ini = date0
    # Given the initial date and the forecast horizon we now get the final date
    date_end = date_ini + timedelta(days = N*7) # day_ini + horizon weeks * 7 days/week
    if (date_end-dates[-1]).days > 0:
        print('Error: The defined horizon is too long, please try with a lower number of weeks')
    
    index_ini = np.where(dates==date_ini)[0][0]
    dates_week = dates[index_ini]
    data_week = [np.zeros(np.shape(data)[1])]
    data_cum_week = [np.zeros(np.shape(data)[1])]
    
    for i in np.arange(N)+1:
        dates_week = np.append(dates_week,[dates[index_ini+i*delta]])
        data_week = np.append(data_week,[np.sum(data[index_ini+np.max([i-1,0])*delta:index_ini+i*delta,:],axis =0)],axis = 0)
        data_cum_week = np.append(data_cum_week,[np.sum(data[index_ini:index_ini+i*delta,:],axis =0)],axis = 0)
    dates_week = pd.to_datetime(dates_week)
    
    return dates_week,data_week,data_cum_week