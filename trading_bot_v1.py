### Import necessary libraries
##import pandas as pd
##import numpy as np
##from keras.models import load_model
##
### Load the saved model
##model = load_model('my_model.h5')
##
### Load historical price data for ETH
##data = pd.read_json('eth_price_data.json')
##
### Define the input features for the model
##input_features = ['price', 'volume', 'sentiment']
##
### Define a function to preprocess input data
##def preprocess_data(data):
##    # Convert data to numpy array
##    data = data[input_features].values
##    
##    # Normalize the data
##    data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
##    
##    # Reshape the data for input to the model
##    data = np.reshape(data, (1, -1))
##    
##    return data
##
### Define a function to make a prediction using the model
##def predict_price(model, data):
##    # Preprocess the input data
##    data = preprocess_data(data)
##    
##    # Use the model to make a prediction
##    prediction = model.predict(data)[0][0]
##    
##    return prediction
##
### Define a function to execute trades based on the model prediction
##def execute_trade(prediction):
##    # If the predicted price is greater than the current price, buy ETH
##    if prediction > data['price'].iloc[-1]:
##        # Place a buy order on the exchange
##        buy_order = exchange.place_order('buy', 'eth', 'usd', 100)
##        print('Placed buy order for 100 ETH at', data['price'].iloc[-1], 'USD per ETH.')
##        
##    # If the predicted price is less than the current price, sell ETH
##    elif prediction < data['price'].iloc[-1]:
##        # Place a sell order on the exchange
##        sell_order = exchange.place_order('sell', 'eth', 'usd', 100)
##        print('Placed sell order for 100 ETH at', data['price'].iloc[-1], 'USD per ETH.')
##        
##    # Otherwise, do nothing
##    else:
##        print('No trade executed.')
##
### Make a prediction using the model
##prediction = predict_price(model, data)
##
### Execute a trade based on the model prediction
##execute_trade(prediction)




from keras.models import load_model
from keras.layers import LSTM
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the model
model = load_model('my_model.h5')

# Open csv file and load it into pandas dataframe
df = pd.read_csv('eth1month10s.csv')

# Add a new column for the target variable (Close)
df['value'] = df['value']

# Split the data into training and testing sets
train_size = int(len(df) * 0.8)
train_data = df[:train_size]
test_data = df[train_size:]

# Scale the data
scaler = MinMaxScaler()
train_data = scaler.fit_transform(train_data)
test_data = scaler.transform(test_data)

# Reshape the input data to have 3 dimensions
train_data = train_data.reshape(-1, 1, 4)
test_data = test_data.reshape(-1, 1, 4)

# Evaluate the model
mse = model.evaluate(test_data[:, :, :3], test_data[:, :, 3])
print('Mean Squared Error:', mse)

# Make predictions on test data
predictions = model.predict(test_data[:, :, :3])
predictions = np.concatenate((test_data[:, :, :3], predictions), axis=2)
predictions = scaler.inverse_transform(predictions.reshape(-1 ,4))[:, 3]
print(predictions)


##import os
##from binance.client import Client
##from binance.enums import *
##
##api_key = os.environ.get('BINANCE_API_KEY')
##api_secret = os.environ.get('BINANCE_API_SECRET')
##
##client = Client(api_key, api_secret)
##
### Example: Place a test order to buy 1 BTC at 40000 USDT
##try:
##    order = client.create_test_order(
##        symbol='BTCUSDT',
##        side=SIDE_BUY,
##        type=ORDER_TYPE_LIMIT,
##        timeInForce=TIME_IN_FORCE_GTC,
##        quantity=1,
##        price='40000')
##    print("Test order successfully placed.")
##except Exception as e:
##    print(e)
