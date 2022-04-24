import os
import json

files = os.listdir("data")
files.remove("amount.json")

with open("data/amount.json", "w") as d:
    d.write(json.dumps("0"))

for i in files:
    os.remove(f"data/{i}")