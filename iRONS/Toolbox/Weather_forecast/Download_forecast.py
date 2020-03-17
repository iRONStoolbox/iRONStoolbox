# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 12:22:02 2019

@author: ap18525
"""
import os
import cdsapi
server = cdsapi.Client()

def data_retrieval_request(originating_centre,system,weather_variables,
                           years, months, days, leadtime_hours,
                           grid_resolution, coordinates,
                           file_format,folder_path,file_name_end):
    
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    
    for year in years:
        for month in months:
            for day in days:
                           
                server.retrieve(
                    'seasonal-original-single-levels',
                    {
                        'format': file_format,
                        'originating_centre': originating_centre,
                        'system': system,
                        'variable': weather_variables,
                        'year': str(year),
                        'month': str(month).zfill(2),
                        'day': str(day).zfill(2),
                        'leadtime_hour': leadtime_hours,
                        'grid': grid_resolution, 
                        'area': coordinates, 
                    },
                    folder_path+"//"+str(year)+str(month).zfill(2)+str(day).zfill(2)+file_name_end)