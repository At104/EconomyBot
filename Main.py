import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
#bot = commands.Bot(command_prefix = '!', description="") # Defines the command prefix to be "!"
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
async def hello(ctx, nameinput: str = ""):
    name = nameinput or ctx.author.nameinput
    await ctx.respond(f"Hello {name}!")
    
@bot.slash_command(name = "send", description = "Send another person money")
async def send(ctx, nameinput = "", amount = ""):
    
    if (amount == "" and nameinput == ""):
        await ctx.respond("Need to input at least the reciever or amount you want to send!")
        
    elif (amount == ""):
        await ctx.respond("How much do you want to send?") 
        try:
            amount = await bot.wait_for("amount", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.respond("timeout stoopid")
        else:
            if amount.content.lower() == " ":
                await ctx.respond("Your entered value is blank!")    
            else:
                await ctx.respond("Sent " + amount + " to " + nameinput + "!")
                     
    elif (nameinput == ""):
        await ctx.respond("Who do you want to send the money to?") 
        try:
            nameinput = await bot.wait_for("nameinput", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.respond("timeout stoopid")
        else:
            if nameinput == " ":
                await ctx.respond("Your entered value is blank!")
            else:
                await ctx.respond("Sent " + amount + " to " + nameinput + "!")
    

    
    else:
        await ctx.respond("Sent " + amount + " to " + nameinput + "!")
   
        
   
    
    
bot.run(os.getenv("apikey"))
