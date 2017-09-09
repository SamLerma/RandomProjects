# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 23:54:10 2017

@author: Sam

just a quick test to make sure I remember how to 
query an API. Ars Technica headlines are used as an example
"""

import urllib
import requests

main_api = 'https://newsapi.org/v1/articles?source=ars-technica&sortBy=latest&apiKey=fd206b4eab1e470d954fea3afb6c9eb3'


url = main_api

json_data = requests.get(url).json()

print(json_data)