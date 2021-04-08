# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 12:51:56 2019

This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi and at 
Bristol University (2020).

Licence: MIT
"""
import numpy as np
import pandas as pd
#from datetime import timedelta

def rule_curve(param): 
    
    ### Curves definition ###
    curves      = param['curves']
    points_date = np.array(curves['year_date'])
    points_s    = np.array(curves['storage_frac'])
    
    points_num = points_s.shape[1]
    curves_num = points_s.shape[0]
    
    di    = np.zeros(points_num)
    ydayi = np.zeros(points_num)
    si    = np.zeros([curves_num,points_num])
    
    
    di[0]    = pd.to_datetime(points_date[0], format = '%d %b').dayofyear
    ydayi[0] = di[0]
    si[:,0]    = points_s[:,0]
    
    for i in np.arange(1,points_num):
        di[i] = pd.to_datetime(points_date[i], format = '%d %b').dayofyear
        
        if di[i]<di[0]:
            ydayi[i] = di[i] + 366
        else:
            ydayi[i] = di[i]
    
    ydayi[-1] = di[0] + 366
    yday1      = np.arange(ydayi[0],ydayi[-1]+1)
    yday       = np.concatenate((np.arange(ydayi[0],366+1),np.arange(1,ydayi[0])))
#    ydate      = []
    s_yday     = np.zeros([curves_num,366])
    
    for j in np.arange(0,curves_num):
        s_ydate    = np.interp(yday1, ydayi, points_s[j])

        for i in range(366):
    #        ydate    = np.append(ydate, pd.to_datetime(x[0,0]+' '+str(1900), format = '%d %b %Y') + timedelta(days = i))
            s_yday[j,i] = s_ydate[np.where(yday == i+1)]
#    ydate = pd.to_datetime(ydate)

    ### Rules definition ####
    rules      = param['rules']
    points_date = np.array(rules['year_date'])
    points_r    = np.array(rules['release'])
    
    points_num = points_r.shape[1]
    rules_num = points_r.shape[0]
    
    di    = np.zeros(points_num)
    ydayi = np.zeros(points_num)
    ri    = np.zeros([rules_num,points_num])
    
    
    di[0]    = pd.to_datetime(points_date[0], format = '%d %b').dayofyear
    ydayi[0] = di[0]
    ri[:,0]    = points_r[:,0]
    
    for i in np.arange(1,points_num):
        di[i] = pd.to_datetime(points_date[i], format = '%d %b').dayofyear
        
        if di[i]<di[0]:
            ydayi[i] = di[i] + 366
        else:
            ydayi[i] = di[i]
    
    ydayi[-1] = di[0] + 366
    yday1      = np.arange(ydayi[0],ydayi[-1]+1)
    yday       = np.concatenate((np.arange(ydayi[0],366+1),np.arange(1,ydayi[0])))
    r_yday     = np.zeros([rules_num,366])
    
    for j in np.arange(0,rules_num):
        r_ydate    = np.interp(yday1, ydayi, points_r[j])

        for i in range(366):
            r_yday[j,i] = r_ydate[np.where(yday == i+1)]    
            
    return s_yday,r_yday

#def rule_curve(release,date,s_yday):
#    c_dim = np.ndim(s_yday)
#    T = date.shape[0]
#    s_step = 0.01
#    s_frac = np.arange(0,1+s_step,s_step)
#    
#    rc = np.zeros([T,len(s_frac)])
#    
#    for t in range(T):
#        for i in range(len(s_frac)):
#            rc[t,i] = release[0]
#            for j in range(c_dim):
#                if s_frac[i]>s_yday[j,0]:
#                    rc[t,i] = release[j+1]
#                    
#    return rc
    