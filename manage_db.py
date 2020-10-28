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
    else:
        for cuisine in restaurant["cuisine"]:
            if cuisine.strip() in acceptedTypes:
                types.append(cuisine)
        id = restaurant['id']
        name = restaurant['name']
        try:
            phone = restaurant['phone']
        except:
            phone = ""
        address = restaurant['address']
        try:
            email = restaurant['email']
        except:
            email = ""
        country = restaurant['address'].split(" ")[-1]
        city = restaurant['address'].split(" ")[-2]
        latitude = restaurant['latitude']
        longitude = restaurant['longitude']
        try:
            website = restaurant['website']
        except:
            website = ""
        webUrl = restaurant['webUrl']
        images = restaurant['image']
        menu = restaurant['menu']
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

        {"1":[13,16,20,23],"2":[13,16,20,23],"3":[13,16,20,23],"4":[13,16,20,23],"5":[13,16,20,23],"6":[13,16,20,23],"0":[13,16]}
    
def main(): 
  uploadJson(sys.argv[1])
main()