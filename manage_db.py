# -*- coding: utf-8 -*-

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from pathlib import Path
import json
from datetime import datetime
import sys,os
import time 
import re
from geopy.geocoders import GoogleV3
import requests
from urllib.request import urlopen
from unidecode import unidecode


def compareScrapTripad(scrapFile, tripadFile):
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

def sumScrapFiles(file1, file2):
    scrap1 = json.load(open(file1, encoding='utf-8'))
    scrap2 = json.load(open(file2, encoding='utf-8'))
    
    if len(scrap1) > len(scrap2):
        for i,restaurant1  in enumerate(scrap1):
            print((i+1)*100/len(scrap1),"%")
            restaurant1 = scrap1[str(i)] 
            geolocator = GoogleV3(
                api_key='AIzaSyAIIK4P68Ge26Yc0HkQ6uChj_NEqF2VeCU',
                user_agent='lookinmeal'
            )
            location = geolocator.geocode(restaurant1["address"])
            restaurant1["latitude"] = location.latitude
            restaurant1["longitude"] = location.longitude 
            latitude1 = restaurant1["latitude"]
            longitude1 = restaurant1["longitude"]
            done = False
            for j,restaurant2 in enumerate(scrap2):
                restaurant2 = scrap2[str(j)] 
                geolocator = GoogleV3(
                    api_key='AIzaSyAIIK4P68Ge26Yc0HkQ6uChj_NEqF2VeCU',
                    user_agent='lookinmeal'
                )
                location = geolocator.geocode(restaurant2["address"])
                restaurant2["latitude"] = location.latitude
                restaurant2["longitude"] = location.longitude
                latitude2 = restaurant2["latitude"]
                longitude2 = restaurant2["longitude"]
                if restaurant1["url"] == restaurant2["url"]:
                    del scrap2[str(j)]
                    scrap2 = reordenateDic(scrap2)
                    break
                else:
                    if format(latitude1, '.3f') == format(latitude2, '.3f') and format(longitude1, '.3f') == format(longitude2, '.3f'):
                        if len(restaurant1["name"].split()) <= len(restaurant2['name'].split()):
                            for word in clean(restaurant1["name"]):
                                if word in clean(restaurant2['name']):
                                    scrap1[str(i)]["url2"] = restaurant2["url"]
                                    del scrap2[str(j)]
                                    done = True
                                    scrap2 = reordenateDic(scrap2)
                                    break
                        else:
                            for word in clean(restaurant2['name']):
                                if word in clean(restaurant1["name"]):
                                    scrap1[str(i)]["url2"] = restaurant2["url"]
                                    del scrap2[str(j)]
                                    done = True
                                    scrap2 = reordenateDic(scrap2)
                                    break
                        if done: break
        final = concatenateDics(scrap1,scrap2)
    else:
        for i,restaurant2 in enumerate(scrap2):
            print((i+1)*100/len(scrap2),"%")
            restaurant2 = scrap2[str(i)] 
            geolocator = GoogleV3(
                api_key='AIzaSyAIIK4P68Ge26Yc0HkQ6uChj_NEqF2VeCU',
                user_agent='lookinmeal'
            )
            location = geolocator.geocode(restaurant2["address"])
            restaurant2["latitude"] = location.latitude
            restaurant2["longitude"] = location.longitude
            latitude2 = restaurant2["latitude"]
            longitude2 = restaurant2["longitude"]
            done = False
            for j,restaurant1 in enumerate(scrap1):
                restaurant1 = scrap2[str(j)] 
                geolocator = GoogleV3(
                    api_key='AIzaSyAIIK4P68Ge26Yc0HkQ6uChj_NEqF2VeCU',
                    user_agent='lookinmeal'
                )
                location = geolocator.geocode(restaurant1["address"])
                restaurant1["latitude"] = location.latitude
                restaurant1["longitude"] = location.longitude
                latitude1 = restaurant1["latitude"]
                longitude1 = restaurant1["longitude"]
                if restaurant1["url"] == restaurant2["url"]:
                    del scrap1[str(j)]
                    scrap1 = reordenateDic(scrap1)
                    break
                else:
                    if format(latitude1, '.3f') == format(latitude2, '.3f') and format(longitude1, '.3f') == format(longitude2, '.3f'):
                        if len(restaurant1["name"].split()) <= len(restaurant2['name'].split()):
                            for word in clean(restaurant1["name"]):
                                if word in clean(restaurant2['name']):
                                    scrap2[str(i)]["url2"] = restaurant1["url"]
                                    del scrap1[str(j)]
                                    done = True
                                    scrap1 = reordenateDic(scrap1)
                                    break
                        else:
                            for word in clean(restaurant2['name']):
                                if word in clean(restaurant1["name"]):
                                    scrap2[str(i)]["url2"] = restaurant1["url"]
                                    del scrap1[str(j)]
                                    done = True
                                    scrap1 = reordenateDic(scrap1)
                                    break
                        if done: break
        final = concatenateDics(scrap2,scrap1)
    with open('SCRAP_SCRAP.json', 'w') as fp:
        json.dump(final, fp) 


def concatenateDics(dic1, dic2):
    nextIndex = len(dic1)
    for element in dic2:
        dic1[str(nextIndex)] = element
        nextIndex += 1
    return dic1

def reordenateDic(dic):
    final={}
    for i,element in enumerate(dic):
        final[str(i)] = element
    return final

def clean(text):
    stop_words_es = ['a', 'al', 'con','de', 'del', 'e', 'el', 'en', 'la', 'las', 'lo', 'los', 'y']
    stop_words_en = ['a', 'an', 'and', 'the', 'of']
    aux = text.split()
    result = []
    for word in aux:
        if word.lower() not in stop_words_en and word.lower() not in stop_words_es:
            clean = re.sub(r'\W+', '', word).strip()
            if clean != "":
                result.append(unidecode(clean))
    return result

        

def main(): 
  #compareScrapTripad(sys.argv[1],sys.argv[2])
  sumScrapFiles(sys.argv[1],sys.argv[2])
main()