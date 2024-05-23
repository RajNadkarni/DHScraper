import requests
from bs4 import BeautifulSoup
import urllib3
import re
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://nutrition.sa.ucsc.edu/"

def check_food_availability(food):
    s = requests.Session()
    s.verify = False  # Disable SSL verification for the session

    response = s.get(url)

    results = {}  # Initialize an empty dictionary to store the results

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        locations = soup.find_all(class_='locations')

        links = [item.find('a').get('href') for item in locations[:3]]
        for link in links:
            location = re.search(r'locationName=(.+?)&', link).group(1).replace('+', ' ').replace('%2f', '/')
            resp = s.get(url + link)  # Use the session to make the request
            soup = BeautifulSoup(resp.content, 'html.parser')
            meals = soup.find_all(class_='shortmenurecipes')
            for meal in meals:
                if meal.text.strip() == food:
                    results[location] = True
                    break
            else:
                results[location] = False

    else:
        return json.dumps({"error": "Failed to fetch the page"})

    return json.dumps(results)  # Output the entire results dictionary as a JSON string

if __name__ == "__main__":
    print(check_food_availability("Steamed Rice"))
