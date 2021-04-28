# -*- coding: utf-8 -*-
# Consultar que el restaurante no tenga ya carta, subir por pagina
import sys,os
import re
import time
import json
import zipfile
import requests
import pathlib
from os import listdir
from os.path import isfile, join
import manage_xml

path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
ip = "http://37.133.134.99:4000"

def unzip():
  with zipfile.ZipFile(str(path) +"\\nanonets" + "\\carta.zip", 'r') as zip_ref:
    zip_ref.extractall(str(path) +"\\nanonets")
  os.remove(str(path) +"\\nanonets" + "\\carta.zip")

def load():
  #unzip()
  #print(os.listdir(pathZip))
  pathZip = str(path) +"\\nanonets" +  "\\" + os.listdir(str(path) +"\\nanonets")[0] + "\\"
  onlyfiles = [f for f in listdir(pathZip) if isfile(join(pathZip, f))]
  ids = []
  add = []
  for f in onlyfiles:
    restaurant_id = f.split("-")[0]
    if restaurant_id not in ids:
      ids.append(restaurant_id)
      response = requests.request("GET", ip + "/restbyid", headers = {"ids" : "{" + restaurant_id + "}", "latitude" : "0", "longitude" : "0"})
      json_data = json.loads(response.text)
      if json_data[0]["sections"] is None or len(json_data[0]["sections"]) == 0:
        add.append(restaurant_id)

  for id in add:
    pages = []
    final = {}
    for f in [f for f in onlyfiles if f.split("-")[0] == id]:
      f = pathZip + f
      pages.append(manage_xml.menuFromXml(f))
    for page in pages:
      final = {**final, **page}
    uploadMenu(final, id)
  os.remove(str(path) +"\\nanonets" +  "\\" + os.listdir(str(path) +"\\nanonets")[0])
  
def uploadMenu(data, restaurant_id):
  sections = []
  finalMenu = []
  i = 0
  for section, entries in data.items():
      sections.append(section[0:149])
      for element in entries:
          priceA = re.findall("\d+\,\d+", element["price"])
          if priceA == []:
              priceA = re.findall("\d+\.\d+", element["price"])
              if priceA == []:
                  priceA = re.findall("\d+", element["price"])
                  if priceA == []:
                      price = 0.0
                  else:
                      price = priceA[0]
              else:
                  price = priceA[0]
          else:
              price = priceA[0]
          entry = {
              "restaurant_id": str(restaurant_id), 
              "name" : element["name"][0:149],
              "section" : section[0:149],
              "price" : str(price).replace(",", "."),
              "image" : "",
              "pos" : str(i),
              "description" : "",
              "allergens" : str({})
          }
          i += 1
          finalMenu.append(entry)

  response = requests.request("PUT", ip + "/sections", data =  {
      "restaurant_id": restaurant_id, 
      "sections":str(sections).replace("[", "").replace("]", "")
  })
  print(response.text)
  for entry in finalMenu:
      response = requests.request("POST", ip + "/menus", data = entry)
      print(response.text)

def main(): 
  load()
main()



