# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:56:06 2018

@author: Andres Peñuela (University of Bristol)
     This function is Python adaptation of the R package TUWmodel and the HBV 
     Fortran script both by Alberto Viglione and Juraj Parajka.
     
     The model, developed at the Vienna University of Technology, is a lumped 
     conceptual rainfall-runoff model, following the structure of the HBV model. 
     The model runs on a daily or shorter time step and consists of a snow 
     routine, a soil moisture routine and a flow routing routine. 
"""

import numpy as np
from numba import njit

import cProfile, pstats, io
# Profiler as a decorator
def profile(fnc):
    
    """A decorator that uses cProfile to profile a function"""
    
    def inner(*args):
        
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner


#@profile
@njit # Set "nopython" mode for best performance, equivalent to @njit
def TUWmodel(P,T,ept,param,ini,area):
    """
     inputs = (P,T,ept,param,Case,inic)
     outputs = (Q_sim,STATES,FLUXES)
    
         P = time series of precipitation                      - vector (T,1)
         T = time series of temperature                        - vector (T,1)
       ept = time series of potential evapotranspiration       - vector (T,1)
     param = vector of model parameters                        - vector (1,15)
                1.  BETA   = Exponential parameter in soil routine [-]
                2.  LP     = evapotranspiration limit [-]
                3.  FC     = field capacity [mm] 
                4.  PERC   = maximum flux from Upper to Lower Zone [mm/Dt]
                5.  K0     = Near surface flow coefficient (ratio) [1/Dt]  
                6.  K1     = Upper Zone outflow coefficient (ratio) [1/Dt]  
                7.  K2     = Lower Zone outflow coefficient (ratio) [1/Dt]  
                8.  UZL    = Near surface flow threshold [mm]
                9.  MAXBAS = Flow routing coefficient [Dt]
                10. croute = free scaling parameter [Dt/mm]
                11. SCF    = snow correction factor [-]
                12. DDF    = degree day factor [mm/degC/timestep]
                13. Tr     = threshold temperature above which precipitation is rain [degC]
                14. Ts     = threshold temperature below which precipitation is snow [degC]
                15. Tm     = threshold temperature above which melt starts [degC];
      Case = flag for preferred path in the Upper Zone dynamics - scalar
                flag=1 -> Preferred path is runoff 
                flag=2 -> Preferred path is percolation
       ini = vector of initial conditions
                1.  SSM0   = initial soil moisture [mm]
                2.  SUZ0   = initial upper zone storage [mm]
                3.  SLZ0   = initial lower zone storage [mm]
                4.  SWE0   = initial snow water equivalent [mm]
    
      Q_sim = time series of simulated flow                    - vector (T,1)
     STATES = time series of simulated storages (all in mm)    - matrix (T,4)
              1: water content of soil (soil moisture)
              2. water content of upper reservoir of flow routing routine 
              3. water content of lower reservoir of flow routing routine
              4. snow water equivalent
     FLUXES = time series of simulated fluxes (all in mm/Dt)   - matrix (T,8)
              1: actual evapotranspiration
              2: recharge (water flux from soil moisture accounting module
                 to flow routing module)
              3: percolation (water flux from upper to lower reservoir of the 
                 flow routing module)
              4: Surface runoff from Upper Zone
              5: Subsurface flow from Upper Zone
              6: Outflow from Lower Zone
              7: snow solid precipitation
              8: snowmelt
              
     References: 
    
     Parajka, J., R. Merz, G. Bloeschl (2007) Uncertainty and multiple 
     objective calibration in regional water balance modelling: case study in 
     320 Austrian catchments, Hydrological Processes, 21, 435-446.
    
     Comments:
     * The Capillary flux (from upper tank to soil moisture accounting module)
     is not considered
     * The recharge from the soil to the upper zone is considered to be a
     faster process than evapotranspiration.
     * The preferential path from the upper zone can be modified 
               - Case 1: interflow is dominant
               - Case 2: percolation is dominant
    
     """
    # ----------------------
    # Read model parameters:
    # ----------------------
    BETA = param[0] # Exponential parameter in soil routine [-]
    LP = param[1] # evapotranspiration limit [-]
    epsilon = 0.000001
    FC = np.max(np.array([epsilon,param[2]])) # field capacity [mm] cannot be zero
     
    PERC  = param[3] # maximum flux from Upper to Lower Zone [mm/Dt]
    K0    = param[4] # Near surface flow coefficient (ratio) [1/Dt]  
    K1    = param[5] # Upper Zone outflow coefficient (ratio) [1/Dt]  
    K2    = param[6] # Lower Zone outflow coefficient (ratio) [1/Dt]  
    UZL   = param[7] # Near surface flow threshold [mm]
    
    MAXBAS = np.max(np.array([1,round(param[8])])) # Flow routing coefficient [Dt]
    croute = param[9]
    
    # Snow module parameters
    SCF = param[10] # snow correction factor (0.9-1.5)
    DDF = param[11] # degree day factor (0.0-5.0 mm/degC/timestep)
    Tr  = param[12] # threshold temperature above which precipitation is rain (1.0-3.0 degC)
    Ts  = param[13] # threshold temperature below which precipitation is snow (-3.0-1.0 degC)
    Tm  = param[14] # threshold temperature above which melt starts (-2.0-2.0 degC)
    
    # Initial conditions    
    SSM0 = ini[0] # initial soil moisture [mm]
    SUZ0 = ini[1] # initial upper zone storage [mm]
    SLZ0 = ini[2] # initial lower zone storage [mm]
    SWE0 = ini[3] # initial snow water equivalent [mm]

    N = len(ept) # number of time samples
    
    dquh = np.zeros((N,))
    SW   = np.zeros((N,))   # snow
    SWE  = np.zeros((N+1,)) # snow water equivalent
    MT   = np.zeros((N,))   # snowmelt
    P_m  = np.zeros((N,))   # Rain + snowmelt
    # ----------------------
    # Soil moisture routine:
    # ----------------------
    
    EA = np.zeros((N,))   # Actual Evapotranspiration [mm/Dt]
    SM = np.zeros((N+1,)) # Soil Moisture [mm]
    SM[0] = SSM0
    R  = np.zeros((N,)) # Recharge (water flow from Soil to Upper Zone) [mm/Dt]
    UZ = np.zeros((N+1,)) # Upper Zone moisture [mm]
    UZ[0] = SUZ0          # Initial Upper Zone moisture [mm]
    LZ = np.zeros((N+1,)) # Lower Zone moisture [mm]
    LZ[0] = SLZ0          # Initial Lower Zone moisture [mm]
    RL = np.zeros((N,))   # Recharge to the lower zone [mm]
    Q0 = np.zeros((N,))   # Surface runoff from Upper Zone [mm/Dt]
    Q1 = np.zeros((N,))   # Subsurface flow from Upper Zone [mm/Dt]
    Q2 = np.zeros((N,))   # Outflow from Lower Zone [mm/Dt]
    Q = np.zeros((N,))    # Total daily flow [mm/Dt]
    
    SWE[0] = SWE0
    
    for t in range(N):

        # -------------
        # Snow routine: 
        # -------------        
        temp = T[t]; precip = P[t]; swe = SWE[t]
        
        if temp<Ts:
            snow=precip
        elif temp>Tr:
            snow=0
        else:
            snow=precip*np.abs(temp-Tr)/np.abs(Tr-Ts)
        precip = precip-snow
        
        melt=(temp-Tm)*DDF
        if melt<0:
            melt = 0
        # Bestime SWE
        sweold = swe
        swe = sweold + SCF*snow-melt
        if swe < 0.0001:
            swe = 0
            melt = sweold + SCF*snow
            if melt < 0:
                melt = 0
        
#        precip, snow, melt, swe = snowmod(SCF,DDF,Tr,Ts,Tm,T[t],P[t],SWE[t])
        
        P_m[t] = precip + melt # Precipitation + snowmelt
        SW[t] = snow         # snow solid precipitation
        SWE[t+1] = swe       # snow water equivalent
        MT[t] = melt         # snowmelt
        
        # --------------------------
        #    Soil Moisture Dynamics:
        # --------------------------
    
        R[t]= P_m[t]*(SM[t]/FC)**BETA  # Compute the value of the recharge to the 
        # upper zone (we assumed that this process is faster than evaporation)
        SM_dummy = np.max(np.array([np.min(np.array([SM[t]+P_m[t]-R[t],FC])),0])) # Compute the water balance 
        # with the value of the recharge  
        R[t]=R[t]+ np.max(np.array([SM[t]+P_m[t]- R[t]-FC,0]))+np.min(np.array([SM[t]+P_m[t]-R[t],0])) #adjust R 
        # by an amount equal to the possible negative SM amount or to the 
        # possible SM amount above FC
        
        EA[t]=ept[t]*np.min(np.array([SM_dummy/(FC*LP),1])) # Compute the evaporation
        SM[t+1] = np.max(np.array([np.min(np.array([SM_dummy-EA[t],FC])),0])) # Compute the water balance 
        
        EA[t]=EA[t]+ np.max(np.array([SM_dummy-EA[t]-FC,0]))+np.min(np.array([SM_dummy-EA[t],0])) # adjust EA
        # by an amount equal to the possible negative SM amount or to the 
        # possible SM amount above FC
        
        # --------------------
        # Upper Zone dynamics:
        # --------------------

#        if Case==np.array([1.0]):
            # Case 1: Preferred path = runoff from the upper zone 
        Q0[t] = np.max(np.array([np.min(np.array([np.exp(-K0)*K0*np.max(np.array([UZ[t]-UZL,0])),UZ[t]])),0]))
        UZ[t] = UZ[t] - Q0[t]
        Q1[t] = np.max(np.array([np.exp(-K1)*K1*UZ[t],0]))
        RL[t] = np.max(np.array([np.min(np.array([UZ[t]-Q0[t],PERC])),0]))
    
#        elif Case==np.array([2.0]):
#            # Case 2: Preferred path = percolation
#            RL[t]= max(min(PERC,UZ[t]),0)
#            Q0[t] = max(min(np.exp(-K0)*K0*max(UZ[t]-UZL,0),UZ[t]-RL[t]),0)
#            UZ[t] = UZ[t] - Q0[t]
#            Q1[t] = max(-RL[t] + RL[t]*np.exp(-K1) + np.exp(-K1)*K1*UZ[t],0)
        
#        else:
#            raise ValueError('Case must equal to 1 or 2 ')
            
        UZ[t+1] = UZ[t]+R[t]-Q1[t]-RL[t]   
        
        # --------------------
        # Lower Zone dynamics: 
        # --------------------

        Q2[t] = np.max(np.array([np.min(np.array([RL[t] - RL[t]*np.exp(-K2) + np.exp(-K2)*K2*LZ[t],LZ[t]+RL[t]])),0]))
        LZ[t+1] = LZ[t]+RL[t]-Q2[t]
        
        Q[t]=Q0[t]+Q1[t]+Q2[t]
        
        # -------------
        # Flow routing: 
        # -------------
        
        if MAXBAS-croute*Q[t]>1.0:
            bq=MAXBAS-croute*Q[t]
            bql=np.int(bq)
            suma=0
            for j in np.arange(0,bql,1):
                if j<=bql/2:
                    dquh[j]=((j-0.5)*4*Q[t])/(bql*bql*1)
                elif (np.abs(j-(bql/2+0.5)))<0.1:
                    dquh[j]=((j-0.75)*4*Q[t])/(bql*bql*1)
                else:
                    dquh[j]=((bql-j+0.75)*4*Q[t])/(bql*bql*1)
                suma = suma+dquh[j]
        else:
            bql=1
            dquh[0]=Q[t]
            suma=Q[t]
                
    Q_sim = Q
        
#    STATES=np.array([SM,UZ,LZ,SWE])
#    FLUXES=np.array([EA,R,RL,Q0*area,Q1*area,Q2*area,SW,MT]) # flows Q in mm * area (km2) = ML
#    
    return Q_sim*area,SM,UZ,LZ,SWE,EA,R,RL,Q0*area,Q1*area,Q2*area,SW,MT
    

# -------------
# Snow routine: 
# -------------
#def snowmod(SCF,DDF,Tr,Ts,Tm,temp,precip,swe):
#    if temp<Ts:
#        snow=precip
#    elif temp>Tr:
#        snow=0
#    else:
#        snow=precip*np.abs(temp-Tr)/np.abs(Tr-Ts)
#    precip = precip-snow
#    
#    melt=(temp-Tm)*DDF
#    if melt<0:
#        melt = 0
#    # Bestime SWE
#    sweold = swe
#    swe = sweold + SCF*snow-melt
#    if swe < 0.0001:
#        swe = 0
#        melt = sweold + SCF*snow
#        if melt < 0:
#            melt = 0
#    
#    return (precip, snow, melt, swe)

#x = TUWmodel(P,T,ept,param,Case,ini,area)