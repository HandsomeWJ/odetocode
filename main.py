import pandas as pd
import boto3
import csv
import io
import requests
from io import StringIO
from bs4 import BeautifulSoup

def risk_free_rate():
    url="https://tradingeconomics.com/singapore/government-bond-yield"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")

    bond_table = soup.find("table", attrs={"class": "table table-hover sortable-theme-minimal table-heatmap"})
    tags = bond_table.find_all('td', id = "p")
    return tags[0].text

risk_coefficient = 2 #placeholder value for risk_coefficient, obtained from questionnaire
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

portfolio_weight = (returns - rf)/ (risk_coefficient * variance)
total_returns = rf + portfolio_weight * (returns - rf)
total_variance = portfolio_weight**2 * variance

print("You should put " + str(round((1-portfolio_weight)*100, 2)) + "% of your money in the Singapore 10Y Government Bond.")
print("The other " + str(round(portfolio_weight*100, 2)) + "% of your money should go to the following portfolio.")
print("==========================================================================")
print(portfolio)
print("==========================================================================")
print("Total returns: " + str(round(total_returns*100,2)) + "%")
print("Total variance: " + str(round(total_variance*100, 2)) + "%")

