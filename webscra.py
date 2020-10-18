# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep 
from pathlib import Path
import json
import sys,os
import time 
from geopy.geocoders import GoogleV3

def scrap_web(address):
  print("Buscando ", address)
  tripad = json.load(open('valencia_tripad.json', encoding='utf-8'))
  
  driver = webdriver.Firefox(executable_path=r'C:\D\lookin_mealDB\geckodriver.exe') 
  driver.get("https://www.just-eat.es/")
  final = {}
  i = 0
  errors = {}
  #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Form_c-search-input_3ySg3 Form_is-notEmpty_WFw9O")))
  WebDriverWait(driver, 5)
  input_name = driver.find_element_by_css_selector("input[type='text']")
  input_name.send_keys(address)
  time.sleep(2)
  button = driver.find_element_by_css_selector("button[type='submit']")
  button.click()
  time.sleep(1)
  results1 = driver.find_element_by_css_selector("div[data-test-id='searchresults']").find_element_by_class_name("c-listing ").find_element_by_class_name("c-listing-loader").find_elements_by_tag_name("section")
  results2 = driver.find_element_by_css_selector("div[data-test-id='searchresults']").find_element_by_css_selector("div[class='c-listing c-listing--subsequent ']").find_element_by_class_name("c-listing-loader").find_elements_by_tag_name("section")
  results3 = driver.find_element_by_css_selector("div[data-test-id='searchresults']").find_element_by_css_selector("div[class='c-listing c-listing--inactive ']").find_element_by_class_name("c-listing-loader").find_elements_by_tag_name("section")
  results = results1 + results2 + results3

  for result in results:
    if "McDonald" in result.find_element_by_css_selector("a[class='c-listing-item-link u-clearfix']").get_attribute("title") or "Burguer King" in result.find_element_by_css_selector("a[class='c-listing-item-link u-clearfix']").get_attribute("title"):
      continue
    result.find_element_by_css_selector("a[class='c-listing-item-link u-clearfix']").send_keys(Keys.CONTROL + Keys.RETURN)
    sleep(1)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    driver.switch_to.window(driver.window_handles[1])
    
    sleep(3)
    try:
      name = driver.find_element_by_css_selector("h1[class='infoTextBlock-item-title']").text
    except:
      continue
    print(name)
    link = driver.current_url
    address = driver.find_element_by_css_selector("p[class='restInfoAddress']").text
    types = driver.find_element_by_css_selector("p[class='infoTextBlock-item-text']").text.split(",")
    image = driver.find_element_by_tag_name("picture").find_element_by_css_selector("img[class='c-pageBanner-img']").get_attribute("src")
    sections = driver.find_element_by_css_selector("div[class='menuCard-wrapper']").find_elements_by_tag_name("section")

    menu = {}
    for section in sections :
      menu[section.get_attribute("data-test-id")] = []
      for element in section.find_element_by_css_selector("div[class='accordion-content']").find_elements_by_tag_name("div") : #coge todos los div
        entry = {}
        aux = element.text.split("\n")
        if len(aux) < 2:
          continue
        entry["name"] = aux[0]
        if len(aux) == 4:
          entry["price"] = aux[2][:-2]
          entry["description"] = aux[1]
        else:
          entry["price"] = aux[1][:-2]
          entry["description"] = ""
        #entry["name"] = element.find_element_by_tag_name("h4").text
        #entry["price"] = element.find_element_by_css_selector("div[class='product-price u-noWrap']").text[:-2]
        #try:
          #entry["description"] = element.find_element_by_css_selector("div[class='product-description']").text
        #except:
          #entry["description"] = ""
        menu[section.get_attribute("data-test-id")].append(entry)
    #print(menu)

    geolocator = GoogleV3(
              api_key='AIzaSyAIIK4P68Ge26Yc0HkQ6uChj_NEqF2VeCU',
              user_agent='lookinmeal'
          )
    location = geolocator.geocode(address)
    tid = ""
    for i,val in enumerate(tripad):
      if "latitude" in tripad[i] and format(float(tripad[i]['latitude']), '.3f') == format(location.latitude, '.3f') and format(float(tripad[i]['longitude']), '.3f') == format(location.longitude, '.3f'):
        if len(name) <= len(tripad[i]['name']):
          for word in name.split():
            if word in tripad[i]['name'].split():
              tid = tripad[i]['id']
        else:
          for word in tripad[i]['name'].split():
            if word in name.split():
              tid = tripad[i]['id']   
    data = {}
    data["url"] = link
    data["menu"] = menu
    if tid == "":
      data["name"] = name
      data["types"] = types
      data["image"] = image
      data["address"] = address
      data["latitude"] = location.latitude
      data["longitude"] = location.longitude
    else:
      data["id"] = tid
    final[i] = data
    i += 1
    driver.close()
    driver.switch_to.window(driver.window_handles[0]) 

  with open('valencia.json', 'w') as fp:
    json.dump(final, fp) 
  driver.close()


def main(): 
  scrap_web(sys.argv[1])
main()
