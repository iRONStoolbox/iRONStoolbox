# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 16:41:57 2019

@author: ap18525
"""
import numpy as np

def Water_system_model(simtime,I,E,d,S0,Smax,env_min):
    
    I = np.array(I)
    E = np.array(E)
    d = np.array(d)

    r = np.array(d)
    
    members_num = np.shape(I)[0]
    
    # Declare output variables

    S = np.array(np.zeros([np.shape(I)[0],np.shape(I)[1]+1]))

    w = np.array(np.zeros(np.shape(I)))

    env = np.array(np.zeros(np.shape(I)))+env_min
    
    for m in range(members_num):
        
        S[m,0] = S0

        for t in range(simtime):

            # If at day t the inflow (I) is lower than the required environmental compensation (env_min), 
            # then environmental compensation (env) = inflow (I)  
            if env_min >= I[m,t] :
                env[m,t] = I[m,t]

            if env_min >= S[m,t] + I[m,t] - E[m,t]:
                env[m,t] = max(0,S[m,t] + I[m,t] - E[m,t])

            if d[m,t] >= S[m,t] + I[m,t] - E[m,t] - env[m,t]:
                r[m,t] = min(r[m,t],max(0,S[m,t] + I[m,t] - E[m,t] - env[m,t]))

            w[m,t] = max(0,S[m,t] + I[m,t] - r[m,t] - env[m,t] - E[m,t] - Smax)

            S[m,t+1] = S[m,t] + I[m,t] - r[m,t] - env[m,t]- E[m,t] - w[m,t]
              
    return S,env,w,r