# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:45:43 2019

@author: ap18525
"""
import numpy as np
from platypus import NSGAII, Problem, Real

from Subroutines.HBV_sim import HBV_sim

def HBV_calibration(P,E,Case,area, Q_obs, objective):

    if objective == 'all':
        num_objectives = 1
        population_size = 1
        # Consider the entire hydrograph
        pass
    elif objective == 'low':
        num_objectives = 1
        population_size = 1
        low_flow_indexes = [Q_obs < np.percentile(Q_obs,50)]
        Q_obs_low = Q_obs[low_flow_indexes]
    elif objective == 'high':
        num_objectives = 1
        population_size = 1
        high_flow_indexes = [Q_obs > np.percentile(Q_obs,50)]
        Q_obs_high = Q_obs[high_flow_indexes]
    elif objective == 'double':
        num_objectives = 2
        population_size = 100
        low_flow_indexes = [Q_obs < np.percentile(Q_obs,50)]
        Q_obs_low = Q_obs[low_flow_indexes]
        high_flow_indexes = [Q_obs > np.percentile(Q_obs,50)]
        Q_obs_high = Q_obs[high_flow_indexes]
    
    def auto_calibration(vars):
            
        SSM0   = vars[0]
        SUZ0   = vars[1]
        SLZ0   = vars[2]
        
        BETA   = vars[3]
        LP     = vars[4]
        FC     = vars[5]
        PERC   = vars[6]
        K0     = vars[7]
        K1     = vars[8]
        K2     = vars[9]
        UZL    = vars[10]
        MAXBAS = vars[11]
        
        ini    = [SSM0,SUZ0,SLZ0]
        param  = [BETA, LP, FC, PERC, K0, K1, K2, UZL, MAXBAS]
        
        Q_sim,[SM,UZ,LZ],[EA,R,RL,Q0,Q1] = HBV_sim(P,E,param,Case,ini,area)
        
        if objective == 'all':
            # Consider the entire hydrograph
            value = np.sqrt(((Q_sim - Q_obs) ** 2).mean())
            return [value]
        elif objective == 'low':
            Q_sim_low = Q_sim[low_flow_indexes]
            value = np.sqrt(((Q_sim_low - Q_obs_low) ** 2).mean())
            return [value]
        elif objective == 'high':
            Q_sim_high = Q_sim[high_flow_indexes]
            value = np.sqrt(((Q_sim_high - Q_obs_high) ** 2).mean())
            return [value]
        elif objective == 'double':
            Q_sim_low = Q_sim[low_flow_indexes]
            Q_sim_high = Q_sim[high_flow_indexes]
            value = [np.sqrt(((Q_sim_low - Q_obs_low) ** 2).mean()),np.sqrt(((Q_sim_high - Q_obs_high) ** 2).mean())]
            return value
        

    problem = Problem(12,num_objectives)
    real0 = Real(0, 400)
    real1 = Real(0, 100)
    real2 = Real(0, 100)
    real3 = Real(0, 7)
    real4 = Real(0.3, 1)
    real5 = Real(1, 2000)
    real6 = Real(0, 100)
    real7 = Real(0.05, 2)
    real8 = Real(0.01, 1)
    real9 = Real(0, 0.1)
    real10 = Real(0, 100)
    real11 = Real(1, 6)
    problem.types[:] = [real0] + [real1] + [real2] + [real3] + [real4] + [real5] + [real6] + [real7] + [real8] + [real9]  + [real10] + [real11]
    problem.function = auto_calibration
    
    algorithm = NSGAII(problem,population_size)
    algorithm.run(1000) # Number of iterations
    
    if objective == 'double':
        results_low = np.array([algorithm.result[i].objectives[0] for i in range(population_size)])
        results_high = np.array([algorithm.result[i].objectives[1] for i in range(population_size)])
    else:
        results = np.array([algorithm.result[i].objectives[0] for i in range(population_size)])
        
    solution = [algorithm.result[i].variables[0:12] for i in range(population_size)]
    
    RMSE = [np.sqrt(((HBV_sim(P,E,solution[i][3:13],Case,solution[i][0:3],area)[0] - Q_obs) ** 2).mean()) for i in range(population_size)]
    
    if objective == 'double':
        return results_low, results_high, solution, RMSE
    else:
        return results, solution, RMSE