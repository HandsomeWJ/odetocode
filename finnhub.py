#API from Finnhub (https://finnhub.io/), implemented in "deploy" using Django

import requests

def collate_news(stocks=["AAPL", "GOOG", "XOM", "GE", "PFE", "GSK", "PEP", "NSRGY", "GLD", "VOO"]):
    for stock in stocks:
        data = get_news(stock)
        total = len(data)
        output = {}
        if data != []:
            output[stock] = []
            for i in range(total):
                output[stock].append({'headline' : data[i]['headline'],
                                'image' : data[i]['image'],
                                'source' : data[i]['source'],
                                'summary' : data[i]['summary'],
                                'url' : data[i]['url']})       
    return output

def get_news(ticker, start_date="2020-09-04", end_date="2020-09-07", token="bt968tn48v6v8iv1le4g"):
    r = requests.get('https://finnhub.io/api/v1/company-news?symbol=%s&from=%s&to=%s&token=%s' % (ticker, start_date, end_date, token))
    return r.json()


