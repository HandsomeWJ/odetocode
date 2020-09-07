#code is adapted from the following article https://medium.com/python-data/effient-frontier-in-python-34b0c3043314

from pandas_datareader import data as web
import pandas as pd
import numpy as np
import investpy
import boto3
from datetime import datetime

def lambda_handler(event, context):

  assets =  ["C6L.SI", "C38U.SI", "ES3.SI", "AAPL", "GOOG", "XOM", "GE", "PFE", "GSK", "PEP", "NSRGY", "GLD", "VOO"]
  # assets = ["C38U.SI", "D05.SI", "S63.SI", "C6L.SI", "QQQ", "XLV", "VNQ", "GDX", "XLF", "XLY", "XLE", "XLI", "XLU", "XLP", "VOX"]

  #Get the stock starting date
  stockStartDate = '2016-06-02'
  # Get the stocks ending date aka todays date and format it in the form YYYY-MM-DD
  today = datetime.today().strftime('%Y-%m-%d')

  #Create a dataframe to store the adjusted close price of the stocks
  df = pd.DataFrame()
  #Store the adjusted close price of stock into the data frame
  for stock in assets:
    df[stock] = web.DataReader(stock,data_source='yahoo',start=stockStartDate , end=today)['Adj Close']

  bonds = ["097023BJ3=", "594918AQ7="]
  bond_obj = []
  for bond in bonds:
    result = investpy.search.search_quotes(bond, products= ["bonds"])
    bond_obj.append(result[0])

  bondStartDate = datetime.strptime(stockStartDate, '%Y-%m-%d').strftime('%d/%m/%Y')
  new_today = datetime.today().strftime('%d/%m/%Y')
  for obj in bond_obj:
    # print(obj.retrieve_historical_data("01/01/2016", "04/09/2020") ["Close"])
    df[obj.name] = obj.retrieve_historical_data(bondStartDate, new_today) ["Close"]
    assets.append(obj.name)

  df = (df.ffill()+df.bfill())/2
  df = df.bfill().ffill()

  returns_daily = df.pct_change()
  returns_annual = returns_daily.mean() * 250

  cov_daily = returns_daily.cov()
  cov_annual = cov_daily * 250

  # empty lists to store returns, volatility and weights of imiginary portfolios
  port_returns = []
  port_volatility = []
  sharpe_ratio = []
  stock_weights = []

  # set the number of combinations for imaginary portfolios
  num_assets = len(assets) 
  num_portfolios = 50000

  #set random seed for reproduction's sake
  np.random.seed(101)

  # populate the empty lists with each portfolios returns,risk and weights
  for single_portfolio in range(num_portfolios):
      weights = np.random.random(num_assets)
      weights /= np.sum(weights)
      returns = np.dot(weights, returns_annual)
      volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
      sharpe = (returns - 0.02) / volatility #assume risk free rate
      sharpe_ratio.append(sharpe)
      port_returns.append(returns)
      port_volatility.append(volatility)
      stock_weights.append(weights)

  # a dictionary for Returns and Risk values of each portfolio
  portfolio = {'Returns': port_returns,
              'Volatility': port_volatility,
              'Sharpe Ratio': sharpe_ratio}

  # extend original dictionary to accomodate each ticker and weight in the portfolio
  for counter,symbol in enumerate(assets):
      portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]

  # make a nice dataframe of the extended dictionary
  data = pd.DataFrame(portfolio)

  # get better labels for desired arrangement of columns
  column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in assets]

  # reorder dataframe columns
  data = data[column_order]

  max_sharpe = data['Sharpe Ratio'].max()

  # use the min, max values to locate and create the two special portfolios
  sharpe_portfolio = data.loc[data['Sharpe Ratio'] == max_sharpe]
  optimal_portfolio = sharpe_portfolio.T
  optimal_portfolio.to_csv('/tmp/portfolio.csv')

  s3 = boto3.resource('s3')
  bucket = s3.Bucket('ode-to-code-2020')
  key = "portfolio.csv"
  bucket.upload_file('/tmp/portfolio.csv', key)
  return {
        'message': 'success!!'
    }
