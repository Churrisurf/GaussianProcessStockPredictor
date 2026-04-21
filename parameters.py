ticker = "AAPL"

# auto_adjust debe ser True para tener en cuenta los dividendos y los desdoblamientos de acciones
ticker_parameters = {
    "period" : "5d",
    "interval" : "1m",
    "auto_adjust" : True
}

MA_interval = 20
RSI_interval = 14

macd_parameters = {
    "fast_ema_interval" : 12,
    "slow_ema_interval" : 26,
    "signal_interval" : 9
}

bollinger_parameters = {
    "interval" : 20,
    "deviations" : 2 
}

volatility_interval = 20

graph_interval = 100