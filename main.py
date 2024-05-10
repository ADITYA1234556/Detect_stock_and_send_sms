import requests
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = "API_KEY_FROM_STOCK_ENDPOINT"
NEWS_API = "YOUR_NEWS_API_KEY"
account_sid = 'YOUR ACCOUNT SID FROM TWILIO'
auth_token = 'TWILIO_AUTH_TOKEN'
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
parameters_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY
}
parameters_news = {
    "q": COMPANY_NAME,
    "from": '2024-05-08',
    "to": '2024-05-09',
    "sortBy": "popularity",
    "apikey": NEWS_API,
}
reponse_stock = requests.get(url=STOCK_ENDPOINT, params=parameters_stock)
reponse_stock.raise_for_status()
data = reponse_stock.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
day_b4_yesterday_data = data_list[1]
yesterday = float(yesterday_data['4. close'])
day_b4_yesterday = float(day_b4_yesterday_data['4. close'])
if yesterday > day_b4_yesterday:
    percentage_increase = round((((yesterday -day_b4_yesterday) / day_b4_yesterday) * 100),2)
else:
    percentage_increase = round((((day_b4_yesterday - yesterday) / day_b4_yesterday) * 100),2)
response_news = requests.get(url=NEWS_ENDPOINT,params=parameters_news)
response_news.raise_for_status()
news_data = response_news.json()
required_data = len((news_data["articles"][:3]))
print(required_data)
title= [news_data["articles"][i]["title"] for i in range(required_data)]
description= [news_data["articles"][i]["description"] for i in range(required_data)]
print(title)
print(description)
client = Client(account_sid, auth_token)
for y in range(len(title)):
    if yesterday > day_b4_yesterday:
        message = client.messages.create(body=f"TSLA 🔺{percentage_increase}%\nHeadline:{title[y]}\nBrief:{description[y]}",  from_= '+447883317242', to= '+447587997662')
    else:
        message = client.messages.create(
            body=f"TSLA 🔺{percentage_increase}%\nHeadline:{title[y]}\nBrief:{description[y]}", from_= '+447883317242', to= '+447587997662')
