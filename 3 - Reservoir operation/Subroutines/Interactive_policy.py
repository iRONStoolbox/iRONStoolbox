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
from IPython.display import display

def Interactive_policy_single(simtime,I,E,d,S0,Smax,env_min, demand_plot):
    def syst_sim(simtime,I,E,d,S0,Smax,env_min,u):
    
        # Declare output variables
    
        S = [0]*(simtime+1) # reservoir storage in ML
    
        w = [0]*(simtime) # spillage in ML
    
        env = [env_min]*(simtime) # environmental compensation flow
        
        S[0] = S0 # initial storage
    
        for t in range(simtime): # Loop for each time-step (week)
    
            # If at week t the inflow (I) is lower than the minimum environmental compensation (env_min), 
            # then the environmental compensation (env) = inflow (I)  
            if env_min >= I[t] :
                env[t] = I[t]
            # If the minimum environmental compensation is higher than the water resource available (S + I - E)
            # then the environmental compensation is equal to the higher value between 0 and the resource available
            if env_min >= S[t] + I[t] - E[t]:
                env[t] = max(0,S[t] + I[t] - E[t]) # S[t] = Smin then env[t] = I[t] and S[t+1] < Smin
            # If the demand is higher than the water resource available (S + I - E - env)
            # then the release for water supply is equal to the higher value between 0 and the resource available            
            if d[t] >= S[t] + I[t] - E[t] - env[t]:
                u[t] = min(u[t],max(0,S[t] + I[t] - E[t] - env[t]))
            # The spillage is equal to the higher value between 0 and the resource available exceeding the reservoir capacity
            w[t] = max(0,S[t] + I[t] - u[t] - env[t] - E[t] - Smax)
            # The final storage (initial storage in the next step) is equal to the storage + inflow - outflows
            S[t+1] = S[t] + I[t] - u[t] - env[t]- E[t] - w[t]
            
        return S,env,w,u
    
    # Interactive operating rule definition
    def update_operation_2(u):
        S,env,w,u1 = syst_sim(simtime,I,E,d,S0,Smax,env_min,u)
        sdpen = (np.sum((np.maximum(d-u1,[0]*simtime))**2)).astype('int')
        fig_2b.title = 'Supply vs Demand - Deficit penalty = '+str(sdpen)
        return S,u1
    
    def policy_changed_2a(change):
        y_vals_2a = update_operation_2([release1.value,release2.value,release3.value,release4.value,
                                        release5.value,release6.value,release7.value,release8.value])[0]
        storage_2.y = y_vals_2a
        
    def policy_changed_2b(change):
        y_vals_2b = update_operation_2([release1.value,release2.value,release3.value,release4.value,
                                        release5.value,release6.value,release7.value,release8.value])[1]
        releases_2.y = y_vals_2b
        
    release1 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 1',orientation='vertical',layout={'width': '100px'})
    release1.observe(policy_changed_2a,'value')
    release1.observe(policy_changed_2b,'value')
    release2 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 2',orientation='vertical',layout={'width': '100px'})
    release2.observe(policy_changed_2a,'value')
    release2.observe(policy_changed_2b,'value')
    release3 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 3',orientation='vertical',layout={'width': '100px'})
    release3.observe(policy_changed_2a,'value')
    release3.observe(policy_changed_2b,'value')
    release4 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 4',orientation='vertical',layout={'width': '100px'})
    release4.observe(policy_changed_2a,'value')
    release4.observe(policy_changed_2b,'value')
    release5 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 5',orientation='vertical',layout={'width': '100px'})
    release5.observe(policy_changed_2a,'value')
    release5.observe(policy_changed_2b,'value')
    release6 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 6',orientation='vertical',layout={'width': '100px'})
    release6.observe(policy_changed_2a,'value')
    release6.observe(policy_changed_2b,'value')
    release7 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 7',orientation='vertical',layout={'width': '100px'})
    release7.observe(policy_changed_2a,'value')
    release7.observe(policy_changed_2b,'value')
    release8 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 8',orientation='vertical',layout={'width': '100px'})
    release8.observe(policy_changed_2a,'value')
    release8.observe(policy_changed_2b,'value')
    
    u=[release1.value,release2.value,release3.value,release4.value,release5.value,release6.value,release7.value,release8.value]
    
    S,env,w,u1 = syst_sim(simtime,I,E,d,S0,Smax,env_min,np.array([0]*simtime))
    sdpen = np.sum((np.maximum(d-u1,[0]*simtime))**2).astype('int')

    x_sc_1 = LinearScale();y_sc_1 = LinearScale(min=0,max=35);x_ax_1 = Axis(label='week', scale=x_sc_1);y_ax_1 = Axis(label='ML/week', scale=y_sc_1, orientation='vertical')
    
    x_sc_2a             = LinearScale(min=0,max=simtime);y_sc_2a = LinearScale(min=0,max=200);x_ax_2a = Axis(label='week', scale=x_sc_2a,tick_values=np.arange(8)+0.5);y_ax_2a = Axis(label='ML', scale=y_sc_2a, orientation='vertical')
    storage_2           = Lines(x=np.arange(0,simtime+1),y=S,colors=['blue'],scales={'x': x_sc_2a, 'y': y_sc_2a},fill = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    max_storage_2       = plt.plot(x=np.arange(0,simtime+1),y=[Smax]*(simtime+1),colors=['red'],scales={'x': x_sc_2a, 'y': y_sc_2a})
    max_storage_label_2 = plt.label(text = ['Max storage'], x=[0],y=[Smax+15],colors=['red'])
    fig_2a              = plt.Figure(marks = [storage_2,max_storage_2,max_storage_label_2],title = 'Reservoir storage volume',
                                     axes=[x_ax_2a, y_ax_2a],layout={'width': '950px', 'height': '300px'}, 
                                       animation_duration=1000,scales={'x': x_sc_2a, 'y': y_sc_2a})
    
    releases_2 = plt.bar(np.arange(1,simtime+1),u1,colors=['green'],opacities = [0.7]*simtime,
                        labels = ['release'], display_legend = True, stroke_width = 1,scales={'x': x_sc_1, 'y': y_sc_1})
    fig_2b   = plt.Figure(marks = [demand_plot,releases_2],axes=[x_ax_1, y_ax_1],
                        layout={'min_width': '950px', 'max_height': '300px'}, 
                        animation_duration=0,legend_location = 'top-left',legend_style = {'fill': 'white', 'opacity': 0.5})
    
    storage_2.y  = update_operation_2(u)[0]
    releases_2.y = update_operation_2(u)[1]
    
    storage_2.observe(policy_changed_2a, ['x', 'y'])
    releases_2.observe(policy_changed_2b, ['x', 'y'])
    
    return fig_2a,fig_2b,release1,release2,release3,release4,release5,release6,release7,release8

def Interactive_policy_double(simtime,I,E,d,S0,Smax,ms,env_min, demand_plot):
    def syst_sim(simtime,I,E,d,S0,Smax,env_min,u):
    
        # Declare output variables
    
        S = [0]*(simtime+1) # reservoir storage in ML
    
        w = [0]*(simtime) # spillage in ML
    
        env = [env_min]*(simtime) # environmental compensation flow
        
        S[0] = S0 # initial storage
    
        for t in range(simtime): # Loop for each time-step (week)
    
            # If at week t the inflow (I) is lower than the minimum environmental compensation (env_min), 
            # then the environmental compensation (env) = inflow (I)  
            if env_min >= I[t] :
                env[t] = I[t]
            # If the minimum environmental compensation is higher than the water resource available (S + I - E)
            # then the environmental compensation is equal to the higher value between 0 and the resource available
            if env_min >= S[t] + I[t] - E[t]:
                env[t] = max(0,S[t] + I[t] - E[t]) # S[t] = Smin then env[t] = I[t] and S[t+1] < Smin
            # If the demand is higher than the water resource available (S + I - E - env)
            # then the release for water supply is equal to the higher value between 0 and the resource available            
            if d[t] >= S[t] + I[t] - E[t] - env[t]:
                u[t] = min(u[t],max(0,S[t] + I[t] - E[t] - env[t]))
            # The spillage is equal to the higher value between 0 and the resource available exceeding the reservoir capacity
            w[t] = max(0,S[t] + I[t] - u[t] - env[t] - E[t] - Smax)
            # The final storage (initial storage in the next step) is equal to the storage + inflow - outflows
            S[t+1] = S[t] + I[t] - u[t] - env[t]- E[t] - w[t]
            
        return S,env,w,u
    
    def update_operation_3(u):
        S,env,w,u1 = syst_sim(simtime,I,E,d,S0,Smax,env_min,u)
        lspen = np.sum((np.maximum(ms-S,[0]*(simtime+1)))).astype('int')
        fig_3a.title = 'Reservoir storage - Low storage penalty = '+str(lspen)
        sdpen = (np.sum((np.maximum(d-u1,[0]*simtime))**2)).astype('int')
        fig_3b.title = 'Supply vs Demand - Deficit penalty = '+str(sdpen)
        return S,u1
    
    def policy_changed_3a(change):
        y_vals_3a = update_operation_3([release1.value,release2.value,release3.value,release4.value,
                                        release5.value,release6.value,release7.value,release8.value])[0]
        storage_3.y = y_vals_3a
        
    def policy_changed_3b(change):
        y_vals_3b = update_operation_3([release1.value,release2.value,release3.value,release4.value,
                                        release5.value,release6.value,release7.value,release8.value])[1]
        releases_3.y = y_vals_3b
    
    release1 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 1',orientation='vertical',layout={'width': '100px'})
    release1.observe(policy_changed_3a,'value')
    release1.observe(policy_changed_3b,'value')
    release2 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 2',orientation='vertical',layout={'width': '100px'})
    release2.observe(policy_changed_3a,'value')
    release2.observe(policy_changed_3b,'value')
    release3 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 3',orientation='vertical',layout={'width': '100px'})
    release3.observe(policy_changed_3a,'value')
    release3.observe(policy_changed_3b,'value')
    release4 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 4',orientation='vertical',layout={'width': '100px'})
    release4.observe(policy_changed_3a,'value')
    release4.observe(policy_changed_3b,'value')
    release5 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 5',orientation='vertical',layout={'width': '100px'})
    release5.observe(policy_changed_3a,'value')
    release5.observe(policy_changed_3b,'value')
    release6 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 6',orientation='vertical',layout={'width': '100px'})
    release6.observe(policy_changed_3a,'value')
    release6.observe(policy_changed_3b,'value')
    release7 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 7',orientation='vertical',layout={'width': '100px'})
    release7.observe(policy_changed_3a,'value')
    release7.observe(policy_changed_3b,'value')
    release8 = widgets.FloatSlider(min = 0, max = 40, step=1, value = 0, description = 'Week 8',orientation='vertical',layout={'width': '100px'})
    release8.observe(policy_changed_3a,'value')
    release8.observe(policy_changed_3b,'value')
    
    u=[release1.value,release2.value,release3.value,release4.value,release5.value,release6.value,release7.value,release8.value]
    
    S,env,w,u1 = syst_sim(simtime,I,E,d,S0,Smax,env_min,np.array([0]*simtime))

    x_sc_1 = LinearScale();y_sc_1 = LinearScale(min=0,max=35);x_ax_1 = Axis(label='week', scale=x_sc_1);y_ax_1 = Axis(label='ML/week', scale=y_sc_1, orientation='vertical')
    
    x_sc_2a             = LinearScale(min=0,max=simtime);y_sc_2a = LinearScale(min=0,max=200);x_ax_2a = Axis(label='week', scale=x_sc_2a,tick_values=np.arange(8)+0.5);y_ax_2a = Axis(label='ML', scale=y_sc_2a, orientation='vertical')
    max_storage_2       = plt.plot(x=np.arange(0,simtime+1),y=[Smax]*(simtime+1),colors=['red'],scales={'x': x_sc_2a, 'y': y_sc_2a})
    max_storage_label_2 = plt.label(text = ['Max storage'], x=[0],y=[Smax+15],colors=['red'])

    storage_3           = Lines(x=np.arange(0,simtime+1),y=S,colors=['blue'],scales={'x': x_sc_2a, 'y': y_sc_2a},fill = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    min_storage_3 = plt.plot(np.arange(0,simtime+1),ms,scales={'x': x_sc_2a, 'y': y_sc_2a},colors=['red'],opacities = [1],line_style = 'dashed',
                           fill = 'bottom',fill_opacities = [0.4],fill_colors = ['red'], stroke_width = 1)
    min_storage_label_3 = plt.label(text = ['Min storage'], x=[0],y=[ms[0]-10],colors=['red'])
    fig_3a              = plt.Figure(marks = [min_storage_3,storage_3,max_storage_2,max_storage_label_2,min_storage_label_3],
                                     title = 'Reservoir storage volume',axes=[x_ax_2a, y_ax_2a],
                                     layout={'width': '950px', 'height': '300px'}, animation_duration=1000,scales={'x': x_sc_2a, 'y': y_sc_2a})
    
    releases_3 = plt.bar(np.arange(1,simtime+1),u1,colors=['green'],opacities = [0.7]*simtime,labels = ['release'], 
                        display_legend = True, stroke_width = 1,scales={'x': x_sc_1, 'y': y_sc_1})
    releases_3.observe(policy_changed_3b, ['x', 'y'])
    fig_3b = plt.Figure(marks = [demand_plot,releases_3],axes=[x_ax_1, y_ax_1],
                        layout={'min_width': '950px', 'max_height': '300px'},animation_duration=0,
                        legend_location = 'top-left', legend_style = {'fill': 'white', 'opacity': 0.5})
    
    storage_3.y  = update_operation_3(u)[0]
    releases_3.y = update_operation_3(u)[1]
    
    storage_3.observe(policy_changed_3a, ['x', 'y'])
    releases_3.observe(policy_changed_3b, ['x', 'y'])
    
    return fig_3a,fig_3b,release1,release2,release3,release4,release5,release6,release7,release8

def Interactive_Pareto_front(simtime,I,E,d,S0,Smax,ms,env_min, demand_plot,solutions_optim_relea,results1_optim_relea,results2_optim_relea):
    def syst_sim(simtime,I,E,d,S0,Smax,env_min,u):
    
        # Declare output variables
    
        S = [0]*(simtime+1) # reservoir storage in ML
    
        w = [0]*(simtime) # spillage in ML
    
        env = [env_min]*(simtime) # environmental compensation flow
        
        S[0] = S0 # initial storage
    
        for t in range(simtime): # Loop for each time-step (week)
    
            # If at week t the inflow (I) is lower than the minimum environmental compensation (env_min), 
            # then the environmental compensation (env) = inflow (I)  
            if env_min >= I[t] :
                env[t] = I[t]
            # If the minimum environmental compensation is higher than the water resource available (S + I - E)
            # then the environmental compensation is equal to the higher value between 0 and the resource available
            if env_min >= S[t] + I[t] - E[t]:
                env[t] = max(0,S[t] + I[t] - E[t]) # S[t] = Smin then env[t] = I[t] and S[t+1] < Smin
            # If the demand is higher than the water resource available (S + I - E - env)
            # then the release for water supply is equal to the higher value between 0 and the resource available            
            if d[t] >= S[t] + I[t] - E[t] - env[t]:
                u[t] = min(u[t],max(0,S[t] + I[t] - E[t] - env[t]))
            # The spillage is equal to the higher value between 0 and the resource available exceeding the reservoir capacity
            w[t] = max(0,S[t] + I[t] - u[t] - env[t] - E[t] - Smax)
            # The final storage (initial storage in the next step) is equal to the storage + inflow - outflows
            S[t+1] = S[t] + I[t] - u[t] - env[t]- E[t] - w[t]
            
        return S,env,w,u
    
    def update_operation_4(i):
        u = solutions_optim_relea[i]
        S,env,w,u1 = syst_sim(simtime,I,E,d,S0,Smax,env_min,u)
        lspen = np.sum((np.maximum(ms-S,[0]*(simtime+1)))).astype('int')
        fig_4a.title = 'Reservoir storage - Low level penalty = '+str(lspen)
        sdpen = (np.sum((np.maximum(d-u1,[0]*simtime))**2)).astype('int')
        fig_4b.title = 'Supply vs Demand - Deficit penalty = '+str(sdpen)
        return S,env,w,u1
    
    def solution_selected(change):
        if pareto_front.selected == None:
            pareto_front.selected = [0]
        y_vals_4a = update_operation_4(pareto_front.selected[0])[0]
        storage_4.y = y_vals_4a
        y_vals_4b = update_operation_4(pareto_front.selected[0])[3]
        releases_4.y = y_vals_4b
    
    x_sc_pf = LinearScale();y_sc_pf = LinearScale()
    x_ax_pf = Axis(label='Demand deficit penalty [ML]', scale=x_sc_pf)
    y_ax_pf = Axis(label='Low storage penalty [ML]', scale=y_sc_pf, orientation='vertical')
    pareto_front = plt.scatter(results1_optim_relea[:],results2_optim_relea[:],scales={'x': x_sc_pf, 'y': y_sc_pf},
                               colors=['deepskyblue'], interactions={'hover':'tooltip','click': 'select'})
    pareto_front.unselected_style={'opacity': 0.4}
    pareto_front.selected_style={'fill': 'red', 'stroke': 'yellow', 'width': '1125px', 'height': '125px'}
    def_tt = Tooltip(fields=['x', 'y'],labels=['Water deficit', 'Min storage'], formats=['.1f', '.1f'])
    pareto_front.tooltip=def_tt
    fig_pf = plt.Figure(marks = [pareto_front],title = 'Interactive Pareto front', axes=[x_ax_pf, y_ax_pf],
                        layout={'width': '500px', 'height': '500px'}, animation_duration=1000)
    
    if pareto_front.selected == []:
        pareto_front.selected = [0]
    
    pareto_front.observe(solution_selected,'selected')
    
    S,env,w,u1 = syst_sim(simtime,I,E,d,S0,Smax,env_min,solutions_optim_relea[pareto_front.selected[0]])

    x_sc_1 = LinearScale();y_sc_1 = LinearScale(min=0,max=35);x_ax_1 = Axis(label='week', scale=x_sc_1);y_ax_1 = Axis(label='ML/week', scale=y_sc_1, orientation='vertical')
    
    x_sc_2a             = LinearScale(min=0,max=simtime);y_sc_2a = LinearScale(min=0,max=200);x_ax_2a = Axis(label='week', scale=x_sc_2a,tick_values=np.arange(8)+0.5);y_ax_2a = Axis(label='ML', scale=y_sc_2a, orientation='vertical')
    max_storage_2       = plt.plot(x=np.arange(0,simtime+1),y=[Smax]*(simtime+1),colors=['red'],scales={'x': x_sc_2a, 'y': y_sc_2a})
    max_storage_label_2 = plt.label(text = ['Max storage'], x=[0],y=[Smax+15],colors=['red'])

    min_storage_3 = plt.plot(np.arange(0,simtime+1),ms,scales={'x': x_sc_2a, 'y': y_sc_2a},colors=['red'],opacities = [1],line_style = 'dashed',
                           fill = 'bottom',fill_opacities = [0.4],fill_colors = ['red'], stroke_width = 1)
    min_storage_label_3 = plt.label(text = ['Min storage'], x=[0],y=[ms[0]-10],colors=['red'])
    
    storage_4 = Lines(x=range(simtime+1),y=S,scales={'x': x_sc_2a, 'y': y_sc_2a}, fill = 'bottom',fill_opacities = [0.7]*simtime,
                      fill_colors = ['blue'])
    fig_4a = plt.Figure(marks = [min_storage_3,storage_4,max_storage_2,max_storage_label_2,min_storage_label_3], 
                        axes=[x_ax_2a, y_ax_2a],layout={'width': '480px', 'height': '250px'},animation_duration=1000)
    
    releases_4 = plt.bar(np.arange(1,simtime+1),u1,colors=['green'],opacities = [0.7]*simtime,scales={'x': x_sc_1, 'y': y_sc_1},
                                labels = ['release'], display_legend = True, stroke_width = 1)
    fig_4b = plt.Figure(marks = [demand_plot, releases_4], axes=[x_ax_1, y_ax_1],layout={'width': '480px', 'height': '250px'},
                        animation_duration=1000,legend_location = 'top-left',legend_style = {'fill': 'white', 'opacity': 0.5})
                                                                                                                  
    storage_4.y  = update_operation_4(pareto_front.selected[0])[0]
    releases_4.y = update_operation_4(pareto_front.selected[0])[3]
                         
    storage_4.observe(solution_selected, ['x', 'y'])
    releases_4.observe(solution_selected, ['x', 'y'])
    
    return fig_4a,fig_4b,fig_pf