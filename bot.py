import discord
import json
import cassiopeia as cass
import urllib.request
import os.path
from os import path
from objects import Ability, Champion
from cassiopeia import Summoner


client = discord.Client()
cass.set_default_region("NA")

# Check for any updates within the league client.
with urllib.request.urlopen("https://ddragon.leagueoflegends.com/api/versions.json") as url:
    data = json.load(url)
    with open("currentversion.json") as versionNum:
        version = json.load(versionNum)
    #If there's a new version, update the version.
    if version["version"] != data[0]:
        version["version"] = data[0]
        with open("currentversion.json", "w") as output:
            json.dump(version, output)



def extractNames(message):
    # I feel like [1:-1] should be working here but it's not?
    summoner = " ".join(message.content.split()[1:len(message.content.split())])
    return summoner

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$match'):
        x = extractNames(message)
        summoner = Summoner(name=x, region="NA")
        emptyStr = "{name} is not in a match right now!".format(name = x)
        if summoner.current_match is not None:
            participant = summoner.current_match.participants
            c = 0
            emptyStr = "{type} {time}\n".format(type=summoner.current_match.queue.name, time= summoner.current_match.duration)
            for x in participant:
                emptyStr += "{name} ({rank}) is playing {champion}\n".format(name=x.summoner.name, champion=x.champion.name, rank = str(x.summoner.league_entries[0].tier) + ' ' + str(x.summoner.league_entries[0].division))
                c += 1
                if c == 5:
                    emptyStr += "\n"
        await message.channel.send(emptyStr)

    if message.content.startswith('$challenger'):
        name = extractNames(message)
        challenger = cass.get_challenger_league(queue=cass.Queue.ranked_solo_fives)
        players = challenger.entries
        i = 1
        playerDict = {}
        for x in players:
            playerDict[x.summoner.name] = x.league_points
        sorteds = sorted(playerDict.items(), key=lambda x: x[1], reverse=True)
        for x in sorteds:
            playerDict[x[0]] = i
            i += 1
        #with open('challengers.txt','r') as rankings:
           # rank = json.load(rankings)
            #if playerDict[rankings.keys] !=
        with open('challengers.txt','w') as outfile:
            json.dump(playerDict,outfile)
        returned = "{player} is rank {rank} in Challenger queue!".format(player=name, rank=playerDict[name])
        await message.channel.send(returned)

    if message.content.startswith('$champion'):
        name = extractNames(message).title().replace(" ", "")
        if name == "Wukong":
            name = "MonkeyKing"
        champion = Champion.Champion(name)
        if (not path.exists("champions/{champion}.json".format(champion=name))) or champion.version() != version["version"]:
            print(version["version"])
            print (champion.version())
            champion.update()
        abilities = champion.abilities()
        P = "Passive: {name} - {description}\n".format(name=abilities["PASSIVE"].name,description=abilities["PASSIVE"].description)
        Q = "Q: {name} - {description} | Cooldown: {cooldownBurn}\n".format(name=abilities["Q"].name,description=abilities["Q"].description, cooldownBurn=abilities["Q"].cooldown)
        W = "W: {name} - {description} | Cooldown: {cooldownBurn}\n".format(name=abilities["W"].name,description=abilities["W"].description, cooldownBurn=abilities["W"].cooldown)
        E = "E: {name} - {description} | Cooldown: {cooldownBurn}\n".format(name=abilities["E"].name,description=abilities["E"].description, cooldownBurn=abilities["E"].cooldown)
        R = "R: {name} - {description} | Cooldown: {cooldownBurn}\n".format(name=abilities["R"].name,description=abilities["R"].description, cooldownBurn=abilities["R"].cooldown)
        print("Returned champion data for {champ}".format(champ=name))
        await message.channel.send(P + Q + W + E + R)
        


with open("logindata.json") as json_data_file:
    logindata = json.load(json_data_file)
    cass.set_riot_api_key(logindata["riotkey"])
    client.run(logindata["discordkey"])