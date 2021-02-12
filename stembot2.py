import discord
import os
from discord.ext import commands
from datetime import datetime
import asyncio
import random
import time

from pytz import timezone
tz = timezone('EST')
datetime.now(tz) 
client = commands.Bot(command_prefix='+')

lastMessage = ""
name = "cap"
quoteResponseWaiting = False
quoteResponseTimer = 0
quote = ""
quotter = ""

@client.event
async def on_ready():
  print('We have logged in as (0.user)')
  #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Hendy')) 


@client.event
async def on_message(message):
  global name
  global lastMessage
  global quoteResponseWaiting
  global quoteResponseTimer
  global quote
  global quotter
  quoteChannel = client.get_channel(809524819661684758)
  if (message.author == client.user):
      return
  if message.content.startswith("!" + name):
    command = message.content
    await message.channel.send(command[5:] + " is " + str(random.randint(0,100)) + "% " + name)
  if message.content.startswith("!rainbowflag"):
    command = message.content
    await message.channel.send(command[13:] + " is a " + str(random.randint(0,10)) + "/10 on the rainbow flag scale")

  if (message.content.startswith("!quote")):
    quotter = message.author
    quoteResponseTimer = 0
    await message.channel.send("Are you sure you want to quote " + "\"" + lastMessage.content + "\" by " + '{}'.format(lastMessage.author.mention) + " y/n")
    quote = lastMessage
    quoteResponseWaiting = True
  if (quoteResponseWaiting):
    quoteResponseTimer += 1
    if (message.content == "y" and message.author == quotter):
      await quoteChannel.send("\"" + quote.content + "\"\n-" + '{}'.format(quote.author.mention) + "\n")
    if (quoteResponseTimer > 5 or message.content == "n" and message.author == quotter):
      quoteResponseWaiting = False
      quoteResponseTimer = 0

  lastMessage = message
  print(message)
client.run(os.environ['DISCORD_TOKEN'])



