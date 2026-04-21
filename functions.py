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

    def calculate_MA(data):

        # Calculamos la media movil
        data["MA"] = data["close"].rolling(window = MA_interval).mean()

        return data
    
    def calculate_RSI(data):

        # Calculamos los componentes del índice de fuerza relativa
        delta = data["close"].diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window = RSI_interval).mean()
        avg_loss = loss.rolling(window = RSI_interval).mean()

        rs = avg_gain / avg_loss

        # Calculamos el índice de fuerza relativa
        data["RSI"] = 100 - (100 / (1 + rs))

        return data
    
    def calculate_MACD(data):

        # Calculamos los componentes de la convergencia / divergencia de medias moviles
        fast_ema = data["close"].ewn(span = macd_parameters["fast_ema_period"], adjust = False).mean()
        slow_ema = data["close"].ewn(span = macd_parameters["slow_ema_period"], adjust = False).mean()

        #Calculamos el MACD, la señal, y el histograma
        data["MACD"] = fast_ema - slow_ema

        data["Signal"] = data["MACD"].ewm(span = macd_parameters["signal_period"], adjust=False).mean()

        data["MACD_histogram"] = data["MACD"] - data["Signal"]

        return data
    
    print("Calcular MA20, RSI, MACD, Bollinger, Volatilidad")
    
    data = calculate_MA(data)
    data = calculate_RSI(data)
    data = calculate_MACD(data)
    
    return data

    



