import csv
import json
import re
from datetime import datetime
from google_play_scraper import app, reviews_all, Sort

# Leia o arquivo lista-android-apps.txt
with open('lista-android-apps.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()  

    app_name, app_id = line.split(' = ')

    clean_app_name = re.sub(r'[^a-zA-Z0-9 ]', '', app_name).replace(' ', '_')

    csv_file = f'dados_{clean_app_name}_android.csv'

    json_file = f'dados_{clean_app_name}_android.json'

    app_details = app(app_id)

    reviews = reviews_all(
        app_id,
        sort=Sort.MOST_RELEVANT,
        sleep_milliseconds=0,  # padrão: 0
        lang='br',  # padrão: 'en'
        country='us',  # padrão: 'us'
    )

    # Escreve os dados em um arquivo CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome do Aplicativo', 'Instalações', 'Score', 'Ratings', 'Versão',
                         'Nome do Revisor', 'Comentário', 'Nota', 'Data do Review', 'Respondido'])

        # Escreve os detalhes do aplicativo no arquivo CSV
        writer.writerow([app_details['title'], app_details['installs'], app_details['score'],
                         app_details['ratings'], app_details['version']])

        # Escreve os reviews no arquivo CSV
        for review in reviews:
            reviewer_name = review['userName']
            comment = review['content']
            rating = review['score']
            review_date = review['at']
            replied = review['replyContent'] is not None

            writer.writerow(['', '', '', '', '', reviewer_name, comment, rating, review_date, replied])

    # Salva os dados em um arquivo JSON
    data = {
        'Nome do Aplicativo': app_details['title'],
        'Instalações': app_details['installs'],
        'Score': app_details['score'],
        'Ratings': app_details['ratings'],
        'Versão': app_details['version'],
        'Reviews': []
    }

    for review in reviews:
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

        data['Reviews'].append(review_data)

    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f'Dados do aplicativo "{app_name}" salvos com sucesso.')
    print(f'Todos os dados salvos nos arquivos: {csv_file} e {json_file}')
