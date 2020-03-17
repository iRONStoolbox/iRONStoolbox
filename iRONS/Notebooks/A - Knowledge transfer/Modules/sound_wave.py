# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 13:01:41 2018

@author: ap18525
"""
import numpy as np

def sound_wave():
    amp = 2.7 # amplitude
    phase = 0.6 # phase
    freq = 4.2 # frequency
    x = np.linspace(0,1,500) # x axis from 0 to 1 with a 1/500 step
    y = amp * np.sin(2 * np.pi * (freq * x + phase))
    return x,y
