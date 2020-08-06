import cassiopeia as cass
from cassiopeia.core import *
from cassiopeia import Summoner
import json


cass.set_default_region("NA")
with open("logindata.json") as json_data_file:
    logindata = json.load(json_data_file)
    cass.set_riot_api_key(logindata["riotkey"])


def print_leagues():
    challenger = cass.get_challenger_league(queue=cass.Queue.ranked_solo_fives)
    summoner = Summoner(name="Nightblue3", region="NA")
    entries = summoner.league_entries
    participant = summoner.current_match.participants
    for x in participant:
        print("{name} ({rank}) is playing {champion}".format(name = x.summoner.name, champion=x.champion.name, rank=x.summoner.level))



def challenger_leagues():
    zven = "$challenger C9 Zven"
    splits = " ".join(zven.split()[1:len(zven.split())])
    challenger = cass.get_challenger_league(queue=cass.Queue.ranked_solo_fives)
    players = challenger.entries
    i = 1
    playerDict = {}
    for x in players:
        playerDict[x.summoner.name] = x.league_points
    sorteds = sorted(playerDict.items(), key = lambda x: x[1], reverse = True)
    for x in sorteds:
        playerDict[x[0]] = i
        i += 1
    print(playerDict[splits])







if __name__ == "__main__":
    challenger_leagues()