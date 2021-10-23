import discord
import os
from discord.ext import commands
from datetime import datetime
import asyncio
from discord.utils import get

from pytz import timezone
tz = timezone('EST')
datetime.now(tz) 
client = commands.Bot(command_prefix='+')

mazes = []
mazeMessages = []
mazeUsers = []


import random

class pos:
  def __init__(self,x,y):
    self.x = x
    self.y = y

class Cell:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.checked = False
    """N S W E"""
    self.walls = [True, True, True, True]

class Maze:

  def __init__(self, width, height):
    self.Space = ':black_small_square:'
    self.Space = ':white_small_square:'
    self.private = False
    self.stringMaze = '```\n'
    self.symWidth = 2
    self.totalWidth = 0
    self.playerCell = 0
    self.totalWidthRound = 0
    self.genX = 0
    self.genY = 0
    self.lastPlayerPos = 0
    self.canMove = True
    self.readyToMove = False
    self.cellsChecked = 0
    self.width = width
    self.height = height
    self.path = []
    self.Cells = []
    for y in range(self.width):
      for x in range(self.height):
        self.Cells.append(Cell(x,y))
    while self.cellsChecked < self.width*self.height:
      self.path.append(pos(self.genX, self.genY))
      while not self.readyToMove:
          self.wallGone = random.randrange(0,4,1)
          if (self.wallGone == 0 and self.getCell(self.genX,self.genY-1) != -1):
            self.readyToMove = True
            self.getCellOn(self.genX,self.genY).walls[0] = False
            self.getCellOn(self.genX,self.genY-1).walls[1] = False
            self.genY -= 1
          elif (self.wallGone == 1 and self.getCell(self.genX,self.genY+1) != -1):
            self.readyToMove = True
            self.getCellOn(self.genX,self.genY).walls[1] = False
            self.getCellOn(self.genX,self.genY+1).walls[0] = False
            self.genY += 1
          elif (self.wallGone == 2 and self.getCell(self.genX-1,self.genY) != -1):
            self.readyToMove = True
            self.getCellOn(self.genX,self.genY).walls[2] = False
            self.getCellOn(self.genX-1,self.genY).walls[3] = False
            self.genX -= 1
          elif (self.wallGone == 3 and self.getCell(self.genX+1,self.genY) != -1):
            self.readyToMove = True
            self.getCellOn(self.genX,self.genY).walls[3] = False
            self.getCellOn(self.genX+1,self.genY).walls[2] = False
            self.genX += 1
          else:
            self.fail()
            
      if not self.getCellOn(self.genX,self.genY).checked:
        self.getCellOn(self.genX,self.genY).checked = True
        self.cellsChecked += 1
      self.readyToMove = False

  def fail(self):
    if (self.getCell(self.genX,self.genY-1) == -1 and self.getCell(self.genX,self.genY+1) == -1 and self.getCell(self.genX-1,self.genY) == -1 and self.getCell(self.genX+1,self.genY) == -1):
      del self.path[len(self.path)-1]
      self.genX = self.path[len(self.path)-1].x
      self.genY = self.path[len(self.path)-1].y
      

  def getCell(self, x, y):
    if (x < self.width and y < self.height and x > -1 and y > -1):
        
        if (self.Cells[x+(y*self.width)].checked == False):
   
          return self.Cells[x+(y*self.width)]
        else:
          return -1
    else:
      return -1

  def getCellOn(self,x,y):
    return self.Cells[x+(y*self.width)]

  def addSpace(self):
      self.totalWidth += self.symWidth
      returnNum = int(self.totalWidth-self.totalWidthRound)
      self.totalWidthRound += returnNum
      returnStr = ''
      for i in range(returnNum):
          returnStr += ' '
      return returnStr

  def draw(self):
      for y in range(self.height):
          for x in range(self.width):
            self.stringMaze += "■ "
            if (self.getCellOn(x,y).walls[0]):
                self.stringMaze += "■ "
            else:
                self.stringMaze += self.addSpace()
          self.stringMaze += "■ "
          self.stringMaze += "\n"
          for x in range(self.width):
            if (self.getCellOn(x,y).walls[2]):
              self.stringMaze += "■ "
            else:
              self.stringMaze += self.addSpace()
            self.stringMaze += self.addSpace()
          self.stringMaze += "■ "
          self.stringMaze += "\n"
      for x in range(self.width):
        self.stringMaze += "■ "
        self.stringMaze += "■ "
      self.stringMaze += "■ "
      self.stringMaze += "\n```"

  def Down(self):
    if (not self.Cells[self.playerCell].walls[1]):
      self.playerCell += self.width
      self.stringMaze = replacer(self.stringMaze, ' ', self.lastPlayerPos)
      self.stringMaze = replacer(self.stringMaze, '□', self.lastPlayerPos+(self.width*8)+6)
      self.lastPlayerPos += (self.width*8)+6
  def Up(self):
    if (not self.Cells[self.playerCell].walls[0]):
      self.playerCell -= self.width
      self.stringMaze = replacer(self.stringMaze, ' ', self.lastPlayerPos)
      self.stringMaze = replacer(self.stringMaze, '□', self.lastPlayerPos-((self.width*8)+6))
      self.lastPlayerPos -= ((self.width*8)+6)
  def Left(self):
    if (not self.Cells[self.playerCell].walls[2]):
      self.playerCell -= 1
      self.stringMaze = replacer(self.stringMaze, ' ', self.lastPlayerPos)
      self.stringMaze = replacer(self.stringMaze, '□', self.lastPlayerPos-4)
      self.lastPlayerPos -= 4
  def Right(self):
    if (not self.Cells[self.playerCell].walls[3]):
      self.playerCell += 1
      self.stringMaze = replacer(self.stringMaze, ' ', self.lastPlayerPos)
      self.stringMaze = replacer(self.stringMaze, '□', self.lastPlayerPos+4)
      self.lastPlayerPos += 4

