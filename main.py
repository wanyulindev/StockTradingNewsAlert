import requests
import os
import datetime
from twilio.rest import Client
import time

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

def day_time(day, hour):
    return datetime.datetime.combine((CURRENT_TIME - datetime.timedelta(days=day)).date(),
                                                  datetime.time(hour, 0, 0))
# Since this doesn't work with every occasion:
def date(day):
    return (CURRENT_TIME - datetime.timedelta(days=day)).date()

news_api_keys = os.environ.get("NEWS_API_KEYS")
news_url = "https://newsapi.org/v2/everything"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
CURRENT_TIME = datetime.datetime.now()
# print(CURRENT_TIME)
TWO_DAYS_AGO_MIDNIGHT = day_time(2, 0)
# print(TWO_DAYS_AGO_MIDNIGHT)

news_parameters = {
    "apiKey": news_api_keys,
    "q": COMPANY_NAME
    # "q": f"{COMPANY_NAME.lower()} AND {STOCK}"
    # "from": TWO_DAYS_AGO_MIDNIGHT,
    # "to": CURRENT_TIME,
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
stock_response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=E21LGXJU3D3Q1VL7')
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
# print(stock_data)

# This method will cause some problem: (ex: stock market only works on weekdays)
# YESTERDAY = str(date(1))
# DAY_BEFORE_YESTERDAY = str(date(2))
# # print(stock_data["Time Series (Daily)"])
# # print(stock_data["Time Series (Daily)"][YESTERDAY])
#
#
# yesterday_data = stock_data["Time Series (Daily)"][YESTERDAY]
# day_before_yesterday_data = stock_data["Time Series (Daily)"][DAY_BEFORE_YESTERDAY]
# print(yesterday_data)
# print(day_before_yesterday_data)

# So, Let's try to change its type and iterate the value:
stock_data_list = [value for key, value in stock_data.items()]
# print(stock_data_list)
yesterday_data = stock_data_list[0]
# print(yesterday_data)
yesterday_value= float(yesterday_data["4. close"])
# print(yesterday_value)
day_before_yesterday_value = float(stock_data_list[1]["4. close"])
# print(day_before_yesterday_value)

difference = abs(yesterday_value - day_before_yesterday_value)
# print(difference)
diff_percent = (difference / yesterday_value) * 100
# print(diff_percent)
if  diff_percent >= 1:
    # print(news_data["articles"][:3])
    print("News API Response:")
    print(news_data)
    for item in news_data["articles"][:3]:
        print("Processing article...")
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='+18444821071',
            body=f"Your {STOCK} stock, has either drops/rises between these two days!\n"
                 f"Here's article that you may concern:\n"
                 f"Headline: {item['title']}.\n"
                 f"Brief: {item['description']}",
            to='+16268736132'
        )
        print(item)
        print(message.status)
        print(message.sid)
        print("Message sent.")
        time.sleep(10)



# YESTERDAY_1900 = str(day_time(1, 19))
# DAY_BEFORE_YESTERDAY_1900 = str(day_time(2, 19))
# print(type(YESTERDAY_1900))
# print(YESTERDAY_1900)

# print(stock_data["Time Series (60min)"][YESTERDAY_1900])
# Step 1. done

# Here what I can approve my code:
# stock_url = "https://www.alphavantage.co/query"
# stock_api_keys = "E21LGXJU3D3Q1VL7"
#
# stock_parameters = {
#     "function": "TIME_SERIES_DAILY",
#     "symbol": STOCK,
#     "apiKey": stock_api_keys
# }
#
# stock_response = requests.get(stock_url, params=stock_parameters)
# stock_response.raise_for_status()
# stock_data = stock_response.json()
# print(stock_data)
# These doesn't work!:
# {'Error Message': 'the parameter apikey is invalid or missing. Please claim your free API key on (https://www.alphavantage.co/support/#api-key). It should take less than 20 seconds.'}
#---------------------------------------------------------------------------------------------


## STEP 1: Use https://www.alphavantage.co  VVVVV
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


# My Bug:
# Since they are all three queued. could you tell me why I only got two SMS?
# GPT:
# The reason you are receiving only two SMS messages instead of three could be due to
# various factors, and it might require some debugging to identify the exact cause.
# Here are some potential reasons:
#
# News Availability: There may not have been enough relevant news articles available in
# the specified date range and search criteria to fulfill all three messages. If the API
# did not return three articles, you would have fewer SMS messages.
#
# Twilio Limitations: Twilio may have limitations on sending messages in quick succession.
# It's possible that there was a rate-limiting issue or an issue with sending multiple
# messages within a short timeframe.
#
# Conditional Logic: Your code may have conditional logic that filters out some articles
# based on certain criteria. Ensure that your code is correctly filtering and selecting
# the articles to send as messages.
#
# Error Handling: Check for any errors or exceptions that might have occurred during the
# execution of your code. An error could have interrupted the process of sending the
# third SMS.
#
# To troubleshoot this issue:
#
# Verify that the News API is returning the expected number of articles.
# Check for any error messages or exceptions in your code or logs.
# Add debugging statements or print statements to track the flow of your code and see
# which articles are being processed and sent as SMS messages.
# By systematically examining these factors and debugging your code, you should be able
# to determine why you are receiving only two SMS messages and address the issue
# accordingly.