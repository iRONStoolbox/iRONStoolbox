# -*- coding: utf-8 -*-
"""
This function implements the reservoir simulation model (Res_sys_sim). First,
it extracts and process the regulated flows contained in the Qreg variable. 
This makes the regulated flow data readable by the mass balance function 
(Mass_bal_func). Then, Mass_bal_func links all the key variables that represent 
the reservoir dynamics (inflow, storage and outflows).

To speed-up the computation this module applies the just-in-time compiler Numba 
(http://numba.pydata.org/; (Lam & Seibert, 2015; Marowka, 2018).

This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi and at 
Bristol University (2020).

Licence: MIT

References:
Lam, P., Siu Kwan, & Seibert, S. (2015). Numba: A llvm-based python jit 
compiler. doi:10.1145/2833157.2833162
"""
import numpy as np
from numba import njit,prange

### Mass balance function ###
@njit(parallel = True) # Numba decorator to speed-up the function below
def Mass_bal_func(I, e, 
                  s_ini, s_min, s_max, 
                  env_min, d,
                  Qreg_inf, Qreg_rel, 
                  s_frac,
                  policy_inf, policy_rel):
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
                  free variable that the reservoir operator will need to specify. 
                  Note: Here, Qreg_rel is assumed to be released entirely to the
                  downstream river, but if part of the release is abstracted 
                  through pipes, then the splitting must be performed outside 
                  of this function
                  
    Policy related inputs: s_frac, policy_inf, policy_rel, rules
    """
    
    T = I.shape[0] # number of time-steps
    M = I.shape[1] # number of ensemble members
    ### Declare output variables ###
    # Reservoir storage
    s = np.zeros((T+1,M))
    
    # Environmental flow
    env = np.zeros((T,M))

    # Spillage
    spill = np.zeros((T,M))
    
    # Evaporation
    E = np.zeros((T,M))
    
    ### Initial conditions ###
    s[0,:] = s_ini # initial storage
    
    for m in prange(M):
    
        for t in range(T): # Loop for each time-step
            
            if len(policy_inf)>1:

                if policy_inf.ndim > 1:
                    ### Rule curve ###
                    Qreg_inf[t,m] = np.interp(s[t,m]/s_max, s_frac, policy_inf[:,t])
                else:
                    ### Policy function ###
                    Qreg_inf[t,m] = np.interp(s[t,m]/s_max, s_frac, policy_inf)
            
            if len(policy_rel)>1:
                
                if policy_rel.ndim > 1:
                    ### Rule curve ###
                    Qreg_rel[t,m] = np.interp(s[t,m]/s_max, s_frac, policy_rel[:,t])       
                else:
                    ### Policy function ###
                    Qreg_rel[t,m] = np.interp(s[t,m]/s_max, s_frac, policy_rel)
                
            ### Evaporation volume ### 
            # (E) = evaporation depth * water surface area (A)
            # By default we assume A = 1 km2, but it should be modified according 
            # to your reservoir charateristics and to take into account the 
            # variation of the water surface area as a function of the water 
            # surface elevation""" 
            A = 1 # in km2. 
            E[t,m] = e[t,m] * A # in ML (= mm * km2) 
            
            # If at week t the inflow (I) is lower than the required environmental compensation (env_min), 
            # then the environmental compensation (Qenv) = total inflows (natural + regulated). Otherwise Qenv = env_min.
            if env_min[t,m] >= I[t,m] + Qreg_inf[t,m] :
                env[t,m] = I[t,m] + Qreg_inf[t,m]
            else:
                env[t,m] = env_min[t,m]
            # If the required environmental compensation is higher than the water resource available (s + I - E)
            # then the environmental compensation is equal to the higher value between 0 and the resource available  
            if env_min[t,m] >= s[t,m] - s_min + I[t,m] + Qreg_inf[t,m] - E[t,m]:
                env[t,m] = np.array([0,s[t,m] - s_min + I[t,m] + Qreg_inf[t,m] - E[t,m]]).max()
            else:
                env[t,m] = env_min[t,m]
            # If the regulated release (Qreg_rel) is higher than the water resource available (s + I - E - Qenv)
            # then the release is equal to the lower value between the resource available and the pre-defined release (Qreg_rel)
            Qreg_rel[t,m] = np.array([Qreg_rel[t,m], np.array([0,s[t,m] - s_min + I[t,m] + Qreg_inf[t,m] - E[t,m] - env[t,m]]).max()]).min()
            # The spillage is equal to the higher value between 0 and the resource available exceeding the reservoir capacity
            spill[t,m] = np.array([0,s[t,m] + I[t,m] + Qreg_inf[t,m] - Qreg_rel[t,m] - env[t,m] - E[t,m] - s_max]).max()
            # The final storage (initial storage in the next step) is equal to the storage + inflow - outflows
            s[t+1,m] = np.array([s_min,s[t,m] + I[t,m] + Qreg_inf[t,m] - Qreg_rel[t,m] - env[t,m] - E[t,m] - spill[t,m]]).max()
            
    return env, spill, Qreg_rel, Qreg_inf, s, E


