# -*- coding: utf-8 -*-
import sys,os
import re
import json
import requests

acceptedTypes = [ "Cafe",  "African",  "American",  "Argentinean",  "Asian",  "Bar",  "Barbeque",  "Bistro",  "Brazilian",  "British",  "Canadian",  "Chinese",  "South American",  "Contemporary", "Dessert",  "English",  "French",  "Fusion",  "German", "Gourmet",  "Greek",  "Grill",  "Hamburgers",  "Hawaiian",  "Healthy",  "Indian",  "Indonesian",  "Italian",  "Korean",  "Lebanese",  "Mediterranean",  "Mexican",  "Organic",  "Pizza",  "Pub", "Seafood",  "Street Food",  "Sushi",  "Tapas",  "Thai",  "Turkish",  "Vegan Options",  "Vegetarian Friendly",  "Wine Bar"]

 
otherTypes = {'Hamburguesas':"Hamburgers", 'Estadounidense':"Hamburgers", 'Italiana':'Italian', 'Pizza ':'Pizza', 'Pasta ':'Italian', 'Gourmet':'Gourmet', 'Alcohol':'Bar', 'Postres':'Dessert', 'Saludable':'Healthy', 'Hawaiana':'Hawaiian', 'Pollo ':'American', 'Ensaladas ':'Healthy', 'Sushi':'Sushi', 'Japonesa':'Sushi', 'Asiática':'Asian', 'Cocina vegana':'Vegan Options','Cocina vegetariana':'Vegetarian Friendly', 'Mediterránea':'Mediterranean', 'Alitas de pollo ':'American','Turca':'Turkish', 'Tailandesa':'Thai', 'Comida callejera':'Street Food', 'Cafe':'Cafe', 'Cafe y té':'Cafe', 'Zumos y batidos':'Cafe','China':'Chinese', 'Fusión asiática':'Fusion', 'Noodles':'Asian', 'India':'Indian', 'Barbacoa japonesa':'Barbeque', 'Brochetas de pollo al estilo japonés':'Barbeque', 'Aus Burger':'Hamburgers', 'Mexicana':'Mexican', 'Tex Mex':'Mexican', 'De Nuevo México':'Mexican', 'Estadounidense tradicional':'American', 'Vegana':'Vegan Options', 'Vegetariana':'Vegetarian Friendly', 'Latinoamericana':'South American', 'Fusión latina':'South American', 'Argentina':'Argentinean', 'Española':'Mediterranean', 'Boles de arroz':'Asian', 'Tapas y raciones':'Mediterranean', 'Venezolana':'South American', 'Mariscos':'Seafood', 'Helado y yogur helado':'Dessert', 'Desayuno y brunch':'Dessert', 'Cafetería':'Cafe', 'Pasteles':'Dessert', 'Brasileña':'Grill', 'Helado y yogur helado':'Dessert', 'Yogur helado':'Dessert', 'Carnicería':'Grill', 'Sudamericana':'South American', 'Panadería':'Dessert', 'Barbacoa':'Barbeque', 'Francesa':'French', 'Curry indio':'indian', 'Dulces japoneses':'Dessert', 'Burgers':'Hamburgers', 'Drinks':'Bar', 'Vegetariano puro':'Vegetarian Friendly', 'Fish & chips':'Seafood', 'Cafe':'Cafe', 'Griega':'Greek', 'Ice Cream & Frozen Yogurt':'Dessert', 'Desserts':'Dessert', 'Wine':'Wine Bar', 'Licorerías':'Bar', "Coreana":"Korean",'Pollo':'American', 'Americana':'American', 'Tailandesa':'Thai', 'Medio Oriental':'Asian', 'Americana Hamburguesas':'Hamburgers', 'Italiana':'Italian', 'Pizza':'Pizza', 'Pollo Americana':'American', 'Venezolana':'South American', 'Sudamericana':'South American', 'Mediterránea':'Mediterranean', 'Japonesa':'Sushi', 'Sushi':'Sushi', 'Hamburguesas':'Hamburgers', 'Tapas':'Mediterranean', 'China':'Chinese', 'Oriental':'Asian', 'India':'Indian', 'Kebab':'Turkish', 'Mexicana':'Mexican', 'Tex-Mex':'Mexican', 'Española':'Mediterranean', 'Gourmet':'Gourmet', 'Brasería':'Grill', 'Colombiana':'South American', 'Repostería':'Dessert', 'Fusión':'Fusion', 'Arroceria':'Mediterranean', 'Paellas':'Mediterranean', 'Heladería':'Dessert', 'Repostería':'Dessert', 'Brasileña':'Grill', 'Turca':'Turkish', 'Vegetariana':'Vegetarian Friendly', 'Sana':'Healthy', 'Vegana':'Vegan Options', 'Desayuno':'Dessert', 'Poke':'Hawaiian',"Coreana":"Korean"}

def uploadJson(filename):
    data = json.load(open(filename, encoding='utf-8'))
    restaurant = data[str(158)]
    types = []
    if "id" not in restaurant:
        for cuisine in restaurant["cuisine"]:
            if cuisine.strip() in otherTypes:
                types.append(otherTypes[cuisine.strip()])
        taid = ""
        phone = ""
        email = ""
        website = ""
        webUrl = ""
        country = ""
        city = ""
        final = {}
        address = restaurant['address']
    else:
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
        print(final)
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
        "name": name,
        "phone": phone,
        "website": website,
        "webUrl": webUrl,
        "address": address,
        "email": email,
        "city": city.strip().toUpperCase(),
        "country": country.strip(),
        "latitude": latitude,
        "longitude": longitude,
        "rating": 0.0,
        "numrevta": 0,
        "images": str(image).replace("[", "{").replace("]", "}")
        "types": str(types).replace("[", "{").replace("]", "}"),
        "schedule": json.encode(schedule)
        "delivery": str(delivery).replace("[", "{").replace("]", "}")
	}
    
def main(): 
  uploadJson(sys.argv[1])
main()