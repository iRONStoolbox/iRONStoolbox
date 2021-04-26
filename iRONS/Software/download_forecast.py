# -*- coding: utf-8 -*-
"""
This module send a request to the European Centre for Medium-Range Weather 
Forecasts servers to download seasonal forecast data.

You can also learn how to write these scripts yourself and view examples in
these links:
    https://confluence.ecmwf.int/display/WEBAPI/ECMWF+Web+API+Home
    https://confluence.ecmwf.int/display/UDOC/MARS+user+documentation


This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi and at 
Bristol University (2020).

Licence: MIT
"""
import os
import cdsapi
server = cdsapi.Client()

def data_retrieval_request(originating_centre,system,weather_variables,
                           years, months, days, leadtime_hours,
                           grid_resolution, coordinates,
                           file_format,folder_path,file_name_end):
    
    """
    This module retrieves seasonal forecast data in Netcdf (Network Common Data
    Form) format (https://confluence.ecmwf.int/display/CKB/What+are+NetCDF+files+and+how+can+I+read+them)
    
    Input:
        originating_centre = specifies the origin of the data, usually as the 
                             WMO centre identifier, either specified as number 
                             or 4 character abbreviation as listed in:
                             https://apps.ecmwf.int/codes/grib/format/mars/centre/
        system = labels the version of the operational forecast system for 
                 seasonal forecast related products.
        weather_variables = specifies the meteorological parameter of a field. 
                            List  of all parameters: https://apps.ecmwf.int/codes/grib/param-db/
        years = list of years of forecast base time 
        months = list of months of forecast base time 
        days = list of days of forecast base time
        leadtime_hours = The forecast time step in hours from the forecast base 
                         time
        grid_resolution = specifies the target grid resolution in degrees. 
                          The first number denotes the east-west resolution 
                          (longitude) and the second denotes the north-south 
                          resolution (latitude).    
        coordinates = specifies the coordinated of the desired area of the data
                      to be retrieved. North/West/South/East in decimal degrees
        file_format = format of the file containing the seasonal weather
                      forecast data
        folder_path = path to the folder where the file will be downloaded
        file_name_end = end of the name the downloaded file
    """
    
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