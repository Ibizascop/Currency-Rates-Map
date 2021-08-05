# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 15:49:52 2021

@author: ibiza
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import json


def get_currencies() :
    req =requests.get("https://www.sport-histoire.fr/en/Geography/Currencies_countries_of_the_world.php")
    page = BeautifulSoup(req.content,'html.parser')
    table = page.find("table",{"class":"tableau_gris_centrer"})
    
    Country = []
    Currency = []
    Code = []
    table.findAll("tr")[1].findAll("td")
    for pays in tqdm(table.findAll("tr")[1:]) :
        if len(pays) > 1:
            Country.append(pays.findAll("td")[0].get_text())
            Currency.append(pays.findAll("td")[1].get_text())
            Code.append(pays.findAll("td")[2].get_text())
    Currency = [currency.title() for currency in Currency]
    
    dic = {"Country":Country,"Currency":Currency,"Code":Code,"EUR Exchange Rate":0}    
    data = pd.DataFrame(dic)
    
    return(data)

data = get_currencies()

def get_rates(data) :
    req =requests.get("https://www.fx-exchange.com/currency-exchange-rates-list.html")
    page = BeautifulSoup(req.content,'html.parser')
    all_tables = page.findAll("table",{"class":"tables"})
    
    for table in all_tables :
        region_table =  table.findAll("tr")[1:]
        for country in region_table :
            currency = country.findAll("td")[0].a.get_text().title()
            rate = country.findAll("td")[2].get_text()
            if currency in list(data["Currency"]): 
                data['EUR Exchange Rate'][data["Currency"]==currency] = float(rate)
    return(data)

data = get_currencies(data)
data.to_excel("EUR Exchange Rate.xlsx")

#def add_features(geojson,csv) :
with open('all_countries.json','r') as file :
    countries_geojson = json.load(file)

data = pd.read_csv("Rates.csv")

for dic in countries_geojson["features"] :
    if dic["properties"]["admin"] in list(data["Country"]) :
       dic["properties"]["Rate"] = data['Rate'][data["Country"]==dic["properties"]["admin"]].item()
       dic["properties"]["Currency"] = data['Currency'][data["Country"]==dic["properties"]["admin"]].item()
    else :
       dic["properties"]["Rate"] = 0
       dic["properties"]["Currency"] = 0


                 
with open('countries_rates.geojson', 'w') as f:
   json.dump(countries_geojson, f)      