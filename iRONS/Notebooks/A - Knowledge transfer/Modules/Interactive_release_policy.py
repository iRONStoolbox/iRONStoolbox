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
import sys

# Submodules
sys.path.append('../../Toolbox')
from Reservoir_operating_policy.Operating_policy_functions import four_points_policy
from Reservoir_system_simulation.Res_sys_sim import Res_sys_sim

def Interactive_policy_manual(N, 
                              I_hist, e_hist, 
                              s_0, s_min, s_max, 
                              u_0, u_1, u_mean, u_max,
                              env_min, d_hist, 
                              rc):
    
    #Function to update the release policy when changing the parameters with the sliders
    def update_operating_policy_1(s_ref_1,s_ref_2,u_ref):
        if s_ref_1 > s_ref_2:
            s_ref_1 = s_ref_2   
        x0 = [0,       u_0]
        x1 = [s_ref_1, u_ref]
        x2 = [s_ref_2, u_ref]
        x3 = [1,       u_1]
        param = [x0, x1, x2, x3, u_mean]
        u_frac = four_points_policy(param)/u_mean
        
        Qreg = {'releases' : {'file_name' : 'Reservoir_operating_policy.Operating_policy_functions',
                             'function' : 'four_points_policy',
                             'param': param},
                'inflows' : [],
                'rel_inf' : []}
        
        Qenv, Qspill, u, I_reg, s, E = Res_sys_sim(I_hist, e_hist, s_0, s_min, s_max, env_min, d_hist, Qreg)
        
        TSD = (np.sum((np.maximum(d_hist-u,[0]*N))**2)).astype('int')
        fig_1b.title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2'
        
        MSV = (np.sum((np.maximum(rc-s,[0]*(N+1))))).astype('int')
        fig_1c.title = 'Reservoir storage volume - MSV = '+str(MSV)+' ML'
    
        return u_frac, Qenv, Qspill, u, I_reg, s
    
    # Function to update the figures when changing the parameters with the sliders
    def update_figure_1(change):
        policy_function.y = update_operating_policy_1(s_ref_1.value,s_ref_2.value,u_ref.value)[0]
        releases.y = update_operating_policy_1(s_ref_1.value,s_ref_2.value,u_ref.value)[3]
        storage.y = update_operating_policy_1(s_ref_1.value,s_ref_2.value,u_ref.value)[5]
    
    # Definition of the sliders    
    u_ref = widgets.FloatSlider(min=0.5, max=u_1, value=1, step=0.05,
                                description = 'u_ref: ',
                                continuous_update = False)
    u_ref.observe(update_figure_1,names = 'value')
    
    s_ref_1 = widgets.FloatSlider(min=0, max=1, value=0.25, step=0.05, 
                                  description = 's_ref_1: ',
                                  continuous_update=False)
    s_ref_1.observe(update_figure_1,names = 'value')
    
    s_ref_2 = widgets.FloatSlider(min=0, max=1, value=0.75, step=0.05,
                                  description = 's_ref_2: ',
                                  continuous_update=False)
    s_ref_2.observe(update_figure_1,names = 'value')
    
    # Initial simulation applying the default slider values of the parameters 
    x0 = [0,       u_0]
    x1 = [s_ref_1.value, u_ref.value]
    x2 = [s_ref_2.value, u_ref.value]
    x3 = [1,       u_1]
    param = [x0, x1, x2, x3, u_mean]
    u_frac = four_points_policy(param)/u_mean

    Qreg = {'releases' : {'file_name' : 'Reservoir_operating_policy.Operating_policy_functions',
                         'function' : 'four_points_policy',
                         'param': param},
            'inflows' : [],
            'rel_inf' : []}
    
    Qenv, Qspill, u, I_reg, s, E = Res_sys_sim(I_hist, e_hist, s_0, s_min, s_max, env_min, d_hist, Qreg)
    
    ### Figures ###
    # Fig 1a: Policy function
    s_frac = np.arange(0,1.01,0.01)
    
    x_sc_1a = LinearScale(min=0,max=1); y_sc_1a = LinearScale(min=0,max=u_1);
    x_ax_1a = Axis(label='Storage fraction', scale=x_sc_1a); 
    y_ax_1a = Axis(label='Release fraction', scale=y_sc_1a, orientation='vertical')
    
    policy_function           = Lines(x   = s_frac,
                              y      = u_frac,
                              colors = ['blue'],
                              scales = {'x': x_sc_1a, 'y': y_sc_1a})
    
    fig_1a             = plt.Figure(marks = [policy_function],
                                   title = 'Policy function',
                                   axes=[x_ax_1a, y_ax_1a],
                                   layout={'width': '400px', 'height': '375px'}, 
                                   animation_duration=1000,
                                   scales={'x': x_sc_1a, 'y': y_sc_1a})
    
    policy_function.observe(update_figure_1, ['x', 'y'])
    
    # Fig 1b: Releases vs Demand
    x_sc_1b = LinearScale(min=0,max=N);         y_sc_1b = LinearScale(min=0,max=u_max);
    x_ax_1b = Axis(label='week', scale=x_sc_1b); y_ax_1b = Axis(label='ML/week', scale=y_sc_1b, orientation='vertical')
    
    demand             = Bars(x   = np.arange(1,N+1),
                              y      = d_hist,
                              colors = ['gray'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b})
    
    releases           = Bars(x   = np.arange(1,N+1),
                              y      = u,
                              colors = ['green'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b})
    
    TSD = (np.sum((np.maximum(d_hist-u,[0]*N))**2)).astype('int')
    
    fig_1b             = plt.Figure(marks = [demand, releases],
                                   title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2',
                                   axes=[x_ax_1b, y_ax_1b],
                                   layout={'width': '950px', 'height': '250px'}, 
                                   animation_duration=1000,
                                   scales={'x': x_sc_1b, 'y': y_sc_1b})
    
    releases.observe(update_figure_1, ['x', 'y'])
    
    # Fig 1c: Storage
    x_sc_1c = LinearScale();                    y_sc_1c = LinearScale(min=0,max=200);
    x_ax_1c = Axis(label='week', scale=x_sc_1c); y_ax_1c = Axis(label='ML', scale=y_sc_1c, orientation='vertical')
    
    storage           = Lines(x      = np.arange(0,N+1),
                              y      = s ,
                              colors = ['blue'],
                              scales = {'x': x_sc_1c, 'y': y_sc_1c},
                              fill   = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    
    max_storage       = plt.plot(x=np.arange(0,N+1),
                                 y=[s_max]*(N+1),
                                 colors=['red'],
                                 scales={'x': x_sc_1c, 'y': y_sc_1c})
    
    max_storage_label = plt.label(text = ['Max storage'], 
                                  x=[0],
                                  y=[s_max+15],
                                  colors=['red'])
    
    min_storage = plt.plot(np.arange(0,N+1),rc,
                             scales={'x': x_sc_1c, 'y': y_sc_1c},
                             colors=['red'],opacities = [1],
                             line_style = 'dashed',
                             fill = 'bottom',fill_opacities = [0.4],fill_colors = ['red'], stroke_width = 1)
    min_storage_label = plt.label(text = ['Min storage'], 
                                    x=[0],
                                    y=[rc[0]-10],
                                    colors=['red'])
    
    MSV = (np.sum((np.maximum(rc-s,[0]*(N+1))))).astype('int')
    
    fig_1c             = plt.Figure(marks = [storage,max_storage,max_storage_label,
                                            min_storage,min_storage_label],
                                   title = 'Reservoir storage volume - MSV = '+str(MSV)+' ML',
                                   axes=[x_ax_1c, y_ax_1c],
                                   layout={'width': '950px', 'height': '250px'}, 
                                   animation_duration=1000,
                                   scales={'x': x_sc_1c, 'y': y_sc_1c})
    
    storage.observe(update_figure_1, ['x', 'y'])
    
    return fig_1a,fig_1b,fig_1c, u_ref,s_ref_1,s_ref_2

def Interactive_policy_auto(N, 
                            I_hist, e_hist, 
                            s_0, s_min, s_max, 
                            u_0, u_1, u_mean, u_max,
                            env_min, d_hist, 
                            rc, 
                            results1_optim,results2_optim,sol_optim):
    
    # Function to update the release policy when clicking on the points of the Pareto front
    def update_operating_policy_2(i):
        
        u_ref,s_ref_1,s_ref_2 = sol_optim[i]
        x0 = [0,       u_0]
        x1 = [s_ref_1, u_ref]
        x2 = [s_ref_2, u_ref]
        x3 = [1,       u_1]
        param = [x0, x1, x2, x3, u_mean]
        u_frac = four_points_policy(param)/u_mean
        
        Qreg = {'releases' : {'file_name' : 'Reservoir_operating_policy.Operating_policy_functions',
                             'function' : 'four_points_policy',
                             'param': param},
                'inflows' : [],
                'rel_inf' : []}
        
        Qenv, Qspill, u, I_reg, s, E = Res_sys_sim(I_hist, e_hist, s_0, s_min, s_max, env_min, d_hist, Qreg)
        
        MSV = (np.sum((np.maximum(rc-s,[0]*(N+1))))).astype('int')
        fig_2c.title = 'Reservoir storage volume - MSV = '+str(MSV)+' ML'
        
        TSD = (np.sum((np.maximum(d_hist-u,[0]*N))**2)).astype('int')
        fig_2b.title = 'Supply vs Demand - Total squared deficit = '+str(TSD)+' ML^2'
        
        return u_frac, Qenv, Qspill, u, I_reg, s
    
    # Function to update the figures when clicking on the points of the Pareto front
    def update_figure_2(change):
        
        policy_function.y = update_operating_policy_2(pareto_front.selected[0])[0]
        releases.y = update_operating_policy_2(pareto_front.selected[0])[3]
        storage.y = update_operating_policy_2(pareto_front.selected[0])[5]
    
    # Fig_pf: Pareto front  
    x_sc_pf = LinearScale();y_sc_pf = LinearScale()
    x_ax_pf = Axis(label='Total squared deficit [ML^2]', scale=x_sc_pf)
    y_ax_pf = Axis(label='Minimum storage violation [ML]', scale=y_sc_pf, orientation='vertical')
    
    pareto_front = plt.scatter(results1_optim[:],results2_optim[:],
                               scales={'x': x_sc_pf, 'y': y_sc_pf},
                               colors=['deepskyblue'], 
                               interactions={'hover':'tooltip','click': 'select'})
    
    pareto_front.unselected_style={'opacity': 0.4}
    pareto_front.selected_style={'fill': 'red', 'stroke': 'yellow', 'width': '1125px', 'height': '125px'}
    def_tt = Tooltip(fields=['index','x', 'y'],
                     labels=['index','Water deficit', 'Min storage'], 
                     formats=['.d','.1f', '.1f'])
    pareto_front.tooltip=def_tt
    
    fig_pf = plt.Figure(marks = [pareto_front],title = 'Interactive Pareto front', 
                        axes=[x_ax_pf, y_ax_pf],
                        layout={'width': '400px', 'height': '400px'}, animation_duration=1000)
    
    if pareto_front.selected == []:
        pareto_front.selected = [0]
    
    pareto_front.observe(update_figure_2,'selected')
    
    # Initial simulation applting the point of the Pareto Fron selected by default 
    u_ref,s_ref_1,s_ref_2 = sol_optim[pareto_front.selected[0]]
    x0 = [0,       u_0]
    x1 = [s_ref_1, u_ref]
    x2 = [s_ref_2, u_ref]
    x3 = [1,       u_1]
    param = [x0, x1, x2, x3, u_mean]
    u_frac = four_points_policy(param)/u_mean
    
    Qreg = {'releases' : {'file_name' : 'Reservoir_operating_policy.Operating_policy_functions',
                         'function' : 'four_points_policy',
                         'param': param},
            'inflows' : [],
            'rel_inf' : []}
    
    Qenv, Qspill, u, I_reg, s, E = Res_sys_sim(I_hist, e_hist, s_0, s_min, s_max, env_min, d_hist, Qreg)
    
    # Fig 2a: Policy function
    s_frac = np.arange(0,1.01,0.01)
    
    x_sc_2a = LinearScale(min=0,max=1); y_sc_2a = LinearScale(min=0,max=u_max/u_mean);
    x_ax_2a = Axis(label='Storage fraction', scale=x_sc_2a); 
    y_ax_2a = Axis(label='Release fraction', scale=y_sc_2a, orientation='vertical')
    
    policy_function           = Lines(x   = s_frac,
                              y      = u_frac ,
                              colors = ['blue'],
                              scales = {'x': x_sc_2a, 'y': y_sc_2a})
    
    fig_2a             = plt.Figure(marks = [policy_function],
                                   title = 'Policy function',
                                   axes=[x_ax_2a, y_ax_2a],
                                   layout={'width': '400px', 'height': '375px'}, 
                                   animation_duration=1000,
                                   scales={'x': x_sc_2a, 'y': y_sc_2a})
    
    policy_function.observe(update_figure_2, ['x', 'y'])
    
    # Fig 2b: Releases vs Demand
    x_sc_2b = LinearScale(min=0,max=N);         y_sc_2b = LinearScale(min=0,max=u_max);
    x_ax_2b = Axis(label='week', scale=x_sc_2b); y_ax_2b = Axis(label='ML/week', scale=y_sc_2b, orientation='vertical')
    
    demand             = Bars(x   = np.arange(1,N+1),
                              y      = d_hist,
                              colors = ['gray'],
                              scales = {'x': x_sc_2b, 'y': y_sc_2b})
    
    releases           = Bars(x   = np.arange(1,N+1),
                              y      = u,
                              colors = ['green'],
                              scales = {'x': x_sc_2b, 'y': y_sc_2b})
    
    TSD = (np.sum((np.maximum(d_hist-u,[0]*N))**2)).astype('int')
    
    fig_2b             = plt.Figure(marks = [demand, releases],
                                   title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2',
                                   axes=[x_ax_2b, y_ax_2b],
                                   layout={'width': '950px', 'height': '250px'}, 
                                   animation_duration=1000,
                                   scales={'x': x_sc_2b, 'y': y_sc_2b})
    
    releases.observe(update_figure_2, ['x', 'y'])
    
    # Fig 2c: Storage
    x_sc_2c = LinearScale();                    y_sc_2c = LinearScale(min=0,max=200);
    x_ax_2c = Axis(label='week', scale=x_sc_2c); y_ax_2c = Axis(label='ML', scale=y_sc_2c, orientation='vertical')
    
    storage           = Lines(x      = np.arange(0,N+1),
                              y      = s ,
                              colors = ['blue'],
                              scales = {'x': x_sc_2c, 'y': y_sc_2c},
                              fill   = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    
    max_storage       = plt.plot(x=np.arange(0,N+1),
                                 y=[s_max]*(N+1),
                                 colors=['red'],
                                 scales={'x': x_sc_2c, 'y': y_sc_2c})
    
    max_storage_label = plt.label(text = ['Max storage'], 
                                  x=[0],
                                  y=[s_max+15],
                                  colors=['red'])
    
    min_storage = plt.plot(np.arange(0,N+1),rc,
                             scales={'x': x_sc_2c, 'y': y_sc_2c},
                             colors=['red'],opacities = [1],
                             line_style = 'dashed',
                             fill = 'bottom',fill_opacities = [0.4],fill_colors = ['red'], stroke_width = 1)
    min_storage_label = plt.label(text = ['Min storage'], 
                                    x=[0],
                                    y=[rc[0]-10],
                                    colors=['red'])
    
    MSV = (np.sum((np.maximum(rc-s,[0]*(N+1))))).astype('int')
    
    fig_2c             = plt.Figure(marks = [storage,max_storage,max_storage_label,
                                            min_storage,min_storage_label],
                                   title = 'Reservoir storage volume - MSV = '+str(MSV)+' ML',
                                   axes=[x_ax_2c, y_ax_2c],
                                   layout={'width': '950px', 'height': '250px'}, 
                                   animation_duration=1000,
                                   scales={'x': x_sc_2c, 'y': y_sc_2c})
    
    storage.observe(update_figure_2, ['x', 'y'])
    
    return fig_pf, fig_2a,fig_2b,fig_2c