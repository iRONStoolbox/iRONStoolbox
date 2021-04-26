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

def day2week(dates,data,date_ini=None,date_end=None):
    
    if data.ndim == 1:
        data = data.reshape([data.shape[0],1])
    
    delta = 7 # days of a week
    # Initial day
    if date_ini==None:
        date_ini = dates[0]
    else:
        if (dates[0]-date_ini).days > 0:
            raise Exception('Error: The defined initial date is not within the data period, please try with a date equal or later than '+str(dates[-1]))
    
#    # Day of the week of the initial day (Monday = 0,..., Sunday = 6)
#    wday0 = date_ini.weekday()
#    # We define the inital date according to the day of the week we would like to start with, in this case Monday
#    if wday0 != 0:
#        date_ini = date_ini + timedelta(days = 7-wday0)

#    # Now we get the final date
    if date_end==None:
        date_end = dates[-1]
    else:
        if (date_end-dates[-1]).days > 0:
            raise Exception('Error: The defined end date is not within the data period, please try with a date equal or earlier than '+str(dates[-1]))
        
    N = (date_end - date_ini).days//7 # number of entire weeks
    date_end = date_ini + timedelta(days = N*7) # day_ini + horizon weeks * 7 days/week

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