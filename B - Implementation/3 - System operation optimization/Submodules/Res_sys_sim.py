# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:18:26 2019

@author: ap18525
"""
import numpy as np
#from numba import njit,prange

#@njit(parallel = False) # Set "nopython" mode for best performance, equivalent to @njit
def Res_sys_sim(I, e, s_0, s_min, s_max, Qreq_env, Qreq_dem, Qreg):

    # Evaporation volume (E) = evaporation depth * water surface area (A)
    """By default we assume A = 1 km2, but it should be modified according to 
    your reservoir charateristics and to take into account the variation of 
    the water surface area as a function of the water surface elevation""" 
    A = 1 # in km2. 
    E = e * A # in ML (= mm * km2) 
    
    # Time length
    T = I.shape[0]
    # Required environmental compensation flow
    Qreq_env = Qreq_env + np.zeros(T)
    # Required demand
    Qreq_dem = Qreq_dem + np.zeros(T)
    
    ### Declare output variables ###
    # Reservoir storage
    s = np.zeros(T)
    
    # Environmental flow
    Qenv = np.zeros(T)

    # Regulated releases + inflows
    if Qreg['rel_inf'] == None:
        Qreg_rel = np.zeros(T)
        Qreg_inf = np.zeros(T)
    elif isinstance(Qreg['rel_inf'],(dict)):
        exec('from Submodules.'+Qreg['rel_inf']['file_name']+' import '+Qreg['rel_inf']['function'])
        Qreg_rel = np.zeros(T)
        Qreg_inf = np.zeros(T)
   
    # Regulated water release
    if isinstance(Qreg['releases'],(np.ndarray)): # a release scheduling is provided as an input
        Qreg_rel = Qreg['releases'] + np.zeros(T)
    elif isinstance(Qreg['releases'],(dict)):
        exec('from Submodules.'+Qreg['releases']['file_name']+' import '+Qreg['releases']['function'])
    elif Qreg['releases'] == None: 
        Qreg_rel = Qreq_dem # releases = demand
        
    # Regulated inflows 
    if Qreg['inflows'] == None: 
        Qreg_inf = np.zeros(T)  # No regulated inflows
    elif isinstance(Qreg['inflows'],(np.ndarray)): # a regulated inflows scheduling is provided as an input
        Qreg_inf = Qreg['inflows'] + np.zeros(T)
    elif isinstance(Qreg['releases'],(dict)):
        exec('from Submodules.'+Qreg['inflows']['file_name']+' import '+Qreg['inflows']['function'])
        
    # Spillage
    Qspill = np.zeros(T)
    
    ### Initial conditions ###
    s[0] = s_0 # initial storage
    for k in range(T-1): # Loop for each time-step 
        t = k+1
        
        if isinstance(Qreg['rel_inf'],(dict)): # a dictionary with: the name of the function,  
            # file name where it is contained and the parameters of the function
            exec('Qreg_rel[t], Qreg_inf[t] = '+Qreg['rel_inf']['function']+'('+str(Qreg['rel_inf']['param'])+','+str(s[t-1]/s_max)+')')
            
        if isinstance(Qreg['releases'],(dict)): # a dictionary with: the name of the function,  
            # file name where it is contained and the parameters of the function
            exec('Qreg_rel[t] = '+Qreg['releases']['function']+'('+str(Qreg['releases']['param'])+','+str(s[t-1]/s_max)+')')
            
        if isinstance(Qreg['inflows'],(dict)): # a dictionary with: the name of the function,  
            # file name where it is contained and the parameters of the function
            exec('Qreg_inf[t] = '+Qreg['inflows']['function']+'('+str(Qreg['inflows']['param'])+','+str(s[t-1]/s_max)+')')
            
        # If at week t the inflow (I) is lower than the required environmental compensation (Qreq_env), 
        # then the environmental compensation (Qenv) = inflow (I). Otherwise Qenv = Qreq_env.
        if Qreq_env[t] >= I[t] + Qreg_inf[t] :
            Qenv[t] = I[t] + Qreg_inf[t]
        else:
            Qenv[t] = Qreq_env[t]
        # If the required environmental compensation is higher than the water resource available (s + I - e)
        # then the environmental compensation is equal to the higher value between 0 and the resource available  
        if Qreq_env[t] >= s[t-1] - s_min + I[t] + E[t] + Qreg_inf[t]:
            Qenv[t] = s[t-1] - s_min + I[t] + E[t] + Qreg_inf[t]
        else:
            Qenv[t] = Qreq_env[t]
        # If the demand (Qreq_dem) is higher than the water resource available (s + I - e - Qenv)
        # then the release for water supply is equal to the higher value between 0 and the resource available 
        # and the lower value between the latter and the pre-defined release (u)
        if Qreq_dem[t] >= s[t-1] - s_min + I[t] + E[t] + Qreg_inf[t] - Qenv[t]:
            Qreg_rel[t] = np.min([Qreg_rel[t],np.max([0,s[t-1] - s_min + I[t] + E[t] + Qreg_inf[t] - Qenv[t]])])
        # The spillage is equal to the higher value between 0 and the resource available exceeding the reservoir capacity
        Qspill[t] = np.max([0,s[t-1] + I[t] - Qreg_rel[t] - Qenv[t] + E[t] + Qreg_inf[t] - s_max])
        # The final storage (initial storage in the next step) is equal to the storage + inflow - outflows
        s[t] = s[t-1] + I[t] - Qreg_rel[t] - Qenv[t] + E[t] + Qreg_inf[t] - Qspill[t]
                
    outputs = (Qenv, Qspill, Qreg_rel, Qreg_inf, s)
    return outputs