import requests
from bs4 import BeautifulSoup
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://nutrition.sa.ucsc.edu/"

# Create a Session object
s = requests.Session()
s.verify = False  # Disable SSL verification for the session

response = s.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    locations = soup.find_all(class_='locations')

    links = [item.find('a').get('href') for item in locations[:3]]
    for link in links:
        # shortmenu.aspx?sName=UC Santa Cruz Dining&locationNum=40&locationName=College Nine/John R. Lewis Dining Hall&naFlag=1
        # Extract College Nine
        location = re.search(r'locationName=(.+?)&', link).group(1).replace('+', ' ').replace('%2f', '/')

        resp = s.get(url + link)  # Use the session to make the request
        soup = BeautifulSoup(resp.content, 'html.parser')
        meals = soup.find_all(class_='shortmenurecipes')
        for meal in meals:
            if meal.text.strip() == 'Daal Saag':
                print("Daal Saag is available at", location, "(:")
                break
        else:
            print("Daal Saag is not available at", location, "):")
                

else:
    print("Failed to retrieve the webpage")