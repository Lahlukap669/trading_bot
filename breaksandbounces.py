import json
import numpy as np
import pandas as pd

# Open the text file
with open('eth1month10s.txt', 'r') as f:
    # Read the contents of the file
    data = f.read()

# Parse the JSON data
parsed_data = json.loads(data)

def get_breaks_and_bounces(data, sensitivity=1):
    # calculate moving average
    ma = np.mean(data)
    # calculate standard deviation
    std = np.std(data)

    # initialize output arrays
    breaks = np.zeros(len(data))
    bounces = np.zeros(len(data))

    # loop through the data
    for i in range(1, len(data)):
        # check for break
        if data[i] > ma + sensitivity * std and data[i-1] <= ma + sensitivity * std:
            breaks[i] = 1
            bounces[i] = 0
        # check for bounce
        elif data[i] < ma - sensitivity * std and data[i-1] >= ma - sensitivity * std:
            bounces[i] = 1
            breaks[i] = 0
        else:
            bounces[i] = 0
            breaks[i] = 0

    return breaks, bounces

# Assume your data is stored in two arrays: `time` and `value`
#data = np.array([1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1])
#breaks, bounces = get_breaks_and_bounces(data, sensitivity=1)
value=[]
time=[]
for i in range(len(parsed_data["values"])):
    value.append(parsed_data["values"][i]["value"])
    time.append(parsed_data["values"][i]["time"])
    
# Get bounce and break values for each data point
bounce_vals, break_vals = get_breaks_and_bounces(np.array(value))

# Convert boolean arrays to 0/1 arrays
bounce = np.asarray(bounce_vals, dtype=int)
break_ = np.asarray(break_vals, dtype=int)

# Split data for NN training
time_train = time[:-1]
value_train = value[:-1]
bounce_train = bounce[1:]
break_train = break_[1:]


data = {
    "time": time_train,
    "bounce": bounce_train,
    "break": break_train,
    "value": value_train
}
#make me a similar structure as pd dataframe
df = pd.DataFrame(data)
#save df to cvs
df.to_csv('eth1month10s.csv', index=False)