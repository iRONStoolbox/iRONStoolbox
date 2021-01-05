# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 12:51:56 2019

This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi and at 
Bristol University (2020).

Licence: MIT
"""
import numpy as np
import pandas as pd
from datetime import timedelta

def curve(curve_points): # 1 April = 91 day of the year
    
    x = np.array(curve_points)
    
    points_dim  = x.shape[0]
    
    di    = np.zeros(points_dim)
    ydayi = np.zeros(points_dim)
    si    = np.zeros(points_dim)
    
    di[0]    = pd.to_datetime(x[0,0], format = '%d %b').dayofyear
    ydayi[0] = di[0]
    si[0]    = x[0,1]
    
    for i in np.arange(1,points_dim):
        di[i] = pd.to_datetime(x[i,0], format = '%d %b').dayofyear
        
        if di[i]<di[0]:
            ydayi[i] = di[i] + 366
        else:
            ydayi[i] = di[i]
        si[i] = x[i,1]
    
    ydayi[-1] = di[0] + 366

    yday1      = np.arange(ydayi[0],ydayi[-1]+1)
    s_ydate    = np.interp(yday1, ydayi, si)
    yday       = np.concatenate((np.arange(ydayi[0],366+1),np.arange(1,ydayi[0])))
    ydate      = []
    s_yday     = np.zeros(366)
    
    for i in range(366):
        ydate    = np.append(ydate, pd.to_datetime(x[0,0]+' '+str(1900), format = '%d %b %Y') + timedelta(days = i))
        s_yday[i] = s_ydate[np.where(yday == i+1)]
    ydate = pd.to_datetime(ydate)
    
    return ydate, s_ydate, s_yday

def rule_curve(release,date,s_yday):
    c_dim = np.ndim(s_yday)
    T = date.shape[0]
    s_step = 0.01
    s_frac = np.arange(0,1+s_step,s_step)
    
    rc = np.zeros([T,len(s_frac)])
    
    for t in range(T):
        for i in range(len(s_frac)):
            rc[t,i] = release[0]
            for j in range(c_dim):
                if s_frac[i]>s_yday[j,0]:
                    rc[t,i] = release[j+1]
                    
    return rc
    