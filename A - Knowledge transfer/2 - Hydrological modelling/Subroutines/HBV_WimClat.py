# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 10:58:33 2018

@author: ap18525
"""
from Subroutines.HBV_sim import HBV_sim

def HBV_WimClat(P,ept,area):
    
    # Set of calibrated parameters (rmseAllBest)
#    1. BETA  = Exponential parameter in soil routine [-]
#    2. LP    = evapotranspiration limit [-]
#    3. FC    = field capacity [mm] 
#    4. PERC  = maximum flux from Upper to Lower Zone [mm/day]
#    5. K0    = Near surface flow coefficient (ratio) [1/day]  
#    6. K1    = Upper Zone outflow coefficient (ratio) [1/day]  
#    7. K2    = Lower Zone outflow coefficient (ratio) [1/day]  
#    8. UZL   = Near surface flow threshold for K0 [mm]
#    9. MAXBAS= Flow routing coefficient or Transfer function parameter [day]
    Case = 1
    ini = [260,5.5,84.5]
    param = [6.40239,0.8422094,247.1199,0.8984092,1/3.907456,1/11.03344,1/61.30392,27.25851,1.894377]
    
    Q_sim,STATES,FLUXES = HBV_sim(P,ept,param,Case,ini,area)
    
    return Q_sim,STATES,FLUXES