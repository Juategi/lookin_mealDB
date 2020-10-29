# -*- coding: utf-8 -*-
import sys,os
import re
import json
import requests


ip = "http://37.133.2.195:4000"


acceptedTypes = [ "Cafe",  "African",  "American",  "Argentinean",  "Asian",  "Bar",  "Barbeque",  "Bistro",  "Brazilian",  "British",  "Canadian",  "Chinese",  "South American",  "Contemporary", "Dessert",  "English",  "French",  "Fusion",  "German", "Gourmet",  "Greek",  "Grill",  "Hamburgers",  "Hawaiian",  "Healthy",  "Indian",  "Indonesian",  "Italian",  "Korean",  "Lebanese",  "Mediterranean",  "Mexican",  "Organic",  "Pizza",  "Pub", "Seafood",  "Street Food",  "Sushi",  "Tapas",  "Thai",  "Turkish",  "Vegan Options",  "Vegetarian Friendly",  "Wine Bar"]

 
otherTypes = {'Hamburguesas':"Hamburgers", 'Estadounidense':"Hamburgers", 'Italiana':'Italian', 'Pizza ':'Pizza', 'Pasta ':'Italian', 'Gourmet':'Gourmet', 'Alcohol':'Bar', 'Postres':'Dessert', 'Saludable':'Healthy', 'Hawaiana':'Hawaiian', 'Pollo ':'American', 'Ensaladas ':'Healthy', 'Sushi':'Sushi', 'Japonesa':'Sushi', 'Asiática':'Asian', 'Cocina vegana':'Vegan Options','Cocina vegetariana':'Vegetarian Friendly', 'Mediterránea':'Mediterranean', 'Alitas de pollo ':'American','Turca':'Turkish', 'Tailandesa':'Thai', 'Comida callejera':'Street Food', 'Cafe':'Cafe', 'Cafe y té':'Cafe', 'Zumos y batidos':'Cafe','China':'Chinese', 'Fusión asiática':'Fusion', 'Noodles':'Asian', 'India':'Indian', 'Barbacoa japonesa':'Barbeque', 'Brochetas de pollo al estilo japonés':'Barbeque', 'Aus Burger':'Hamburgers', 'Mexicana':'Mexican', 'Tex Mex':'Mexican', 'De Nuevo México':'Mexican', 'Estadounidense tradicional':'American', 'Vegana':'Vegan Options', 'Vegetariana':'Vegetarian Friendly', 'Latinoamericana':'South American', 'Fusión latina':'South American', 'Argentina':'Argentinean', 'Española':'Mediterranean', 'Boles de arroz':'Asian', 'Tapas y raciones':'Mediterranean', 'Venezolana':'South American', 'Mariscos':'Seafood', 'Helado y yogur helado':'Dessert', 'Desayuno y brunch':'Dessert', 'Cafetería':'Cafe', 'Pasteles':'Dessert', 'Brasileña':'Grill', 'Helado y yogur helado':'Dessert', 'Yogur helado':'Dessert', 'Carnicería':'Grill', 'Sudamericana':'South American', 'Panadería':'Dessert', 'Barbacoa':'Barbeque', 'Francesa':'French', 'Curry indio':'indian', 'Dulces japoneses':'Dessert', 'Burgers':'Hamburgers', 'Drinks':'Bar', 'Vegetariano puro':'Vegetarian Friendly', 'Fish & chips':'Seafood', 'Cafe':'Cafe', 'Griega':'Greek', 'Ice Cream & Frozen Yogurt':'Dessert', 'Desserts':'Dessert', 'Wine':'Wine Bar', 'Licorerías':'Bar', "Coreana":"Korean",'Pollo':'American', 'Americana':'American', 'Tailandesa':'Thai', 'Medio Oriental':'Asian', 'Americana Hamburguesas':'Hamburgers', 'Italiana':'Italian', 'Pizza':'Pizza', 'Pollo Americana':'American', 'Venezolana':'South American', 'Sudamericana':'South American', 'Mediterránea':'Mediterranean', 'Japonesa':'Sushi', 'Sushi':'Sushi', 'Hamburguesas':'Hamburgers', 'Tapas':'Mediterranean', 'China':'Chinese', 'Oriental':'Asian', 'India':'Indian', 'Kebab':'Turkish', 'Mexicana':'Mexican', 'Tex-Mex':'Mexican', 'Española':'Mediterranean', 'Gourmet':'Gourmet', 'Brasería':'Grill', 'Colombiana':'South American', 'Repostería':'Dessert', 'Fusión':'Fusion', 'Arroceria':'Mediterranean', 'Paellas':'Mediterranean', 'Heladería':'Dessert', 'Repostería':'Dessert', 'Brasileña':'Grill', 'Turca':'Turkish', 'Vegetariana':'Vegetarian Friendly', 'Sana':'Healthy', 'Vegana':'Vegan Options', 'Desayuno':'Dessert', 'Poke':'Hawaiian',"Coreana":"Korean"}

