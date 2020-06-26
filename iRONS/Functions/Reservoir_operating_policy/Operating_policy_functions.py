# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 12:51:56 2019

This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi and at 
Bristol University (2020).

Licence: MIT
"""
import numpy as np

def three_points_policy(param,*args):
    x0, x1, x2, u_mean = param
    si = np.array([x0[0],
                   np.min([x1[0], x2[0]]),
                   x2[0]])
    ui = np.array([np.min([x0[1], x1[1], x2[1]]),
                   np.min([x1[1], x2[1]]),
                   x2[1]])
    if args:
        s = args
        u = np.interp(s, si, ui)*u_mean
    else:
        s_step = 0.01
        s = np.arange(0,1+s_step,s_step)
        u = np.interp(s, si, ui)*u_mean
    
    return u

def four_points_policy(param,*args):
    x0, x1, x2, x3, u_mean = param
    si = np.array([x0[0],
                   np.min([x1[0], x3[0]]),
                   np.min([x2[0], x3[0]]),
                   x3[0]])
    ui = np.array([np.min([x0[1], x1[1], x3[1]]),
                   np.min([x1[1], x3[1]]),
                   np.min([x2[1], x3[1]]),
                   x3[1]])
    if args:
        s = args
        u = np.interp(s, si, ui)*u_mean
    else:
        s_step = 0.01
        s = np.arange(0,1+s_step,s_step)
        u = np.interp(s, si, ui)*u_mean
    
    return u

def five_points_policy(param,*args):
    x0, x1, x2, x3, x4, u_mean = param
    si = np.array([x0[0],
                   np.min([x1[0], x4[0]]),
                   np.min([x2[0], x4[0]]),
                   np.min([x3[0], x4[0]]),
                   x4[0]])
    ui = np.array([np.min([x0[1], x1[1], x4[1]]),
                   np.min([x1[1], x4[1]]),
                   np.min([x2[1], x4[1]]),
                   np.min([x2[1], x4[1]]),
                   x4[1]])
    if args:
        s = args
        u = np.interp(s, si, ui)*u_mean
    else:
        s_step = 0.01
        s = np.arange(0,1+s_step,s_step)
        u = np.interp(s, si, ui)*u_mean
    
    return u