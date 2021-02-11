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


name = "cap"


@client.event
async def on_ready():
  print('We have logged in as (0.user)')
  #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Hendy')) 


@client.event
async def on_message(message):
  global name
  if (message.author == client.user):
      return
  if message.content.startswith("!" + name):
    command = message.content
    await message.channel.send(command[5:] + " is " + str(random.randint(0,100)) + "% " + name)
  if message.content.startswith("!rainbowflag"):
    command = message.content
    await message.channel.send(command[13:] + " is a " + str(random.randint(0,10)) + "/10 on the rainbow flag scale")
  




client.run(os.environ['DISCORD_TOKEN'])



