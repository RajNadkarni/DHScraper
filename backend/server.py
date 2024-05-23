import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://nutrition.sa.ucsc.edu/"

response = requests.get(url, verify=False)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    locations = soup.find_all(class_='locations')

    links = [item.find('a').get('href') for item in locations[:3]]
    for link in links:
        resp = requests.get(url + link, verify=False)
        soup = BeautifulSoup(resp.content, 'html.parser')
        print(soup)
        meals = soup.find_all(class_='shortmenurecipes')
        for meal in meals:
            print(meal)

else:
    print("Failed to retrieve the webpage")