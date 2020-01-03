# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 16:33:48 2019

@author: ap18525
"""
import numpy as np
from netCDF4 import num2date,date2num
from datetime import datetime
from bqplot.traits import convert_to_date

def Climate_data(year):
    forc_inputs_file = 'Input data/input_data_68_11.txt'
    forc_inputs_date_str = np.genfromtxt(forc_inputs_file, dtype='str',skip_header=1,delimiter = '\t',usecols=[0])
    forc_inputs_date = [datetime.strptime(i, '%d/%m/%Y') for i in forc_inputs_date_str]
    
    PET  = np.genfromtxt(forc_inputs_file, dtype='float',skip_header=1,delimiter = '\t',usecols=[1])
    Rain = np.genfromtxt(forc_inputs_file, dtype='float',skip_header=1,delimiter = '\t',usecols=[2])
    Temp = np.genfromtxt(forc_inputs_file, dtype='float',skip_header=1,delimiter = '\t',usecols=[3])
    
    day_ini = date2num(datetime(year, 1, 1, 0, 0),'days since 1900-01-01')
    day_end = date2num(datetime(year, 12, 31, 0, 0),'days since 1900-01-01')
    
    day_ini_idx = np.where(forc_inputs_date==np.datetime64(num2date(day_ini,'days since 1900-01-01')))[0][0]
    day_end_idx = np.where(forc_inputs_date==np.datetime64(num2date(day_end,'days since 1900-01-01')))[0][0]
    
    date = convert_to_date(forc_inputs_date[day_ini_idx:day_end_idx])
    ept = PET[day_ini_idx:day_end_idx]
    P = Rain[day_ini_idx:day_end_idx]
    T = Temp[day_ini_idx:day_end_idx]
    
    if year == 2000:
        P = P*1.5 # Artificially modified to have a wetter calibration year than the evaluation year (2001)
    
    return date,ept, P, T

def Flow_data(year):
    # Flow data
    Q_obs_file = 'Input data/cal_data_72_03.txt'
    Q_obs_date_str = np.genfromtxt(Q_obs_file, dtype='str',skip_header=1,delimiter = ' ',usecols=[0])
    Q_obs_date = [datetime.strptime(i, '%Y-%m-%d') for i in Q_obs_date_str]
    Q_obs = np.genfromtxt(Q_obs_file, dtype='float',skip_header=1,delimiter = ' ',usecols=[1])*60*60*24/10**3 # from m3/s to ML/day
    
    day_ini = date2num(datetime(year, 1, 1, 0, 0),'days since 1900-01-01')
    day_end = date2num(datetime(year, 12, 31, 0, 0),'days since 1900-01-01')
    
    day_ini_idx = np.where(Q_obs_date==np.datetime64(num2date(day_ini,'days since 1900-01-01')))[0][0]
    day_end_idx = np.where(Q_obs_date==np.datetime64(num2date(day_end,'days since 1900-01-01')))[0][0]
    
    date = convert_to_date(Q_obs_date[day_ini_idx:day_end_idx])
    Q_obs = Q_obs[day_ini_idx:day_end_idx]
    
    if year == 2000:
        Q_obs = Q_obs*1.5 # Artificially modified to have a wetter calibration year than the evaluation year (2001)
    
    return date, Q_obs