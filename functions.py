import yfinance as yf
from parameters import *


def data_fetch():
    # Descargamos los datos del ticker que hemos elegido. 
    stock = yf.Ticker(ticker = ticker)

    # Dividimos la información entre información general e información bursatil.
    stock_info, stock_data = stock.info, stock.history(**ticker_parameters)
