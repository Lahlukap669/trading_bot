import json

# Open the text file
with open('eth1month10s.txt', 'r') as f:
    # Read the contents of the file
    data = f.read()

# Parse the JSON data
parsed_data = json.loads(data)

for i in parsed_data["values"]:
    print(i["time"], ":",i["value"])
