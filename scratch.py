#import cassiopeia as cass
#from cassiopeia.core import *
#from cassiopeia import Summoner, ShardStatus
import os.path
from objects import Champion
import urllib.request
from os import path
import json


# Everything written in here is generally my first attempt at getting things to work. I also do my testing here because restarting the bot to allow it to make changes takes too long.
# I wouldn't stay in this file for too long. You might get a headache from me. Have fun! :)'


#cass.set_default_region("NA")

with open("logindata.json") as json_data_file:
    logindata = json.load(json_data_file)
    #cass.set_riot_api_key(logindata["riotkey"])


# def print_leagues():
#     challenger = cass.get_challenger_league(queue=cass.Queue.ranked_solo_fives)
#     summoner = Summoner(name="Nightblue3", region="NA")
#     entries = summoner.league_entries
#     participant = summoner.current_match.participants
#     for x in participant:
#         print("{name} ({rank}) is playing {champion}".format(name = x.summoner.name, champion=x.champion.name, rank=x.summoner.level))



# def challenger_leagues():
#     # I dislike this library. I would like to write my own perhaps.
#     zven = "$challenger C9 Zven"
#     splits = " ".join(zven.split()[1:len(zven.split())])
#     challenger = cass.get_challenger_league(queue=cass.Queue.ranked_solo_fives)
#     players = challenger.entries
#     i = 1
#     playerDict = {}
#     for x in players:
#         playerDict[x.summoner.name] = x.league_points
#     sorteds = sorted(playerDict.items(), key = lambda x: x[1], reverse = True)
#     for x in sorteds:
#         playerDict[x[0]] = i
#         i += 1
#     print(playerDict[splits])

# def shard():
#     summoner = Summoner(name="GibIe",region="NA")
#     rank = str(summoner.league_entries[0].tier) + ' ' + str(summoner.league_entries[0].division)
#     print(rank)

def champions(name):
    name = name.capitalize().replace(" ", "")
    with open('champions/{champion}.json'.format(champion=name), encoding="utf8") as champData:
        data = json.load(champData)
        #print(data['data'][name]['spells'][3])
        champQ = data['data'][name]['spells'][0]
        champW = data['data'][name]['spells'][1]
        champE = data['data'][name]['spells'][2]
        champR = data['data'][name]['spells'][3]
        champPassive = data['data'][name]['passive']
        P = "Passive: {name} - {description}\n".format(name=champPassive['name'],description=champPassive['description'])
        Q = "Q: {name} - {description} | {cooldownBurn}\n".format(name=champQ['name'],description=champQ['description'], cooldownBurn=champQ['cooldownBurn'])
        W = "W: {name} - {description} | {cooldownBurn}\n".format(name=champW['name'],description=champW['description'], cooldownBurn=champW['cooldownBurn'])
        E = "E: {name} - {description} | {cooldownBurn}\n".format(name=champE['name'],description=champE['description'], cooldownBurn=champE['cooldownBurn'])
        R = "R: {name} - {description} | {cooldownBurn}\n".format(name=champR['name'],description=champR['description'], cooldownBurn=champR['cooldownBurn'])
        print(P + Q + W + E + R)


def fileTesting(name):
    url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion}.json".format(version="10.16.1", champion=name)
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
        with open("testingDir/{champion}.json".format(champion=name), "w") as output:
            json.dump(data,output)

def champTesting(name):
    champ = Champion.Champion("Yone")
    abilities = champ.abilities()
    print(str(abilities["PASSIVE"].description))


if __name__ == "__main__":
    champTesting("Yone")