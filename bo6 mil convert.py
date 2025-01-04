import json

with open("bo6 military tracker info.json", "r") as file:
  data = json.load(file)

for category in data["Weapons"]:
  for weapon in data["Weapons"][category]:
    data["Weapons"][category][weapon] = 0

with open("bo6 military tracker info upload.json", "w") as file:
  json.dump(data, file, indent=2)