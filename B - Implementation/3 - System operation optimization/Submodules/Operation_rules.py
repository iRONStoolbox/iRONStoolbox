# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 12:51:56 2019

@author: andro
"""
import numpy as np

#def release_rule(R_ref, S_ref, S_max, s, x):
#    
#    si = np.array([0,
#                   np.min([R_ref / np.tan(x[0]),
#                           S_ref + S_ref / (np.tan(np.pi/4) / np.tan(x[0]) - 1)]),
#                   np.min([R_ref / np.tan(x[0]) + x[1],
#                           R_ref / np.tan(np.pi/4) + S_ref]),
#                   S_max])
#    ui = np.array([0,
#                   np.min([R_ref, S_ref / (np.tan(np.pi/4) / np.tan(x[0]) - 1) * np.tan(np.pi/4)]),
#                   R_ref,
#                   R_ref+(S_max - np.min([R_ref/np.tan(x[0]) + x[1],
#                                          R_ref/np.tan(np.pi/4) + S_ref]))*np.tan(x[2])])
#    u = np.interp(s, si, ui)
#    return u

def release_rule(param,*args):
    x0, x1, x2, x3, r_mean = param
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
        u = np.interp(s, si, ui)*r_mean
    else:
        s_step = 0.01
        s = np.arange(0,1+s_step,s_step)
        u = np.interp(s, si, ui)*r_mean
    
    return u