
# API for alphavantage = GFY9VILXRYRKKT0U
# API for newsapi = 74874ae72b8d407ea743f4e53525f3ee

import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":"GFY9VILXRYRKKT0U"
}
response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
daily_data = [value for (key, value) in stock_data.items()]
yesterday_date = daily_data[0]
yesterday_closing = yesterday_date["4. close"]

day_before_yesterday_date = daily_data[1]
day_before_yesterday_closing = day_before_yesterday_date["4. close"]

diff = abs(float(yesterday_closing) - float(day_before_yesterday_closing))

up_down = None
if diff > 0:
    up_down = "📈"
else:
    up_down = "📉"

diff_percentage = (diff / float(yesterday_closing)) * 100

if abs(diff_percentage) > 0:
    news_parameter = {
        "q":COMPANY_NAME,
        "apiKey":"74874ae72b8d407ea743f4e53525f3ee",
    }
    response = requests.get(NEWS_ENDPOINT, params=news_parameter)
    response.raise_for_status()
    news_data = response.json()["articles"]
    three_articles = news_data[:3]

    formatted_article = [f"{STOCK_NAME}: {up_down} \n {round(diff_percentage)}% \n Headline : {news_data[0]['title']}, \nBrief : {news_data[0]['description']}" for article in three_articles]
    account_sid = "AC13375670ade94902c339179e651f1f52"
    auth_token = "3e35b2e86661f7af00bd3bd98f9d3b4a"
    client = Client(account_sid, auth_token)

    for article in formatted_article:
        message = client.messages.create(
            body=article,
            from_='+13347215371',
            to='+919790321615'
        )
        print(message.sid)

