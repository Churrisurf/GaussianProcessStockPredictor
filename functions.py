import yfinance as yf
import numpy as np
from parameters import *



def fetch_stock_data():
    # Descargamos los datos del ticker que hemos elegido. 
    stock = yf.Ticker(ticker = ticker)

    # Dividimos la información entre información general e información bursatil.
    info, data = stock.info, stock.history(**ticker_parameters)

    return info, data

def add_technical_indicators(data):
    print("Calcular MA20, RSI, MACD, Bollinger, Volatilidad")