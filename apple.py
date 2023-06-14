from app_store_scraper import AppStore

aplicativo = AppStore(country="br", app_name="app", app_id=922529225)
aplicativo.review(how_many=10000)

for review in aplicativo.reviews:
    date = review['date']
    comment = review['review']
    rating = review['rating']
    title = review['title']
    username = review['userName']
    response = "Respondida" if 'developerResponse' in review else "Não respondida"
    
    print("Data:", date)
    print("Comentário:", comment)
    print("Rating:", rating)
    print("Título:", title)
    print("Nome do usuário:", username)
    print("Resposta do desenvolvedor:", response)
    print("----------------------------------------")
