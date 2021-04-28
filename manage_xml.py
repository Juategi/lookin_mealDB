# -*- coding: utf-8 -*-

import sys,os
import json
import http
import re
import requests
import unidecode
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import xml.etree.ElementTree as ET

def xmlJson(filename):
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
    #element["score"] = score
    menu.append(element)
  return menu

def isCloseX(sections, entry, sectionSelected):
  distance = abs(int(sectionSelected["coordinates"][0]) - int(entry["coordinates"][0]))
  total = 0
  X_threshold = 20
  for section in sections:
    total += abs(int(entry["coordinates"][0]) - int(section["coordinates"][0]))
  avg = total/len(sections)
  if distance <= avg + X_threshold:
    return True
  else:
    return False

def menuFromXml(filename):
  menu = xmlJson(filename)
  sections = [element for element in menu if element["category"] == "category"]
  entries = [element for element in menu if element["category"] == "name"]
  prices = [element for element in menu if element["category"] == "price"]
  PRICE_Y_threshold = 50
  PRICE_X_threshold = 15
  for entry in entries:
    closest = None
    validSections = []
    if len(sections) == 1:
      entry["section"] = sections[0]["name"]
    else:
      for section in sections:
        if int(section["coordinates"][3]) < int(entry["coordinates"][1]):
          validSections.append(section)
      for section in validSections:
        if closest == None:
            closest = section
        if int(section["coordinates"][1]) > int(closest["coordinates"][1]) and isCloseX(validSections,entry,section): 
            closest = section
      if closest == None:
        closest = sections[0]
      entry["section"] = closest["name"]
   
    if len(prices) == 0:
      entry["price"] = 0.0
    else:
      closestPrice = None
      aux = []
      for price in prices:
        if int(price["coordinates"][0]) > int(entry["coordinates"][2]) and abs((int(price["coordinates"][3]) + int(price["coordinates"][1]))/2 - (int(entry["coordinates"][3]) + int(entry["coordinates"][1]))/2) < PRICE_Y_threshold:
          if closestPrice == None:
            closestPrice = price
          elif int(price["coordinates"][0]) < (int(closestPrice["coordinates"][0])+PRICE_X_threshold) and int(price["coordinates"][0]) - int(closestPrice["coordinates"][0]) < (abs(int(closestPrice["coordinates"][0])-int(closestPrice["coordinates"][2]))) and abs((int(price["coordinates"][3]) + int(price["coordinates"][1]))/2 - (int(entry["coordinates"][3]) + int(entry["coordinates"][1]))/2) < abs((int(closestPrice["coordinates"][3]) + int(closestPrice["coordinates"][1]))/2 - (int(entry["coordinates"][3]) + int(entry["coordinates"][1]))/2):
            closestPrice = price
      if closestPrice == None:
        entry["price"] = "0"
      else:
        entry["price"] = closestPrice["name"]
  final = {}
  for section in sections:
    final[section["name"]] = []
  for entry in entries:
    price = re.findall("\d+\,\d+", entry["price"])
    if price == []:
      price = re.findall("\d+\.\d+", entry["price"])
    if price == []:
      price = re.findall("\d+", entry["price"])
    if price == []:
      price.append(0.0)
    final[entry["section"]].append({
      "name" : entry["name"],
      "price" : price[0],
    })
  #print(final)
  #with open(filename[:-4] + '.json', 'w') as fp:
    #json.dump(final, fp) 
  return final


