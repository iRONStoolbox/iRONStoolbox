# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 11:11:48 2019

@author: ap18525
"""
import numpy as np

def HBV_model(dates, E, P, ini, param, case):
    [SSM0,SUZ0,SLZ0] = ini
    [BETA, LP, FC, PERC, K0, K1, K2, UZL, MAXBAS] = param
    # -----------------------
    # Outputs initialization:
    # -----------------------
    N  = len(dates)         # number of time samples
    EA = np.zeros([N,])   # Actual Evapotranspiration [mm/Dt]
    SM = np.zeros([N+1,]) # Soil Moisture [mm]
    SM[0]=SSM0
    R  = np.zeros([N,]) # Recharge (water flow from Soil to Upper Zone) [mm/Dt]
    UZ = np.zeros([N+1,]) # Upper Zone moisture [mm]
    UZ[0] = SUZ0
    LZ = np.zeros([N+1,]) # Lower Zone moisture [mm]
    LZ[0] = SLZ0
    RL = np.zeros([N,])   # Recharge to the lower zone [mm]
    Q0 = np.zeros([N,])   # Outflow from Upper Zone [mm/Dt]
    Q1 = np.zeros([N,])   # Outflow from Lower Zone [mm/Dt]
    
    for t in range(N):

        # --------------------------
        #    Soil Moisture Dynamics:
        # --------------------------

        R[t]= P[t]*(SM[t]/FC)**BETA  # Compute the value of the recharge to the 
        # upper zone (we assumed that this process is faster than evaporation)
        SM_dummy = max(min(SM[t]+P[t]-R[t],FC),0) # Compute the water balance 
        # with the value of the recharge  
        R[t]=R[t]+ max(SM[t]+P[t]- R[t]-FC,0)+min(SM[t]+P[t]-R[t],0) #adjust R 
        # by an amount equal to the possible negative SM amount or to the 
        # possible SM amount above FC

        EA[t]=E[t]*min(SM_dummy/(FC*LP),1) # Compute the evaporation
        SM[t+1] = max(min(SM_dummy-EA[t],FC),0) # Compute the water balance 

        EA[t]=EA[t]+ max(SM_dummy-EA[t]-FC,0)+min(SM_dummy-EA[t],0) # adjust EA
        # by an amount equal to the possible negative SM amount or to the 
        # possible SM amount above FC

        # --------------------
        # Upper Zone dynamics:
        # --------------------

        if case==1:
            # Case 1: Preferred path = runoff from the upper zone 
            Q0[t] = max(min(K1*UZ[t]+K0*max(UZ[t]-UZL,0),UZ[t]),0)              	 
            RL[t] = max(min(UZ[t]-Q0[t],PERC),0)

        elif case==2:
            # Case 2: Preferred path = percolation
            RL[t]= max(min(PERC,UZ[t]),0)
            Q0[t] = max(min(K1*UZ[t]+K0*max(UZ[t]-UZL,0),UZ[t]-RL[t]),0)
        else:
            raise ValueError('Case must equal to 1 or 2 ')

        UZ[t+1] = UZ[t]+R[t]-Q0[t]-RL[t]   

        # --------------------
        # Lower Zone dynamics: 
        # --------------------

        Q1[t] = max(min(K2*LZ[t],LZ[t]),0)
        LZ[t+1] = LZ[t]+RL[t]-Q1[t]

    Q = Q0 + Q1 ; # total flow (mm/Dt)
    
    # ------------
    # Flow routing
    # ------------
    def mytrimf(x,param):
        # implements triangular-shaped membership function
        # (available in Matlab Fuzzy Logic Toolbox as 'trimf')
        x=np.array(x)
        f = np.zeros(np.shape(x))
        idx = (x>param[0]) & (x<=param[1])
        f[idx] = (x[idx]-param[0])/(param[1]-param[0])
        idx = (x>param[1]) & (x<=param[2])
        f[idx] = (param[2]-x[idx])/(param[2]-param[1])

        return f

    c = mytrimf(np.arange(1,MAXBAS+1,1),[0, (MAXBAS+1)/2, MAXBAS+1]) # (Seibert,1997)


    c = c/np.sum(c) # vector of normalized coefficients - (1,MAXBAS)
    Q_sim = np.zeros([N,])
    for t in np.arange(MAXBAS,N+1,1):
        Q_sim[t-1] = c.dot(Q[t-MAXBAS:t]) # (Seibert,1997)

    STATES=[SM,UZ,LZ]
    FLUXES=[EA,R,RL,Q0,Q1,Q_sim]
    
    return STATES, FLUXES