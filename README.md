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


## Extra Notes

Valor is written in Python utilizing the [discord.py](https://github.com/Rapptz/discord.py) and the [cassiopeia](https://github.com/meraki-analytics/cassiopeia/tree/master/cassiopeia) wrapper.

This will be subject to change.



