import discord
import json
import cassiopeia as cass
from cassiopeia import Summoner


client = discord.Client()
cass.set_default_region("NA")


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
        with open('champions/{champion}.json'.format(champion=name), encoding="utf8") as champData:
            data = json.load(champData)
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
        print("Returned champion data for {champ}".format(champ=name))
        await message.channel.send(P + Q + W + E + R)
        


with open("logindata.json") as json_data_file:
    logindata = json.load(json_data_file)
    cass.set_riot_api_key(logindata["riotkey"])
    client.run(logindata["discordkey"])