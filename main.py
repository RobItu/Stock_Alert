import requests
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
AV_API_KEY = "0BG20OQKJ3L1M64M"
NEWS_API_KEY = "a671393a89fb420c9b8ca9efadab0563"

AV_Parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": AV_API_KEY
}

NEWS_parameters = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,

}

# -------------------------NEWS_API---------------------------------- #
news_response = requests.get(url="https://newsapi.org/v2/top-headlines?q=Tesla&apiKey=a671393a89fb420c9b8ca9efadab0563")
news_response.raise_for_status()
data = news_response.json()
articles = data["articles"][:2]
news_content = {index["title"]: index["description"] for index in articles}

# ----------------------------STOCK_API------------------------------ #
response = requests.get(url="https://www.alphavantage.co/query", params=AV_Parameters)
response.raise_for_status()
data = response.json()
daily_data = data["Time Series (Daily)"]

daily_closes = {day: daily_data[day]["4. close"] for day in daily_data}
daily_closes_list = list(daily_closes.values())

daily_closes_values = [float(num) for num in daily_closes_list[:3]]
previous_day_close = daily_closes_values[0]

for number in daily_closes_values:
    percent_change = abs(((number - previous_day_close) / previous_day_close) * 100)
    if percent_change >= 5:
        text = ""
        for n in news_content:
            text += f"Headline: {n}\n\n Brief:{news_content[n]}\n\n"

        client = Client(os.environ["account_sid"], os.environ['auth_token'])
        message = client.messages \
            .create(
            body=f"{STOCK}🔺{percent_change}%\n\n {text}",
            from_='+12073869879',
            to=os.environ["phone"]
        )
    elif percent_change < -5:
        text = ""
        for n in news_content:
            text += f"Headline: {n}\n\n Brief:{news_content[n]}\n\n"

        client = Client(os.environ["account_sid"], os.environ['auth_token'])
        message = client.messages \
            .create(
            body=f"{STOCK}🔻{percent_change}%\n\n {text}",
            from_='+12073869879',
            to=os.environ["phone"]
        )
    previous_day_close = number


