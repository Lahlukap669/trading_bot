from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
#from tensorflow.keras import layers
from sklearn.preprocessing import MinMaxScaler

import json

# Open csv file and load it into pandas dataframe
df = pd.read_csv('eth1month10s.csv')

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

# Define the model architecture
model = Sequential()
model.add(LSTM(units=64, input_shape=(1, 4), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=128, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=256))
model.add(Dense(units=1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy')

# Train the model
model.fit(train_data, train_data[:, :, 3], epochs=50, validation_split=0.2)

# Get binary values for each data point
y_pred = model.predict(test_data)
y_pred_binary = (y_pred > 0.5).astype(int)
#print(y_pred_binary)
model.save('my_model.h5')


