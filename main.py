import requests
import datetime as dt
import timedelta

bot_api_key = "hide"
news_api_key = "hide"
stock_api_key = "hide"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
date = dt.date.today()
delta = timedelta.Timedelta(days=-1)
yesterday = date + delta
day_before_yesterday = yesterday + delta
print(yesterday)


parameters = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK,
    'apikey': stock_api_key,

}
url = 'https://www.alphavantage.co/query'
r = requests.get(url, params=parameters)
data = r.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

print(day_before_yesterday_closing_price)
print(yesterday_closing_price)

difference = yesterday_closing_price - day_before_yesterday_closing_price
diff_percent = round((difference / yesterday_closing_price) * 100)

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

news_url = ('https://newsapi.org/v2/everything?'
       f'qInTitle={COMPANY_NAME}&'
       f'from={yesterday}&'
       'sortBy=popularity&'
       f'apiKey={news_api_key}')

response = requests.get(news_url)
articles = response.json()['articles']
three_articles = articles[:3]

formatted_article = [f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}\nBrief: {article['description']}"
                     for article in three_articles]


def send_telegram(text: str):
    token = bot_api_key
    url = "https://api.telegram.org/bot"
    channel_id = "-1001531724002"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")


if abs(diff_percent) > 5:
    send_telegram(formatted_article[0])
    send_telegram(formatted_article[1])
    send_telegram(formatted_article[2])





## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
