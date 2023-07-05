import requests
import time
import json
import csv
from authlib.jose import jwt
from datetime import datetime
import os
import unicodedata
from dotenv import load_dotenv


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém os valores das variáveis de ambiente
KEY_ID = os.getenv('KEY_ID')
ISSUER_ID = os.getenv('ISSUER_ID')

EXPIRATION_TIME = int(round(time.time() + (20.0 * 60.0)))  # 20 minutes timestamp
PATH_TO_KEY = 'key.p8'
PATH_TO_APPS_LIST = 'lista-ios-apps.txt'

with open(PATH_TO_KEY, 'r') as f:
    PRIVATE_KEY = f.read()

header = {
    "alg": "ES256",
    "kid": KEY_ID,
    "typ": "JWT"
}

payload = {
    "iss": ISSUER_ID,
    "exp": EXPIRATION_TIME,
    "aud": "appstoreconnect-v1"
}

def create_jwt(header, payload, private_key):
    token = jwt.encode(header, payload, private_key)
    return token.decode()

def write_csv(data, app_info):
    app_name = app_info['data']['attributes']['name']
    app_name_normalized = normalize_app_name(app_name)
    current_date = datetime.now()  # Obtém a data atual
    month_year = current_date.strftime("%m_%Y")
    csv_filename = f"dados_{app_name_normalized}_{month_year}_apple.csv"
    current_date = datetime.now()  # Obtém a data atual

    with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if file.tell() == 0:
            writer.writerow(['Aplicativo ID', 'Aplicativo', 'Nota', 'Título', 'Contéudo', 'Nome do Autor', 'Data', 'País'])
        
        sorted_data = sorted(data, key=lambda x: x['attributes']['createdDate'])
        
        for review in sorted_data:
            created_date = datetime.strptime(review['attributes']['createdDate'], "%Y-%m-%dT%H:%M:%S%z")
            if created_date.month == current_date.month and created_date.year == current_date.year:  # Verifica se a revisão é do mês e ano atual
                review_id = review['id']
                rating = review['attributes']['rating']
                title = review['attributes']['title']
                body = review['attributes']['body']
                reviewer_nickname = review['attributes']['reviewerNickname']
                created_date_str = created_date.strftime("%d/%m/%Y")
                territory = review['attributes']['territory']
                
                if 'response' in review.get('relationships', {}):
                    responded = True
                else:
                    responded = False
                
                writer.writerow([app_info['data']['id'], app_info['data']['attributes']['name'], rating, title, body, reviewer_nickname, created_date_str, territory])

def fetch_reviews(url, headers, app_info):
    response = requests.get(url, headers=headers)
    response_json = response.json()
    
    if 'data' in response_json:
        data = response_json['data']
        write_csv(data, app_info)
    else:
        print('No data found in the response.')
    
    if 'next' in response_json['links']:
        next_url = response_json['links']['next']
        return next_url
    else:
        return None

def get_app_info(app_id, headers):
    url = f'https://api.appstoreconnect.apple.com/v1/apps/{app_id}'
    response = requests.get(url, headers=headers)
    app_info = response.json()
    return app_info

def normalize_app_name(app_name):
    normalized = unicodedata.normalize('NFKD', app_name).encode('ASCII', 'ignore').decode('utf-8')
    return normalized.replace(" ", "_")

def main():
    if not os.path.isfile(PATH_TO_APPS_LIST):
        print("O arquivo 'lista-ios-apps.txt' não existe.")
        return

    with open(PATH_TO_APPS_LIST, 'r') as apps_file:
        for line in apps_file:
            line = line.strip()
            if line:
                app_name, app_id = line.split('=')
                app_id = app_id.strip()
                
                print(f"Coletando dados do aplicativo: {app_name}")
                
                token = create_jwt(header, payload, PRIVATE_KEY)
                JWT = 'Bearer ' + token
                HEAD = {'Authorization': JWT}
                app_info = get_app_info(app_id, HEAD) 
                URL = f'https://api.appstoreconnect.apple.com/v1/apps/{app_id}/customerReviews?limit=200'
                while URL:
                    URL = fetch_reviews(URL, HEAD, app_info)

if __name__ == '__main__':
    main()
