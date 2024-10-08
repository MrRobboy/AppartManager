import requests
from bs4 import BeautifulSoup

def scrape_apartment_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Exemple d'extraction des données, à adapter selon la structure de la page
    nom = soup.find('h1').text
    adresse = soup.find('div', class_='adresse').text
    loyer = int(soup.find('span', class_='prix').text.replace('€', ''))
    surface = float(soup.find('span', class_='surface').text.replace('m²', ''))
    
    return {'nom': nom, 'adresse': adresse, 'loyer': loyer, 'surface': surface}