def Res_sys_sim(date, I, e, s_ini, s_min, s_max, env_min, d, Qreg):
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
    T = I.shape[0] # number of time-steps
    # Inflow ensemble
    M = I.shape[1] # number of ensemble members
    # Required environmental compensation flow
    env_min = env_min + np.zeros([T,M])
    # Required demand
    d = d + np.zeros([T,M])
    # Regulated flows
    Qreg_rel = np.zeros([T,M]) # we will define it through the mass balance simulation
    Qreg_inf = np.zeros([T,M]) # we will define it through the mass balance simulation
    # Policy functions
    s_step = 0.01
    s_frac = np.arange(0,1+s_step,s_step) # storage fraction
    policy_rel = np.zeros((1,1)) + np.nan # Regulated release policy
    policy_inf = np.zeros((1,1)) + np.nan # Regulated inflow policy
        
    # Regulated releases
    if Qreg['releases'] == []:
        Qreg_rel = d # releases = demand
    elif Qreg['releases']['type'] == 'scheduling': # a regulated inflows scheduling is provided as an input
        Qreg_rel = Qreg['releases']['input']
    elif Qreg['releases']['type'] == 'operating policy': 
        ### Operating policy ###
        rel_func = Qreg['releases']['input']
        param    = Qreg['releases']['param']
        # Policy function
        policy_rel = np.zeros(len(s_frac)) + np.nan # Regulated release policy
#        policy_inf = np.zeros(len(s_frac)) + np.nan # Regulated inflow policy
        for i in np.arange(len(s_frac)):
            policy_rel[i] = rel_func(param,s_frac[i])        
    elif Qreg['releases']['type'] == 'rule curve': 
        ### Rule curve ###
        rel_func_1 = Qreg['releases']['input'][0]
        rel_func_2 = Qreg['releases']['input'][1]
        s_yday,r_yday = rel_func_2(Qreg['releases']['param'])
        rule_curve_dim = s_yday.shape[0]
        policy_rel = np.zeros([len(s_frac),T]) + np.nan # Regulated releases rule curve
#        policy_inf = np.zeros([len(s_frac),T]) + np.nan # Regulated inflows rule curve
        param = np.zeros([rule_curve_dim,2])
        for j in np.arange(T):
            yday = date[j].dayofyear
            param[:,0] = s_yday[:,yday]
            param[:,1] = r_yday[:,yday]
            for i in np.arange(len(s_frac)):
                policy_rel[i,j] = rel_func_1(param,s_frac[i])         
    
    # Regulated inflows 
    if Qreg['inflows'] == []: 
        Qreg_inf = np.zeros([T,M])  # no regulated inflows
    elif Qreg['inflows']['type'] == 'scheduling': # a regulated inflows scheduling is provided as an input
        Qreg_inf = Qreg['inflows']['input']
    elif Qreg['inflows']['type'] == 'operating policy': 
        ### Operating policy ###
        inf_func = Qreg['inflows']['input']
        param    = Qreg['inflows']['param']
        # Policy function
#        policy_rel = np.zeros(len(s_frac)) + np.nan # Regulated release policy
        policy_inf = np.zeros(len(s_frac)) + np.nan # Regulated inflow policy
        for i in np.arange(len(s_frac)):
            policy_inf[i] = inf_func(param,s_frac[i])        
    elif Qreg['inflows']['type'] == 'rule curve': 
        ### Rule curve ###
        inf_func_1 = Qreg['releases']['input'][0]
        inf_func_2 = Qreg['releases']['input'][1]
        s_yday,i_yday = inf_func_2(Qreg['releases']['param'])
        rule_curve_dim = s_yday.shape[0]
#        policy_rel = np.zeros([len(s_frac),T]) + np.nan # Regulated releases rule curve
        policy_inf = np.zeros([len(s_frac),T]) + np.nan # Regulated inflows rule curve
        param = np.zeros([rule_curve_dim,2])
        for j in np.arange(T):
            yday = date[j].dayofyear
            param[:,0] = s_yday[:,yday]
            param[:,1] = i_yday[:,yday]
            for i in np.arange(len(s_frac)):
                policy_inf[i,j] = inf_func_1(param,s_frac[i])  

#    # Regulated releases + inflows
#    if Qreg['rel_inf'] == []:
#        Qreg_rel = np.zeros(T) # here is a problem because it makes it 0 even if it was defined above
#        Qreg_inf = np.zeros(T)
#    elif isinstance(Qreg['rel_inf'],(dict)):
#        rel_inf_func = Qreg['rel_inf']['function']
#        param        = Qreg['rel_inf']['param']
#        if Qreg['rel_inf']['file_name'] == 'Reservoir_operating_policy.Operating_policy':
#            ### Operating policy ###
#            # Regulated flows
#            Qreg_rel = np.zeros(T) # we will define it through the mass balance simulation
#            Qreg_inf = np.zeros(T) # we will define it through the mass balance simulation
#            # Policy function
#            policy_rel = np.zeros(len(s_frac)) + np.nan # Regulated release policy
#            policy_inf = np.zeros(len(s_frac)) + np.nan # Regulated inflow policy
#            for i in np.arange(len(s_frac)):
#                policy_rel[i], policy_inf[i] = rel_inf_func(param,s_frac[i])
            
    ### Run mass balance function ### 
    env, spill, Qreg_rel, Qreg_inf, s, E = Mass_bal_func(I, e, 
                                                         s_ini, s_min, s_max, 
                                                         env_min, d,
                                                         Qreg_inf, Qreg_rel, 
                                                         s_frac,
                                                         policy_inf,policy_rel)

    return env, spill, Qreg_rel, Qreg_inf, s, E
