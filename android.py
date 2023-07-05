import csv
import json
import re
import time
from datetime import datetime
from google_play_scraper import app, Sort, reviews

# Leia o arquivo lista-android-apps.txt
with open('lista-android-apps.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()

    app_name, app_id = line.split(' = ')

    clean_app_name = re.sub(r'[^a-zA-Z0-9 ]', '', app_name).replace(' ', '_')

    current_month_year = datetime.now().strftime('%m_%Y')

    csv_file = f'dados_{clean_app_name}_{current_month_year}_android.csv'
    json_file = f'dados_{clean_app_name}_{current_month_year}_android.json'

    app_details = app(app_id)

    reviews_data = reviews(
        app_id,
        lang='pt',  # defaults to 'en'
        country='br',  # defaults to 'us'
        sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT you can use Sort.NEWEST to get newst reviews_data
        count=100000,  # defaults to 100
        filter_score_with=None  # defaults to None(means all score) Use 1 or 2 or 3 or 4 or 5 to select certain score
    )

    # Ordena as reviews pelo campo 'at' (data)
    sorted_reviews = sorted(reviews_data[0], key=lambda x: x['at'])

    # Escreve os dados em um arquivo CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome do Aplicativo', 'Instalações', 'Score', 'Ratings', 'Versão',
                         'Nome do Revisor', 'Comentário', 'Nota', 'Data do Review', 'Respondido'])

        # Escreve os detalhes do aplicativo no arquivo CSV
        writer.writerow([app_details['title'], app_details['installs'], app_details['score'],
                         app_details['ratings'], app_details['version']])

        # Escreve os reviews no arquivo CSV
        total_reviews = len(sorted_reviews)
        current_date = datetime.now().strftime('%Y-%m')  # Obter o mês atual
        for i, review in enumerate(sorted_reviews, 1):
            reviewer_name = review['userName']
            comment = review['content']
            rating = review['score']
            review_date = review['at']
            replied = review['replyContent'] is not None

            review_month = review_date.strftime('%Y-%m')

            # Verifica sea data do review pertence ao mês atual
            if review_month == current_date:
                writer.writerow(['', '', '', '', '', reviewer_name, comment, rating, review_date, replied])

            # Exibe a quantidade de dados coletados
            #print(f'Dados coletados: {i}/{total_reviews}')

    # Salva os dados em um arquivo JSON
    data = {
        'Nome do Aplicativo': app_details['title'],
        'Instalações': app_details['installs'],
        'Score': app_details['score'],
        'Ratings': app_details['ratings'],
        'Versão': app_details['version'],
        'reviews_data': []
    }

    for review in sorted_reviews:
        reviewer_name = review['userName']
        comment = review['content']
        rating = review['score']
        review_date = review['at'].strftime('%Y-%m-%d %H:%M:%S')  # Converte para string
        replied = review['replyContent'] is not None

        review_data = {
            'Nome do Revisor': reviewer_name,
            'Comentário': comment,
            'Nota': rating,
            'Data do Review': review_date,
            'Respondido': replied
        }

        data['reviews_data'].append(review_data)

    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f'Dados do aplicativo "{app_name}" salvos com sucesso.')
    print(f'Todos os dados salvos nos arquivos: {csv_file} e {json_file}')
