ticker = "AAPL"

ticker_parameters = {
    "period" : "5d",
    "interval" : "1m",
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

lagged_features_parameters = {
    "close_lags" : "auto",
    "max_lags" : 20,
    "significance_threshold" : 0.1,
}

target_column = "Close"

exclude_columns = [target_column]

# handle_missing can be: drop, fill_mean, fill_median, fill_zero
split_parameters = {
    "split_ratio" : 0.2,
    "handle_missing" : "drop",
    "scaling" : "standard"
}