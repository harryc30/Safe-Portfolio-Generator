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
