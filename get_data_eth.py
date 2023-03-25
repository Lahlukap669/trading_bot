import requests
import json
import time

url = 'https://api.binance.com/api/v3/klines'

params = {
    'symbol': 'ETHUSDT',
    'interval': '1min',
    'endTime': int(time.time()) * 1000,
}

data = []

# retrieve data for the last 3 hours
params['startTime'] = int(time.time() - 10800) * 1000
response = requests.get(url, params=params)
if response.status_code == 200:
    result = response.json()
    for r in result:
        timestamp = int(r[0]) // 1000
        marketcap = float(r[5])
        total_marketcap = float(r[7])
        trading_volume = float(r[8])
        value = float(r[4])
        data.append({
            'timestamp': timestamp,
            'marketcap': marketcap,
            'total_marketcap': total_marketcap,
            'trading_volume': trading_volume,
            'value': value
        })
else:
    print(f"Error: {response.status_code}")

# retrieve data for the rest of the month
params['startTime'] = int(time.time() - 2592000) * 1000
while True:
    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        for r in result:
            timestamp = int(r[0]) // 1000
            marketcap = float(r[5])
            total_marketcap = float(r[7])
            trading_volume = float(r[8])
            value = float(r[4])
            data.append({
                'timestamp': timestamp,
                'marketcap': marketcap,
                'total_marketcap': total_marketcap,
                'trading_volume': trading_volume,
                'value': value
            })
    else:
        print(f"Error: {response.status_code}")
        break
    # check if we have retrieved all the data for the month
    if timestamp < params['startTime'] // 1000:
        break
    # update the start time for the next request
    params['startTime'] = (timestamp + 1) * 1000

# save the data to a text file
with open('eth1month.txt', 'w') as outfile:
    outfile.write('{ "values": [')
    for d in data:
        outfile.write('{'+'"time": '+str(d['timestamp'])+',"marketcap": '+str(d['total_marketcap'])+',"trading_volume": '+str(d['trading_volume'])+', "value": '+str(d['value'])+' },')
    outfile.write("]}")