import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.utils import to_categorical

# Load the data into a pandas dataframe
df = pd.read_csv('eth1month10s.csv', header=None, names=['marketcap', 'volume', 'value', 'bb'])

# Split the data into training and testing sets
train_size = int(len(df) * 0.8)
train_data = df.iloc[1:train_size]
test_data = df.iloc[train_size:]

print(train_data)

# Scale the data
scaler = MinMaxScaler()
train_data = scaler.fit_transform(train_data)
test_data = scaler.transform(test_data)

# Prepare the data for the LSTM model
def create_dataset(data, look_back=1):
    x_data, y_data = [], []
    for i in range(len(data) - look_back):
        x_data.append(data[i:(i + look_back), 0:3])
        y_data.append(data[i + look_back, 3])
    return np.array(x_data), np.array(y_data)

look_back = 50
train_data_x, train_data_y = create_dataset(train_data, look_back)
test_data_x, test_data_y = create_dataset(test_data, look_back)

# Convert the target labels to one-hot encoded format
num_classes = 3
train_data_y = to_categorical(train_data_y, num_classes)
test_data_y = to_categorical(test_data_y, num_classes)

print(train_data_y)

# Define the model architecture
model = Sequential()
model.add(LSTM(units=256, input_shape=(look_back, 3), activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(units=num_classes, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_data_x, train_data_y, epochs=40, validation_split=0.2)

# Get predicted class for each data point
y_pred = model.predict(test_data_x)
y_pred_class = np.argmax(y_pred, axis=1)
print(y_pred_class)

# Save y_pred_class to json file
with open('breaks_bounces.json', 'w') as f:
    json.dump(y_pred_class.tolist(), f)

# Save the model
model.save('breaks_bounces_bot.h5')