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

# Slash command pain
testingservers = [783415814342574151]

@bot.slash_command(guild_ids = testingservers, name = "hello", description = "Just a command to test slash commands!")
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")
    
bot.run(os.getenv("apikey"))
