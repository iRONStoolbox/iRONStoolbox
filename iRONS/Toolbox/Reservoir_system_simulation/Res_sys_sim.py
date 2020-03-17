# -*- coding: utf-8 -*-
"""
This function implements the reservoir simulation model (Res_sys_sim). First,
it extracts and process the regulated flows contained in the Qreg variable. 
This makes the regulated flow data readable by the mass balance function 
(Mass_bal_func). Then, Mass_bal_func links all the key variables that represent 
the reservoir dynamics (inflow, storage and outflows).

@author: Andres Peñuela
"""
import numpy as np
from numba import njit

### Mass balance function ###
@njit(parallel = False) # Numba decorator to speed-up the function below
def Mass_bal_func(I, e, 
                  s_0, s_min, s_max, 
                  env_min, 
                  Qreg_inf, Qreg_rel, 
                  s_frac, 
                  Policy_inf, Policy_rel):
    """
    The mathematical model (Mass_bal_func) of the reservoir essentially consists 
    of a water balance equation, where the storage (s) at a future time step 
    (for example, at the beginning of the next week) is predicted from the storage 
    at the current time (the beginning of the this week) by adding and subtracting 
    the inflows and outflows that will occur during the temporal interval ahead:
    
    s(t+1) = s(t) + I(t) + Qreg_inf – E(t) – env(t) - spill(t) – Qreg_rel(t)
    
    Where
    
    s(t) = reservoir storage at time-step t, in Vol (for example: ML)
    
    I(t) = reservoir inflows in the interval [t,t+1], in Vol/time (for example: 
           ML/week). This is usually provided by a flow forecasting system or 
           assumed by looking, for example, at historical inflow records for the 
           relevant time of year
    
    E(t) = evaporation from the reservoir surface area in the interval [t,t+1], in 
           Vol/time (for example: ML/week). This is calculated internally to the 
           model, by multipling the evaporation rate for unit surface area 
           (e(t)) by the reservoir surface area (which is derived from the storage 
           S given that the reservoir geometry is known)
    
    env(t) = environmental compensation flow in the interval [t,t+1], in Vol/time 
             (for example: ML/week). This is usually set to the value that was 
             agreed upon with the environemtal regulator
    
    spill(t) = outflow through spillways (if any) in the interval [t,t+1], in 
               Vol/time (for example: ML/week). This is calculated internally to 
               the model, and is equal to the excess volume with respect to the 
               maximum reservoir capacity (so most of the time spill(t) is 
               equal to 0 as the maximum capacity is not reached, but it 
               occasionally is >0 so that the capacity is never exceeded)
    
    Qreg_inf(t) = reservoir regulated inflows in the interval [t,t+1], in Vol/time 
                  (for example: ML/week). This is a completely free variable that 
                  the reservoir operator will need to specify
    
    Qreg_rel(t) = reservoir regulated release for water supply in the interval 
                  [t,t+1], in Vol/time (for example: ML/week). This is a completely 
                  free variable that the reservoir operator will need to specify
                  
    Policy related inputs: s_frac, Policy_inf, Policy_rel
    """
    
    T = I.shape[0]
    ### Declare output variables ###
    # Reservoir storage
    s = np.zeros(T+1)
    
    # Environmental flow
    env = np.zeros(T)

    # Spillage
    spill = np.zeros(T)
    
    # Evaporation
    E = np.zeros(T)
    
    ### Initial conditions ###
    s[0] = s_0 # initial storage
    
    for t in range(T): # Loop for each time-step
        
        if not np.isnan(Policy_inf[0]):
            Qreg_inf[t] = np.interp(s[t]/s_max, s_frac, Policy_inf)
        
        if not np.isnan(Policy_rel[0]):
            Qreg_rel[t] = np.interp(s[t]/s_max, s_frac, Policy_rel) 
        
        ### Evaporation volume ### 
        # (E) = evaporation depth * water surface area (A)
        # By default we assume A = 1 km2, but it should be modified according 
        # to your reservoir charateristics and to take into account the 
        # variation of the water surface area as a function of the water 
        # surface elevation""" 
        A = 1 # in km2. 
        E[t] = e[t] * A # in ML (= mm * km2) 
        
        # If at week t the inflow (I) is lower than the required environmental compensation (env_min), 
        # then the environmental compensation (Qenv) = total inflows (natural + regulated). Otherwise Qenv = env_min.
        if env_min[t] >= I[t] + Qreg_inf[t] :
            env[t] = I[t] + Qreg_inf[t]
        else:
            env[t] = env_min[t]
        # If the required environmental compensation is higher than the water resource available (s + I - E)
        # then the environmental compensation is equal to the higher value between 0 and the resource available  
        if env_min[t] >= s[t] - s_min + I[t] + Qreg_inf[t] - E[t]:
            env[t] = np.array([0,s[t] - s_min + I[t] + Qreg_inf[t] - E[t]]).max()
        else:
            env[t] = env_min[t]
        # If the regulated release (Qreg_rel) is higher than the water resource available (s + I - E - Qenv)
        # then the release is equal to the lower value between the resource available and the pre-defined release (Qreg_rel)
        Qreg_rel[t] = np.array([Qreg_rel[t], np.array([0,s[t] - s_min + I[t] + Qreg_inf[t] - E[t] - env[t]]).max()]).min()
        # The spillage is equal to the higher value between 0 and the resource available exceeding the reservoir capacity
        spill[t] = np.array([0,s[t] + I[t] + Qreg_inf[t] - Qreg_rel[t] - env[t] - E[t] - s_max]).max()
        # The final storage (initial storage in the next step) is equal to the storage + inflow - outflows
        s[t+1] = np.array([s_min,s[t] + I[t] + Qreg_inf[t] - Qreg_rel[t] - env[t] - E[t] - spill[t]]).max()
        
    return env, spill, Qreg_rel, Qreg_inf, s, E


