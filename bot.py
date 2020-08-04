import discord
import json
import cassiopeia as cass



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
        challenger_league = cass.get_challenger_league(queue=cass.Queue.ranked_solo_fives)
        


with open("logindata.json") as json_data_file:
    logindata = json.load(json_data_file)
    cass.set_riot_api_key(logindata["riotkey"])
    client.run(logindata["discordkey"])