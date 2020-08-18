# Valor - League of Legends Discord Bot

Valor is a bot that utilizes Riot Game's API for their game League of Legends.

The bot was a project that came out of me always having Discord on my second monitor and wishing I could see what the enemy champion's abilities are.  

This bot supports a few commands (more to come!) that help you track your friends, and help you play the game optimally.   

Valor is written entirely in Python and is also self-updating for all its data so that its return values for champion cooldowns are never outdated when Riot patches the game.

## Using the bot

Invite the Discord bot to your server by clicking [here!](https://discord.com/api/oauth2/authorize?client_id=740037528953815090&permissions=228352&scope=bot)

### Commands

```
$match ingameName
```
This command will return you the breakdown of <ingameName's> match that displays all ten players of the match based on side along with their rank and the Champion that they are playing.

```
$champion championName
```
This command returns you up-to-date information on all four abilities of a champion. It also includes their cooldowns and a brief description of the actual ability.

```
$challenger ingameName
```
This command will return you the current rank of a player in Challenger ranking. There can only be 300 players in this ranking at all time.

### Visuals
![Alt Text](https://media.giphy.com/media/S6fmx8tBqTFSlJMZ3c/giphy.gif)


![Alt Text](https://media.giphy.com/media/MFaiv2uXZ2DGtNxSKL/giphy.gif)


## Extra Misc. Notes

Valor is written in Python utilizing the [discord.py](https://github.com/Rapptz/discord.py) and the [cassiopeia](https://github.com/meraki-analytics/cassiopeia/tree/master/cassiopeia) wrapper.

This will be subject to change.

Interesting issue's I've run into: Input sanitization. I didn't want to worry if typing the champion name without capitals and there's also very commonly used abbreviations
for champion names. For example, Jarvan IV ingame is usually known as j4 to players and I wanted it to work with that too. This was solved by careful sanitization and
a dictionary mapping to common abbreviations or mispellings. For some reason, Riot's API endpoints for Wukong (a champion in-game) points to MonkeyKing, which confused me at first.

The self-updating system gave me the most stress! It works by pinging Riot's API that contains all the versions of the game that ever existed, with the first entry in the list being the most recent. The bot pings the endpoint everytime it starts and if there's a new version, an internal version variable changes and this is used to compare with all the locally stored data which has its own version. If the two of them differ, the data is grabbed again from the Riot servers and replaces the old data. Most of the difficulty involved was making sure that every call that could depend on data from Riot's servers to be accurate by doing this version check every step of the way.




