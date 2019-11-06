# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 16:51:42 2018

@author: ap18525
"""

#from Submodules.CRPS import crps_ensemble
import hydrostats.ens_metrics as em
import numpy as np

error_factor = 1
num_mem = 3
np.random.seed(3849590438)
Rain_predictions = (np.random.rand(15, num_mem) + 1) * 10 # 52 Ensembles
Rain_observation = (np.random.rand(15) + 1) * 10
Rain_benchmarks = (np.random.rand(15, num_mem) + 1) * 10  * error_factor

I_predictions = (np.random.rand(15, num_mem) + 1) * 100 # 52 Ensembles
I_observation = (np.random.rand(15) + 1) * 100
I_benchmarks = (np.random.rand(15, num_mem) + 1) * 100 * error_factor
  
def Forecast_SkillScore_CRPSS(I_observation,I_benchmarks,I_predictions,Rain_observation,Rain_benchmarks,Rain_predictions):

#    #Inflows
#    I_RPS_CL_k = crps_ensemble(I_observation,I_benchmarks)
#    I_RPS_FC_k = crps_ensemble(I_observation,I_predictions)
#
#    I_RPS_CL = np.sum(I_RPS_CL_k)
#    I_RPS_FC = np.sum(I_RPS_FC_k)
#    
#    I_RPSS = 1 - (I_RPS_FC/I_RPS_CL)
#    
#    # Rainfall
#    Rain_RPS_CL_k = crps_ensemble(Rain_observation,Rain_benchmarks)
#    Rain_RPS_FC_k = crps_ensemble(Rain_observation,Rain_predictions)
#
#    Rain_RPS_CL = np.sum(Rain_RPS_CL_k)
#    Rain_RPS_FC = np.sum(Rain_RPS_FC_k)
#
#    Rain_RPSS = 1 - (Rain_RPS_FC/Rain_RPS_CL)
    
    ### Hydrostats ###
    # Inflow forecast skill score
    I_CRPS_CL_k = em.ens_crps(I_observation,I_benchmarks)
    I_CRPS_FC_k = em.ens_crps(I_observation,I_predictions)

    I_CRPS_CL_t = I_CRPS_CL_k['crps']
    I_CRPS_FC_t = I_CRPS_FC_k['crps']

    I_CRPS_CL = I_CRPS_CL_k['crpsMean']
    I_CRPS_FC = I_CRPS_FC_k['crpsMean']
    
    I_CRPSS_t = 1 - (I_CRPS_FC_t/I_CRPS_CL_t)
    I_CRPSS = 1 - (I_CRPS_FC/I_CRPS_CL)
    
    # Rainfall forecast skill score
    Rain_CRPS_CL_k = em.ens_crps(Rain_observation,Rain_benchmarks)
    Rain_CRPS_FC_k = em.ens_crps(Rain_observation,Rain_predictions)

    Rain_CRPS_CL_t = Rain_CRPS_CL_k['crps']
    Rain_CRPS_FC_t = Rain_CRPS_FC_k['crps']
    
    Rain_CRPS_CL = Rain_CRPS_CL_k['crpsMean']
    Rain_CRPS_FC = Rain_CRPS_FC_k['crpsMean']
    
    Rain_CRPSS_t = 1 - (Rain_CRPS_FC_t/Rain_CRPS_CL_t)
    Rain_CRPSS = 1 - (Rain_CRPS_FC/Rain_CRPS_CL)
    
    return I_CRPSS,Rain_CRPSS,I_CRPSS_t,Rain_CRPSS_t


    