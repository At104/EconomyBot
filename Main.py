import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
#client = commands.Bot(command_prefix = '!', description="") # Defines the command prefix to be "!"
bot = discord.Bot()

load_dotenv()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="the stonk market")) # Displays the "playing as" for the bot
    print('Bot is on')
    # Bot ready

@bot.slash_command()
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")
    
bot.run(os.getenv("apikey"))