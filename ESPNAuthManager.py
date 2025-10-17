import requests
import json
import os

url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

headers = {
    "Content-Type": "application/json"
}

#fetches url
response = requests.get(url)

#parse data
curr_data = response.json()

#fetch directory
script_dir = os.path.dirname(os.path.abspath(__file__))

#get correct file path
file_path = os.path.join(script_dir, "livedata.json")

#open file
with open(file_path, 'r') as file:
    old_data = json.load(file)

#write file
def writeESPNData():
    """writes the updated information to livedata.json"""
    live_data = json.dumps(curr_data, indent=4)
    with open(file_path, "w") as f:
        f.write(live_data)
