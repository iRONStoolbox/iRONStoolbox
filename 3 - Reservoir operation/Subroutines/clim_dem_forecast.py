# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 16:35:37 2018

@author: ap18525

"""
import numpy as np

def forecast(N, members,inflow0=15,demand0=25):
    inflow = np.zeros([members,N])
    demand   = np.zeros([members,N])
    inflow_low = np.zeros([N])
    inflow_high = np.zeros([N])
    demand_low = np.zeros([N])
    demand_high = np.zeros([N])
    
    for i in range(N):
    
        inflow_low[i]  = np.maximum(inflow0*(1-(i+0.5)*0.2),0)
        inflow_high[i] = inflow0*(1+(i+0.5)*0.2)
        
        demand_low[i]  = np.maximum(demand0*(1-(i+0.5)*0.1),20)
        demand_high[i] = np.minimum(demand0*(1+(i+0.5)*0.1),35)
        
        for j in range(members):
            inflow[j,i] = np.random.uniform(inflow_low[i],inflow_high[i])
            demand[j,i] = np.random.uniform(demand_low[i],demand_high[i])
            
    return inflow, demand