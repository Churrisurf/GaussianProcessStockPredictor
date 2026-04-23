from functions import *

info, data = fetch_stock_data()
data = add_technical_indicators(data)
data = create_lagged_features(data)
X_train, X_test, y_train, y_test = preprocess_data(data)
