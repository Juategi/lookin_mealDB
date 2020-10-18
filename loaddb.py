# -*- coding: utf-8 -*-

#\copy place TO 'placesdata.csv' CSV;
#\copy place FROM '/home/apptodotrofeo/app/geoguayAPI/placesdata.csv' DELIMITER ',' csv header encoding 'windows-1251';
#Usage: arg1: Filename arg2: Categories. Example: '{Cat1,Cat2,Cat3}'

import sys,os
import json
import http
import requests
import unidecode

def load_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        for i, val in enumerate(data):
            name = data[str(i)]['name']
            
            
    
def main(): 
  load_json(sys.argv[1])
main()
