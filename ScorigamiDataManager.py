import requests
import json
import os

url = 'https://nflscorigami.com/data'

#pulls the data from the url using requests
resp = requests.get(url, timeout=10)

#if the site is down, raise
resp.raise_for_status()

#parse data
scorigami_data = json.loads(resp.text)

#fetch directory
script_dir = os.path.dirname(os.path.abspath(__file__))

#get correct file path
file_path = os.path.join(script_dir, "scorigami_data.json")

#write to file
def updateScorigamiData(_scorigami_data):
    """writes the updated scorigami data to scorigami_data.json"""
    _scorigami_data = json.dumps(_scorigami_data, indent=4)
    with open(file_path, "w") as f:
        f.write(_scorigami_data)