import os
import time
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

from playwright.sync_api import sync_playwright
import csv
data_list = []
with sync_playwright() as p:
    try:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.beatstats.com/labels/home/list?genre=0&period=3')

        divs_xpath = '//div[contains(@id, "top10artistchart-full-nopad")]'
        divs_list = page.query_selector_all(divs_xpath)
        
        for div in divs_list:
            coin_dict = {}
            div_name=div.query_selector('div[id*="top10labelchart-name"]')
            coin_dict["label_name"]=div_name.query_selector('span[class*="labelcharttextname"]').inner_text()
            coin_dict["label_points"]=div_name.query_selector('span[class*="charttextpoints"]').inner_text()
            
            div_img=div.query_selector('div[id*="top10artistchart-image"] img')
            href_img=div_img.get_attribute('src')
            coin_dict["label_image"]="https://www.beatstats.com"+href_img
            coin_dict["label_instagram"]="https://www.instagram.com/"+coin_dict['label_name']
            data_list.append(coin_dict)
    except Exception as e:
        print("il ya un erreur",e)
        with open('logfile.log', 'a') as error_file:
            error_file.write(f"{datetime.now()} - {str(e)}\n")


for i in range(2,30):
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto('https://www.beatstats.com/labels/home/list?genre=0&period=3&page='+str(i))

            divs_xpath = '//div[contains(@id, "top10artistchart-full-nopad")]'
            divs_list = page.query_selector_all(divs_xpath)
            
            for div in divs_list:
                coin_dict = {}
                div_name=div.query_selector('div[id*="top10labelchart-name"]')
                coin_dict["label_name"]=div_name.query_selector('span[class*="labelcharttextname"]').inner_text()
                coin_dict["label_points"]=div_name.query_selector('span[class*="charttextpoints"]').inner_text()
                
                div_img=div.query_selector('div[id*="top10artistchart-image"] img')
                href_img=div_img.get_attribute('src')
                coin_dict["label_image"]="https://www.beatstats.com"+href_img
                coin_dict["label_instagram"]="https://www.instagram.com/"+coin_dict['label_name']
                data_list.append(coin_dict)
        except Exception as e:
            print("il ya un erreur",e)
            with open('logfile.log', 'a') as error_file:
                error_file.write(f"{datetime.now()} - {str(e)}\n")
    
# Nom du fichier CSV
nom_fichier = 'liste_labels.csv'
# Ouverture du fichier en mode écriture
with open(nom_fichier, mode='w', newline='', encoding='utf-8') as fichier:
    # Création d'un writer CSV
    writer = csv.DictWriter(fichier, fieldnames=data_list[0].keys())
    # Écriture de l'en-tête (les clés du dictionnaire)
    writer.writeheader()
    # Écriture des lignes de données
    writer.writerows(data_list)

print("terminé avec success")