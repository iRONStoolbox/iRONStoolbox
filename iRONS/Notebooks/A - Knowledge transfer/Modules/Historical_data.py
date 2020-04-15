# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 16:33:48 2019

@author: ap18525
"""
import numpy as np
import pandas as pd

def Climate_data(year):
    data = pd.read_csv('Inputs/input_data.csv')
    forc_inputs_date = pd.to_datetime(np.array(data['Date']),format = '%d/%m/%Y')
    
    PET  = np.array(data['PET'])
    Rain = np.array(data['Rain'])
    Temp = np.array(data['Temp'])
    
    day_ini_idx = np.where(forc_inputs_date==pd.Timestamp('01/01/'+str(year)))[0][0]
    day_end_idx = np.where(forc_inputs_date==pd.Timestamp('31/12/'+str(year)))[0][0]
    
    date = forc_inputs_date[day_ini_idx:day_end_idx]
    ept = PET[day_ini_idx:day_end_idx]
    P = Rain[day_ini_idx:day_end_idx]
    T = Temp[day_ini_idx:day_end_idx]
    
    if year == 2000:
        P = P*1.5 # Artificially modified to have a wetter calibration year than the evaluation year (2001)
    
    return date,ept, P, T

def Flow_data(year):
    # Flow data
    data = pd.read_csv('Inputs/cal_data.csv')
    Q_obs_date = pd.to_datetime(np.array(data['Date']),format = '%d/%m/%Y')
    
    Q_obs  = np.array(data['Inflow'])*60*60*24/10**3 # from m3/s to ML/day
    
    day_ini_idx = np.where(Q_obs_date==pd.Timestamp('01/01/'+str(year)))[0][0]
    day_end_idx = np.where(Q_obs_date==pd.Timestamp('31/12/'+str(year)))[0][0]
    
    date = Q_obs_date[day_ini_idx:day_end_idx]
    Q_obs = Q_obs[day_ini_idx:day_end_idx]
    
    if year == 2000:
        Q_obs = Q_obs*1.5 # Artificially modified to have a wetter calibration year than the evaluation year (2001)
    
    return date, Q_obs