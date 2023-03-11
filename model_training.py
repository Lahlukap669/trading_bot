from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import numpy as np
import tensorflow as tf
from tensorflow import keras
#from tensorflow.keras import layers
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

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

# get values from train_data
time = np.array(train_data[:, 0:1])
marketcap = np.array(train_data[:, 1:2])
volume = np.array(train_data[:, 2:3])
values = np.array(train_data[:, 3:4])
breaks = np.array(train_data[:, 4:5])
bounces = np.array(train_data[:, 5:6])

# get values from test_data
time1 = np.array(test_data[:, 0:1])
marketcap1 = np.array(test_data[:, 1:2])
volume1 = np.array(test_data[:, 2:3])
values1 = np.array(test_data[:, 3:4])
breaks1 = np.array(test_data[:, 4:5])
bounces1 = np.array(test_data[:, 5:6])

train_data_x = np.concatenate([marketcap, volume, values], axis=1).reshape(1, len(time), 3)
train_data_y = np.concatenate([breaks, bounces], axis=1).reshape(1, len(breaks), 2)

test_data = np.concatenate([time1, marketcap1, volume1, values1])

# Define the model architecture
model = Sequential()
model.add(LSTM(units=64, input_shape=(None, 150, 4), activation='relu'))
model.add(Dropout(0.2))
model.add(LSTM(units=128, activation='relu'))
model.add(Dropout(0.2))
model.add(LSTM(units=256, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(units=2, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_data_x, train_data_y, epochs=40, validation_split=0.2)

# Get binary values for each data point
y_pred = model.predict(test_data)
y_pred_binary = (y_pred > 0.5).astype(int)
print(y_pred)
# save y_pred_binary to json file
with open('breaks_bounces.json', 'w') as f:
    json.dump(y_pred_binary.tolist(), f)

model.save('breaks_bounces_bot.h5')


