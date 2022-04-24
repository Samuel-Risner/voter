import os
files = os.listdir("saved rooms")
files.remove("amount.json")

for i in files:
    os.remove(f"saved rooms/{i}")

with open("saved rooms/amount.json", "w") as d:
    d.write("0")