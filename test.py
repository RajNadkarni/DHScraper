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

    results = {}

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        locations = soup.find_all(class_='locations')

        links = [item.find('a').get('href') for item in locations[:3]]
        for link in links:
            location = re.search(
                r'locationName=(.+?)&', link).group(1).replace('+', ' ').replace('%2f', '/')
            resp = s.get(url + link)  # Use the session to make the request
            soup = BeautifulSoup(resp.content, 'html.parser')

            categories = {
                "Breakfast": False,
                "Lunch": False,
                "Dinner": False,
                "Late Night": False
            }

            category_sections = soup.find_all(class_='shortmenumeals')
            for section in category_sections:
                category_text = section.text.strip()
                if category_text in categories:
                    meal_section = section.find_next('table')
                    if meal_section:
                        meals = meal_section.find_all(
                            class_='shortmenurecipes')
                        for meal in meals:
                            if meal.text.strip().lower() == food.lower():
                                categories[category_text] = True
                                break

            # Filter out the meal times where the food is not available
            available_meals = {k: v for k, v in categories.items() if v}
            if available_meals:
                results[location] = available_meals
    else:
        return json.dumps({"error": "Failed to fetch the page"})

    if results:
        return json.dumps(results)
    else:
        return json.dumps({"error": "No food found"})


# Test the function
if __name__ == "__main__":
    food_name = input("Enter the name of the food to check: ")
    result = check_food_availability(food_name)
    print(result)
