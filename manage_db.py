# -*- coding: utf-8 -*-
import sys,os
import re
import json
import requests

acceptedTypes = [ "Café",  "African",  "American",  "Argentinean",  "Asian",  "Bar",  "Barbeque",  "Bistro",  "Brazilian",  "British",  "Canadian",  "Chinese",  "Colombian",  "Contemporary", "Dessert",  "English",  "French",  "Fusion",  "German",  "Greek",  "Grill",  "Hamburgers",  "Hawaiian",  "Healthy",  "Indian",  "Indonesian",  "Italian",  "Korean",  "Lebanese",  "Mediterranean",  "Mexican",  "Organic",  "Pizza",  "Pub", "Seafood",  "Street Food",  "Sushi",  "Tapas",  "Thai",  "Turkish",  "Vegan Options",  "Vegetarian Friendly",  "Wine Bar"]
    
uberTypes = [{'Hamburguesas':"Hamburgers"}, {'Estadounidense':"Hamburgers"}, {'Italiana':'Italian'}, {'Pizza ':'Pizza'}, {'Pasta ':'Italian'}, {'Gourmet':''}, {'Alcohol':'Bar'}, {'Postres':'Dessert'}, {'Saludable':'Healthy'}, {'Hawaiana':'Hawaiian'}, {'Pollo ':'American'},, {'Ensaladas ':'Healthy'}, {'Sushi':'Sushi'}, {'Japonesa':'Sushi'}, {'Asiática':'Asian'}, {'Cocina vegana':'Vegan Options'},{'Cocina vegetariana':'Vegetarian Friendly'}, {'Mediterránea':'Mediterranean'}, {'Alitas de pollo ':'American'},{'Turca':'Turkish'}, {'Tailandesa':'Thai'}, {'Comida callejera':'Street Food'}, {'Café':'Café'}, {'Café y té':'Café'}, {'Zumos y batidos':'Café'},{'China':'Chinese'}, {'Fusión asiática':'Fusion'}, {'Noodles':'Asian'}, {'India':'Indian'}, {'Barbacoa japonesa':'Barbeque'}, {'Brochetas de pollo al estilo japonés':'Barbeque'}, {'Aus Burger':'Hamburgers'}, {'Mexicana':'Mexican'}, {'Tex Mex':'Mexican'}, {'De Nuevo México':'Mexican'}, {'Estadounidense tradicional':'American'}, {'Vegana':'Vegan Options'}, {'Vegetariana':'Vegetarian Friendly'}, {'Latinoamericana':'Colombian'}, {'Fusión latina':'Colombian'}, {'Argentina':'Argentinean'}, {'Española':'Mediterranean'}, {'Boles de arroz':'Asian'}, {'Tapas y raciones':'Mediterranean'}, {'Venezolana':'Colombian'}, {'Mariscos':'Seafood'}, {'Helado y yogur helado':'Dessert'}, {'Desayuno y brunch':'Dessert'}, {'Cafetería':'Café'}, {'Pasteles':'Dessert'}, {'Brasileña':'Grill'}, {'Helado y yogur helado':'Dessert'}, {'Yogur helado':'Dessert'}, {'Carnicería':'Grill'},  {'Sudamericana':'Colombian'}, {'Panadería':'Dessert'}, {'Barbacoa':'Barbeque'}, {'Francesa':'French'}, {'Curry indio':'indian'}, {'Dulces japoneses':'Dessert'}, {'Burgers':'Hamburgers'}, {'Drinks':'Bar'}, {'Vegetariano puro':'Vegetarian Friendly'}, {'Fish & chips':'Seafood'}, {'Café':'Café'}, {'Griega':'Greek'},  {'Ice Cream & Frozen Yogurt':'Dessert'}, {'Desserts':'Dessert'}, {'Wine':'Wine Bar'}, {'Licorerías':'Bar'}, {'Coreana':'Asian'}]

jeTypes = ['Pollo', ' Americana', 'Tailandesa', ' Medio Oriental', 'Americana Hamburguesas', 'Italiana', ' Pizza', 'Pollo Americana', 'Pizza', ' Italiana', 'Venezolana', ' Sudamericana', ' Mediterránea', 'Japonesa', ' Sushi', 'Hamburguesas', ' Tapas', 'China', ' Oriental', 'Americana', ' Hamburguesas', 'India', 'Kebab', 'Mexicana', ' Tex-Mex', 'Española', ' Gourmet', 'Brasería', 'Colombiana', ' Caribeña', 'Mediterránea', ' Japonesa', 'Tapas', 'Oriental', ' China', ' Española', 'Repostería', ' Fusión', ' Arroceria', ' Pollo', ' Paellas', 'Sandwiches', 'Heladería', ' Heladería', ' Casera', ' Repostería', 'Brasileña', 'Turca', ' Kebab', 'Bocadillos', 'Paellas', ' Vegetariana', ' Paquistaní', 'Vegetariana', ' Sana', 'Vegana', 'Sudamericana', 'Sushi', 'Desayuno', 'Vietnamita', ' Bocadillos', 'Poke', ' Halal', ' Turca']

def uploadJson(filename):
    data = json.load(open(filename, encoding='utf-8'))
    restaurant = data[str(3)]
    if "id" not in restaurant:


def cleanTypes(filename):
    data = json.load(open(filename, encoding='utf-8'))
    cuisines = []
    for i,restaurant in enumerate(data):
        restaurant = data[str(i)]
        for cuisine in restaurant["types"]:
            if cuisine not in cuisines:
                cuisines.append(cuisine)
    print(cuisines)
    
def main(): 
  #uploadJson(sys.argv[1])
  cleanTypes(sys.argv[1])
main()