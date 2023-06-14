from app_store_scraper import AppStore
import csv
import json
from datetime import datetime

# Read the app names and IDs from the txt file
apps = {}
with open('lista-ios-apps.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            app_name, app_id = line.split('=')
            apps[app_name.strip()] = app_id.strip()

# Iterate over the apps and scrape reviews
for app_name, app_id in apps.items():
    aplicativo = AppStore(country="br", app_name="app", app_id=app_id)
    aplicativo.review(how_many=10000)

    # Create a CSV file for each app
    csv_file = f"{app_name}_reviews.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['App Name', 'Author', 'Date', 'Title', 'Comment', 'Rating', 'Response'])

        for review in aplicativo.reviews:
            date = review['date']
            comment = review['review']
            rating = review['rating']
            title = review['title']
            username = review['userName']
            response = "Respondida" if 'developerResponse' in review else "Não respondida"

            writer.writerow([app_name, username, date, title, comment, rating, response])

    # Create a JSON file for each app
    json_file = f"{app_name}_reviews.json"
    reviews_data = {
        'App Name': app_name,
        'Reviews': aplicativo.reviews
    }
    with open(json_file, 'w', encoding='utf-8') as file:
        # Convert datetime objects to strings
        for review in reviews_data['Reviews']:
            review['date'] = review['date'].strftime('%Y-%m-%d %H:%M:%S')

        json.dump(reviews_data, file, ensure_ascii=False, indent=4)
