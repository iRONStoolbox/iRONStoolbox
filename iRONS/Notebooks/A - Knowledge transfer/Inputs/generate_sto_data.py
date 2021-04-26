# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 17:32:10 2021

@author: andro
"""
import numpy as np
k=0
xx = np.zeros((7305,20))
for i in np.arange(0.5,1.5,0.05):
    xx[:,k]=np.random.normal(loc=35*i, scale=10, size=(7305))
    k = k + 1
    
xx = xx.clip(10)

## 500 replicates of a year time series of the inflow with the mean and SD of the worst drought in records
from scipy.stats import truncnorm
lower = 2
upper = 20
m = 20
s = 20

yy = np.random.normal(loc=20, scale=20, size=(365,5000))
yy = yy.clip(2) # values below 2 are = 2
print(yy.mean(axis=0).mean())
print(yy.std(axis=0).mean())

yy = yy/10
