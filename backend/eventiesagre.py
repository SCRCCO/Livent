import logging
import requests
from bs4 import BeautifulSoup
import json
import time
import html
from consts import regioni,categorie

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def getLastPage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    fine = soup.find_all('div', class_="colonne center spacer20")
    
    try:
        ultima_pag = fine[-1].a['href']
        page_number = ultima_pag.split('pag-')[1].split('.htm')[0]
        return page_number
    except:
        # Handle the case where the last page number is not present
        return None

def scrape_event_data(url, c):
    data_list = []

    # Make a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        title_element = soup.find('div', class_='titolo sfondoGiallo spacer5 rientro25')
        
        # Find the parent container of the title element
        parent_container = title_element.find_parent('div', class_='eventiSponsor')
        
        # Get only the elements after title_element within the parent container
        div_contenuto_list = parent_container.find_all_next('div', class_='risultatoEvento')[4:]

        # Loop through each div element
        for div_contenuto in div_contenuto_list:
            try:
                # Extract link
                link = div_contenuto.a['href'] if div_contenuto.a else None
                
                # Extract title
                title = div_contenuto.find('h3', class_='titolo').text.strip() if div_contenuto.find('h3', class_='titolo') else None
                
                # Extract subtitle
                subtitle = div_contenuto.find('h3', class_='grassetto corsivo testo').text.strip() if div_contenuto.find('h3', class_='grassetto corsivo testo') else None
                
                # Extract regione
                regione = div_contenuto.find('span', class_='grassetto').text.strip() if div_contenuto.find('span', class_='grassetto') else None
                
                # Extract città
                città = div_contenuto.find('span', class_='corsivo').text.strip() if div_contenuto.find('span', class_='corsivo') else None
                
                # Extract data and decode Unicode characters
                data = div_contenuto.find('div', class_=None).text.strip().replace('(', '').replace(')', '')
                data = html.unescape(data.encode('raw_unicode_escape').decode('utf-8')) if data else None
                
                # Create a dictionary to store the extracted data
                event_data = {
                    "Link": link,
                    "Titolo": title,
                    "Subtitolo": subtitle,
                    "Regione": regione.replace('+', ' '),
                    "City": città,
                    "Data": data,
                    "Categoria": c.replace('+', ' ')
                }
                
                # Append the dictionary to the list
                data_list.append(event_data)
            except Exception as e:
                logger.error("An error occurred while scraping event data: %s", e)
            
    else:
        logger.error("Failed to fetch data from URL: %s", url)
    
    return data_list

# Initialize data list
all_data_list = []

# Loop through categories and regions
for r in regioni:
    for c in categorie:
        url = f"https://www.eventiesagre.it/cerca/{c}/sez/mese_Oggi/{r}/prov/cit/rilib"
        last_page = getLastPage(url)
        logger.info("Scraping data for category %s and region %s", c, r)
        all_data_list.extend(scrape_event_data(url, c))
        time.sleep(0.1)
        if last_page:
            for x in range(1, int(last_page) + 1):
                url = f"https://www.eventiesagre.it/cerca/{c}/sez/mese_Oggi/{r}/prov/cit/rilib/pag-{x}.htm"
                logger.info("Scraping data for page %d of region %s and category %s", x, r, c)
                all_data_list.extend(scrape_event_data(url, c))
                time.sleep(0.2)

# Open the JSON file in write mode with truncate to empty it
with open('eventisagre.json', 'w', encoding='utf-8') as file:
    file.truncate(0)

# Write the extracted data to a JSON file with ensure_ascii=False
with open('eventisagre.json', 'w', encoding='utf-8') as file:
    json.dump(all_data_list, file, indent=4, ensure_ascii=False)


logger.info("Data extraction completed. Results written to eventisagre.json.")
