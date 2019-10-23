# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 16:51:42 2018

@author: ap18525
"""
#import time
import numpy as np
from numba import jit
#import matplotlib.pyplot as plt 
import hydrostats.ens_metrics as em

@jit(nopython=True) # Set "nopython" mode for best performance, equivalent to @njit
def Forecast_SkillScore_RPSS(I_observation,I_benchmarks,I_predictions,Rain_observation,Rain_benchmarks,Rain_predictions):
    
    # Inflows
    I_obs_max = np.max(I_observation);I_ben_max = np.max(I_benchmarks);I_pred_max = np.max(I_predictions)
    class_max = np.max(np.array([I_obs_max,I_ben_max,I_pred_max])) # np.array needed because inside of a numpy function there shouldn't be a list
    class_step = 1
    classes = np.arange(1,class_max,class_step)
    num_classes = len(classes)
    t_steps = I_predictions.shape[0]
    num_mem = I_predictions.shape[1]

    I_F = np.zeros(num_classes); I_B = np.zeros(num_classes)
    I_B_O = np.zeros((num_classes,t_steps));I_F_O = np.zeros((num_classes,t_steps))
    I_F_O_Brier = np.zeros((num_classes,t_steps))

    for j in range(t_steps):
        I_O = np.zeros(num_classes)
        for i in range(num_classes):

            if I_observation[j]<classes[i]:
                I_O[i] = 1
                
            I_prediction = np.sort(I_predictions[j,:])
            ID_F = np.where(I_prediction<classes[i])[0]
            I_F[i] = ID_F.size/num_mem
            I_F_O[i,j] = np.abs(I_F[i] - I_O[i])**2*class_step
            
            I_F_O_Brier[i,:] = em.ens_brier(obs=I_observation, fcst_ens=I_predictions,threshold=classes[i])

            I_benchmark = np.sort(I_benchmarks[j,:])
            ID_B = np.where(I_benchmark<classes[i])[0]
            I_B[i] = ID_B.size/num_mem
            I_B_O[i,j] = np.abs(I_B[i] - I_O[i])**2*class_step
            
    I_RPS_FC_t = np.sum(I_F_O,axis = 0) # sum for all the classes/categories
    I_RPS_CL_t = np.sum(I_B_O,axis = 0) # sum for all the classes/categories

    I_RPS_FC = np.mean(I_RPS_FC_t) # average of the values across the time frame
    I_RPS_CL = np.mean(I_RPS_CL_t) # average of the values across the time frame
    
    #I_RPSS_t = 1 - (I_RPS_FC_t/I_RPS_CL_t)
    I_RPSS = 1 - (I_RPS_FC/I_RPS_CL)

    # Rainfall
    Rain_obs_max = np.max(Rain_observation);Rain_ben_max = np.max(Rain_benchmarks);Rain_pred_max = np.max(Rain_predictions)
    class_max = np.max(np.array([Rain_obs_max,Rain_ben_max,Rain_pred_max])) # np.array because inside of a numpy function there shouldn't be a list
    classes = np.arange(1,class_max,class_step)
    num_classes = len(classes)
    
    Rain_F = np.zeros(num_classes); Rain_B = np.zeros(num_classes)
    Rain_B_O = np.zeros((num_classes,t_steps));Rain_F_O = np.zeros((num_classes,t_steps))

    for j in range(t_steps):
        Rain_O = np.zeros(num_classes)
        for i in range(num_classes):

            if Rain_observation[j]<classes[i]:
                Rain_O[i] = 1
                
            Rain_prediction = np.sort(Rain_predictions[j,:])
            ID_F = np.where(Rain_prediction<classes[i])[0]
            Rain_F[i] = ID_F.size/num_mem
            Rain_F_O[i,j] = (Rain_F[i] - Rain_O[i])**2*class_step

            Rain_benchmark = np.sort(Rain_benchmarks[j,:])
            ID_B = np.where(Rain_benchmark<classes[i])[0]
            Rain_B[i] = ID_B.size/num_mem
            Rain_B_O[i,j] = (Rain_B[i] - Rain_O[i])**2*class_step
            
    Rain_RPS_FC_t = np.sum(Rain_F_O,axis = 0)
    Rain_RPS_CL_t = np.sum(Rain_B_O,axis = 0)

    Rain_RPS_FC = np.mean(Rain_RPS_FC_t)
    Rain_RPS_CL = np.mean(Rain_RPS_CL_t)
    
    #Rain_RPSS_t = 1 - (Rain_RPS_FC_t/Rain_RPS_CL_t)
    Rain_RPSS = 1 - (Rain_RPS_FC/Rain_RPS_CL)
    
    return I_RPS_FC,I_RPS_CL,I_RPSS,Rain_RPS_FC,Rain_RPS_CL,Rain_RPSS

print(em.ens_brier(obs=I_observation, fcst_ens=I_predictions,threshold=175))

#start = time.time()
#XX = Forecast_SkillScore_RPSS(I_observation,I_benchmarks,I_predictions,Rain_observation,Rain_benchmarks,Rain_predictions)
#end = time.time()
#print("Elapsed (with compilation) = %s" % (end - start))
#    
#start = time.time()
#XX = Forecast_SkillScore_RPSS(I_observation,I_benchmarks,I_predictions,Rain_observation,Rain_benchmarks,Rain_predictions)
#end = time.time()
#print("Elapsed (after compilation) = %s" % (end - start))
#
#start = time.time()
#XX = Forecast_SkillScore_RPSS(I_observation,I_benchmarks,I_predictions,Rain_observation,Rain_benchmarks,Rain_predictions)
#end = time.time()
#print("Elapsed (after compilation) = %s" % (end - start))

def Forecast_SkillScore_Brier(I_observation,I_benchmarks,I_predictions,Rain_observation,Rain_benchmarks,Rain_predictions):

    # Inflows
    I_obs_max = np.max(I_observation);I_ben_max = np.max(I_benchmarks);I_pred_max = np.max(I_predictions)
    threshold = np.max(np.array([I_obs_max,I_ben_max,I_pred_max])) # np.array needed because inside of a numpy function there shouldn't be a list
    class_step = 1
    classes = np.arange(1,threshold,class_step)
    num_classes = len(classes)
    N = I_predictions.shape[0]
    num_mem = I_predictions.shape[1]
    
    p_F = np.zeros((num_classes,N)); p_B = np.zeros((num_classes,N)); o = np.zeros((num_classes,N))
    I_p_o_B = np.zeros((num_classes,N));I_p_o_F = np.zeros((num_classes,N))
#    ID_F = np.zeros((num_classes,N)); ID_B = np.zeros((num_classes,N))
#    I_B_O_Brier_em = np.zeros((num_classes,t_steps));I_F_O_Brier_em = np.zeros((num_classes,t_steps))
    
    I_Rel_F = np.zeros(len(classes))
    I_Res_F = np.zeros(len(classes))
    I_Unc_F = np.zeros(len(classes))
    
    for i in range(num_classes):
        
        for t in range(N):

            if I_observation[t]<classes[i]:
                o[i,t] = 1
                
            I_prediction = I_predictions[t,:]
            ID_F = np.where(I_prediction<classes[i])[0]
            p_F[i,t] = ID_F.size/num_mem
            I_p_o_F[i,t] = (p_F[i,t] - o[i,t])**2

            I_benchmark = I_benchmarks[t,:]
            ID_B = np.where(I_benchmark<classes[i])[0]
            p_B[i,t] = ID_B.size/num_mem
            I_p_o_B[i,t] = (p_B[i,t] - o[i,t])**2
            
#        I_F_O_Brier_em[i,:] = em.ens_brier(obs=I_observation, fcst_ens=I_predictions,threshold=classes[i])
#        I_B_O_Brier_em[i,:] = em.ens_brier(obs=I_observation, fcst_ens=I_benchmarks,threshold=classes[i])
        
        ### Brier score decomposition ###
        o_mean = np.mean(o,axis=1)
        
        K = 1
        prob_class_step = 0.01
        bins = np.arange(0,K,prob_class_step)
        nk = np.zeros(bins.size)
        Pk = np.zeros(bins.size)
        ok = np.zeros(bins.size)
        pk_ok = np.zeros(bins.size)
        ok_o  = np.zeros(bins.size)
        
        count = 0
        for k in np.arange(0,K,prob_class_step):
            bin0 = k
            bin1 = k+prob_class_step
            ID_Pk = np.where((p_F[i,:]>bin0) & (p_F[i,:]<=bin1))[0]
            nk[count] = len(ID_Pk)
            if nk[count]>0:
                Pk[count] = np.mean(p_F[i,ID_Pk])
                ok[count] = np.mean(o[i,ID_Pk])
                pk_ok[count] = nk[count]*(Pk[count]-ok[count])**2
                ok_o[count] = nk[count]*(o_mean[i]-ok[count])**2
                
            count = count + 1
        I_Rel_F[i] = np.sum(pk_ok)/N
        I_Res_F[i] = np.sum(ok_o)/N
        I_Unc_F[i] = o_mean[i]*(1-o_mean[i])

    I_Brier_F_i = np.sum(I_p_o_F,axis = 1)/N # average over time
    I_Brier_B_i = np.sum(I_p_o_B,axis = 1)/N # average over time
    
    I_Brier = 1 - (I_Brier_F_i/I_Brier_B_i) # Brier score for each class/category (i)
    
#    RPS_F_Brier = np.sum(I_Brier_F_i)
#    RPS_F_Brier_decomp = np.sum(I_Rel_F) + np.sum(I_Res_F) + np.sum(I_Unc_F)
    
    return I_Brier