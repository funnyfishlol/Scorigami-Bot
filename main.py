from XAuthManager import x_client
from ESPNAuthManager import old_data, curr_data, writeESPNData
from ScorigamiManager import getChances, getOriginalGame
from ScorigamiDataManager import scorigami_data, updateScorigamiData

def updateGames():
    """checks through every nfl game to see if quarter has changed. if it has, tweet out info for if the game is over or still going"""
    for i in range(0, len(old_data["events"]), 1):
        event = curr_data["events"][i]

        #check if quarter has changed and its not a completely new game
        if(event["status"]["period"] != old_data["events"][i]["status"]["period"] and not event["status"]["type"]["name"] == "STATUS_SCHEDULED"):

            #format tweet
            return_string = ""
            abbreviation_1 = event["competitions"][0]["competitors"][0]["team"]["abbreviation"]
            score_1 = event["competitions"][0]["competitors"][0]["score"]
            abbreviation_2 = event["competitions"][0]["competitors"][1]["team"]["abbreviation"]
            score_2 = event["competitions"][0]["competitors"][1]["score"]
            quarter = event["status"]["period"]
            
            #return message for if the game has ended or if the game is still going
            if(event["status"]["type"]["name"] == "STATUS_FINAL"):
                return_string += f"Final: {abbreviation_1} {score_1} - {abbreviation_2} {score_2}"
                return_string += f"\n{getOriginalGame(int(score_1), int(score_2))}"
            else:
                return_string += f"Score Update:\n{abbreviation_1} {score_1} - {abbreviation_2} {score_2}"
                return_string += f"\nStart of Q{quarter}"
                return_string += f"\nScorigami Probability: {getChances(quarter, event["status"]["clock"], int(score_1), int(score_2))}"
            print(return_string)
            #x_client.create_tweet(text=return_string)

updateGames()
updateScorigamiData(scorigami_data)
writeESPNData()