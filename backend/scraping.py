import requests
from bs4 import BeautifulSoup

def scrape_apartment_info(url):
    response = requests.get(url)
    if response.status_code != 200:
        return {"nom": "Inconnu", "adresse": "Inconnue", "loyer": 0, "surface": 0}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Exemples de sélection d'éléments, modifiez cela selon la structure de votre site cible
    nom = soup.find("h1", class_="nom").text.strip() if soup.find("h1", class_="nom") else "Inconnu"
    adresse = soup.find("p", class_="adresse").text.strip() if soup.find("p", class_="adresse") else "Inconnue"
    loyer = int(soup.find("span", class_="loyer").text.strip().replace("€", "").replace(" ", "")) if soup.find("span", class_="loyer") else 0
    surface = float(soup.find("span", class_="surface").text.strip().replace(" m²", "").replace(",", ".")) if soup.find("span", class_="surface") else 0

    return {
        "nom": nom,
        "adresse": adresse,
        "loyer": loyer,
        "surface": surface
    }