def Res_sys_sim(I, e, s_0, s_min, s_max, env_min, d, Qreg):
    """ 
    The function extracts both regulated inflows (Qreg_inf) and regulated 
    releases (Qreg_rel) from Qreg. Both, Qreg_inf and Qreg_rel are processed 
    either as empty variables or as a time series, i.e. array of values for 
    each time step, or a as policy function, i.e. a function that can be used 
    to determine the release conditional on the state of the reservoir system 
    in the current time-step. This step essentially makes inputs readable by
    the mass balance function (Mass_bal_func).
    
    Comment: if the release scheduling is not predefined, the model 
    automatically will assume the releases equal to the water demand (Qreg_rel 
    = d)
    
    """
    
    # Time length
    T = I.shape[0]
    # Required environmental compensation flow
    env_min = env_min + np.zeros(T)
    # Required demand
    d = d + np.zeros(T)

    # Regulated releases + inflows
    if Qreg['rel_inf'] == []:
        Qreg_rel = np.zeros(T)
        Qreg_inf = np.zeros(T)
    elif isinstance(Qreg['rel_inf'],(dict)):
        exec('from '+Qreg['rel_inf']['file_name']+' import '+Qreg['rel_inf']['function'])
        Qreg_rel = np.zeros(T)
        Qreg_inf = np.zeros(T)
        
    # Regulated water release
    if Qreg['releases'] == []: 
        Qreg_rel = d # releases = demand
    elif isinstance(Qreg['releases'],(np.ndarray)): # a release scheduling is provided as an input
        Qreg_rel = Qreg['releases'] + np.zeros(T)
    elif isinstance(Qreg['releases'],(dict)):
        exec('from '+Qreg['releases']['file_name']+' import '+Qreg['releases']['function'])
        
    # Regulated inflows 
    if Qreg['inflows'] == []: 
        Qreg_inf = np.zeros(T)  # No regulated inflows
    elif isinstance(Qreg['inflows'],(np.ndarray)): # a regulated inflows scheduling is provided as an input
        Qreg_inf = Qreg['inflows'] + np.zeros(T)
    elif isinstance(Qreg['releases'],(dict)):
        exec('from '+Qreg['inflows']['file_name']+' import '+Qreg['inflows']['function'])
        
    ### Operating policy ###
    s_step = 0.01
    s_frac = np.arange(0,1+s_step,s_step) # storage fraction
    Policy_rel = np.zeros(len(s_frac)) + np.nan # Regulated release policy
    Policy_inf = np.zeros(len(s_frac)) + np.nan # Regulated inflow policy
    
    for i in np.arange(len(s_frac)):
    
        if isinstance(Qreg['rel_inf'],(dict)): # a dictionary with: the name of the function,  
            # file name where it is contained and the parameters of the function
            exec('Policy_rel[i], Policy_inf[i] = '+Qreg['rel_inf']['function']+'('+str(Qreg['rel_inf']['param'])+','+str(s_frac[i])+')')
            
        if isinstance(Qreg['releases'],(dict)): # a dictionary with: the name of the function,  
            # file name where it is contained and the parameters of the function
            exec('Policy_rel[i] = '+Qreg['releases']['function']+'('+str(Qreg['releases']['param'])+','+str(s_frac[i])+')')
            
        if isinstance(Qreg['inflows'],(dict)): # a dictionary with: the name of the function,  
            # file name where it is contained and the parameters of the function
            exec('Policy_inf[i] = '+Qreg['inflows']['function']+'('+str(Qreg['inflows']['param'])+','+str(s_frac[i])+')')
    
    ### Run mass balance function ### 
    env, spill, Qreg_rel, Qreg_inf, s, E = Mass_bal_func(I, e, 
                                                         s_0, s_min, s_max, 
                                                         env_min, 
                                                         Qreg_inf, Qreg_rel, 
                                                         s_frac,
                                                         Policy_inf,Policy_rel)
                
    return env, spill, Qreg_rel, Qreg_inf, s, E