def uploadJson(filename):
    data = json.load(open(filename, encoding='utf-8'))
    ids = []
    for numb, restaurant in enumerate(data): 
        restaurant = data[str(numb)]
        types = []
        if "id" not in restaurant:
            for cuisine in restaurant["cuisine"]:
                if cuisine.strip() in otherTypes:
                    types.append(otherTypes[cuisine.strip()])
            taid = -1
            phone = ""
            email = ""
            website = ""
            webUrl = ""
            country = ""
            city = ""
            final = {}
            address = restaurant['address']
        elif restaurant['id'] not in ids:
            ids.append(restaurant['id'])
            for cuisine in restaurant["cuisine"]:
                if cuisine.strip() in acceptedTypes:
                    types.append(cuisine)
            taid = restaurant['id']
            try:
                phone = restaurant['phone']
            except:
                phone = ""
            try:
                email = restaurant['email']
            except:
                email = ""
            try:
                website = restaurant['website']
            except:
                website = ""
            webUrl = restaurant['webUrl']
            address = restaurant['address']
            country = restaurant['address'].split(" ")[-1]
            city = restaurant['address'].split(" ")[-2]
            schedule = restaurant['hours']
            final = {}
            for i,day in enumerate(schedule):
                final[str(i)] = []
                for hours in day:
                    formatedHour = int(hours["open"]/60)
                    if formatedHour >= 24:
                        formatedHour -= 24
                    final[str(i)].append(formatedHour)
                    formatedHour = int(hours["open"]/60)
                    if formatedHour >= 24:
                        formatedHour -= 24
                    final[str(i)].append(formatedHour)
        name = restaurant['name']
        images = restaurant['image']
        latitude = restaurant['latitude']
        longitude = restaurant['longitude']
        currency = "€"
        uber = ""
        justeat = ""
        menu = restaurant['menu']
        if "uber" in restaurant['scrap']:
            uber = restaurant['scrap']
        elif "just-eat" in restaurant['scrap']:
            justeat = restaurant['scrap']
        try:
            if "uber" in restaurant['scrap2']:
                uber = restaurant['scrap2']
            elif "just-eat" in restaurant['scrap2']:
                justeat = restaurant['scrap2']
        except:
            print("")
        delivery = ["",uber,justeat,""]
        body = {
            "taid": taid,
            "name": name[0:149],
            "phone": phone[0:49],
            "website": website[0:149],
            "webUrl": webUrl[0:299],
            "address": address[0:299],
            "email": email[0:49],
            "city": city.strip().upper()[0:49],
            "country": country.strip()[0:49],
            "latitude": latitude,
            "longitude": longitude,
            "rating": 0.0,
            "numrevta": 0,
            "images": str(images).replace("[", "{").replace("]", "}"),
            "types": str(types).replace("[", "{").replace("]", "}"),
            "schedule": str(final).replace("'", "\""),
            "delivery": str(delivery).replace("[", "{").replace("]", "}")
        }
        
        response = requests.request("POST",ip + "/restaurants", data = body)
        restaurant_id = json.loads(response.text)[0]["restaurant_id"]

        if "menu" in restaurant:
            sections = []
            finalMenu = []
            i = 0
            for section in menu:
                sections.append(section[0:149])
                for element in menu[section]:
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
                        "image" : element["image"],
                        "pos" : str(i),
                        "description" : element["description"][0:249],
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
                
        


def main(): 
  uploadJson(sys.argv[1])
main()