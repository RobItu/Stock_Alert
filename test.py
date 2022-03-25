from newsapi import NewsApiClient
import requests

news_response = requests.get(url="https://newsapi.org/v2/top-headlines?q=Tesla&apiKey=a671393a89fb420c9b8ca9efadab0563")
news_response.raise_for_status()
data= news_response.json()
articles = data["articles"][:4]
news_content = {}

for index in articles:
    news_content[index["title"]] = index["description"]

for n in news_content:
    print(f"Headline: {n}")
    print(f"Brief: {news_content[n]}\n")

