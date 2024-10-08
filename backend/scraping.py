def scrape_apartment_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        nom = soup.find('h1').text.strip()
        adresse = soup.find('div', class_='adresse').text.strip()
        loyer = int(soup.find('span', class_='prix').text.replace('€', '').replace(' ', '').strip())
        surface = float(soup.find('span', class_='surface').text.replace('m²', '').replace(' ', '').strip())
    except AttributeError as e:
        raise ValueError("Erreur lors de l'extraction des données : " + str(e))
    except ValueError as e:
        raise ValueError("Erreur de formatage des données : " + str(e))

    return {'nom': nom, 'adresse': adresse, 'loyer': loyer, 'surface': surface}
