import discord
import json
import cassiopeia as cass
import urllib.request
import os.path
from os import path
from objects import Ability, Champion
from cassiopeia import Summoner
import re

client = discord.Client()
cass.set_default_region("NA")

# Check for any updates within the league client.
# If there is an update, it will replace currentversion.json with the new version.
# This also means that the global variable of version will correspond to the new version.
# In doing so, the rest of the commands will know there is a new version.
with urllib.request.urlopen("https://ddragon.leagueoflegends.com/api/versions.json") as url:
    data = json.load(url)
    with open("currentversion.json") as versionNum:
        version = json.load(versionNum)
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
    # Stops an infinite loop of the bot talking to itself.
    if message.author == client.user:
        return

    # Returns info about a match somebody is playing. It will return one line for each player each containing a {name} {rank} is playing {champion}
    if message.content.startswith('$match'):
        IGN = extractNames(message)
        summoner = Summoner(name=IGN, region="NA")
        emptyStr = "{name} is not in a match right now!".format(name = IGN)
        if summoner.current_match is not None:
            participant = summoner.current_match.participants
            c = 0
            emptyStr = "{type} {time}\n".format(type=summoner.current_match.queue.name, time= summoner.current_match.duration)
            for IGN in participant:
                try:
                    rank =  str(IGN.summoner.league_entries[0].tier) + ' ' + str(IGN.summoner.league_entries[0].division)
                except IndexError:
                    rank = IGN.summoner.level
                emptyStr += "{name} ({rank}) is playing {champion}\n".format(name=IGN.summoner.name, champion=IGN.champion.name, rank = rank)
                c += 1
                if c == 5:
                    emptyStr += "\n"
        await message.channel.send(emptyStr)

    # League of Legends has a ranking system where a Challenger is of the highest level. Only 300 players or so are allowed at a time.
    # Not only are 300 players allowed, they must constantly fight for their place and play a minimum of one game a week.
    # If somebody surpasses them in League Points (LP) which are gained by winning, they are a higher rank of Challenger.
    # This command, given somebody's in game name and if they are in Challenger, will return their current place in the leaderboard.
    if message.content.startswith('$challenger'):
        name = extractNames(message)
        challenger = cass.get_challenger_league(queue=cass.Queue.ranked_solo_fives)
        players = challenger.entries
        i = 1
        playerDict = {}
        for IGN in players:
            playerDict[IGN.summoner.name] = IGN.league_points
        sorteds = sorted(playerDict.items(), key=lambda x: x[1], reverse=True)
        for IGN in sorteds:
            playerDict[IGN[0]] = i #playerDict["IGN"] -> rank
            i += 1
        with open('challengers.txt','w') as outfile:
            json.dump(playerDict,outfile)
        returned = "{player} is rank {rank} in Challenger queue!".format(player=name, rank=playerDict[name])
        await message.channel.send(returned)

    # This command returns data from the Riot DataDragon API that will show a quick breakdown for a requested champion.
    # The command is utilized as $champion "Ashe" and will return you her Passive, and her four abilities broken down along with a cooldown.
    # This command was created mainly because I keep Discord up on my second monitor and checking my opposing player's cooldowns is now easier.
    # This command is also the first command that takes advantage of self-updating.
    if message.content.startswith('$champion'):
        mispellings = {"Wukong": "MonkeyKing", "J4": "JarvanIV", "Jarvan IV": "JarvanIV", "Kai'sa": "Kaisa", "Cho'Gath": "Chogath", "j4": "JarvanIV"}
        name = extractNames(message).title().replace(" ", "")
        if mispellings.get(name) is not None:
            name = mispellings[name]
        print(name)
        re.sub(r'\W+', '', name)
        champion = Champion.Champion(name)
        if (not path.exists("champions/{champion}.json".format(champion=name))) or champion.version() != version["version"]:
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