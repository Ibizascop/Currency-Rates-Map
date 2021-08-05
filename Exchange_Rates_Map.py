# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 12:05:12 2021

@author: w.grasina
"""

import folium
import pandas as pd
import json
import sys

#Csv contenant les taux d'échange par rapport à l'EURO
rates = pd.read_csv("Rates.csv")
rates= rates.set_index('Country')['Rate']
#Geojson contenant les polygones des pays du monde
with open('countries_rates.geojson','r') as file :
       countries_geojson = json.load(file)
       
#Change reference currency based on a country name input
def change_currency(country,rates = rates) :
    for i,x in enumerate(list(rates.index)):
        if x == country :
            value =rates[i]
    new_rates = rates/value
    return new_rates, country

#Step-based color scale
def my_color_function(feature,rates):
    """Maps low values to green and hugh values to red."""
    try :
        if rates[feature['properties']["admin"]] < 0.1:
            return '#1a9850'
        elif rates[feature['properties']["admin"]] < 0.5:
            return '#66bd63'
        elif rates[feature['properties']["admin"]] < 1:
            return '#a6d96a'
        elif rates[feature['properties']["admin"]] == 1:
            return '#d9ef8b'
        elif rates[feature['properties']["admin"]] < 1.5:
            return '#fee08b'
        elif rates[feature['properties']["admin"]] < 2:
            return '#fdae61'
        elif rates[feature['properties']["admin"]] < 10:
            return '#f46d43'
        else :
            return '#d73027'
    except:
        return "#ffffff"

#Function to generate a map based on an input of one country
def get_map(country) :
    rates, country = change_currency(country)
    Map = folium.Map(location=[46.00,2.00],zoom_start = 3, 
                     control_scale = True)
    folium.GeoJson(
        countries_geojson,
        style_function=lambda feature: {
            'fillColor': my_color_function(feature,rates),
            'fillOpacity':0.7,
            'color' : 'black',
            'weight' : 1,
            'dashArray' : '5, 5'
            }
        ).add_to(Map)
    outfp = "Exchange_Rates_Map.html"
    Map.save(outfp)

get_map("Russia")

if __name__ == "__main__":
    # execute only if run as a script
    get_map(sys.argv[1])
    
#Test
#import branca

#colormap = branca.colormap.linear.YlOrRd_09.scale(0, 8500)
#colormap = colormap.to_step(index=[0, 1000, 3000, 5000, 8500])
#colormap.caption = 'Incidents of Crime in Victoria (year ending June 2018)'
#colormap.add_to(world_map)
