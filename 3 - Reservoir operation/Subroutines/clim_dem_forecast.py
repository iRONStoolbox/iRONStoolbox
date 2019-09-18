# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 16:35:37 2018

@author: ap18525
"""
import numpy as np

def forecast(days, members,inflow0=15,temp0=25):
    inflow = np.zeros([members,days])
    evap   = np.zeros([members,days])
    temp   = np.zeros([members,days])
    inflow_low = np.zeros([days])
    inflow_high = np.zeros([days])
    evap_low = np.zeros([days])
    evap_high = np.zeros([days])
    temp_low = np.zeros([days])
    temp_high = np.zeros([days])
    
    for i in range(days):
    
        inflow_low[i]  = np.maximum(inflow0*(1-(i+0.5)*0.2),0)
        inflow_high[i] = inflow0*(1+(i+0.5)*0.2)
        
        temp_low[i]  = np.maximum(temp0*(1-(i+0.5)*0.1),20)
        temp_high[i] = np.minimum(temp0*(1+(i+0.5)*0.1),35)
        
        for j in range(members):
            inflow[j,i] = np.random.uniform(inflow_low[i],inflow_high[i])
            temp[j,i] = np.random.uniform(temp_low[i],temp_high[i])
            
            
        evap = temp/10
        evap_low = temp_low/10
        evap_high = temp_high/10
        
        demand = temp
    uncertain = [inflow_low,inflow_high,evap_low,evap_high,temp_low,temp_high]
            
    return inflow, temp, evap, demand, uncertain