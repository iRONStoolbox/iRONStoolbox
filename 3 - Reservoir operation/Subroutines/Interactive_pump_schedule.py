# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 16:03:57 2019

@author: ap18525
"""

import ipywidgets as widgets
import numpy as np
from bqplot import pyplot as plt
from bqplot import *
from bqplot.traits import *
from IPython.display import display

from Subroutines.Water_system_model import Water_system_model as syst_sim

def Interactive_Pareto_front_det(N,I_sel,E,d_sel,S0,Smax,Smin,env_min,c,solutions_optim_relea_2,results1_optim_relea_2,results2_optim_relea_2):
    
    def update_operation_2(i):
        u            = solutions_optim_relea_2[i]
        S,env,w,r    = syst_sim(N,I_sel+u,E,d_sel,S0,Smax,env_min)
#        sdpen        = (np.sum((np.maximum(d_sel-r,[0]*N))**2)).astype('int')
        fig_2b.title = 'Weekly supply deficit (max(0,d-r)) - Total = '+str((np.sum((np.maximum(d_sel-r,[0]*N))**2)).astype('int'))+' ML'
#        pcost        = (np.sum(np.array(u)*c)).astype('int')
        fig_2d.title = 'Natural + pumped inflows - Total pumped vol = '+str((np.sum(np.array(u))).astype('int'))+' ML'
        return       S,u,r,i
    
    def solution_selected_2(change):
        if pareto_front_2.selected  == None:
            pareto_front_2.selected = [0]
#        releases_2.y = update_operation_2(pareto_front_2.selected[0])[2] 
        deficit_2.y = np.maximum(d_sel-update_operation_2(pareto_front_2.selected[0])[2],[0]*N)
        storage_2.y  = update_operation_2(pareto_front_2.selected[0])[0]
        inflows_2.y = [I_sel[0],update_operation_2(pareto_front_2.selected[0])[1]]
#        nat_inflows_2.y = I_sel[0]
#        pump_inflows_2.y = solutions_optim_relea_2[pareto_front_2.selected[0]]
        
    x_sc_2pf = LinearScale();y_sc_2pf = LinearScale()
    x_ax_2pf = Axis(label='Total Pumping Cost [£]', scale=x_sc_2pf)
    y_ax_2pf = Axis(label='Total Squared Deficit [ML^2]', scale=y_sc_2pf, orientation='vertical')
    pareto_front_2                  = plt.scatter(results2_optim_relea_2[:],results1_optim_relea_2[:],scales={'x': x_sc_2pf, 'y': y_sc_2pf},
                                                colors=['deepskyblue'], interactions={'hover':'tooltip','click': 'select'})
    pareto_front_2.unselected_style = {'opacity': 0.4}
    pareto_front_2.selected_style   = {'fill': 'red', 'stroke': 'yellow', 'width': '1125px', 'height': '125px'}
    def_tt                          = Tooltip(fields=['x', 'y','index'],labels=['Squared deficit', 'Pumping cost','sol index'], 
                                            formats=['.1f', '.1f', '.0f'])
    pareto_front_2.tooltip          = def_tt
    fig_2pf                         = plt.Figure(marks = [pareto_front_2],title = 'Pareto front', axes=[x_ax_2pf, y_ax_2pf],
                                               layout={'width': '500px', 'height': '500px'}, animation_duration=1000)
    if pareto_front_2.selected      == []:
        pareto_front_2.selected     = [0]
    pareto_front_2.observe(solution_selected_2,'selected')    
    
    S,env,w,r = syst_sim(N,I_sel+solutions_optim_relea_2[pareto_front_2.selected[0]],E,d_sel,S0,Smax,env_min)
    
    x_sc_2b    = OrdinalScale(min=1,max=N);y_sc_2b = LinearScale(min=0,max=60)
    x_ax_2b = Axis(label='week', scale=x_sc_2b)
    y_ax_2b = Axis(label='ML/week', scale=y_sc_2b, orientation='vertical')
#    demand_2   = plt.bar(x=np.arange(1,N+1),y=d_sel,colors=['gray'],opacities = [0.7]*N, labels = ['demand (d)'], display_legend = True,
#                          scales={'x': x_sc_2b, 'y': y_sc_2b},marker = None,marker_size = 20, stroke = 'lightgray')
#    releases_2 = plt.bar(x=np.arange(1,N+1),y=r,colors=['green'],opacities = [0.7]*N, labels = ['release (r)'], display_legend = True,
#                          scales={'x': x_sc_2b, 'y': y_sc_2b}, stroke = 'lightgray')
    deficit_2 = plt.bar(x=np.arange(1,N+1),y=np.maximum(d_sel-r,[0]*N),colors=['red'],opacities = [1]*N, display_legend = False,
                          scales={'x': x_sc_2b, 'y': y_sc_2b}, stroke = 'lightgray')    
    fig_2b     = plt.Figure(marks = [deficit_2],axes=[x_ax_2b, y_ax_2b],layout={'width': '480px', 'height': '250px'},
                                      scales={'x': x_sc_2b, 'y': y_sc_2b}, animation_duration=1000,
                                      legend_location = 'bottom-right', legend_style = {'fill': 'white', 'opacity': 0.5})
    
    x_sc_2c             = LinearScale(min=0,max=N);y_sc_2c = LinearScale(min=0,max=200)
    x_ax_2c             = Axis(label='week', scale=x_sc_2c)
    y_ax_2c             = Axis(label='ML', scale=y_sc_2c, orientation='vertical')
    storage_2           = Lines(x=np.arange(0,N+1),y=S,colors=['blue'],scales={'x': x_sc_2c, 'y': y_sc_2c},fill = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    max_storage_2       = plt.plot(x=np.arange(0,N+1),y=[Smax]*(N+1),colors=['red'],scales={'x': x_sc_2c, 'y': y_sc_2c})
    max_storage_label_2 = plt.label(text = ['Max storage'], x=[0],y=[Smax+15],colors=['red'])
    fig_2c              = plt.Figure(marks = [storage_2,max_storage_2,max_storage_label_2],title = 'Reservoir storage (s)',
                                     axes=[x_ax_2c, y_ax_2c],layout={'width': '1000px', 'height': '350px'}, 
                                       animation_duration=1000,scales={'x': x_sc_2c, 'y': y_sc_2c})
    
    x_sc_2d    = OrdinalScale(min=1,max=N);y_sc_2d = LinearScale(min=0,max=60)
    x_ax_2d = Axis(label='week', scale=x_sc_2d);y_ax_2d = Axis(label='ML/week', scale=y_sc_2d, orientation='vertical')
#    Stacked bars
    inflows_2  = plt.bar(x=np.arange(1,N+1),y=(I_sel[0],solutions_optim_relea_2[pareto_front_2.selected[0]]),
                         colors=['blue','orange','blue','blue','blue','blue'],opacities = [0.7]*(N+3), stroke = 'lightgray', 
                         labels = ['natural (I)', 'pumped (u)'], display_legend = True,scales={'x': x_sc_2d, 'y': y_sc_2d})
#    nat_inflows_2  = plt.bar(x=np.arange(1,N+1),y=I_sel[0],
#                         colors=['blue']*N,opacities = [0.5]*(N+3), stroke = 'lightgray', scales={'x': x_sc_2d, 'y': y_sc_2d},
#                         labels = ['natural (I)'], display_legend = True)
#    pump_inflows_2  = plt.bar(x=np.arange(1,N+1),y=solutions_optim_relea_2[pareto_front_2.selected[0]],
#                         colors=['yellow']*N,opacities = [0.5]*(N+3), stroke = 'lightgray', 
#                         labels = ['natural (I)', 'pumped (u)'], display_legend = True,scales={'x': x_sc_2d, 'y': y_sc_2d})
    fig_2d     = plt.Figure(marks = [inflows_2],title = 'Natural + pumped inflows', axes=[x_ax_2d, y_ax_2d],
                         layout={'width': '480px', 'height': '250px'}, scales={'x': x_sc_2d, 'y': y_sc_2d}, animation_duration=1000,
                         legend_location = 'top-right', legend_style = {'fill': 'white', 'opacity': 0.5})
    
#    releases_2.y = update_operation_2(pareto_front_2.selected[0])[2]
    deficit_2.y = np.maximum(d_sel-update_operation_2(pareto_front_2.selected[0])[2],[0]*N)
    storage_2.y  = update_operation_2(pareto_front_2.selected[0])[0]
    inflows_2.y = [I_sel[0],update_operation_2(pareto_front_2.selected[0])[1]]
#    nat_inflows_2.y = I_sel[0]
#    pump_inflows_2.y = solutions_optim_relea_2[pareto_front_2.selected[0]]
    
#    releases_2.observe(solution_selected_2, ['x', 'y'])
    deficit_2.observe(solution_selected_2, ['x', 'y'])
    storage_2.observe(solution_selected_2, ['x', 'y'])
    inflows_2.observe(solution_selected_2, ['x', 'y'])
#    nat_inflows_2.observe(solution_selected_2, ['x', 'y'])
#    pump_inflows_2.observe(solution_selected_2, ['x', 'y'])
    
    return fig_2pf,fig_2b,fig_2c,fig_2d,pareto_front_2

def Interactive_Pareto_front_act(N,I_act,E_act,d_act,S0,Smax,Smin,env_min,c,solutions_optim_relea_2,results1_optim_relea_2,results2_optim_relea_2,sel_policy):
    
    population_size = np.shape(solutions_optim_relea_2)[0]
    sdpen_act_4 = np.zeros(population_size); pcost_act_4 = np.zeros(population_size)
    
    for i in range(population_size):
    
        pinfl_policy_4 = np.array(solutions_optim_relea_2[i])
    
        S_act_4,env_act_4,w_act_4,r_act_4    = syst_sim(N,I_act+pinfl_policy_4,E_act,d_act,S0,Smax,env_min)
        sdpen_act_4[i]       = (np.sum((np.maximum(d_act-r_act_4,[0]*N))**2)).astype('int')
        pcost_act_4[i]       = (np.sum(np.array(pinfl_policy_4)*c)).astype('int')    
        
    def update_operation_act_4(i):
        u            = solutions_optim_relea_2[i]
        S,env,w,r    = syst_sim(N,I_act+u,E_act,d_act,S0,Smax,env_min)
#        sdpen        = (np.sum((np.maximum(d_act-r,[0]*N))**2)).astype('int')
        fig_4b.title = 'Weekly supply deficit (max(0,d-r)) - Total = '+str((np.sum((np.maximum(d_act-r,[0]*N))**2)).astype('int'))+' ML'
#        pcost        = (np.sum(np.array(u)*c)).astype('int')
        fig_4d.title = 'Natural + pumped inflows - Total pumped vol = '+str((np.sum(np.array(u))).astype('int'))+' ML'
        return       S,u,r,i
    
    def solution_selected_act_4(change):
        if pareto_front_act_4.selected  == None:
            pareto_front_act_4.selected = [0]
#        releases_4.y = update_operation_act_4(pareto_front_act_4.selected[0])[2] 
        deficit_4.y = np.maximum(d_act-update_operation_act_4(pareto_front_act_4.selected[0])[2], [0]*N)
        storage_4.y  = update_operation_act_4(pareto_front_act_4.selected[0])[0]
        inflows_4.y = [I_act[0],update_operation_act_4(pareto_front_act_4.selected[0])[1]]
        
    def on_hover_4pf(self, target):
        hover_elem_id = list(target.values())[1]['index']
        
    def on_element_click_4pf(self, target):
        click_elem_id = list(target.values())[1]['index']
        colors = ['deepskyblue']*population_size
        colors[click_elem_id] = 'black'
        pareto_front_4.colors = colors
    

    x_sc_2pf = LinearScale();y_sc_2pf = LinearScale()
    x_ax_2pf = Axis(label='Total Pumping Cost [£]', scale=x_sc_2pf)
    y_ax_2pf = Axis(label='Total Squared Deficit [ML^2]', scale=y_sc_2pf, orientation='vertical')
    
    pareto_front_4                  = plt.scatter(results2_optim_relea_2[:],results1_optim_relea_2[:],scales={'x': x_sc_2pf, 'y': y_sc_2pf},
                                                colors=['deepskyblue'], opacity = [0.11]*population_size,
                                                  interactions={'hover':'tooltip'})
    pareto_front_4.tooltip          = None
    pareto_front_act_4                  = plt.scatter(pcost_act_4[:],sdpen_act_4[:],scales={'x': x_sc_2pf, 'y': y_sc_2pf},
                                                colors=['green'], interactions={'hover':'tooltip'})

    pareto_front_act_4.unselected_style = {'opacity': 0}
    pareto_front_act_4.selected_style   = {'fill': 'black', 'stroke': 'black', 'width': '1125px', 'height': '125px'}
    pareto_front_4.selected_style   = {'fill': 'red', 'stroke': 'yellow', 'width': '1125px', 'height': '125px'}
    pareto_front_act_4.tooltip          = None

    fig_4pf                         = plt.Figure(marks = [pareto_front_4,pareto_front_act_4 ],title = 'Pareto front', axes=[x_ax_2pf, y_ax_2pf],
                                               layout={'width': '500px', 'height': '500px'}, animation_duration=1000)
    
    if pareto_front_act_4.selected      == []:
        pareto_front_4.selected     = [sel_policy]
        pareto_front_act_4.selected     = [sel_policy]
    pareto_front_act_4.observe(solution_selected_act_4,'selected')
    pareto_front_act_4.on_hover(on_hover_4pf)
    pareto_front_4.on_hover(on_hover_4pf)
    
    x_sc_2b    = OrdinalScale(min=1,max=N);y_sc_2b = LinearScale(min=0,max=40)
    x_ax_2b = Axis(label='week', scale=x_sc_2b)
    y_ax_2b = Axis(label='ML/week', scale=y_sc_2b, orientation='vertical')
#    demand_4   = plt.bar(x=np.arange(1,N+1),y=d_act,colors=['gray'],opacities = [0.7]*N, labels = ['demand (d)'], display_legend = True,
#                          scales={'x': x_sc_2b, 'y': y_sc_2b},marker = None,marker_size = 20, stroke = 'lightgray')
#    releases_4 = plt.bar(x=np.arange(1,N+1),y=r_act_4,colors=['green'],opacities = [0.7]*N, labels = ['release (r)'], display_legend = True,
#                          scales={'x': x_sc_2b, 'y': y_sc_2b}, stroke = 'lightgray')
    deficit_4 = plt.bar(x=np.arange(1,N+1),y=np.maximum(d_act-r_act_4,[0]*N),colors=['red'],opacities = [1]*N, display_legend = False,
                          scales={'x': x_sc_2b, 'y': y_sc_2b}, stroke = 'lightgray')   
    fig_4b     = plt.Figure(marks = [deficit_4],axes=[x_ax_2b, y_ax_2b],layout={'width': '480px', 'height': '250px'},
                                      scales={'x': x_sc_2b, 'y': y_sc_2b}, animation_duration=1000,
                                      legend_location = 'bottom-right', legend_style = {'fill': 'white', 'opacity': 0.5})
    
    x_sc_2c             = LinearScale(min=0,max=N);y_sc_2c = LinearScale(min=0,max=200)
    x_ax_2c = Axis(label='week', scale=x_sc_2c)
    y_ax_2c = Axis(label='ML', scale=y_sc_2c, orientation='vertical')  
    max_storage_2       = plt.plot(x=np.arange(0,N+1),y=[Smax]*(N+1),colors=['red'],scales={'x': x_sc_2c, 'y': y_sc_2c})
    max_storage_label_2 = plt.label(text = ['Max storage'], x=[0],y=[Smax+15],colors=['red'])
    storage_4           = Lines(x=np.arange(0,N+1),y=S_act_4,colors=['blue'],scales={'x': x_sc_2c, 'y': y_sc_2c},fill = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    fig_4c              = plt.Figure(marks = [storage_4,max_storage_2,max_storage_label_2],title = 'Reservoir storage (s)',
                                     axes=[x_ax_2c, y_ax_2c],layout={'width': '1000px', 'height': '350px'}, 
                                       animation_duration=1000,scales={'x': x_sc_2c, 'y': y_sc_2c})

    x_sc_2d    = OrdinalScale(min=1,max=N);y_sc_2d = LinearScale(min=0,max=60)
    x_ax_2d = Axis(label='week', scale=x_sc_2d);y_ax_2d = Axis(label='ML/week', scale=y_sc_2d, orientation='vertical')    
    
    inflows_4  = plt.bar(x=np.arange(1,N+1),y=[I_act[0],pinfl_policy_4],
                         colors=['blue','orange','blue','blue','blue','blue'],opacities = [0.7]*(N+3), stroke = 'lightgray', 
                         labels = ['natural (I)', 'pumped (u)'], display_legend = True,scales={'x': x_sc_2d, 'y': y_sc_2d})
    fig_4d     = plt.Figure(marks = [inflows_4],title = 'Natural + pumped inflows', axes=[x_ax_2d, y_ax_2d],layout={'width': '480px', 'height': '250px'},
                                      scales={'x': x_sc_2d, 'y': y_sc_2d}, animation_duration=1000,
                                      legend_location = 'top-right', legend_style = {'fill': 'white', 'opacity': 0.5})
    
#    releases_4.y = update_operation_act_4(sel_policy)[2]
    deficit_4.y = np.maximum(d_act-update_operation_act_4(sel_policy)[2],[0]*N)
    storage_4.y  = update_operation_act_4(sel_policy)[0]
    inflows_4.y = [I_act[0],update_operation_act_4(sel_policy)[1]]
    
#    releases_4.observe(solution_selected_act_4, ['x', 'y'])
    deficit_4.observe(solution_selected_act_4, ['x', 'y'])
    storage_4.observe(solution_selected_act_4, ['x', 'y'])
    inflows_4.observe(solution_selected_act_4, ['x', 'y'])
    
    return fig_4b,fig_4c,fig_4d,fig_4pf
    
def Interactive_Pareto_front(N,I_for,E_for,d_for,S0,Smax,Smin,env_min,c,solutions_optim_relea,results1_optim_relea,results2_optim_relea):
    
    members_num = np.shape(I_for)[0]
    
    population_size = np.shape(solutions_optim_relea)[0]
    sdpen = np.zeros([members_num,population_size])
    sdpen_mean = np.zeros(population_size)
    sdpen_std = np.zeros(population_size)
    
    for i in range(population_size):
        S_opt,env_opt,w_opt,r_opt = syst_sim(N,I_for+solutions_optim_relea[i],E_for,d_for,S0,Smax,env_min)
        sdpen[:,i] = np.sum(np.maximum(d_for-r_opt,np.zeros(np.shape(d_for)))**2,axis = 1)
        sdpen_mean[i] = np.mean(sdpen[:,i])
        sdpen_std[i] = np.std(sdpen[:,i])
        r_opt
    
    # Interactive Pareto front
    def update_operation(i):
        S,env,w,r    = syst_sim(N,I_for+solutions_optim_relea[i],E_for,d_for,S0,Smax,env_min)
        fig_wd.title = 'Supply deficit (max(0,d-r))'
        fig_pi.title = 'Natural + pumped inflows - Total pumped vol = {:.0f} ML'.format(results2_optim_relea[i]/c)
        return       S,solutions_optim_relea[i],r,results1_optim_relea[i],results2_optim_relea[i],i
    
    def solution_selected(change):
        if pareto_front.selected == None:
            pareto_front.selected = [0]
        storage.y = update_operation(pareto_front.selected[0])[0]
        deficit.y = np.maximum(d_for-update_operation(pareto_front.selected[0])[2],np.zeros(np.shape(d_for)))
        pinflows.y = update_operation(pareto_front.selected[0])[1]
        pareto_front_ensemble.x = np.reshape([results2_optim_relea for i in range(0, members_num)],(members_num,population_size))[:,pareto_front.selected[0]]
        pareto_front_ensemble.y = sdpen[:,pareto_front.selected[0]]
        pareto_front_ensemble.unselected_style={'opacity': 0.1}
        pareto_front_ensemble.selected_style={'opacity': 0.1}
        pareto_front_ensemble.opacity = [0.1]*10
        
    x_sc_pf = LinearScale()
    y_sc_pf = LinearScale(min = 0,max = 4000)
    
    x_ax_pf = Axis(label='Total Pumping Cost [£]', scale=x_sc_pf)
    y_ax_pf = Axis(label='Total Squared Deficit [ML^2]', scale=y_sc_pf, orientation='vertical')
    
    pareto_front = plt.scatter(results2_optim_relea[:],results1_optim_relea[:],scales={'x': x_sc_pf, 'y': y_sc_pf},colors=['deepskyblue'], interactions={'hover':'tooltip','click': 'select'})
    pareto_front.unselected_style={'opacity': 0.8}
    pareto_front.selected_style={'fill': 'red', 'stroke': 'yellow', 'width': '1125px', 'height': '125px'}
    
    if pareto_front.selected == []:
        pareto_front.selected = [0]
        
    pareto_front_ensemble = plt.Scatter(x=np.reshape([results2_optim_relea for i in range(0, members_num)],(members_num,population_size))[:,pareto_front.selected[0]],
                                        y=sdpen[:,pareto_front.selected[0]],scales={'x': x_sc_pf, 'y': y_sc_pf},
                                        colors=['red'], interactions={'hover':'tooltip','click': 'select'})
    pareto_front_ensemble.unselected_style={'opacity': 0.1}
    pareto_front_ensemble.selected_style={'opacity': 0.1}
    pareto_front_ensemble.opacity = [0.1]*10
    fig_pf = plt.Figure(marks=[pareto_front,pareto_front_ensemble],title = 'Pareto front', axes=[x_ax_pf, y_ax_pf],layout={'width': '500px', 'height': '500px'}, 
                        animation_duration=500)
    
    pareto_front.observe(solution_selected,'selected')    
    
    S,env,w,r    = syst_sim(N,I_for+solutions_optim_relea[pareto_front.selected[0]],E_for,d_for,S0,Smax,env_min)
    
    x_sc_pi    = OrdinalScale(min=1,max=N);y_sc_pi = LinearScale(min=0,max=60); x_ax_pi = Axis(label='week', scale=x_sc_pi)
    y_ax_pi = Axis(label='ML/week', scale=y_sc_pi, orientation='vertical')
    x_sc_st    = LinearScale(min=0,max=N); y_sc_st = LinearScale(min=10,max=160);x_ax_st = Axis(label='week', scale=x_sc_st)#,tick_values=[0.5,1.5,2.5,3.5])
    y_ax_st = Axis(label='ML', scale=y_sc_st, orientation='vertical')
    x_sc_wd    = OrdinalScale(min=1,max=N);y_sc_wd = LinearScale(min=0,max=60); x_ax_wd = Axis(label='week', scale=x_sc_wd)
    y_ax_wd = Axis(label='ML/week', scale=y_sc_wd, orientation='vertical')
    
    
#    vertical_lines_pi = plt.vline([1,2,3,4,5,6,7],colors = ['black'])
    pinflows = plt.bar(np.arange(1,N+1),solutions_optim_relea[pareto_front.selected[0]],scales={'x': x_sc_pi, 'y': y_sc_pi},
                                   colors=['orange'],opacities = [1],stroke = 'lightgray',
                                   labels = ['pumped inflow'], display_legend = False)
    
    fig_pi   = plt.Figure(marks = [pinflows],axes=[x_ax_pi, y_ax_pi],layout={'max_width': '480px', 'max_height': '250px'},
                        scales={'x': x_sc_pi, 'y': y_sc_pi}, animation_duration=1000,legend_location = 'bottom-right')
    
    storage           = plt.plot(x=np.arange(0,N+1),y=S,scales={'x': x_sc_st, 'y': y_sc_st},
                                  colors=['blue'], stroke_width = 0.1,
                                  fill = 'bottom', fill_opacities = [0.1]*members_num)
    max_storage       = plt.plot(x=np.arange(0,N+1),y=[Smax]*(N+1),colors=['red'],scales={'x': x_sc_st, 'y': y_sc_st})
    max_storage_label = plt.label(text = ['Max storage'], x=[0],y=[Smax+10],colors=['red'])
    fig_st            = plt.Figure(marks = [storage,max_storage,max_storage_label], title = 'Reservoir storage volume', 
                         axes=[x_ax_st, y_ax_st],layout={'width': '1000px', 'height': '350px'}, animation_duration=1000,scales={'x': x_sc_st, 'y': y_sc_st})
    
    vertical_lines_wd = plt.vline([1,2,3,4,5,6,7],colors = ['black'])
    
    deficit = plt.bar(np.arange(1,N+1),np.maximum(d_for-r,np.zeros(np.shape(r))),scales={'x': x_sc_wd, 'y': y_sc_wd},
                                    colors=['red'],opacities = [0.7]*members_num*N,stroke = 'lightgray',
                                    labels = ['release (r)'], display_legend = False,type = 'grouped',base=0,align='center')
    fig_wd = plt.Figure(marks = [deficit,vertical_lines_wd],axes=[x_ax_wd, y_ax_wd],layout={'max_width': '480px', 'max_height': '250px'},
                        scales={'x': x_sc_wd, 'y': y_sc_wd}, animation_duration=1000,legend_location = 'bottom-right')
    
    storage.y  = update_operation(pareto_front.selected[0])[0]
    deficit.y  = np.maximum(d_for-update_operation(pareto_front.selected[0])[2],np.zeros(np.shape(d_for)))
    pinflows.y = update_operation(pareto_front.selected[0])[1]
    
    storage.observe(solution_selected, ['x', 'y'])
    deficit.observe(solution_selected, ['x', 'y'])
    pinflows.observe(solution_selected, ['x', 'y'])
    
    return fig_pf,fig_wd,fig_st,fig_pi,pareto_front