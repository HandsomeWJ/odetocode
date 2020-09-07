from django.shortcuts import render
from django.http import HttpResponse
from .forms import PortfolioForm  
import requests
import boto3
import json
import pandas as pd
import csv
import io
from io import StringIO
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta

# Create your views here.
def collate_news():
    stocks=["AAPL", "GOOG", "XOM", "GE", "PFE", "GSK", "PEP", "NSRGY", "GLD", "VOO"]
    for stock in stocks:
        data = get_news(stock)
        output = []
        if data != []:
            for i in range(len(data)):
                unixtimestamp = data[i]['datetime']
                formatted_date = datetime.fromtimestamp(unixtimestamp).strftime("%d %b %Y")
                temp = {'headline' : data[i]['headline'],
                                'image' : data[i]['image'],
                                'summary' : data[i]['summary'],
                                'url' : data[i]['url'],
                                'date' : formatted_date} 
                output.append(temp)
                
    return output

def get_news(ticker, token="bt968tn48v6v8iv1le4g"):
    today = date.today()
    yesterday = today - timedelta(days = 1)
    end_date = today.strftime("%Y-%m-%d")
    start_date = yesterday.strftime("%Y-%m-%d")
    r = requests.get('https://finnhub.io/api/v1/company-news?symbol=%s&from=%s&to=%s&token=%s' % (ticker, start_date, end_date, token))
    return r.json()

def risk_free_rate():
    url="https://tradingeconomics.com/singapore/government-bond-yield"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")

    bond_table = soup.find("table", attrs={"class": "table table-hover sortable-theme-minimal table-heatmap"})
    tags = bond_table.find_all('td', id = "p")
    return tags[0].text

bucket_name = "ode-to-code-2020"
file_name = "portfolio.csv"

client = boto3.client('s3', aws_access_key_id='AKIAV7HVKNFWFUGEYLVU',
        aws_secret_access_key='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')

csv_obj = client.get_object(Bucket=bucket_name, Key=file_name)

body = csv_obj['Body']
csv_string = body.read().decode('utf-8')

df = pd.read_csv(StringIO(csv_string), names = ["Stock", "Weight in Portfolio"], header = 0)

portfolio = df.iloc[3:]
rf = float(risk_free_rate()) / 100
returns = float(df.iat[0,1])
variance = float(df.iat[1,1])

def portfolio_calc(score, portfolio_weight = None, total_returns = None, total_variance = None, portfolio = portfolio):
    portfolio_weight = (returns - rf)/ (score * variance)
    total_returns = rf + portfolio_weight * (returns - rf)
    total_variance = portfolio_weight**2 * variance
    output = ""
    output += "You should put " + str(round((1-portfolio_weight)*100, 2)) + "% of your money in the Singapore 10Y Government Bond.<br>"
    output += "The other " + str(round(portfolio_weight*100, 2)) + "% of your money should go to the following portfolio.<br>"
    output += "==========================================================================<br>"
    output += portfolio.to_html(index = False)
    output += "<br>==========================================================================<br>"
    output += "Total returns: " + str(round(total_returns*100,2)) + "%<br>"
    output += "Total variance: " + str(round(total_variance*100, 2)) + "%<br>"
    output += "<h1>Putting your money in a bank only gets you an annual return of around 1.3% AT MOST! Start investing wisely now!</h1>"
    return output

def risk(request):
    if request.method == "POST":
        form = PortfolioForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']
            return HttpResponse(portfolio_calc(score))

    form = PortfolioForm()
    return render(request, 'risk.html', {'form': form})

def home(request):
    return render(request, 'home.html', {})

def guide(request):
    return render(request, 'guide.html', {})

# def risk(request):
#     return render(request, 'risk.html', {})

def success(request):
    if request.method == "POST":
        form = PortfolioForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']
            return HttpResponse(portfolio_calc(score))
    else:
        return render(request, 'home.html', {})

def news(request):
    mydict = collate_news()
    return render(request, 'news.html', {'mydict' : mydict })
