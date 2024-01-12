from IPython.display import display, Math, Latex

import pandas as pd
import numpy as np
import numpy_financial as npf
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import random

def get_average__monthly_volume(stock_volume):
    # # get the ticker
    # ticker = yf.Ticker(ticker_symbol)
    # # get the stock data
    # stock_data = ticker.history(start='2023-01-01', end='2023-10-31')

    # # Resample data to monthly frequency and calculate average volume
    # stock_volume = stock_data['Volume']
    # Resample data to monthly frequency and calculate the number of trading days per month
    trading_days_per_month = stock_volume.resample('M').count()

    # Filter out months with less than 18 trading days
    valid_months = trading_days_per_month[trading_days_per_month >= 18]

    # Filter the stock data for the valid months
    stock_volume = stock_volume[stock_volume.index.month.isin(valid_months.index.month)]

    # return the result
    return stock_volume.sum()/len(valid_months)
def validtickers(df):
    ticker_lst = []
    ##start and end dates to check if the ticker is avaliable in those times
    start_date = '2023-01-01'
    end_date = '2023-10-01'
    ##in case there's no title and the column title is a ticker (so in the ticker_example.csv, the title was AAPL, which is a ticker)
    try:
        ticker = df.columns[0]
        stock = yf.Ticker(ticker)
        ##get historical data from it
        history = stock.history(start=start_date, end=end_date)
        ##if it is a valid ticker, this would run and if it hits the requirements, it appends the ticker to the tickerlist
        if ((stock.fast_info['currency'] == "CAD" or stock.fast_info['currency'] == "USD") and (get_average__monthly_volume(history['Volume']) > 150000)): # added my function here
          ticker_lst.append(df.columns[0])
          x = 0
        else:
          ##otherwise, it's not a ticker that hits the requirements,
          print('not a valid stock')
          x = 0
    except:
      ##if the code outputs an error, the ticker isn't valid, so outputs not a ticker
        print('not a ticker')
        x = 0
    while x < len(df):
      ##for the rest of the column, exactly the same process as above, try getting an output from the ticker, and if it doesn't work, go next
        try:
            ticker = df.iloc[x,0]
            stock = yf.Ticker(ticker)
            history = stock.history(start=start_date, end=end_date)
            if ((stock.fast_info['currency'] == 'CAD' or stock.fast_info['currency'] == 'USD') and (get_average__monthly_volume(history['Volume']) > 150000)):
             ticker_lst.append(df.iloc[x,0])
             x += 1
            else:
              print('not a valid stock')
              x += 1
        except:
            print('not a ticker')
            x += 1

    return ticker_lst
    ##return random.sample(ticker_lst, random.randint(10,22))

tickerlist = validtickers(pd.read_csv('Tickers.csv'))
print(tickerlist)

stock_currency = pd.DataFrame({'Ticker':[],
                         'Currency':[]})
for i in tickerlist:
  tempdf = pd.DataFrame(columns=['Ticker','Currency'])
  temp = yf.Ticker(i)
  tempdf['Ticker'] = [i]
  ##Code for industry if avaliable
  tempdf['Currency'] = [temp.fast_info['currency']]
  stock_currency = pd.concat([stock_currency, tempdf],ignore_index=True)
