import json
import numpy as np
import pandas as pd

# Open the text file
with open('eth1month.txt', 'r') as f:
    # Read the contents of the file
    data = f.read()

# Parse the JSON data
parsed_data = json.loads(data)

def get_breaks_and_bounces(data, window_size=30, sensitivity=1.2):
    # initialize output arrays
    bb = np.zeros(len(data))

    # loop through the data
    for i in range(window_size, len(data)):
        # calculate moving average
        ma = np.mean(data[i-window_size:i])
        # calculate standard deviation
        std = np.std(data[i-window_size:i])

        # check for break
        if data[i] > ma + sensitivity * std and data[i-1] <= ma + sensitivity * std:
            bb[i] = 0
        # check for bounce
        elif data[i] < ma - sensitivity * std and data[i-1] >= ma - sensitivity * std:
            bb[i] = 1
        else:
            bb[i]=-1

    return bb

# Assume your data is stored in two arrays: `time` and `value`
#data = np.array([1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1])
#breaks, bounces = get_breaks_and_bounces(data, sensitivity=1)
value=[]
time=[]
volume=[]
marketcap=[]
for i in range(len(parsed_data["values"])):
    value.append(parsed_data["values"][i]["value"])
    time.append(parsed_data["values"][i]["time"])
    volume.append(parsed_data["values"][i]["trading_volume"])
    marketcap.append(parsed_data["values"][i]["marketcap"])
    
# Get bounce and break values for each data point
bb = get_breaks_and_bounces(np.array(value))

# Convert boolean arrays to 0/1 arrays
bb = np.asarray(bb, dtype=int)


data = {
    "marketcap": marketcap,
    "volume": volume,
    "value": value,
    "bb": bb
    
}
#make me a similar structure as pd dataframe
df = pd.DataFrame(data)
#save df to cvs
df.to_csv('eth1month10s.csv', index=False)

# create new txt file
with open('eth1month10x.txt', 'w') as outfile:
    #pass data for each row (marketcap, volume, value) to the new txt file
    outfile.write('[')
    for i in range (len(parsed_data["values"])):
        outfile.write('['+str(marketcap[i])+','+str(volume[i])+','+str(value[i])+'],')
    outfile.write(']')

with open('eth1month10y.txt', 'w') as outfile:
    #pass data for each row (marketcap, volume, value) to the new txt file
    outfile.write('[')
    for i in range (len(parsed_data["values"])):
        outfile.write(str(bb[i])+',')
    outfile.write(']')