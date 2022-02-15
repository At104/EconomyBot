import asyncio
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
    print('Bot is on!')
    # Bot ready

# Slash command pain
testingservers = [783415814342574151]

@bot.slash_command(guild_ids = testingservers, name = "hello", description = "Just a command to test slash commands!")
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")
    
@bot.slash_command()
async def send(ctx):
    await ctx.send("How much do you want to send?")  
    
    try:
        message = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=15.0)
    except asyncio.TimeoutError:
        await ctx.send("timeout stoopid")
    else:
        if message.content.lower() == " ":
            await ctx.send("Your entered value is blank!")
        else:
            await ctx.send("Sent " + message.content.lower() + " !")
    
    
bot.run(os.getenv("apikey"))
