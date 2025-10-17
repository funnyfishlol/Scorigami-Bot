import math
import json
import os
from datetime import datetime

#get current directory to chances.json and scorigami_data.json
current_dir = os.path.dirname(os.path.abspath(__file__))

#gets file path to chances and ScorigamiData
file_path_0 = os.path.join(current_dir, 'chances.json')
file_path_1 = os.path.join(current_dir, 'scorigami_data.json')

#load chances json and ScorigamiData
with open(file_path_0, 'r') as file:
    chances = json.load(file)
with open(file_path_1, 'r') as file:
    matrix = json.load(file)

#get the inner list
matrix_data = matrix["matrix"]

def getProb(quarter, clock, chance):
    """formula for calculating a chance given info"""
    prob = math.exp(-1 * (((4 - quarter) * 15 + (clock / 60.0)) / 60.0 * 4.22)) * math.pow((((4 - quarter) * 15 + (clock / 60.0)) / 60 * 4.22), (chance['td_1pt'] + chance['fg'] + chance['td'] + chance['td_2pt'] + chance['safety'])) / math.factorial(chance['td_1pt'] + chance['fg']+ chance['td']+ chance['td_2pt'] + chance['safety']) * chance['bin_chance']
    return prob

def getChances(quarter, clock, homeScore, awayScore):
    """returns the chances of a scorigami given game info, with the most likely scorigami"""
    probability = 0.0
    most_likely_probability = 0
    most_likely_score = 0

    #create a dictionary based on the matrix
    matrix_dict = {}

    for row in matrix_data: 
        for entry in row:
            if isinstance(entry, dict) and entry.get('count', 0) > 0:
                pts_lose = entry.get('pts_lose')
                pts_win = entry.get('pts_win')
                
                if pts_lose not in matrix_dict:
                    matrix_dict[pts_lose] = {}
                
                matrix_dict[pts_lose][pts_win] = entry

    for i in range(len(chances)):
        chance1 = chances[i]
        prob1 = getProb(quarter, clock, chance1)
        score1 = awayScore + chance1['pts']

        for j in range(len(chances)):
            chance2 = chances[j]
            prob2 = getProb(quarter, clock, chance2)
            score2 = homeScore + chance2['pts']

            if(score1 > score2):
                 winScore = score1
                 loseScore = score2
            else:
                 winScore = score2
                 loseScore = score1
            
            if(loseScore not in matrix_dict or winScore not in matrix_dict[loseScore] or matrix_dict[loseScore][winScore].get("count", 0) == 0):
                if(loseScore == winScore):
                    prob3 = (prob1 * prob2) / 75.0
                else:
                    prob3 = prob1 * prob2
                probability += prob3
                if(prob3>most_likely_probability):
                    most_likely_probability = prob3
                    most_likely_score = f"{winScore} - {loseScore}"
    
    probability = round(probability*100.0, 2)
    return f"{probability}%\nMost likely Scorigami: {most_likely_score}"

def ordinal(n):
    """convert number to ordinal"""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

def getOriginalGame(homeScore, awayScore):
    """"returns a string with info for if a scorigami was reached"""
    if(homeScore > awayScore):
        winScore = homeScore
        loseScore = awayScore
    else:
        winScore = awayScore
        loseScore = homeScore

    #converts date format into new desired format
    if(matrix_data[loseScore][winScore].get("count", 0) == 0):
        matrix["scorigami_count"] += 1
        count = matrix["scorigami_count"]
        updateFile(matrix)
        return f"SCORIGAMI!! This is the {ordinal(count)} unique NFL score!"
    else:
        last_game = matrix_data[loseScore][winScore]
        date = datetime.strptime(last_game['last_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date = date.strftime("%B %d, %Y")
        return f"No Scorigami.\nThis score has been reached {last_game["count"]} times.\nLast game with this score:\n{last_game['last_team_win']} vs {last_game['last_team_lose']}\n{formatted_date}"

def updateFile(matrix_):
    """if a scorigami was reached, write to ScorigamiData.json"""
    matrix_ = json.dumps(matrix_, indent=4)
    with open(file_path_1, "w") as file:
        file.write(matrix_)