import yfinance as yf
import numpy as np
import pandas as pd
import mplfinance as mpf
from typing import Union, List, Optional
from parameters import *
from statsmodels.tsa.stattools import pacf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

def fetch_stock_data():

    # Descargamos los datos del ticker que hemos elegido. 
    stock = yf.Ticker(ticker = ticker)

    # Dividimos la información entre información general e información bursatil.
    info, data = stock.info, stock.history(**ticker_parameters, auto_adjust = True)

    return info, data

def add_technical_indicators(data):

    def calculate_MA(data):

        # Calculamos la media movil
        data["MA"] = data["Close"].rolling(window = MA_interval).mean()

        return data
    
    def calculate_RSI(data):

        # Calculamos los componentes del índice de fuerza relativa
        delta = data["Close"].diff()

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
        fast_ema = data["Close"].ewm(span = macd_parameters["fast_ema_interval"], adjust = False).mean()
        slow_ema = data["Close"].ewm(span = macd_parameters["slow_ema_interval"], adjust = False).mean()

        #Calculamos el MACD, la señal, y el histograma
        data["MACD"] = fast_ema - slow_ema

        data["Signal"] = data["MACD"].ewm(span = macd_parameters["signal_interval"], adjust=False).mean()

        data["MACD_histogram"] = data["MACD"] - data["Signal"]

        return data
    
    def calculate_Bollinger_Bands(data):

        # Calculamos la banda central
        data["BB_middle"] = data["Close"].rolling(window = bollinger_parameters["interval"]).mean()
        
        # Calculamos la banda superior e inferior
        std_dev = data["Close"].rolling(window = bollinger_parameters["interval"]).std()

        data["BB_upper"] = data["BB_middle"] + (std_dev * bollinger_parameters["deviations"])
        data["BB_lower"] = data["BB_middle"] - (std_dev * bollinger_parameters["deviations"])
        
        return data
    
    def calculate_Volatility(data):

        # Calculamos los retornos de cada registro
        data["Returns"] = data["Close"].pct_change()

        # Calculamos la volatilidad
        data["Volatility"] = data["Returns"].rolling(window = volatility_interval).std()

        return data

    data = calculate_MA(data)
    data = calculate_RSI(data)
    data = calculate_MACD(data)
    data = calculate_Bollinger_Bands(data)
    data = calculate_Volatility(data)

    return data

def graph_data(data):

    # Creamos el gráfico de velas japonesas
    mpf.plot(data[-graph_interval:], type = "candle", volume = False, style = "charles", title = "Candlestick Chart", ylabel = "Price")

def create_lagged_features(data):

    # Si auto, se crean los lags óptimos
    if lagged_features_parameters["close_lags"] == "auto":

        # Calculamos la correlación entre los lags y Close
        pacf_values = pacf(data["Close"], nlags = lagged_features_parameters["max_lags"], method = 'ywm')
        
        # Guardamos los lags más significativos por encima del umbral
        significant_lags = []
        for i, pacf_val in enumerate(pacf_values[1:], start = 1):
            if abs(pacf_val) > lagged_features_parameters["significance_threshold"]:
                significant_lags.append(i)
        
        if not significant_lags:

            #Si no hay logs significativo, se cogen los 5 últimos por defecto
            lag_list = list(range(1,6))

        else:
            
            # Guardamos los 10 relevantes más recientes máximo
            lag_list = significant_lags[:10]
                
    # Si un número n, se cogen los n últimos lags
    elif isinstance(lagged_features_parameters["close_lags"], int):
        lag_list = list(range(1, lagged_features_parameters["close_lags"] + 1))

    # Si una lista, se cogen esos lags
    elif isinstance(lagged_features_parameters["close_lags"], list):
        lag_list = lagged_features_parameters["close_lags"]
    
    # Creamos los lags
    for lag in lag_list:
        col_name = f'Close_lag_{lag}'
        data[col_name] = data["Close"].shift(lag)

    # Eliminamos las filas con NaN (normalmente las primeras)
    data = data.dropna()
    
    return data

def preprocess_data(data):
    
    # Seleccionamos las columnas de características
    feature_columns = [col for col in data.columns if col not in exclude_columns and data[col].dtype in ['float64', 'int64']]
    
    # Gestionamos los valores nulos
    if split_parameters["handle_missing"] == 'drop':
        data = data.dropna()
        
    elif split_parameters["handle_missing"] == 'fill_mean':
        X = X.fillna(X.mean())
        
    elif split_parameters["handle_missing"] == 'fill_median':
        X = X.fillna(X.median())
        
    elif split_parameters["handle_missing"] == 'fill_zero':
        X = X.fillna(0)
    
    # Elegimos las columnas de entrada y de objetivo
    X = data[feature_columns]
    y = data[target_column]

    # Dividimos nuestros datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = split_parameters["split_ratio"], shuffle = False)
    
    # Escalamos nuestros datos conforme al método seleccionado
    scaler = None

    if split_parameters["scaling"] == 'standard':
        scaler = StandardScaler()
        X_train = pd.DataFrame(scaler.fit_transform(X_train), columns = X_train.columns, index = X_train.index)
        X_test = pd.DataFrame(scaler.transform(X_test), columns = X_test.columns, index = X_test.index)
        
    elif split_parameters["scaling"] == 'minmax':
        scaler = MinMaxScaler()
        X_train = pd.DataFrame(scaler.fit_transform(X_train), columns = X_train.columns, index = X_train.index)
        X_test = pd.DataFrame(scaler.transform(X_test), columns = X_test.columns, index = X_test.index)
        
    elif split_parameters["scaling"] == 'robust':
        scaler = RobustScaler()
        X_train = pd.DataFrame(scaler.fit_transform(X_train), columns = X_train.columns, index = X_train.index)
        X_test = pd.DataFrame(scaler.transform(X_test), columns = X_test.columns, index = X_test.index)
    
    return X_train, X_test, y_train, y_test


    