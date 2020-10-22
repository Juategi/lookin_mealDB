# -*- coding: utf-8 -*-

#\copy place TO 'placesdata.csv' CSV;
#\copy place FROM '/home/apptodotrofeo/app/geoguayAPI/placesdata.csv' DELIMITER ',' csv header encoding 'windows-1251';
#Usage: arg1: Filename arg2: Categories. Example: '{Cat1,Cat2,Cat3}'

import sys,os
import json
import http
import requests
import unidecode

def nanonets(filename):
  url = 'https://app.nanonets.com/api/v2/OCR/Model/92368006-2d25-4b9e-a188-17c5b837b0a2/LabelUrls/'

  headers = {
      'accept': 'application/x-www-form-urlencoded'
  }

  data = {'urls' : [filename]}

  response = requests.request('POST', url, headers=headers, auth=requests.auth.HTTPBasicAuth('1Np9aBp8m9j8WCnN6reOjZTpaRD96eF-', ''), data=data)
  
  result = json.loads(response.text)
  img = result["result"][0]["input"]
  menu = result["result"][0]["prediction"]
  print(menu)
  print(img)
                
            
    
def main(): 
  nanonets(sys.argv[1])
main()
