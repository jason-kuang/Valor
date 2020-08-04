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

    if message.content.startswith('$challenger'):
        x = message.content.split()
        summoner = Summoner(name=x[1], region="NA")
        emptyStr = ""
        if (summoner.current_match is not None):
            participant = summoner.current_match.participants
            c = 0
            for x in participant:
                emptyStr += "{name} ({rank}) is playing {champion}\n".format(name=x.summoner.name, champion=x.champion.name, rank=x.summoner.level)
                c += 1
                if c == 5:
                    emptyStr += "\n"
        await message.channel.send(emptyStr)
        


with open("logindata.json") as json_data_file:
    logindata = json.load(json_data_file)
    cass.set_riot_api_key(logindata["riotkey"])
    client.run(logindata["discordkey"])