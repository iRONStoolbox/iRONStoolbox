# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 10:58:33 2018

@author: ap18525
"""
import numpy as np
from Submodules.TUWmodel import TUWmodel

def TUW_WimClat(P,T,ept,ini,area):
    
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
    param = np.array([6.40239,0.8422094,247.1199,0.8984092,1/3.907456,1/11.03344,1/61.30392,27.25851,1.894377,26.93134, 1.141707, 2.1796, 2.981686, 0.0318619, -1.827776])
    
#   inic = [50,2.5,2.5,0]
    
    # No snow effect
#    T = T + 100 # To make sure that temperatures are not close to 0 degC
    
    I_sim,SM,UZ,LZ,SWE,EA,R,RL,I0,I1,I2,SW,MT = TUWmodel(P,T,ept,param,ini,area)
    
    return I_sim,SM,UZ,LZ,SWE,EA,R,RL,I0,I1,I2,SW,MT