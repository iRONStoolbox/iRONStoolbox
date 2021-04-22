# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 18:26:41 2019

@author: ap18525
"""
import ipywidgets as widgets
import numpy as np
from scipy.interpolate import interp1d
from bqplot import pyplot as plt
from bqplot import *
from bqplot.traits import *

def Interactive_var_release_policy(date,
                                   res_sys_sim, policy_function,
                                   policy_rel_var, policy_rel_var_idx,
                                   curve_a, curve_b,
                                   I, e, 
                                   s_ini, s_min, s_max, 
                                   Qreg_rel_mean,Qreg_rel_min,Qreg_rel_max,
                                   cs, d):
    
    N = date.size # weeks
    
    #Function to update the rule curve when changing the parameters with the sliders
    def update_policy(s1_1,s1_2,s1_3,s1_4): 
        
        x0_1 = [s_min/s_max, Qreg_rel_min]
        x1_1 = [s1_1,        Qreg_rel_mean]
        x2_1 = [s1_1+s2_inc, Qreg_rel_mean]
        x3_1 = [s_max/s_max, Qreg_rel_max]
        param_1 = [x0_1, x1_1, x2_1, x3_1]
        policy_rel_1 = policy_function(param_1)

        x0_2 = [s_min/s_max, Qreg_rel_min]
        x1_2 = [s1_2,        Qreg_rel_mean]
        x2_2 = [s1_2+s2_inc, Qreg_rel_mean]
        x3_2 = [s_max/s_max, Qreg_rel_max]
        param_2 = [x0_2, x1_2, x2_2, x3_2]
        policy_rel_2 = policy_function(param_2)
        
        x0_3 = [s_min/s_max, Qreg_rel_min]
        x1_3 = [s1_3,        Qreg_rel_mean]
        x2_3 = [s1_3+s2_inc, Qreg_rel_mean]
        x3_3 = [s_max/s_max, Qreg_rel_max]
        param_3 = [x0_3, x1_3, x2_3, x3_3]
        policy_rel_3 = policy_function(param_3) 
        
        param_4 = [x0_1, x1_1, x2_1, x3_1] # equal to the parameters on 1 Jan
        policy_rel_4 = policy_function(param_4)
        
        policy_rel_var = interp1d(def_ydays, np.hstack([policy_rel_1,policy_rel_2,policy_rel_3,policy_rel_4]), 
                                  axis=1,kind = 'linear')(np.arange(1,367))
        
        curve_a = interp1d(def_ydays, [param_1[1][0],param_2[1][0],param_3[1][0],param_4[1][0]], axis=0)(np.arange(1,367))
        curve_b = interp1d(def_ydays, [param_1[2][0],param_2[2][0],param_3[2][0],param_4[2][0]], axis=0)(np.arange(1,367))
        
        Qreg = {'releases' : {'type'  : 'variable operating policy',
                              'input' : policy_rel_var,
                              'index' : policy_rel_var_idx},
                'inflows' : [],
                'rel_inf' : []}
        
        env, spill, Qreg_rel, Qreg_inf, s, E = res_sys_sim(I, e, s_ini, s_min, s_max, Qreg_rel_min, d, Qreg)
        
        TSD = (np.sum((np.maximum(d-Qreg_rel,np.zeros((N,1))))**2)).astype('int')
        fig_1b.title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2'
        
        CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
        fig_1c.title = 'Reservoir storage volume - MSV = '+str(CSV)+' ML'
    
        return curve_a,curve_b, policy_rel_1, policy_rel_2, policy_rel_3, env, spill, Qreg_rel, Qreg_inf, s
    
    # Function to update the figures when changing the parameters with the sliders
    def update_figure(change):
        curve_a_plot.y = update_policy(s1_1.value,s1_2.value,s1_3.value,s1_1.value)[0]
        curve_b_plot.y = update_policy(s1_1.value,s1_2.value,s1_3.value,s1_1.value)[1]
        pol_func_1.y   = update_policy(s1_1.value,s1_2.value,s1_3.value,s1_1.value)[2]
        pol_func_2.y   = update_policy(s1_1.value,s1_2.value,s1_3.value,s1_1.value)[3]
        pol_func_3.y   = update_policy(s1_1.value,s1_2.value,s1_3.value,s1_1.value)[4]
        releases.y = update_policy(s1_1.value,s1_2.value,s1_3.value,s1_1.value)[7][:,0]
        storage.y = update_policy(s1_1.value,s1_2.value,s1_3.value,s1_1.value)[9][:,0]
    
    # Definition of the sliders (Points defining the curves) 
    def_ydays = [1, 121, 244, 366] # year days corresponding to '1 Jan', '1 May', '1 Sep', '31 Dec' 
    s1_1 = widgets.FloatSlider(min=0, max=0.705, value=0.60, step=0.01, 
                                description = 's1 at 1 Jan: ',
                                orientation='vertical',
                                layout={'width': '100px'},
                                continuous_update=False)
    s1_1.observe(update_figure,names = 'value')
    
    s1_2 = widgets.FloatSlider(min=0, max=0.705, value=0.30, step=0.01, 
                                description = 's1 at 1 May: ',
                                orientation='vertical',
                                layout={'width': '100px'},
                                continuous_update=False)
    s1_2.observe(update_figure,names = 'value')
    
    s1_3 = widgets.FloatSlider(min=0, max=0.705, value=0.20, step=0.01, 
                                description = 's1 at 1 Sep: ',
                                orientation='vertical',
                                layout={'width': '100px'},
                                continuous_update=False)
    s1_3.observe(update_figure,names = 'value')
    
    
    # Initial simulation applying the default slider values of the parameters 
    # Points defining the curves
    s2_inc = 0.3    

    Qreg = {'releases' : {'type'  : 'variable operating policy',
                          'input' : policy_rel_var,
                          'index' : policy_rel_var_idx},
            'inflows' : [],
            'rel_inf' : []}
    
    env, spill, Qreg_rel, Qreg_inf, s, E = res_sys_sim(I, e, 
                                               s_ini, s_min, s_max, 
                                               Qreg_rel_min, d, 
                                               Qreg)
    
    ### Figures ###
    # Fig 1a: Rule curve
    
    x_sc_1a = LinearScale(); y_sc_1a = LinearScale(min=0,max=1)
    x_ax_1a = Axis(label='day of the year', scale=x_sc_1a, grid_lines = 'none')
    y_ax_1a = Axis(label='storage fraction', scale=y_sc_1a, orientation='vertical', grid_lines = 'none')
    
    curve_a_plot = Lines(x = np.arange(1,367), y = curve_a,
                         colors=['blue'], stroke = 'lightgray',
                         scales={'x': x_sc_1a, 'y': y_sc_1a},
                         fill   = 'top',fill_opacities = [1],fill_colors = ['blue'])
    curve_b_plot = Lines(x = np.arange(1,367), y = curve_b,
                         colors=['blue'], stroke = 'lightgray',
                         scales={'x': x_sc_1a, 'y': y_sc_1a},
                         fill   = 'top',fill_opacities = [1],fill_colors = ['lightblue'])
    
    fig_1a             = plt.Figure(marks = [curve_a_plot,curve_b_plot],
                                   title = 'Rule curve',
                                   axes=[x_ax_1a, y_ax_1a],
                                   layout={'width': '500px', 'height': '250px'},
                                   background_style = {'fill': 'darkblue'},
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1a, 'y': y_sc_1a})
    
    curve_a_plot.observe(update_figure, ['x', 'y'])
    curve_b_plot.observe(update_figure, ['x', 'y'])
    
    # Fig 1b: Releases vs Demand
    x_sc_1b = DateScale();         y_sc_1b = LinearScale(min=0,max=Qreg_rel_max);
    x_ax_1b = Axis(scale=x_sc_1b); y_ax_1b = Axis(label='ML/week', scale=y_sc_1b, orientation='vertical')
    
    demand             = Bars(x      = date,
                              y      = d[:,0],
                              colors = ['gray'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b})
    
    releases           = Bars(x      = date,
                              y      = Qreg_rel[:,0],
                              colors = ['green'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b})
    
    TSD = (np.sum((np.maximum(d-Qreg_rel,np.zeros((N,1))))**2)).astype('int')
    
    fig_1b             = plt.Figure(marks = [demand, releases],
                                   title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2',
                                   axes=[x_ax_1b, y_ax_1b],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1b, 'y': y_sc_1b})
    
    releases.observe(update_figure, ['x', 'y'])
    
    # Fig 1c: Storage
    x_sc_1c = DateScale(min=date[0]); y_sc_1c = LinearScale(min=0,max=200);
    x_ax_1c = Axis(scale=x_sc_1c); y_ax_1c = Axis(label='ML', scale=y_sc_1c, orientation='vertical')
    
    storage           = Lines(x      = date,
                              y      = s[:,0] ,
                              colors = ['blue'],
                              scales = {'x': x_sc_1c, 'y': y_sc_1c},
                              fill   = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    
    max_storage       = plt.plot(x=date,
                                 y=[s_max]*(N+1),
                                 colors=['red'],
                                 scales={'x': x_sc_1c, 'y': y_sc_1c})
    
#    max_storage_label = plt.label(text = ['max storage'], 
#                                  x=['2015-01-01T00:00:00.000000000'],
#                                  y=[0],
#                                  colors=['red'])
    
    cri_storage = plt.plot(date,cs,
                             scales={'x': x_sc_1c, 'y': y_sc_1c},
                             colors=['red'],opacities = [1],
                             line_style = 'dashed',
                             fill = 'bottom',fill_opacities = [0.4],fill_colors = ['red'], stroke_width = 1)
#    cri_storage_label = plt.label(text = ['critical storage'], 
#                                    x=[0], # don't know what is the right format
#                                    y=[cs[0]-10],
#                                    colors=['red'])
    
    CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
    
    fig_1c             = plt.Figure(marks = [storage,max_storage,#max_storage_label,
                                            cri_storage],#,cri_storage_label],
                                   title = 'Reservoir storage volume - CSV = '+str(CSV)+' ML',
                                   axes=[x_ax_1c, y_ax_1c],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1c, 'y': y_sc_1c})
    
    storage.observe(update_figure, ['x', 'y'])
    
    ### Fig 2: Policy functions
    # Fig 2a: Policy function 1 Apr (year day = 91)
    x0 = [s_min/s_max,       Qreg_rel_min]
    x1 = [s1_1.value,        Qreg_rel_mean]
    x2 = [s1_1.value+s2_inc, Qreg_rel_mean]
    x3 = [s_max/s_max,       Qreg_rel_max]
    param_1 = x0, x1, x2, x3
    policy_rel_1 = policy_function(param_1)

    s_step = 0.01
    s_frac = np.arange(0,1+s_step,s_step)
    x_sc_2 = LinearScale(min=0,max=1); y_sc_2 = LinearScale(min=0,max=Qreg_rel_max);
    x_ax_2 = Axis(label='Storage fraction', scale=x_sc_2); 
    y_ax_2 = Axis(label='Release (ML/week)', scale=y_sc_2, orientation='vertical')
    
    pol_func_1          = Lines(x      = s_frac,
                                y      = policy_rel_1,
                                colors = ['blue'],
                                scales = {'x': x_sc_2, 'y': y_sc_2})
    
    fig_2a             = plt.Figure(marks = [pol_func_1],
                                   title = 'Policy function 1 Jan',
                                   axes = [x_ax_2, y_ax_2],
                                   layout = {'width': '300px', 'height': '200px'}, 
                                   animation_duration = 1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales = {'x': x_sc_2, 'y': y_sc_2})
    
    pol_func_1.observe(update_figure, ['x', 'y'])

    # Fig 2b: Policy function 1 Aug (year day = 213)
    x0 = [s_min/s_max,       Qreg_rel_min]
    x1 = [s1_2.value,        Qreg_rel_mean]
    x2 = [s1_2.value+s2_inc, Qreg_rel_mean]
    x3 = [s_max/s_max,       Qreg_rel_max]
    param_2 = x0, x1, x2, x3
    policy_rel_2 = policy_function(param_2)
    
    pol_func_2          = Lines(x      = s_frac,
                                y      = policy_rel_2,
                                colors = ['blue'],
                                scales = {'x': x_sc_2, 'y': y_sc_2})
    
    fig_2b             = plt.Figure(marks = [pol_func_2],
                                   title = 'Policy function 1 May',
                                   axes = [x_ax_2, y_ax_2],
                                   layout = {'width': '300px', 'height': '200px'}, 
                                   animation_duration = 1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales = {'x': x_sc_2, 'y': y_sc_2})
    
    pol_func_2.observe(update_figure, ['x', 'y'])

    # Fig 2c: Policy function 1 Dec (year day = 335)
    x0 = [s_min/s_max,       Qreg_rel_min]
    x1 = [s1_3.value,        Qreg_rel_mean]
    x2 = [s1_3.value+s2_inc, Qreg_rel_mean]
    x3 = [s_max/s_max,       Qreg_rel_max]
    param_3 = x0, x1, x2, x3
    policy_rel_2 = policy_function(param_3)
    
    pol_func_3          = Lines(x      = s_frac,
                                y      = policy_rel_2,
                                colors = ['blue'],
                                scales = {'x': x_sc_2, 'y': y_sc_2})
    
    fig_2c             = plt.Figure(marks = [pol_func_3],
                                   title = 'Policy function 1 Dec',
                                   axes = [x_ax_2, y_ax_2],
                                   layout = {'width': '300px', 'height': '200px'}, 
                                   animation_duration = 1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales = {'x': x_sc_2, 'y': y_sc_2})
    
    pol_func_3.observe(update_figure, ['x', 'y'])
    
    return fig_1a,fig_1b,fig_1c,fig_2a,fig_2b,fig_2c,s1_1,s1_2,s1_3
