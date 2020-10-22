# -*- coding: utf-8 -*-

#\copy place TO 'placesdata.csv' CSV;
#\copy place FROM '/home/apptodotrofeo/app/geoguayAPI/placesdata.csv' DELIMITER ',' csv header encoding 'windows-1251';
#Usage: arg1: Filename arg2: Categories. Example: '{Cat1,Cat2,Cat3}'

import sys,os
import json
import http
import requests
import unidecode
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import xml.etree.ElementTree as ET

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
                

def xml_json(filename):
  parser = ET.XMLParser(encoding="utf-8")
  xml = ET.parse(filename, parser=parser).getroot()
  img = xml[0].text
  menu = []
  for child in xml[1:] :
    element = {}
    category = child[0].text
    name = child[2].text
    score = child[3].text
    coordinates = [child[1][0].text,child[1][1].text,child[1][2].text,child[1][3].text]
    element["name"] = name
    element["category"] = category
    element["coordinates"] = coordinates
    element["score"] = score
    menu.append(element)
  return menu

  

    
def main(): 
  #nanonets(sys.argv[1])
  xml_json(sys.argv[1])
main()

