# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 18:26:41 2019

@author: ap18525
"""
import ipywidgets as widgets
import numpy as np
from bqplot import pyplot as plt
from bqplot import *
from bqplot.traits import *
#import sys

def Interactive_piecewiselin_manual(Res_sys_sim, policy_function,
                              date, 
                              I,     e, 
                              s_ini, s_min, s_max,
                              u_ini, u_min, u_max,
                              cs, d):
    N = date.shape[0]
    u0, u1, u2, u3 = u_ini
    #Function to update the release policy when changing the parameters with the sliders
    def update_operating_policy(s_ref_1,s_ref_2,u_ref):
        if s_ref_1 > s_ref_2:
            s_ref_1 = s_ref_2   
        x0 = [0,       u0]
        x1 = [s_ref_1, u_ref]
        x2 = [s_ref_2, u_ref]
        x3 = [1,       u3]
        param = x0, x1, x2, x3
        u = policy_function(param)
        
        Qreg = {'releases' : {'type' : 'operating policy',
                             'input' : policy_function,
                             'param' : param},
                'inflows' : [],
                'rel_inf' : []}
        
        Qenv, Qspill, Qreg_rel, I_reg, s, E = Res_sys_sim(date, I, e, s_ini, s_min, s_max, u_min, d, Qreg)
        
        TSD = (np.sum((np.maximum(d-Qreg_rel,np.zeros((N,1))))**2)).astype('int')
        fig_1b.title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2'
        
        CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
        fig_1c.title = 'Reservoir storage volume - CSV = '+str(CSV)+' ML'
    
        return u, Qenv, Qspill, Qreg_rel, I_reg, s
    
    # Function to update the figures when changing the parameters with the sliders
    def update_figure(change):
        pol_func.y = update_operating_policy(s_ref_1.value,s_ref_2.value,u_ref.value)[0]
        releases.y = update_operating_policy(s_ref_1.value,s_ref_2.value,u_ref.value)[3][:,0]
        storage.y = update_operating_policy(s_ref_1.value,s_ref_2.value,u_ref.value)[5][:,0]
    
    # Definition of the sliders    
    u_ref = widgets.FloatSlider(min=0.5, max=u3, value=u1, step=0.05,
                                description = 'u_ref: ',
                                orientation='vertical',
                                continuous_update = False)
    u_ref.observe(update_figure,names = 'value')
    
    s_ref_1 = widgets.FloatSlider(min=0, max=1, value=0.25, step=0.05, 
                                  description = 's_ref_1: ',
                                  continuous_update=False)
    s_ref_1.observe(update_figure,names = 'value')
    
    s_ref_2 = widgets.FloatSlider(min=0, max=1, value=0.75, step=0.05,
                                  description = 's_ref_2: ',
                                  continuous_update=False)
    s_ref_2.observe(update_figure,names = 'value')
    
    # Initial simulation applying the default slider values of the parameters 
    x0 = [0,       u0]
    x1 = [s_ref_1.value, u_ref.value]
    x2 = [s_ref_2.value, u_ref.value]
    x3 = [1,       u3]
    param = x0, x1, x2, x3
    u = policy_function(param)

    Qreg = {'releases' : {'type' : 'operating policy',
                         'input' : policy_function,
                         'param' : param},
            'inflows' : [],
            'rel_inf' : []}
    
    Qenv, Qspill, Qreg_rel, I_reg, s, E = Res_sys_sim(date, I, e, s_ini, s_min, s_max, u_min, d, Qreg)
    
    ### Figures ###
    s_step = 0.01
    s_frac = np.arange(0,1+s_step,s_step)
    # Fig 1a: Policy function
    x_sc_1a = LinearScale(min=0,max=1); y_sc_1a = LinearScale(min=0,max=u3);
    x_ax_1a = Axis(label='Storage fraction', scale=x_sc_1a); 
    y_ax_1a = Axis(label='Release (ML/week)', scale=y_sc_1a, orientation='vertical')
    
    pol_func          = Lines(x      = s_frac,
                              y      = u,
                              colors = ['blue'],
                              scales = {'x': x_sc_1a, 'y': y_sc_1a})
    
    fig_1a             = plt.Figure(marks = [pol_func],
                                   title = 'Policy function',
                                   axes=[x_ax_1a, y_ax_1a],
                                   layout={'width': '400px', 'height': '350px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1a, 'y': y_sc_1a})
    
    pol_func.observe(update_figure, ['x', 'y'])
    
    # Fig 1b: Releases vs Demand
    x_sc_1b = DateScale();                       y_sc_1b = LinearScale(min=0,max=25);
    x_ax_1b = Axis(scale=x_sc_1b); y_ax_1b = Axis(label='ML/week', scale=y_sc_1b, orientation='vertical')
    
    demand             = plt.Bars(x  = date,
                              y      = d[:,0],
                              colors = ['gray'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b},
                              labels = ['demand'], display_legend = True)
    
    releases           = plt.Bars(x  = date,
                              y      = Qreg_rel[:,0],
                              colors = ['green'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b},
                              labels = ['releases'], display_legend = True)
    
    TSD = (np.sum((np.maximum(d-Qreg_rel,np.zeros((N,1))))**2)).astype('int')
    
    fig_1b             = plt.Figure(marks = [demand, releases],
                                   title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2',
                                   axes=[x_ax_1b, y_ax_1b],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1b, 'y': y_sc_1b},
                                   legend_style = {'fill': 'white', 'opacity': 0})
    
    releases.observe(update_figure, ['x', 'y'])
    
    # Fig 1c: Storage
    x_sc_1c = DateScale(min=date[0]);            y_sc_1c = LinearScale(min=0,max=200);
    x_ax_1c = Axis(scale=x_sc_1c); y_ax_1c = Axis(label='ML', scale=y_sc_1c, orientation='vertical')
    
    storage           = Lines(x      = date,
                              y      = s[:,0],
                              colors = ['blue'],
                              scales = {'x': x_sc_1c, 'y': y_sc_1c},
                              fill   = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    
    max_storage       = plt.plot(x=date,
                                 y=[s_max]*(N+1),
                                 colors=['red'],
                                 scales={'x': x_sc_1c, 'y': y_sc_1c})
    
    # max_storage_label = plt.label(text = ['Max storage'], 
    #                               x=[0],
    #                               y=[s_max+15],
    #                               colors=['red'])
    
    cri_storage = plt.plot(date,cs,
                             scales={'x': x_sc_1c, 'y': y_sc_1c},
                             colors=['red'],opacities = [1],
                             line_style = 'dashed',
                             fill = 'bottom',fill_opacities = [0.4],fill_colors = ['red'], stroke_width = 1)

    # cri_storage_label = plt.label(text = ['Critical storage'], 
    #                                 x=[0],
    #                                 y=[s_cri[0]-10],
    #                                 colors=['red'])
    
    CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
    
    fig_1c             = plt.Figure(marks = [storage,max_storage,cri_storage],
                                   title = 'Reservoir storage volume - CSV = '+str(CSV)+' ML',
                                   axes=[x_ax_1c, y_ax_1c],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1c, 'y': y_sc_1c})
    
    storage.observe(update_figure, ['x', 'y'])
    
    return fig_1a,fig_1b,fig_1c, u_ref,s_ref_1,s_ref_2

def Interactive_piecewiselin_auto(Res_sys_sim, policy_function,
                            date, 
                            I,     e, 
                            s_ini, s_min, s_max, 
                            u_ini, u_min, u_max,
                            cs, d, 
                            results1_optim,results2_optim,sol_optim):
    
    N = np.shape(date)[0]
    u0, u1, u2, u3 = u_ini
    # Function to update the release policy when clicking on the points of the Pareto front
    def update_operating_policy(i):
        
        u_ref,s_ref_1,s_ref_2 = sol_optim[i]
        x0 = [0,       u0]
        x1 = [s_ref_1, u_ref]
        x2 = [s_ref_2, u_ref]
        x3 = [1,       u3]
        param = x0, x1, x2, x3
        u = policy_function(param)
        
        Qreg = {'releases' : {'type' : 'operating policy',
                             'input' : policy_function,
                             'param' : param},
                'inflows' : [],
                'rel_inf' : []}
        
        Qenv, Qspill, Qreg_rel, I_reg, s, E = Res_sys_sim(date, I, e, s_ini, s_min, s_max, u_min, d, Qreg)
        
        CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
        fig_2c.title = 'Reservoir storage volume - CSV = '+str(CSV)+' ML'
        
        TSD = (np.sum((np.maximum(d-Qreg_rel,np.zeros((N,1))))**2)).astype('int')
        fig_2b.title = 'Supply vs Demand - Total squared deficit = '+str(TSD)+' ML^2'
        
        return u, Qenv, Qspill, Qreg_rel, I_reg, s
    
    # Function to update the figures when clicking on the points of the Pareto front
    def update_figure(change):
        if pareto_front.selected == None:
            pareto_front.selected = [0]        
        pol_func.y = update_operating_policy(pareto_front.selected[0])[0]
        releases.y = update_operating_policy(pareto_front.selected[0])[3][:,0]
        storage.y = update_operating_policy(pareto_front.selected[0])[5][:,0]
    
    # Fig_pf: Pareto front  
    x_sc_pf = LinearScale();y_sc_pf = LinearScale()
    x_ax_pf = Axis(label='Total squared deficit [ML^2]', scale=x_sc_pf)
    y_ax_pf = Axis(label='Critical storage violation [ML]', scale=y_sc_pf, orientation='vertical')
    
    pareto_front = plt.scatter(results1_optim[:],results2_optim[:],
                               scales={'x': x_sc_pf, 'y': y_sc_pf},
                               colors=['deepskyblue'], 
                               interactions={'hover':'tooltip','click': 'select'})
    
    pareto_front.unselected_style={'opacity': 0.4}
    pareto_front.selected_style={'fill': 'red', 'stroke': 'yellow', 'width': '1125px', 'height': '125px'}
    def_tt = Tooltip(fields=['index','x', 'y'],
                     labels=['index','Water deficit', 'Critical storage'], 
                     formats=['.d','.1f', '.1f'])
    pareto_front.tooltip=def_tt
    
    fig_pf = plt.Figure(marks = [pareto_front],title = 'Interactive Pareto front', 
                        axes=[x_ax_pf, y_ax_pf],
                        layout={'width': '400px', 'height': '350px'},
                        animation_duration=1000,
                        fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0})
    
    if pareto_front.selected == []:
        pareto_front.selected = [0]
    
    pareto_front.observe(update_figure,'selected')
    
    # Initial simulation applting the point of the Pareto Fron selected by default 
    u_ref,s_ref_1,s_ref_2 = sol_optim[pareto_front.selected[0]]
    x0 = [0,       u0]
    x1 = [s_ref_1, u_ref]
    x2 = [s_ref_2, u_ref]
    x3 = [1,       u3]
    param = x0, x1, x2, x3
    u = policy_function(param)
    
    Qreg = {'releases' : {'type' : 'operating policy',
                         'input' : policy_function,
                         'param' : param},
            'inflows' : [],
            'rel_inf' : []}
    
    Qenv, Qspill, Qreg_rel, I_reg, s, E = Res_sys_sim(date, I, e, s_ini, s_min, s_max, u_min, d, Qreg)
    
    # Fig 2a: Policy function
    s_step = 0.01
    s_frac = np.arange(0,1+s_step,s_step)
    
    x_sc_2a = LinearScale(min=0,max=1); y_sc_2a = LinearScale(min=0,max=u3);
    x_ax_2a = Axis(label='Storage fraction', scale=x_sc_2a); 
    y_ax_2a = Axis(label='Release (ML/week)', scale=y_sc_2a, orientation='vertical')
    
    pol_func           = Lines(x      = s_frac,
                                      y      = u ,
                                      colors = ['blue'],
                                      scales = {'x': x_sc_2a, 'y': y_sc_2a})
    
    fig_2a             = plt.Figure(marks = [pol_func],
                                   title = 'Policy function',
                                   axes=[x_ax_2a, y_ax_2a],
                                   layout={'width': '400px', 'height': '350px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_2a, 'y': y_sc_2a})
    
    pol_func.observe(update_figure, ['x', 'y'])
    
    # Fig 2b: Releases vs Demand
    x_sc_2b = DateScale();                       y_sc_2b = LinearScale(min=0,max=25);
    x_ax_2b = Axis(scale=x_sc_2b); y_ax_2b = Axis(label='ML/week', scale=y_sc_2b, orientation='vertical')
    
    demand             = Bars(x      = date,
                              y      = d[:,0],
                              colors = ['gray'],
                              scales = {'x': x_sc_2b, 'y': y_sc_2b},
                              labels = ['demand'], display_legend = True)
    
    releases           = Bars(x      = date,
                              y      = Qreg_rel[:,0],
                              colors = ['green'],
                              scales = {'x': x_sc_2b, 'y': y_sc_2b},
                              labels = ['releases'], display_legend = True)
    
    TSD = (np.sum((np.maximum(d-Qreg_rel,np.zeros((N,1))))**2)).astype('int')
    
    fig_2b             = plt.Figure(marks = [demand, releases],
                                   title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2',
                                   axes=[x_ax_2b, y_ax_2b],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   scales={'x': x_sc_2b, 'y': y_sc_2b},
                                   fig_margin = {'top':0, 'bottom':40, 'left':60, 'right':0},
                                   legend_style = {'fill': 'white', 'opacity': 0})
    
    releases.observe(update_figure, ['x', 'y'])
    
    # Fig 2c: Storage
    x_sc_2c = DateScale();                       y_sc_2c = LinearScale(min=0,max=200);
    x_ax_2c = Axis(scale=x_sc_2c); y_ax_2c = Axis(label='ML', scale=y_sc_2c, orientation='vertical')
    
    storage           = Lines(x      = date,
                              y      = s[:,0],
                              colors = ['blue'],
                              scales = {'x': x_sc_2c, 'y': y_sc_2c},
                              fill   = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    
    max_storage       = plt.plot(x=date,
                                 y=[s_max]*(N+1),
                                 colors=['red'],
                                 scales={'x': x_sc_2c, 'y': y_sc_2c})
    
    # max_storage_label = plt.label(text = ['Max storage'], 
    #                               x=[0],
    #                               y=[s_max+15],
    #                               colors=['red'])
    
    cri_storage = plt.plot(date,cs,
                             scales={'x': x_sc_2c, 'y': y_sc_2c},
                             colors=['red'],opacities = [1],
                             line_style = 'dashed',
                             fill = 'bottom',fill_opacities = [0.4],fill_colors = ['red'], stroke_width = 1)
    
    # cri_storage_label = plt.label(text = ['Critical storage'], 
    #                                 x=[0],
    #                                 y=[s_cri[0]-10],
    #                                 colors=['red'])
    
    CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
    
    fig_2c             = plt.Figure(marks = [storage,max_storage,cri_storage],
                                   title = 'Reservoir storage volume - CSV = '+str(CSV)+' ML',
                                   axes=[x_ax_2c, y_ax_2c],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   fig_margin = {'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_2c, 'y': y_sc_2c})
    
    storage.observe(update_figure, ['x', 'y'])
    
    return fig_pf, fig_2a,fig_2b,fig_2c

def Interactive_logexp_manual_v1(Res_sys_sim, policy_function,
                              date, 
                              I,     e, 
                              s_ini, s_min, s_max,
                              param, u_min, u_max,
                              cs, d):
    N = date.shape[0]
    u_ref = param[4]
    #Function to update the release policy when changing the parameters with the sliders
    def update_operating_policy(u_frac_min, s_frac_ref, α, b):
        param = [u_frac_min, s_frac_ref, α, b, u_ref]
        u = policy_function(param)
        
        Qreg = {'releases' : {'type' : 'operating policy',
                             'input' : policy_function,
                             'param' : param},
                'inflows' : [],
                'rel_inf' : []}
        
        Qenv, Qspill, Qreg_rel, I_reg, s, E = Res_sys_sim(date, I, e, s_ini, s_min, s_max, u_min, d, Qreg)
        
        TSD = (np.sum((np.maximum(d-Qreg_rel,np.zeros((N,1))))**2)).astype('int')
        fig_1b.title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2'
        
        CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
        fig_1c.title = 'Reservoir storage volume - CSV = '+str(CSV)+' ML'
    
        return u, Qenv, Qspill, Qreg_rel, I_reg, s
    
    # Function to update the figures when changing the parameters with the sliders
    def update_figure(change):
        pol_func.y = update_operating_policy(u_frac_min.value, s_frac_ref.value, 
                                            α.value, b.value)[0]
        releases.y = update_operating_policy(u_frac_min.value, s_frac_ref.value, 
                                            α.value, b.value)[3][:,0]
        storage.y = update_operating_policy(u_frac_min.value, s_frac_ref.value, 
                                            α.value, b.value)[5][:,0]

    # Definition of the sliders    
    u_frac_min = widgets.FloatSlider(min=0.0, max=1.0, value=param[0], step=0.01,
                                description = 'u_frac_min: ',
                                orientation='vertical',
                                continuous_update = False)
    u_frac_min.observe(update_figure,names = 'value')

    s_frac_ref = widgets.FloatSlider(min=0, max=0.99, value=param[1], step=0.01, 
                                  description = 's_frac_ref: ',
                                  continuous_update=False)
    s_frac_ref.observe(update_figure,names = 'value')
    
    α = widgets.FloatSlider(min=0, max=1, value=param[2], step=0.01, 
                                  description = 'α: ',
                                  continuous_update=False)
    α.observe(update_figure,names = 'value')
    
    b = widgets.FloatSlider(min=1, max=200, value=param[3], step=1, 
                                  description = 'b: ',
                                  continuous_update=False)
    b.observe(update_figure,names = 'value')
    
    # Initial simulation applying the default slider values of the parameters 

    u = policy_function(param)

    Qreg = {'releases' : {'type' : 'operating policy',
                         'input' : policy_function,
                         'param' : param},
            'inflows' : [],
            'rel_inf' : []}
    
    Qenv, Qspill, Qreg_rel, I_reg, s, E = Res_sys_sim(date, I, e, s_ini, s_min, s_max, u_min, d, Qreg)
    
    ### Figures ###
    s_step = 0.01
    s_frac = np.arange(0,1+s_step,s_step)
    # Fig 1a: Policy function
    x_sc_1a = LinearScale(min=0,max=1); y_sc_1a = LinearScale(min=0);
    x_ax_1a = Axis(label='Storage fraction', scale=x_sc_1a); 
    y_ax_1a = Axis(label='Release (ML/week)', scale=y_sc_1a, orientation='vertical')
    
    pol_func          = Lines(x      = s_frac,
                              y      = u,
                              colors = ['blue'],
                              scales = {'x': x_sc_1a, 'y': y_sc_1a})
    
    ref_rel           = Lines(x      = s_frac,
                              y      = [u_ref]*(N),
                              colors = ['gray'],
                              line_style = 'dashed',
                              scales = {'x': x_sc_1a, 'y': y_sc_1a})   
    
    fig_1a             = plt.Figure(marks = [ref_rel,pol_func],
                                   title = 'Policy function',
                                   axes=[x_ax_1a, y_ax_1a],
                                   layout={'width': '400px', 'height': '350px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1a, 'y': y_sc_1a})
    
    pol_func.observe(update_figure, ['x', 'y'])
    
    # Fig 1b: Releases vs Demand
    x_sc_1b = DateScale();                       y_sc_1b = LinearScale(min=0,max=25);
    x_ax_1b = Axis(scale=x_sc_1b); y_ax_1b = Axis(label='ML/week', scale=y_sc_1b, orientation='vertical')
    
    demand             = plt.Bars(x  = date,
                              y      = d[:,0],
                              colors = ['gray'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b},
                              labels = ['demand'], display_legend = True)
    
    releases           = plt.Bars(x  = date,
                              y      = Qreg_rel[:,0],
                              colors = ['green'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b},
                              labels = ['releases'], display_legend = True)
    
    TSD = (np.sum((np.maximum(d-Qreg_rel,np.zeros((N,1))))**2)).astype('int')
    
    fig_1b             = plt.Figure(marks = [demand, releases],
                                   title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2',
                                   axes=[x_ax_1b, y_ax_1b],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1b, 'y': y_sc_1b},
                                   legend_style = {'fill': 'white', 'opacity': 0})
    
    releases.observe(update_figure, ['x', 'y'])
    
    # Fig 1c: Storage
    x_sc_1c = DateScale(min=date[0]);            y_sc_1c = LinearScale(min=0,max=200);
    x_ax_1c = Axis(scale=x_sc_1c); y_ax_1c = Axis(label='ML', scale=y_sc_1c, orientation='vertical')
    
    storage           = Lines(x      = date,
                              y      = s[:,0],
                              colors = ['blue'],
                              scales = {'x': x_sc_1c, 'y': y_sc_1c},
                              fill   = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    
    max_storage       = plt.plot(x=date,
                                 y=[s_max]*(N+1),
                                 colors=['red'],
                                 scales={'x': x_sc_1c, 'y': y_sc_1c})
    
    # max_storage_label = plt.label(text = ['Max storage'], 
    #                               x=[0],
    #                               y=[s_max+15],
    #                               colors=['red'])
    
    cri_storage = plt.plot(date,cs,
                             scales={'x': x_sc_1c, 'y': y_sc_1c},
                             colors=['red'],opacities = [1],
                             line_style = 'dashed',
                             fill = 'bottom',fill_opacities = [0.4],fill_colors = ['red'], stroke_width = 1)

    # cri_storage_label = plt.label(text = ['Critical storage'], 
    #                                 x=[0],
    #                                 y=[s_cri[0]-10],
    #                                 colors=['red'])
    
    CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
    
    fig_1c             = plt.Figure(marks = [storage,max_storage,cri_storage],
                                   title = 'Reservoir storage volume - CSV = '+str(CSV)+' ML',
                                   axes=[x_ax_1c, y_ax_1c],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1c, 'y': y_sc_1c})
    
    storage.observe(update_figure, ['x', 'y'])
    
    return fig_1a,fig_1b,fig_1c, u_frac_min, s_frac_ref, α, b

def Interactive_logexp_manual_v2(Res_sys_sim, policy_function,
                              date, 
                              I,     e, 
                              s_ini, s_min, s_max,
                              param, u_min, u_max,
                              cs, d):
    N = date.shape[0]
    u_ref = param[6]
    #Function to update the release policy when changing the parameters with the sliders
    def update_operating_policy(u_frac_min, u_frac_max, s_frac_ref, u_frac_ref, p_rel, p_sto):
        param = [u_frac_min, u_frac_max, s_frac_ref, u_frac_ref, p_rel, p_sto, u_ref, 0]
        u = policy_function(param)
        
        Qreg = {'releases' : {'type' : 'operating policy',
                             'input' : policy_function,
                             'param' : param},
                'inflows' : [],
                'rel_inf' : []}
        
        Qenv, Qspill, Qreg_rel, I_reg, s, E = Res_sys_sim(date, I, e, s_ini, s_min, s_max, u_min, d, Qreg)
        
        TSD = (np.sum((np.maximum(d-Qreg_rel,np.zeros((N,1))))**2)).astype('int')
        fig_1b.title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2'
        
        CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
        fig_1c.title = 'Reservoir storage volume - CSV = '+str(CSV)+' ML'
    
        return u, Qenv, Qspill, Qreg_rel, I_reg, s
    
    # Function to update the figures when changing the parameters with the sliders
    def update_figure(change):
        pol_func.y = update_operating_policy(u_frac_min.value, u_frac_max.value, 
                                            s_frac_ref.value, u_frac_ref.value, 
                                            p_rel.value, p_sto.value)[0]
        releases.y = update_operating_policy(u_frac_min.value, u_frac_max.value, 
                                            s_frac_ref.value, u_frac_ref.value, 
                                            p_rel.value, p_sto.value)[3][:,0]
        storage.y = update_operating_policy(u_frac_min.value, u_frac_max.value, 
                                            s_frac_ref.value, u_frac_ref.value, 
                                            p_rel.value, p_sto.value)[5][:,0]

    # Definition of the sliders    
    u_frac_min = widgets.FloatSlider(min=0.0, max=1.0, value=param[0], step=0.01,
                                description = 'u_frac_min: ',
                                orientation='vertical',
                                continuous_update = False)
    u_frac_min.observe(update_figure,names = 'value')

    u_frac_max = widgets.FloatSlider(min=0.0, max=5, value=param[1], step=0.01,
                                description = 'u_frac_max: ',
                                orientation='vertical',
                                continuous_update = False)
    u_frac_max.observe(update_figure,names = 'value')
    
    s_frac_ref = widgets.FloatSlider(min=0, max=0.99, value=param[2], step=0.01, 
                                  description = 's_frac_ref: ',
                                  continuous_update=False)
    s_frac_ref.observe(update_figure,names = 'value')
    
    u_frac_ref = widgets.FloatSlider(min=0, max=5, value=param[3], step=0.01, 
                                  description = 'u_frac_ref: ',
                                  orientation='vertical',
                                  continuous_update=False)
    u_frac_ref.observe(update_figure,names = 'value')
    
    p_rel = widgets.FloatSlider(min=1, max=300, value=param[4], step=1, 
                                  description = 'p_rel: ',
                                  continuous_update=False)
    p_rel.observe(update_figure,names = 'value')
    
    p_sto = widgets.FloatSlider(min=1, max=10, value=param[5], step=1, 
                                  description = 'p_sto: ',
                                  continuous_update=False)
    p_sto.observe(update_figure,names = 'value')
    
    # Initial simulation applying the default slider values of the parameters 

    u = policy_function(param)

    Qreg = {'releases' : {'type' : 'operating policy',
                         'input' : policy_function,
                         'param' : param},
            'inflows' : [],
            'rel_inf' : []}
    
    Qenv, Qspill, Qreg_rel, I_reg, s, E = Res_sys_sim(date, I, e, s_ini, s_min, s_max, u_min, d, Qreg)
    
    ### Figures ###
    s_step = 0.01
    s_frac = np.arange(0,1+s_step,s_step)
    # Fig 1a: Policy function
    x_sc_1a = LinearScale(min=0,max=1); y_sc_1a = LinearScale(min=0);
    x_ax_1a = Axis(label='Storage fraction', scale=x_sc_1a); 
    y_ax_1a = Axis(label='Release (ML/week)', scale=y_sc_1a, orientation='vertical')
    
    pol_func          = Lines(x      = s_frac,
                              y      = u,
                              colors = ['blue'],
                              scales = {'x': x_sc_1a, 'y': y_sc_1a})
    
    ref_rel           = Lines(x      = s_frac,
                              y      = [u_ref]*(N),
                              colors = ['gray'],
                              line_style = 'dashed',
                              scales = {'x': x_sc_1a, 'y': y_sc_1a})   
    
    fig_1a             = plt.Figure(marks = [ref_rel,pol_func],
                                   title = 'Policy function',
                                   axes=[x_ax_1a, y_ax_1a],
                                   layout={'width': '400px', 'height': '350px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1a, 'y': y_sc_1a})
    
    pol_func.observe(update_figure, ['x', 'y'])
    
    # Fig 1b: Releases vs Demand
    x_sc_1b = DateScale();                       y_sc_1b = LinearScale(min=0,max=25);
    x_ax_1b = Axis(scale=x_sc_1b); y_ax_1b = Axis(label='ML/week', scale=y_sc_1b, orientation='vertical')
    
    demand             = plt.Bars(x  = date,
                              y      = d[:,0],
                              colors = ['gray'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b},
                              labels = ['demand'], display_legend = True)
    
    releases           = plt.Bars(x  = date,
                              y      = Qreg_rel[:,0],
                              colors = ['green'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b},
                              labels = ['releases'], display_legend = True)
    
    TSD = (np.sum((np.maximum(d-Qreg_rel,np.zeros((N,1))))**2)).astype('int')
    
    fig_1b             = plt.Figure(marks = [demand, releases],
                                   title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2',
                                   axes=[x_ax_1b, y_ax_1b],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1b, 'y': y_sc_1b},
                                   legend_style = {'fill': 'white', 'opacity': 0})
    
    releases.observe(update_figure, ['x', 'y'])
    
    # Fig 1c: Storage
    x_sc_1c = DateScale(min=date[0]);            y_sc_1c = LinearScale(min=0,max=200);
    x_ax_1c = Axis(scale=x_sc_1c); y_ax_1c = Axis(label='ML', scale=y_sc_1c, orientation='vertical')
    
    storage           = Lines(x      = date,
                              y      = s[:,0],
                              colors = ['blue'],
                              scales = {'x': x_sc_1c, 'y': y_sc_1c},
                              fill   = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    
    max_storage       = plt.plot(x=date,
                                 y=[s_max]*(N+1),
                                 colors=['red'],
                                 scales={'x': x_sc_1c, 'y': y_sc_1c})
    
    # max_storage_label = plt.label(text = ['Max storage'], 
    #                               x=[0],
    #                               y=[s_max+15],
    #                               colors=['red'])
    
    cri_storage = plt.plot(date,cs,
                             scales={'x': x_sc_1c, 'y': y_sc_1c},
                             colors=['red'],opacities = [1],
                             line_style = 'dashed',
                             fill = 'bottom',fill_opacities = [0.4],fill_colors = ['red'], stroke_width = 1)

    # cri_storage_label = plt.label(text = ['Critical storage'], 
    #                                 x=[0],
    #                                 y=[s_cri[0]-10],
    #                                 colors=['red'])
    
    CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
    
    fig_1c             = plt.Figure(marks = [storage,max_storage,cri_storage],
                                   title = 'Reservoir storage volume - CSV = '+str(CSV)+' ML',
                                   axes=[x_ax_1c, y_ax_1c],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1c, 'y': y_sc_1c})
    
    storage.observe(update_figure, ['x', 'y'])
    
    return fig_1a,fig_1b,fig_1c, u_frac_min, u_frac_max, s_frac_ref, u_frac_ref, p_rel, p_sto