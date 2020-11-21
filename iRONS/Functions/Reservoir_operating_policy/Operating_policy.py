# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 12:51:56 2019

This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi at 
Bristol University (2020).

Licence: MIT
"""
import numpy as np

def policy_function(param,*args):
    x           = np.array(param)
    points_dim  = x.shape[0]
    
    si = np.zeros(points_dim)
    ui = np.zeros(points_dim)
    for i in range(points_dim):
        si[i] = np.min(x[i:,0])
        ui[i] = np.min(x[i:,1])
    si[0] = 0; si[-1] = 1
        
    if args:
        s = args
        u = np.interp(s, si, ui)
    else:
        s_step = 0.01
        s = np.arange(0,1+s_step,s_step)
        u = np.interp(s, si, ui)   
    
    return u
