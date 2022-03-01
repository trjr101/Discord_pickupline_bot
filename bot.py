# Bot.py
# Author: Mihir Jetly
# Pickup line bot

# Import our libraries and APIs
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
import pandas as pd

# Retrieve the pickup lines and convert to a list of strings
file = 'pickup_lines.csv'
df = pd.read_csv(file)
pLines = df['lines'].values.tolist()


# Create a random pickup line selector function
def get_pickup():
    rnum = random.randrange(0, len(pLines), 1)
    line = pLines[rnum]
    return line


# Load the .env file that is on the same level as the script
load_dotenv()

# Grab the API token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN', 'value does not exist')

client = commands.Bot(command_prefix='$')


# Start up the discord bot and create initialized values. All Discord commands will be down here
# The startup ready event
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# Message event, will send a pickup line on ping
@client.event
async def on_message(msg):
    if msg.author.bot:
        return

    if str(client.user.id) in msg.content:
        print('I received a message!')
        res = get_pickup()
        await msg.reply(res)
        return

    await client.process_commands(msg)


# Now we want a command to be run
@client.command(
    name='ping',
    help='Uses some crazy complex algorithm to see if pong is the correct value to print',
    brief="Prints pong back to the channel, it's not rocket science"
)
async def on_command(ctx):
    await ctx.channel.send('pong')
    return


@client.command(
    name='getLine',
    aliases=['pickup', 'grabLine', 'smoothOperator', 'smooth', 'butter'],
    help="Grabs an epic pickup line from our repository and delivers to be smooth as butter",
    brief="Grab a pickup line and sends it. Nothing else."
)
async def getLine(ctx):
    li = f'{ctx.author.mention} '
    li = li + get_pickup()
    print(li)
    await ctx.channel.send(li)
    return


client.run(TOKEN)
