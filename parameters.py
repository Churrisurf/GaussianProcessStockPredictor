ticker = "AAPL"

# auto_adjust debe ser True para tener en cuenta los dividendos y los desdoblamientos de acciones
ticker_parameters = {
    "period" : "5d",
    "interval" : "1m",
    "auto_adjust" : True
}

# intervalo de la media movil y el índice de fuerza relativa
MA_interval = 20
RSI_interval = 14

macd_parameters = {
    "fast_ema_period" : 12,
    "slow_ema_period" : 26,
    "signal_period" : 9
}