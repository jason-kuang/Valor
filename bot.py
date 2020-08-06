import discord
import json
import cassiopeia as cass
from cassiopeia import Summoner


client = discord.Client()
cass.set_default_region("NA")



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
        x = " ".join(message.content.split()[1:len(message.content.split())])
        summoner = Summoner(name=x, region="NA")
        emptyStr = "{name} is not in a match right now!".format(name = x)
        if (summoner.current_match is not None):
            participant = summoner.current_match.participants
            c = 0
            for x in participant:
                emptyStr += "{name} (Level:{rank}) is playing {champion}\n".format(name=x.summoner.name, champion=x.champion.name, rank=x.summoner.level)
                c += 1
                if c == 5:
                    emptyStr += "\n"
        await message.channel.send(emptyStr)

    if message.content.startswith('$challenger'):
        name = " ".join(message.content.split()[1:len(message.content.split())])
        print(name)
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
        returned = "{player} is rank {rank} in the Challenger".format(player=name, rank=playerDict[name])
        await message.channel.send(returned)
        


with open("logindata.json") as json_data_file:
    logindata = json.load(json_data_file)
    cass.set_riot_api_key(logindata["riotkey"])
    client.run(logindata["discordkey"])