def replacer(s, newstring, index, nofail=False):
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")
    if index < 0: 
        return newstring + s
    if index > len(s):
        return s + newstring
    return s[:index] + newstring + s[index + 1:]


while True:

  if len(mazeMessages) > 5:
    mazeMessages.pop(0)
    mazes.pop(0)
    mazeMessages.pop(0)

  @client.event
  async def on_ready():
    print('We have logged in as (0.user)')

  @client.event
  async def on_message(message):
    if message.content.startswith("+maze") or message.content.startswith("+pmaze"):
      [command, width, height] = message.content.split(" ", 3)
      if (int(width)*int(height)*8)+(int(height)*2)+(int(width)*2) > 1900:
        await message.channel.send("That Maze is tooooo big")
      else:
        mazeUsers.append(message.author)
        maze = Maze(int(width), int(height))
        maze.draw()
        maze.stringMaze = replacer(maze.stringMaze, '□', (9+(maze.width*4)))
        maze.stringMaze = replacer(maze.stringMaze, '★', len(maze.stringMaze)-(9+(maze.width*4))-2)
        maze.lastPlayerPos = (9+(maze.width*4))
        maze.Down()
        maze.Up()
        mazeMessage = await message.channel.send(maze.stringMaze)
        await mazeMessage.add_reaction("⬅")
        await mazeMessage.add_reaction("⬆")
        await mazeMessage.add_reaction("⬇")
        await mazeMessage.add_reaction("➡")
        mazes.append(maze)
        mazeMessages.append(mazeMessage)
        
      if (message.content.startswith("+pmaze")):
        maze.private = True
      
  

  @client.event
  async def on_reaction_add(reaction, user):
    if user != client.user:
      mazeNum = -1
      for i in range(len(mazeMessages)):
        if (reaction.message == mazeMessages[i]):
          mazeNum = i
      if mazeNum > -1:
        if reaction.emoji == '⬅':
          await reaction.message.remove_reaction(reaction.emoji, user)
          if ((mazes[mazeNum].private and user == mazeUsers[mazeNum]) or (not mazes[mazeNum].private)):
            mazes[mazeNum].Left()
            await mazeMessages[mazeNum].edit(content=mazes[mazeNum].stringMaze)
        if reaction.emoji == '⬆':
          await reaction.message.remove_reaction(reaction.emoji, user)
          if ((mazes[mazeNum].private and user == mazeUsers[mazeNum]) or (not mazes[mazeNum].private)):
            mazes[mazeNum].Up()
            await mazeMessages[mazeNum].edit(content=mazes[mazeNum].stringMaze)
        if reaction.emoji == '⬇':
          await reaction.message.remove_reaction(reaction.emoji, user)
          if ((mazes[mazeNum].private and user == mazeUsers[mazeNum]) or (not mazes[mazeNum].private)):
            mazes[mazeNum].Down()
            await mazeMessages[mazeNum].edit(content=mazes[mazeNum].stringMaze)
        if reaction.emoji == '➡':
          await reaction.message.remove_reaction(reaction.emoji, user)
          if ((mazes[mazeNum].private and user == mazeUsers[mazeNum]) or (not mazes[mazeNum].private)):
            mazes[mazeNum].Right()
            await mazeMessages[mazeNum].edit(content=mazes[mazeNum].stringMaze)
client.run(os.environ['DISCORD_TOKEN'])



