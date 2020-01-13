# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:18:26 2019

@author: ap18525
"""
import numpy as np
from numba import njit,prange

# Mass balance function
#@njit(parallel = False) # Set "nopython" mode for best performance, equivalent to @njit
def Mass_bal_func(I, E, s_0, s_min, s_max, env_min, d, Qenv, Qreg_inf, Qreg_rel, Qspill, s_frac, s, Policy_inf, Policy_rel):
    
    T = I.shape[0]
    for t in range(T): # Loop for each time-step
        if not np.isnan(Policy_inf[0]):
            Qreg_inf[t] = np.interp(s[t]/s_max, s_frac, Policy_inf)
        
        if not np.isnan(Policy_rel[0]):
            Qreg_rel[t] = np.interp(s[t]/s_max, s_frac, Policy_rel) 
            
        # If at week t the inflow (I) is lower than the required environmental compensation (env_min), 
        # then the environmental compensation (Qenv) = inflow (I). Otherwise Qenv = env_min.
        if env_min[t] >= I[t] + Qreg_inf[t] :
            Qenv[t] = I[t] + Qreg_inf[t]
        else:
            Qenv[t] = env_min[t]
        # If the required environmental compensation is higher than the water resource available (s + I - e)
        # then the environmental compensation is equal to the higher value between 0 and the resource available  
        if env_min[t] >= s[t] - s_min + I[t] + E[t] + Qreg_inf[t]:
            Qenv[t] = s[t] - s_min + I[t] + E[t] + Qreg_inf[t]
        else:
            Qenv[t] = env_min[t]
        # If the demand (d) is higher than the water resource available (s + I - e - Qenv)
        # then the release for water supply is equal to the higher value between 0 and the resource available 
        # and the lower value between the latter and the pre-defined release (u)
        if d[t] >= s[t] - s_min + I[t] + E[t] + Qreg_inf[t] - Qenv[t]:
            Qreg_rel[t] = np.array([Qreg_rel[t],np.array([0,s[t] - s_min + I[t] + E[t] + Qreg_inf[t] - Qenv[t]]).max()]).min()
        # The spillage is equal to the higher value between 0 and the resource available exceeding the reservoir capacity
        Qspill[t] = np.array([0,s[t] + I[t] - Qreg_rel[t] - Qenv[t] + E[t] + Qreg_inf[t] - s_max]).max()
        # The final storage (initial storage in the next step) is equal to the storage + inflow - outflows
        s[t+1] = np.array([s_min,s[t] + I[t] - Qreg_rel[t] - Qenv[t] + E[t] + Qreg_inf[t] - Qspill[t]]).max()
        
    return Qenv, Qspill, Qreg_rel, Qreg_inf, s


def Res_sys_sim(I, e, s_0, s_min, s_max, env_min, d, Qreg):

    # Evaporation volume (E) = evaporation depth * water surface area (A)
    """By default we assume A = 1 km2, but it should be modified according to 
    your reservoir charateristics and to take into account the variation of 
    the water surface area as a function of the water surface elevation""" 
    A = 1 # in km2. 
    E = e * A # in ML (= mm * km2) 
    
    # Time length
    T = I.shape[0]
    # Required environmental compensation flow
    env_min = env_min + np.zeros(T)
    # Required demand
    d = d + np.zeros(T)
    
    ### Declare output variables ###
    # Reservoir storage
    s = np.zeros(T+1)
    
    # Environmental flow
    Qenv = np.zeros(T)

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
        
    # Spillage
    Qspill = np.zeros(T)
    
    ### Initial conditions ###
    s[0] = s_0 # initial storage
    
    ### Operating policy ###
    s_step = 0.01
    s_frac = np.arange(0,1+s_step,s_step) # storage fraction
    Policy_rel = np.zeros(len(s_frac)) + np.nan # Regulated releases policy
    Policy_inf = np.zeros(len(s_frac)) + np.nan # Regulated inflows policy
    
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

    Qenv, Qspill, Qreg_rel, Qreg_inf, s = Mass_bal_func(I, E, 
                                                        s_0, s_min, s_max, 
                                                        env_min, d, 
                                                        Qenv, Qreg_inf, Qreg_rel,Qspill, 
                                                        s_frac, s,
                                                        Policy_inf,Policy_rel)
                
    return Qenv, Qspill, Qreg_rel, Qreg_inf, s

#N = 100000
#I = np.abs(np.random.normal(loc=20,scale=10,size=N))
#e = np.abs(np.random.normal(loc=4,scale=1,size=N))
#d = np.abs(np.random.normal(loc=20,scale=5,size=N))
#u = np.abs(np.random.normal(loc=20,scale=1,size=N))
## System constraints
#u_min = 2 # ML/week
#u_max = 80 # ML/week
## Mean long term release
#u_mean = 20 # ML/week
## Policy function parameters
#u_ref = 20/u_mean
#s_ref_1 = 0.2
#s_ref_2 = 0.8
#
#### Constraints ###
#s_max = 150 #  (ML) Maximum storage (=reservoir capacity)
#s_min = 0 # (ML) Minimum storage (set to zero for now)
#u_max = 60 # (ML/week) Maximum release capacity
#env_min = 2 # (ML/week)   # Environmental compensation flow
#
#### Initial conditions ###
#s_0 = 80 # (ML) # Storage volume at the beginning of the simulation period
#### Policy function constrains ###
#u_0 = u_min/u_mean # release at storage fraction = 0
#u_1 = u_max/u_mean # release at storage fraction = 1
#
#### Policy function defining points ###
#x0 = [0,       u_0]
#x1 = [s_ref_1, u_ref]
#x2 = [s_ref_2, u_ref]
#x3 = [1,       u_1]
#
#param = [x0, x1, x2, x3, u_mean]
#from Operating_policy_functions import four_points_policy
#u_frac = four_points_policy(param)/u_mean
#
#Qreg = {'releases' : {'file_name' : 'Operating_policy_functions',
#                     'function' : 'four_points_policy',
#                     'param': param},
#        'inflows' : [],
#        'rel_inf' : []}
#
#time_start = time.clock()
#Qenv, Qspill, Qreg_rel, Qreg_inf, s = Res_sys_sim(I, e, s_0, s_min, s_max, env_min, d, Qreg)
#time_elapsed = (time.clock() - time_start)
#time_elapsed
