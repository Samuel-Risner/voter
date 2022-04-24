import os
files = os.listdir("ready rooms")

for i in files:
    os.remove(f"ready rooms/{i}")