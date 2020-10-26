# -*- coding: utf-8 -*-

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from time import sleep 
from pathlib import Path
import json
from datetime import datetime
import sys,os
import time 
import re
from geopy.geocoders import GoogleV3
import requests
from urllib.request import urlopen


def compare(scrapFile, tripadFile):
    scrap = json.load(open(scrapFile, encoding='utf-8'))
    tripad = json.load(open(tripadFile, encoding='utf-8'))
    
    final= {}
    for j,restaurant in enumerate(scrap):
        restaurant = scrap[str(j)]
        geolocator = GoogleV3(
                api_key='AIzaSyAIIK4P68Ge26Yc0HkQ6uChj_NEqF2VeCU',
                user_agent='lookinmeal'
            )
        location = geolocator.geocode(restaurant["address"])
        tid = None
        for i,val in enumerate(tripad):
            if "latitude" in tripad[i] and format(float(tripad[i]['latitude']), '.3f') == format(location.latitude, '.3f') and format(float(tripad[i]['longitude']), '.3f') == format(location.longitude, '.3f'):
                if len(restaurant["name"].split()) <= len(tripad[i]['name'].split()):
                    for word in clean(restaurant["name"]):
                        if word in clean(tripad[i]['name']):
                            tid = i
                else:
                    for word in clean(tripad[i]['name']):
                        if word in clean(restaurant["name"]):
                            tid = i
        data = {}
        if tid != None:
            data = tripad[tid]
            data["menu"] = restaurant["menu"]
            data["scrap"] = restaurant["url"]
            html = urlopen(data["webUrl"])
            soup = BeautifulSoup(html, 'html.parser')
            data["image"] = []
            for image in soup.find_all("img", {"class": "basicImg"}):
                img = image['data-lazyurl']
                data["image"].append(img)
        else:
            data = {}
            data["scrap"] = restaurant["url"]
            data["menu"] = restaurant["menu"]
            data["name"] = restaurant["name"]
            data["cuisine"] = restaurant["types"]
            data["image"] = [restaurant["image"]]
            data["address"] = restaurant["address"]
            data["latitude"] = location.latitude
            data["longitude"] = location.longitude
        final[j] = data
        print(data["name"])
        print((j+1)*100/len(scrap),"%")

    with open('SCRAP_TRPAD.json', 'w') as fp:
        json.dump(final, fp) 


def clean(text):
    stop_words_es = ['a', 'al', 'con','de', 'del', 'e', 'el', 'en', 'la', 'las', 'lo', 'los', 'y']
    stop_words_en = ['a', 'an', 'and', 'the', 'of']
    aux = text.split()
    result = []
    for word in aux:
        if word.lower() not in stop_words_en and word.lower() not in stop_words_es:
            clean = re.sub(r'\W+', '', word).strip()
            if clean != "":
                result.append(clean)
    return result

        

def main(): 
  compare(sys.argv[1],sys.argv[2])
  #print(clean("HLA PARA - EL ENE A AN PARA THE Y UUU"))
main()