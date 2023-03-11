##import requests
##
##url = 'https://api.binance.com/api/v3/klines'
##
##params = {
##    'symbol': 'ETHUSDT',
##    'interval': '1d',
##    'startTime': '0'
##}
##
##response = requests.get(url, params=params)
##
##if response.status_code == 200:
##    data = response.json()
##    for d in data:
##        print(f"{d[0]} - {d[4]}")
##else:
##    print(f"Error: {response.status_code}")


##import requests
##import time
##
##url = 'https://api.binance.com/api/v3/klines'
##
##params = {
##    'symbol': 'ETHUSDT',
##    'interval': '1m',
##    'startTime': int(time.time() - 2592000) * 1000,  # 2592000 seconds = 30 days
##    'endTime': int(time.time()) * 1000,
##}
##
##response = requests.get(url, params=params)
##
##if response.status_code == 200:
##    data = response.json()
##    i=0
##    for d in data:
##        timestamp = int(d[0]) // 1000  # convert timestamp to seconds
##        value = float(d[4])
##        if timestamp % 1 == 0:  # display data every 1 seconds
##            print(i, f"{timestamp} - {value}")
##        i+=1
##else:
##    print(f"Error: {response.status_code}")


import requests
import json
import time

#f = open("eth1month10s.txt", "w")
#f.close()

url = 'https://api.binance.com/api/v3/klines'

params = {
    'symbol': 'ETHUSDT',
    'interval': '1m',
    'endTime': int(time.time()) * 1000,
}

timestamps = []
values = []

# retrieve data for the last 3 hours
params['startTime'] = int(time.time() - 10800) * 1000
response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    for d in data:
        timestamps.append(int(d[0]) // 1000)
        values.append(float(d[4]))
else:
    print(f"Error: {response.status_code}")

# retrieve data for the rest of the month
params['startTime'] = int(time.time() - 2592000) * 1000  # 2592000 seconds = 30 days
while True:
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        for d in data:
            timestamp = int(d[0]) // 1000
            value = float(d[4])
            timestamps.append(timestamp)
            values.append(value)
    else:
        print(f"Error: {response.status_code}")
        break
    # check if we have retrieved all the data for the month
    if timestamp < params['startTime'] // 1000:
        break
    # update the start time for the next request
    params['startTime'] = (timestamp + 1) * 1000

# print the data every 10 seconds
#f = open("eth1month10s.txt", "a")
#f.write('{"values":[')



for i in range(len(timestamps)):
    if timestamps[i] % 10 == 0:
        print(f"{timestamps[i]} - {values[i]}")
        #f.write('{ "time":'+str(timestamps[i])+', "value":'+str(values[i])+' },')
        #save the timestamps and values to a json file
        data = {
            'timestamps': timestamps,
           'values': values,
        }
        with open('eth1month10s.json', 'a') as outfile:
            json.dump(data, outfile)

#f.write(']}')
#f.close()
