import json

# Your data (Python dict)
data = {
    "name": "Pranav",
    "time": "10:30 AM"
}

# Create (or overwrite) a JSON file and write data
with open("data3.json", "w") as f:
    json.dump(data, f, indent=4)  # indent=4 makes it pretty


data2= {
    "name": "aadhi",
    "time": "11:30 AM"
}
jsondata = []

with open("data3.json","r") as f:
    jsondata=[json.load(f)]

jsondata.append(data2)

with open("data3.json", "w") as f:
    json.dump(jsondata, f, indent=4)  # indent=4 makes it pretty