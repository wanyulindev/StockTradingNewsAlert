import requests
import os
import datetime
from twilio.rest import Client

def day_time(day, hour):
    return datetime.datetime.combine((CURRENT_TIME - datetime.timedelta(days=day)).date(),
                                                  datetime.time(hour, 0, 0))

news_api_keys = os.environ.get("NEWS_API_KEYS")
news_url = "https://newsapi.org/v2/everything"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
CURRENT_TIME = datetime.datetime.now()
print(CURRENT_TIME)
TWO_DAYS_AGO_MIDNIGHT = day_time(2, 0)
print(TWO_DAYS_AGO_MIDNIGHT)

news_parameters = {
    "apiKey": news_api_keys,
    "q": f"{COMPANY_NAME.lower()} AND {STOCK}",
    "from": TWO_DAYS_AGO_MIDNIGHT,
    "to": CURRENT_TIME,
}

news_response = requests.get(news_url, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()
# print(news_data)
print(news_data["articles"][:3])
# Step 2. done.
#-------------------------------------------------------------------------------------------
# Step 1.:

# stock_api_keys = os.environ.get("STOCK_API_KEYS")
# stock_url = "https://www.alphavantage.co/query"
#
# stock_parameters = {
#     "function": "TIME_SERIES_INTRADAY",
#     "symbol": STOCK,
#     "interval": "5min",
#     "apiKey": stock_api_keys
# }
#
# stock_response = requests.get(stock_url, params=stock_parameters)
stock_response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TSLA&interval=60min&apikey=E21LGXJU3D3Q1VL7')
stock_response.raise_for_status()
stock_data = stock_response.json()
# print(stock_data)

YESTERDAY_1900 = str(day_time(1, 19))
DAY_BEFORE_YESTERDAY_1900 = str(day_time(2, 19))
# print(type(YESTERDAY_1900))
# print(YESTERDAY_1900)


print(stock_data["Time Series (60min)"][YESTERDAY_1900])







## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday
# then print("Get News").

## STEP 2: Use https://newsapi.org  VVVVV
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title
# and description to your phone number.


#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


