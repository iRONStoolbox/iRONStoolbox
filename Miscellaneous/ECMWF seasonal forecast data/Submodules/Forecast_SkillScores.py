# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 16:51:42 2018

@author: ap18525
"""
#import time
import numpy as np
from numba import jit
import hydrostats.ens_metrics as em

def CRPS_score(obser,forec,bench):
    
    #CRPSS
    CRPS_B_k = em.ens_crps(obser,bench)
    CRPS_F_k = em.ens_crps(obser,forec)

    CRPS_B_t = CRPS_B_k['crps']
    CRPS_F_t = CRPS_F_k['crps']

    CRPS_B = CRPS_B_k['crpsMean']
    CRPS_F = CRPS_F_k['crpsMean']
    
    CRPSS_t = 1 - (CRPS_F_t/CRPS_B_t)
    CRPSS = 1 - (CRPS_F/CRPS_B)

    return CRPS_F,CRPS_B,CRPSS,CRPS_F_t,CRPS_B_t,CRPSS_t

@jit(nopython=True) # Set "nopython" mode for best performance, equivalent to @njit
def RPS_score(obser,forec,bench):
    
    # RPSS
    obs_max = np.nanmax(obser);ben_max = np.nanmax(bench);pred_max = np.nanmax(forec)
    class_max = np.nanmax(np.array([obs_max,ben_max,pred_max])) # np.array needed because inside of a numpy function there shouldn't be a list
    class_step = 1
    classes = np.arange(1,class_max,class_step)
    num_classes = len(classes)
    t_steps = forec.shape[0]
    num_mem_F = forec.shape[1]
    num_mem_B = bench.shape[1]

    F = np.zeros(num_classes); B = np.zeros(num_classes)
    B_O = np.zeros((num_classes,t_steps));F_O = np.zeros((num_classes,t_steps))

    for j in range(t_steps):
        O = np.zeros(num_classes)
        for i in range(num_classes):

            if obser[j]<classes[i]:
                O[i] = 1
                
            prediction = np.sort(forec[j,:])
            ID_F = np.where(prediction<classes[i])[0]
            F[i] = ID_F.size/num_mem_F
            F_O[i,j] = np.abs(F[i] - O[i])**2*class_step
            
            benchmark = np.sort(bench[j,:])
            ID_B = np.where(benchmark<classes[i])[0]
            B[i] = ID_B.size/num_mem_B
            B_O[i,j] = np.abs(B[i] - O[i])**2*class_step
            
    RPS_F_t = np.sum(F_O,axis = 0) # sum for all the classes/categories
    RPS_B_t = np.sum(B_O,axis = 0) # sum for all the classes/categories

    RPS_F = np.nanmean(RPS_F_t) # average of the values across the time frame
    RPS_B = np.nanmean(RPS_B_t) # average of the values across the time frame
    
    RPSS_t = 1 - (RPS_F_t/RPS_B_t) 
    RPSS = 1 - (RPS_F/RPS_B)

    return RPS_F,RPS_B,RPSS,RPS_F_t,RPS_B_t,RPSS_t

@jit(nopython=True) # Set "nopython" mode for best performance, equivalent to @njit
def MyRPS_score(obser,forec,bench):
    # The difference between CDF is not squared
    # My RPSS
    obs_max = np.nanmax(obser);ben_max = np.nanmax(bench);pred_max = np.nanmax(forec)
    class_max = np.nanmax(np.array([obs_max,ben_max,pred_max])) # np.array needed because inside of a numpy function there shouldn't be a list
    class_step = 1
    classes = np.arange(1,class_max,class_step)
    num_classes = len(classes)
    t_steps = forec.shape[0]
    num_mem_F = forec.shape[1]
    num_mem_B = bench.shape[1]

    F = np.zeros(num_classes); B = np.zeros(num_classes)
    B_O = np.zeros((num_classes,t_steps));F_O = np.zeros((num_classes,t_steps))

    for j in range(t_steps):
        O = np.zeros(num_classes)
        for i in range(num_classes):

            if obser[j]<classes[i]:
                O[i] = 1
                
            prediction = np.sort(forec[j,:])
            ID_F = np.where(prediction<classes[i])[0]
            F[i] = ID_F.size/num_mem_F
            F_O[i,j] = np.abs(F[i] - O[i])*class_step
            
            benchmark = np.sort(bench[j,:])
            ID_B = np.where(benchmark<classes[i])[0]
            B[i] = ID_B.size/num_mem_B
            B_O[i,j] = np.abs(B[i] - O[i])*class_step
            
    RPS_F_t = np.sum(F_O,axis = 0) # sum for all the classes/categories
    RPS_B_t = np.sum(B_O,axis = 0) # sum for all the classes/categories

    RPS_F = np.nanmean(RPS_F_t) # average of the values across the time frame
    RPS_B = np.nanmean(RPS_B_t) # average of the values across the time frame
    
    RPSS_t = 1 - (RPS_F_t/RPS_B_t) 
    RPSS = 1 - (RPS_F/RPS_B)

    return RPS_F,RPS_B,RPSS,RPS_F_t,RPS_B_t,RPSS_t

@jit(nopython=False) # Set "nopython" mode for best performance, equivalent to @njit
def Mean_error(obser,forec,bench):
    
    t_steps = obser.shape[0]
    num_mem_F = forec.shape[1]
    num_mem_B = bench.shape[1]

    F_O = np.zeros((t_steps,num_mem_F))
    B_O = np.zeros((t_steps,num_mem_B))
    
    for t in range(t_steps):
        for j in range(num_mem_F):

            F_O[t,j] = forec[t,j] - obser[t]
            
        for k in range(num_mem_B):
        
            B_O[t,k] = bench[t,k] - obser[t]
            
    ME_F_t = F_O.mean(1) # mean of t values
    ME_B_t = B_O.mean(1) # mean of t values

    ME_F = np.nanmean(ME_F_t) # average of the values across the time frame
    ME_B = np.nanmean(ME_B_t) # average of the values across the time frame
    
    ME_score_t = 1 - (ME_F_t/ME_B_t) 
    ME_score = 1 - (ME_F/ME_B)

    return ME_F,ME_B,ME_score,ME_F_t,ME_B_t,ME_score_t

@jit(nopython=False) # Set "nopython" mode for best performance, equivalent to @njit
def Mean_squared_error(obser,forec,bench):
    
    t_steps = obser.shape[0]
    num_mem_F = forec.shape[1]
    num_mem_B = bench.shape[1]

    F_O = np.zeros((t_steps,num_mem_F))
    B_O = np.zeros((t_steps,num_mem_B))
    
    for t in range(t_steps):
        for j in range(num_mem_F):

            F_O[t,j] = (forec[t,j] - obser[t])**2
            
        for k in range(num_mem_B):
        
            B_O[t,k] = (bench[t,k] - obser[t])**2
            
    MSE_F_t = F_O.mean(1) # mean of t values
    MSE_B_t = B_O.mean(1) # mean of t values

    MSE_F = np.nanmean(MSE_F_t) # average of the values across the time frame
    MSE_B = np.nanmean(MSE_B_t) # average of the values across the time frame
    
    MSE_score_t = 1 - (MSE_F_t/MSE_B_t) 
    MSE_score = 1 - (MSE_F/MSE_B)

    return MSE_F,MSE_B,MSE_score,MSE_F_t,MSE_B_t,MSE_score_t

#@jit(nopython=True) # Set "nopython" mode for best performance, equivalent to @njit
def Brier_score(obser,forec,bench):
    # Brier score
    obs_max = np.max(obser);ben_max = np.max(bench);pred_max = np.max(forec)
    threshold = np.max(np.array([obs_max,ben_max,pred_max])) # np.array needed because inside of a numpy function there shouldn't be a list
    class_step = 1
    classes = np.arange(1,threshold,class_step)
    num_classes = len(classes)
    N = forec.shape[0]
    num_mem_F = forec.shape[1]
    num_mem_B = bench.shape[1]
    
    p_F = np.zeros((num_classes,N)); p_B = np.zeros((num_classes,N)); o = np.zeros(N)
    p_o_B = np.zeros((num_classes,N));p_o_F = np.zeros((num_classes,N))
   
    Rel_F = np.zeros(len(classes))
    Res_F = np.zeros(len(classes))
    Unc_F = np.zeros(len(classes))
    
    Rel_B = np.zeros(len(classes))
    Res_B = np.zeros(len(classes))
    Unc_B = np.zeros(len(classes))

    # Forecast    
    for i in range(num_classes):
        
        for t in range(N):

            if obser[t]<classes[i]:
                o[t] = 1
                
            forecast = forec[t,:]
            ID_F = np.where(forecast<classes[i])[0]
            p_F[i,t] = ID_F.size/num_mem_F
            p_o_F[i,t] = (p_F[i,t] - o[t])**2
            
        ### Brier score decomposition ###
        o_mean = o.mean()
        
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
                p_F_i = p_F[i,:]
                Pk[count] = np.mean(p_F_i[ID_Pk])
                ok[count] = np.mean(o[ID_Pk])
                pk_ok[count] = nk[count]*(Pk[count]-ok[count])**2
                ok_o[count] = nk[count]*(o_mean-ok[count])**2
                
            count = count + 1
        Rel_F[i] = np.sum(pk_ok)/N
        Res_F[i] = np.sum(ok_o)/N
        Unc_F[i] = o_mean*(1-o_mean)

    Brier_F = np.sum(p_o_F,axis = 1)/N # average over time
    
    # Benchmark 
    o = np.zeros(N)
    for i in range(num_classes):
        
        for t in range(N):

            if obser[t]<classes[i]:
                o[t] = 1

            benchmark = bench[t,:]
            ID_B = np.where(benchmark<classes[i])[0]
            p_B[i,t] = ID_B.size/num_mem_B
            p_o_B[i,t] = (p_B[i,t] - o[t])**2
            
        ### Brier score decomposition ###
        o_mean = o.mean()
        
        # Benchmark
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
            ID_Pk = np.where((p_B[i,:]>bin0) & (p_B[i,:]<=bin1))[0]
            nk[count] = len(ID_Pk)
            if nk[count]>0:
                p_B_i = p_B[i,:]
                Pk[count] = np.mean(p_B_i[ID_Pk])
                ok[count] = np.mean(o[ID_Pk])
                pk_ok[count] = nk[count]*(Pk[count]-ok[count])**2
                ok_o[count] = nk[count]*(o_mean-ok[count])**2
                
            count = count + 1
        Rel_B[i] = np.sum(pk_ok)/N
        Res_B[i] = np.sum(ok_o)/N
        Unc_B[i] = o_mean*(1-o_mean)

    Brier_B = np.sum(p_o_B,axis = 1)/N # average over time
    
    # Outputs
    Brier = 1 - (Brier_F/Brier_B) # Brier score for each class/category (i)
    
    Outputs_F = [Rel_F,Res_F,Unc_F,Brier_F]
    
    Outputs_B = [Rel_B,Res_B,Unc_B,Brier_B]
    
    Reliability = 1 - np.sum(Rel_F)/np.sum(Rel_B)
    if np.sum(Res_F) == 0 and np.sum(Res_F) == 0:
        Resolution = 0
    else:
        Resolution  = 1 - np.sum(Res_F)/np.sum(Res_F) # The higher the forecast resolution the better
    Uncertainty = np.sum(Unc_F)
    
#    RPS_F_Brier = np.sum(Brier_F)
#    RPS_F_Brier_decomp = np.sum(Rel_F) + np.sum(Res_F) + np.sum(Unc_F)
    
    return Outputs_F,Outputs_B,Brier, Reliability, Resolution, Uncertainty
