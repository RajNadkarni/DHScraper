import requests
from bs4 import BeautifulSoup
url = "https://nutrition.sa.ucsc.edu/"

response = requests.get(url, verify=False)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    locations = soup.find_all(class_='locations')
    for item in locations:
        print(item.text.strip())

else:
    print("Failed to retrieve the webpage")
