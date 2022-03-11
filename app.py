#from scrap import *

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import webbrowser

import re
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import urllib.request
import os

#Partie Scrappeur

class Crawler :

#Initialisation des différents paramètres du scrappeur
    
    def __init__(self, nom, lien, nbr_scroll):
        self.nom = nom
        self.lien = lien
        self.nbr_scroll = nbr_scroll
        self.chrome = None
        self.SCROLL_PAUSE_TIME = 2

#Initialisation du webdriver
        
    def initialisation(self) :
        CHROME_PATH = "./chromedriver"

        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        chrome = webdriver.Chrome(executable_path=CHROME_PATH,
                                  options=chrome_options
                                 )  
        chrome.get(self.lien)
        self.chrome = chrome

#Fonction permettant de scroller la page web
        
    def scroll(self, l_h):
        # Scroll down to bottom
        self.chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(self.SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = self.chrome.execute_script("return document.body.scrollHeight")
        return new_height

#Fonction permettant de récupérer les liens des images
    
    def scrapping(self) :

        tag_l = self.chrome.find_elements_by_tag_name('img')

        for i in tag_l:
            if i.get_attribute('src') != None :
                if  len(i.get_attribute('src')) > 100:
                    res = i.get_attribute('src')

        # Get scroll height
        last_height = self.chrome.execute_script("return document.body.scrollHeight")

        for i in range(self.nbr_scroll) :
    
            new_height = self.scroll(last_height)
    
            if new_height == last_height:
                try:
                    element = self.chrome.find_elements_by_class_name('mye4qd') #correspond au bouton "afficher plus"
                    element[0].click()
                except : 
                    break
                
            last_height = new_height   
    
        tag_l = self.chrome.find_element_by_class_name('islrc')
        tag_l = tag_l.find_elements_by_tag_name('img')
        res = []
        for i in tag_l :
            if i.get_attribute('src') != None :
                res.append(i.get_attribute('src'))

        res = list(set(res)) #on supprime les doublons
                
        return res

#Fonction permettant de télécharger les images sur la machine de l'utilisateur
            
    def upload(self, liste, root) :
        chemin = os.getcwd()
        os.chdir(root)
        try :
            os.makedirs(str(self.nom))
        except :
            os.makedirs(str(self.nom)+'_')
        for count, value in enumerate(liste) :
            n_fichier = str(self.nom) + '/' + str(self.nom) + str(count) + ".jpg"
            try :
                urllib.request.urlretrieve(value, n_fichier)
            except :
                None
        os.chdir(chemin)

def scrap(lien, rep, nom, nbr) :
    liens = lien.split(',')
    res = []
    for i in liens : #permet de récupérer les images à partir de plusieurs liens sans doublons
        crawler = Crawler(nom, 
                    i,
                    nbr)
        crawler.initialisation()
        res.append(crawler.scrapping())
    flat_res = [item for sublist in res for item in sublist]
    flat_res = list(set(flat_res))
    crawler.upload(flat_res, rep)    


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1(children="Appli de scrapping google images", style={"text-align": "center", "font-size":"350%","background-color": "#757473", "color":"#E7E6E3", "height":"75px"}),

        html.P(
            children="Rentrer les valeurs dans les zones de textes et appuyez sur submit pour lancer le téléchargement.",
            style={"text-align": "center", "font-size":"150%", "color":"#E7E6E3"}
        ),

        html.P(
            children="Afin d'obtenir le chemin du répertoire dans lequel enregistrer le dossier d'images, shift + clic droit sur le dossier -> copier en tant que chemin d'accès.",
            style={"text-align": "center", "font-size":"150%", "color":"#E7E6E3"}
        ),

        html.P(
            children="Tu peux rentrer plusieurs lien google image, il faut les séparer par une virgule !",
            style={"text-align": "center", "font-size":"150%", "color":"#E7E6E3"}
        ),

        html.Br(), #Retour à la ligne

        html.Div([
        dcc.Input(id="input1",
            type="text",
            placeholder="lien de la page google image",
            style={'marginRight':'40px', "box-sizing": "border-box", "height":"75px", "width":"45%","background-color": "#DAD9D6", "border": "None"}
            ),
        
        dcc.Input(id="input2",
            type="text",
            placeholder="lien du dossier où enregistrer la base de données",
            style={'marginRight':'40px', "box-sizing": "border-box", "height":"75px", "width":"45%", "background-color": "#DAD9D6","border": "None"}
            ),], style={"text-align":"center"}),
        
        html.Br(),
        html.Br(),

        html.Div([
        dcc.Input(id="input3",
            type="text",
            placeholder="nom du dossier",
            style={'marginRight':'40px', "box-sizing": "border-box", "height":"75px", "width":"45%", "background-color": "#DAD9D6","border": "None"}
            ),

        dcc.Input(id="input4",
            type="text",
            placeholder="nombre de scrolls à effectuer",
            style={'marginRight':'40px', "height":"75px", "width":"45%", "background-color": "#DAD9D6","border": "None"})], style={"text-align":"center"}),

        html.Br(),
        html.Br(),

        html.Div([
        html.Button('Submit', id='button', n_clicks=0, style={'marginRight':'40px',"height":"40px", "width":"30%", "background-color": "#DAD9D6", "border": "None"})], style={"text-align":"center"}),

        html.Br(),
        html.Div(id = 'output', style={"text-align": "center", "font-size":"150%", "color":"#E7E6E3"}) 
            
    ], style={"background-color": "#ABA9A6"}
)

@app.callback(
    Output("output", "children"),
    [Input('button', 'n_clicks'),
    Input("input1", "value"),
    Input("input2", "value"),
    Input("input3", "value"),
    Input("input4", "value")]
)

def run_script_onClick(n_clicks, input1, input2, input3, input4):      
    if not n_clicks:
        return dash.no_update

    if type(input1)==str and type(input2)==str and type(input3)==str and type(input4)==str:
        chemin = input2.strip('\"')
        scrap(str(input1),chemin,str(input3),int(input4))
        n_clicks = 0
        return "Fini"
    
    else :
        return "Il manque un/des paramètre(s)"
        

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=False)