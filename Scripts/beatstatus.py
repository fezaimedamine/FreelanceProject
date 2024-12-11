# Import des bibliothèques
import os
import time
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler
from pymongo import MongoClient

from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import sys
import csv
def convertirName(name):
    # Convertir le nom en minuscules et remplacer les espaces par des underscores
    return name.strip().lower().replace(" ", "_")
data = []
data_list=[]
def extract_artist(url):
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)
            #page = browser.new_page()
            context = browser.new_context()
            page=context.new_page()
            page.goto(url)
            liens_xpath = '//*[@id="content-artists"]/a'

            liens_list = page.query_selector_all(liens_xpath)
            page = browser.new_page()
            for lien in liens_list:
                artist = {}
                a_href = lien.get_attribute('href')
                nouveau_lien = "https://www.beatstats.com" + a_href
                artist['profile']=nouveau_lien
                data.append(artist)
        
        except Exception as e:
            print("Il y a une erreur :", e)
            with open('logfile.log', 'a') as error_file:
                error_file.write(f"{datetime.now()} - {str(e)}\n")

extract_artist('https://www.beatstats.com/artists/home/list?genre=0&period=3')
for i in range(2,30):
    extract_artist('https://www.beatstats.com/artists/home/list?genre=0&period=3&page='+str(i))

df_profile=pd.DataFrame(data)
#print(df_profile)
for profile in df_profile['profile']:
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)
            #page = browser.new_page()
            context = browser.new_context()
            page=context.new_page()
            page.goto(profile)
            artist = {}
            # Chercher le nom d'artiste
            name_xpath = '//*[@id="header-selectiontext"]/span/strong'
            name_element = page.query_selector(name_xpath)
            if name_element:
                name = name_element.inner_text()
            else:
                print(f"Nom non trouvé pour le lien : {profile}")
                continue  # Passer à la prochaine itération si l'élément est introuvable
            # Chercher le lien de l'image 
            img_xpath = '//*[@id="content-column1-image"]/img'
            img = page.query_selector(img_xpath)
            href_img = img.get_attribute('src')
            lien_img = "https://www.beatstats.com" + href_img
            
            # Construire le lien du compte Instagram
            insta_lien = "https://www.instagram.com/" + convertirName(name)
            
            # Chercher les labels avec lesquels l'artiste travaille
            labels_xpath = '//*[@id="top10artistchart-med"]'
            labels = page.query_selector_all(labels_xpath)
            label_list = []
            for label in labels:
                label_name_element = label.query_selector('//*[@id="top10trackchart-text"]/span[1]')
                if label_name_element:
                    label_name = label_name_element.inner_text()
                    label_list.append(label_name)
                else:
                    print(f"Label introuvable pour le lien : {profile}")
            
            # Ajouter les informations dans un dictionnaire
            artist['name'] = name
            artist['img'] = lien_img
            artist['instagram'] = insta_lien
            artist['labels'] = label_list
            data_list.append(artist)
            
        
        except Exception as e:
            print("detectition d'un erreur",e)
            with open('logfile.log', 'a') as error_file:
                error_file.write(f"{datetime.now()} - {str(e)}\n")



# Programme principal
def load_data(data_list,nom_fichier):

# Nom du fichier CSs

    # Ouverture du fichier en mode écriture
    if data_list:  # Vérifier si la liste data contient des éléments
        with open(nom_fichier, mode='w', newline='', encoding='utf-8') as fichier:
            # Création d'un writer CSV
            writer = csv.DictWriter(fichier, fieldnames=data_list[0].keys())
            
            # Écriture de l'en-tête (les clés du dictionnaire)
            writer.writeheader()
            
            # Écriture des lignes de données
            writer.writerows(data_list)

        print(f"Les données ont été enregistrées dans le fichier {nom_fichier}.")
    else:
        print("Aucune donnée à écrire dans le fichier CSV.")
        with open('logfile.log', 'a') as error_file:
                error_file.write(f"{datetime.now()} - {str(e)}\n")

load_data(data_list, 'liste_artiste.csv')
