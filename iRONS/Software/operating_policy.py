# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 12:51:56 2019

This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi at 
Bristol University (2020).

Licence: MIT
"""
import numpy as np

### Piece-wise linear ###
def op_piecewiselin_1res(param,*args):
    """ This function creates a reservoir operating curve that determines the
    reservoir releases (u) as a function of the storage fraction (s).
    s_frac is the reservoir storage scaled by the reservoir active capacity, so 
    that in the operating policy function the storage fraction (s) varies 
    between 0 (dead storage) and 1 (full storage). The policy is a piece-wise 
    linear function of the storage defined a points, which are the parameters 
    of the function. 
    
    Inputs = (param,*args)
    Outputs = u
    
    param = list coordinates of the points that define the operating policy [s,u]
        Please note that the storage must be scaled by the reservoir active 
        capacity, so that in the operating policy function the storage fraction 
        (s) varies between 0 (dead storage) and 1 (full storage)
        Example: param = [[0,2],[0.4,5],[1,10]]
    *args = optional argument that defines a single storage value. If this
        argument is provided then the function will only output the value of
        the realease that corresponds to the storage value provided. Otherwise,
        the function outputs all the releases values that correspond, according
        to the operating policy, to the storage values from 0 to 1.
        
    u = reservoir releases determined by the operating policy and that 
        correspond to the storage fraction values from 0 (dead storage) to 1
        (full storage). This corresponds to the total regulated releases to the 
        downstream river so if for instance, in a reservoir part of the 
        outflows are deviated to a treatment works the splitting of the flow
        should be done out of this function. Note: If *args is provided then u 
        is a single value.
    
    """
    # ----------------
    # Read parameters:
    # ----------------
    x           = np.array(param)
    points_dim  = x.shape[0]
    
    # ------------------------
    # Variables initialization
    # ------------------------
    si = np.zeros(points_dim)
    ui = np.zeros(points_dim)
    for i in range(points_dim):
        si[i] = np.min(x[i:,0])
        ui[i] = np.min(x[i:,1])
    si[0] = 0; si[-1] = 1
    
    # ------------------------
    # Reservoir release policy
    # ------------------------
    if args:
        s = args
        policy_rel = np.interp(s, si, ui)
    else:
        s_step = 0.01
        s_frac = np.arange(0,1+s_step,s_step)
        u = np.zeros([len(s_frac),1]) + np.nan 
        for i in np.arange(len(s_frac)):
            u[i,0] = np.interp(s_frac[i], si, ui) 
    
    return u

### Logarithmic-Exponential by Proussevitch et al (2016) ###
def op_logexp_1res_v1(param,*args):
    """ This function creates a reservoir operating curve that determines the
    reservoir releases (u) as a function of the storage fraction (s_frac).
    s_frac is the reservoir storage scaled by the reservoir active capacity, so 
    that in the operating policy function s_frac varies between 0 (dead storage) 
    and 1 (full storage). This curve is an adaptation of the one proposed by 
    Proussevitch et al (2016) and consists of two segments:
        1. reservoir storage below the reference storage (s_frac < s_frac_ref) - Logarithmic behavior:
            
            u = (u_frac_min + ln(k*s_frac**α + 1)) * u_ref 
                
            where:
                k = 1 / (s_frac_ref**(α)) * (exp(1 - u_frac_min) - 1)
            
        2. reservoir storage above the reference storage (s_frac ≥ s_frac_ref) - Exponential behavior:
            
            u = exp(b*(s_frac - s_frac_ref)**2) * u_ref
        
    Inputs = (param,*args)
    Outputs = u
    
    param = list of the parameters that define the operating policy 
        [u_frac_min, s_frac_ref, α, b, u_ref] 
        
        u_frac_min = minimum allowed reservoir release scaled by the release at the 
                     reference storage.
        
        s_frac_ref = reference reservoir storage fraction. When the reservoir is at 
                     this level the reservoir release is equal to the reference release,
                     e.g. target demand. It varies from 0 to 1.
        
        α     = shape parameter for the logarithmic.
        
        b     = shape parameter for the exponential.
        
        u_ref = reference or target release. Reservoir release when the 
                s = s_ref. This value can be defined for instance as the target 
                demand or as the average annual discharge over the past 5 years - [vol/Dt]
                
    *args = optional argument that defines a single storage value. If this
        argument is provided then the function will only output the value of
        the realease that corresponds to the storage value provided. Otherwise,
        the function outputs all the releases values that correspond, according
        to the operating policy, to the storage values from 0 to 1.
        
    u = reservoir releases determined by the operating policy and that 
        correspond to the storage fraction values from 0 (dead storage) to 1
        (full storage). This corresponds to the total regulated releases to the 
        downstream river so if for instance, in a reservoir part of the 
        outflows are deviated to a treatment works the splitting of the flow
        should be done out of this function. Note: If *args is provided then u 
        is a single value.
        
    References:Proussevitch, A., et al.: Log-Exponential Reservoir Operating 
                   Rules for Global And Regional Hydrological Modeling, in: AGU 
                   Fall Meeting 2013, 9–13 December2013, San Francisco, CA, USE, GC21B-0827, 2013.
               Oyerinde et al: Quantifying Uncertainties in Modeling Climate 
                   Change Impacts on Hydropower Production, Climate, 4, 34, 
                   https://doi.org/10.3390/cli4030034, 2016.

    
    """
    
    # ----------------
    # Read parameters:
    # ----------------
    u_frac_min, s_frac_ref, α, b, u_ref = param
    
    # ------------------------
    # Reservoir release policy
    # ------------------------
    if args:
        s_frac = args[0]
        if s_frac < s_frac_ref:
            # Logarihmic segment (s_frac < s_frac_ref)
            k = 1 / (s_frac_ref**α) * (np.exp(1 - u_frac_min) - 1) 
            u = (u_frac_min + np.log(k*s_frac**α + 1)) * u_ref
        elif s_frac >= s_frac_ref:
            # Exponential segment (s_frac < s_frac_ref)
            u = np.exp(b*(s_frac - s_frac_ref)**2) * u_ref
    else:
        s_step = 0.01
        s_frac = np.arange(0,1+s_step,s_step)
        u = np.zeros([len(s_frac),1]) + np.nan 
        # Logarihmic segment (s_frac < s_frac_ref)
        k = 1 / (s_frac_ref**(α)) * (np.exp(1 - u_frac_min) - 1) 
        u[s_frac<s_frac_ref,0] = (u_frac_min + np.log(k*s_frac[s_frac<s_frac_ref]**α + 1)) * u_ref 
        # Exponential segment (s_frac < s_frac_ref)
        u[s_frac>=s_frac_ref,0] = np.exp(b*(s_frac[s_frac>=s_frac_ref] - s_frac_ref)**2) * u_ref
        
    return u

### Logarithmic-Exponential by Rouge et al (2021) ###
def op_logexp_1res_v2(param,*args):
    """ This function creates a reservoir operating curve that determines the
    reservoir releases (u) as a function of the storage fraction (s_frac).
    s_frac is the reservoir storage scaled by the reservoir active capacity, so 
    that s_frac varies between 0 (dead storage) and 1 (full storage). This 
    curve is an adaptation of the one proposed by Rouge et al (2021) and 
    consists of two segments:
        
        1. reservoir storage below optimal level (s < s_ref) - Logarithmic behavior:
            
            u = (u_frac_min + ln(1 + p_rel*s_frac)/ln(1 + p_rel*s_frac_ref) * 
                 (u_frac_ref - u_frac_min)) * u_ref
            
        2. reservoir storage above optimal level (s ≥ s_ref)- Exponential behavior:
            
            u = (u_frac_ref + ((s_frac-s_frac_ref+Δs)**p_sto - Δs**p_sto)/
                ((1-s_frac_ref+Δs)**p_sto - Δs**p_sto) * (u_frac_max-u_frac_ref)) * u_ref
        
    Inputs = (param,*args)
    Outputs = u
    
    param = list of the parameters that define the operating policy 
        [u_frac_min, u_frac_max, s_frac_ref, u_frac_ref, p_rel, p_sto, u_ref, Δs] 
        
        u_frac_min = minimum allowed reservoir release scaled by the reference
                     release
                
        u_frac_max = max allowed reservoir release scaled by the reference 
                     release
        
        s_frac_ref = reference reservoir storage fraction. When the reservoir is at 
                     this level the reservoir release is equal to the reference release,
                     e.g. target demand. It varies from 0 to 1.
        
        u_frac_ref = reference fractional release when s_frac = s_frac_ref
        
        p_rel = shape parameter for the logarithmic segment that controls the
                propensity for release at low storage. p_rel close to zero leads 
                to an almost linear rule, whereas high values, the more release 
                comes close to u_ref even for near-empty storage.
        
        p_sto = shape parameter for the exponential segment that controls the
                propensity for storage at near-full storage. It minimizes 
                releases until storage is close to its maximal level.

        u_ref = reference or target release. Reservoir release when 
                s_frac = s_frac_ref. This value can be defined for instance as 
                the target demand or as the average annual discharge over the 
                past 5 years - [vol/Dt]
                
        Δs    = ensures that the transition between the logarithmic and 
                exponential segments of the operating curve is smooth 
                (continuously differentiable). It is computed from the other 
                parameters. 

    *args = optional argument that defines a single storage value. If this
        argument is provided then the function will only output the value of
        the realease that corresponds to the storage value provided. Otherwise,
        the function outputs all the releases values that correspond, according
        to the operating policy, to the storage values from 0 to 1.
        
    u = reservoir releases determined by the operating policy and that 
        correspond to the storage fraction values from 0 (dead storage) to 1
        (full storage). This corresponds to the total regulated releases to the 
        downstream river so if for instance, in a reservoir part of the 
        outflows are deviated to a treatment works the splitting of the flow
        should be done out of this function. Note: If *args is provided then u 
        is a single value.
        
    References:Rouge et al 2021,  Hydrol. Earth Syst. Sci., 25, 1365–1388, 2021 
               https://doi.org/10.5194/hess-25-1365-2021

    """
    # ----------------
    # Read parameters:
    # ----------------
    u_frac_min, u_frac_max, s_frac_ref, u_frac_ref, p_rel, p_sto, u_ref, Δs = param
    
    # ------------------------
    # Reservoir release policy
    # ------------------------
    if args:
        s_frac = args[0]
        if s_frac < s_frac_ref:
            # Logarihmic segment (s < s_ref)
            u = (u_frac_min + np.log(1 + p_rel*s_frac)/np.log(1 + p_rel*s_frac_ref) * (u_frac_ref - u_frac_min)) * u_ref
        elif s_frac >= s_frac_ref:
            # Exponential segment (s < s_ref)
            u = (u_frac_ref + ((s_frac-s_frac_ref+Δs)**p_sto - Δs**p_sto)/((1-s_frac_ref+Δs)**p_sto - Δs**p_sto) * (u_frac_max-u_frac_ref)) * u_ref
    else:
        s_step = 0.01
        s_frac = np.arange(0,1+s_step,s_step)
        u = np.zeros([len(s_frac),1]) + np.nan 
        # Logarihmic segment (s < s_ref)
        u[s_frac<s_frac_ref,0] = (u_frac_min + np.log(1 + p_rel*s_frac[s_frac<s_frac_ref])/np.log(1 + p_rel*s_frac_ref) * (u_frac_ref - u_frac_min)) * u_ref
        # Exponential segment (s < s_ref)
        u[s_frac>=s_frac_ref,0] = (u_frac_ref + ((s_frac[s_frac>=s_frac_ref]-s_frac_ref+Δs)**p_sto - Δs**p_sto)/((1-s_frac_ref+Δs)**p_sto - Δs**p_sto) * (u_frac_max - u_frac_ref)) * u_ref
        
    return u