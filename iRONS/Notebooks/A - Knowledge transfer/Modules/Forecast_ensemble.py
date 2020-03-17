# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:17:14 2019

@author: ap18525
"""
import numpy as np
from bqplot import pyplot as plt
from bqplot import *
from bqplot.traits import *

def Ensemble_member_sel(N,members_num,I_for,d_for):
    
    I_sel = np.array([[0]*N])
    d_sel = np.array([[0]*N])
    
    def on_element_click_event_1a(self, target):
        click_elem_id = list(target.values())[1]['index']
        line_opacities = [0.4]*members_num
        line_opacities[click_elem_id] = 1
        inflow_forecast.opacities = line_opacities
        line_colors = ['deepskyblue']*members_num
        line_colors[click_elem_id] = 'darkblue'
        inflow_forecast.colors = line_colors
        for t in range(N):
            I_sel[0,t] = I_for[click_elem_id][t]
        fig_1a.title = 'Inflow forecast - Chosen forecast member = '+str(click_elem_id)
        fig_1a.title_style = {'fill': 'black','stroke': 'black', 'font-size': '20px'}
        
    def on_element_click_event_1b(self, target):
        click_elem_id = list(target.values())[1]['index']
        line_opacities = [0.4]*members_num
        line_opacities[click_elem_id] = 1
        demand_forecast.opacities = line_opacities
        line_colors = ['lightgreen']*members_num
        line_colors[click_elem_id] = 'darkolivegreen'
        demand_forecast.colors = line_colors
    #    line_styles = ['solid']*members_num
    #    line_styles[click_elem_id] = 'dash_dotted'
    #    demand_forecast.line_styles = line_styles
        for t in range(N):
            d_sel[0,t] = d_for[click_elem_id][t]
        fig_1b.title = 'Demand forecast  - Chosen forecast member = '+str(click_elem_id)
        fig_1b.title_style = {'fill': 'black','stroke': 'black', 'font-size': '20px'}
    
    def on_hover_1a(self, target):
        hover_elem_id = list(target.values())[1]['index']
        line_opacities = [0.4]*members_num
        line_opacities[hover_elem_id] = 1
        inflow_forecast.opacities = line_opacities
        
    def on_hover_1b(self, target):
        hover_elem_id = list(target.values())[1]['index']
        line_opacities = [0.4]*members_num
        line_opacities[hover_elem_id] = 1
        demand_forecast.opacities = line_opacities
    
    x_sc_1 = LinearScale()
    y_sc_1 = LinearScale(min = 0,max = 40)
    x_ax_1 = Axis(label='week',scale=x_sc_1,tick_values = np.arange(1,N+1),tick_style={'fill': 'black', 'font-size': 16})
    y_ax_1 = Axis(label='ML/week', scale=y_sc_1, orientation='vertical',tick_style={'fill': 'black', 'font-size': 16})
    
    def_tt = Tooltip(fields=['index'], formats=['.0f'], labels=['Forecast member'])
    inflow_forecast = plt.plot(x=np.arange(1,N+1),y=I_for,colors=['deepskyblue'],stroke_width = 4,opacities = [0.4]*members_num,
                               tooltip=def_tt, display_legend=False,scales={'x': x_sc_1, 'y': y_sc_1})
    inflow_forecast.on_element_click(on_element_click_event_1a)
    inflow_forecast.on_hover(on_hover_1a)
    fig_1a = plt.Figure(marks = [inflow_forecast],title = 'Inflow forecast  - Choose a forecast member:',
                        title_style={'fill': 'blue', 'font-size': '20px'},axes=[x_ax_1, y_ax_1],
                        layout={'min_width': '1000px', 'max_height': '300px'},scales={'x': x_sc_1, 'y': y_sc_1})
    
    demand_forecast = plt.plot(np.arange(1,N+1),d_for,colors=['lightgreen'],stroke_width = 4,opacities = [0.4]*members_num,
                               tooltip=def_tt,scales={'x': x_sc_1, 'y': y_sc_1})
    demand_forecast.on_element_click(on_element_click_event_1b)
    demand_forecast.on_hover(on_hover_1b)
    fig_1b = plt.Figure(marks = [demand_forecast],title = 'Demand forecast - Choose a forecast member:', 
                        title_style={'fill': 'dimgray', 'font-size': '20px'},axes=[x_ax_1, y_ax_1],
                        layout={'min_width': '1000px', 'max_height': '300px'},scales={'x': x_sc_1, 'y': y_sc_1})
    
    return fig_1a,fig_1b,I_sel,d_sel

def Observed_inflows(N,members_num,I_sel,d_sel,I_for,d_for):
    I_act = np.array([[14.85, 20.17, 21.84, 20.59,14.85, 20.17, 21.84, 20.59]])
    T_act = np.array([[24.81, 22.37, 20.13, 18.91,24.81, 22.37, 20.13, 18.91]])
    E_act = T_act/10
    d_act = T_act
 
    x_sc_1 = LinearScale()
    y_sc_1 = LinearScale(min = 0,max = 40)
    x_ax_1 = Axis(label='week',scale=x_sc_1,tick_values = np.arange(1,9),tick_style={'fill': 'black', 'font-size': 16})
    y_ax_1 = Axis(label='ML/week', scale=y_sc_1, orientation='vertical',tick_style={'fill': 'black', 'font-size': 16})
    
    inflow_forecast_3 = plt.plot(x=np.arange(1,N+1),y=I_for,colors=['deepskyblue'],stroke_width = 4,opacities = [0.4]*members_num,
                               display_legend=False,scales={'x': x_sc_1, 'y': y_sc_1})
    sel_inflow_3 = plt.plot(np.arange(1,N+1),I_sel,scales={'x': x_sc_1, 'y': y_sc_1}, colors=['darkblue'],stroke_width = 4,line_style = 'solid',marker = None,marker_size = 20,labels = ['forecast'], display_legend = True)
    act_inflow_3 = plt.plot(np.arange(1,N+1),I_act,scales={'x': x_sc_1, 'y': y_sc_1}, colors=['black'],stroke_width = 4,marker = None,marker_size = 40,labels = ['actual'], display_legend = True)
    fig_3a       = plt.Figure(marks = [inflow_forecast_3,sel_inflow_3,act_inflow_3], title = 'Inflows in the last 8 weeks', 
                        axes=[x_ax_1, y_ax_1],layout={'min_width': '1000px', 'max_height': '300px'},
                        scales={'x': x_sc_1, 'y': y_sc_1},legend_location = 'bottom-left')
    
    demand_forecast_3 = plt.plot(x=np.arange(1,N+1),y=d_for,colors=['lightgreen'],stroke_width = 4,opacities = [0.4]*members_num,
                               display_legend=False,scales={'x': x_sc_1, 'y': y_sc_1})
    sel_demand_3 = plt.plot(np.arange(1,N+1),d_sel,scales={'x': x_sc_1, 'y': y_sc_1},colors=['darkolivegreen'],stroke_width = 4,line_style = 'solid',label = 'selected',marker = None,marker_size = 20,labels = ['forecast'], display_legend = True)
    act_demand_3 = plt.plot(np.arange(1,N+1),d_act,scales={'x': x_sc_1, 'y': y_sc_1},colors=['black'],stroke_width = 4,label = 'actual',marker = None,marker_size = 40,labels = ['actual'], display_legend = True)
    fig_3b       = plt.Figure(marks = [demand_forecast_3,sel_demand_3,act_demand_3], title = 'Demand in the last 8 weeks', axes=[x_ax_1, y_ax_1],
                        layout={'min_width': '1000px', 'max_height': '300px'},
                        scales={'x': x_sc_1, 'y': y_sc_1},legend_location = 'bottom-left')
    return I_act,T_act,E_act,d_act,fig_3a,fig_3b

def Forecast_ensemble(N,members_num,I_for,d_for):
    x_sc_1 = LinearScale()
    y_sc_1 = LinearScale(min = 0,max = 40)
    x_ax_1 = Axis(label='week',scale=x_sc_1,tick_values = np.arange(1,9),tick_style={'fill': 'black', 'font-size': 16})
    y_ax_1 = Axis(label='ML/week', scale=y_sc_1, orientation='vertical',tick_style={'fill': 'black', 'font-size': 16})
    
    inflow_forecast_9 = plt.plot(x=np.arange(1,N+1),y=I_for,colors=['deepskyblue'],stroke_width = 4,opacities = [1]*members_num,
                               display_legend=False,scales={'x': x_sc_1, 'y': y_sc_1})
    fig_9a       = plt.Figure(marks = [inflow_forecast_9], title = 'Inflow forecast for the next 8 weeks', 
                        axes=[x_ax_1, y_ax_1],layout={'min_width': '1000px', 'max_height': '300px'},
                        scales={'x': x_sc_1, 'y': y_sc_1},legend_location = 'bottom-left')
    
    demand_forecast_9 = plt.plot(x=np.arange(1,N+1),y=d_for,colors=['ligthgreen'],stroke_width = 4,opacities = [1]*members_num,
                               display_legend=False,scales={'x': x_sc_1, 'y': y_sc_1})
    fig_9b       = plt.Figure(marks = [demand_forecast_9], title = 'Demand forecast for the next 8 weeks', axes=[x_ax_1, y_ax_1],
                        layout={'min_width': '1000px', 'max_height': '300px'},
                        scales={'x': x_sc_1, 'y': y_sc_1},legend_location = 'bottom-left')
    
    return fig_9a,fig_9b