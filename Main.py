import json
import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
#bot = commands.Bot(command_prefix = '!', description="") # Defines the command prefix to be "!"
bot = discord.Bot()

load_dotenv()

# Functions handling json (maybe put this in seperate file in the future)
def read_json_file(filename: str) -> dict:
    with open(filename, 'r') as json_file:
        json_decoded = json.load(json_file)
        json_file.close()

    return json_decoded

def write_json_file(filename: str, data: dict) -> None:
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)
        json_file.close()

def idCheck (idNums: dict, id: int) -> dict:
    if str(id) not in idNums:
        idNums[str(id)] = [{"id": id,"amount": 0}]
    return idNums

###########################################################################
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=" with the stonk market")) # Displays the "playing as" for the bot
    print('Bot is on!')
    # Bot ready

# Slash command pain
testingservers = [783415814342574151]

@bot.slash_command(guild_ids = testingservers, name = "hello", description = "Just a command to test slash commands!")
async def hello(ctx, nameinput: str = ""):
    name = nameinput or ctx.author.nameinput
    await ctx.respond(f"Hello {name}!")

@bot.slash_command(name = "getuserid", description = "Get user IDs from mentions")
async def getuserid(ctx, user: discord.User = None):
    yourId = ctx.author.id
    if not user:
        await ctx.respond("Please enter in a user!")
    else:
        userId = user.id
    await ctx.respond(f"<@{yourId}> is stalking <@{userId}> smh...")
    
@bot.slash_command(name = "send", description = "Send another person money")
async def send(ctx, nameinput: discord.User = None, amount = ""):
    yourId = ctx.author.id
    if (amount == "" and not nameinput):
        await ctx.respond("Need to input at least the reciever or amount you want to send!")
        
    elif (amount == "" or not nameinput):
        if amount == "":
            await ctx.respond("How much do you want to send?")
            thing_being_waited = "amount" 
            
        elif not nameinput:
            await ctx.respond("Who do you want to send the money to?")
            thing_being_waited = "nameinput" 
            
        try:
            amount = await bot.wait_for(thing_being_waited, check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=15.0)

        except asyncio.TimeoutError:
            await ctx.respond("timeout stoopid")

        else:
            if amount.content.lower() == " " or not nameinput:
                ctx.respond("Your entered value is blank!")
            else:
                recipiantId = nameinput.id
                if recipiantId == yourId:
                    await ctx.respond("This is not Venezuela... or is it?")
                else:
                    idNums = read_json_file('TestDataHolding.json')
                    idNums = idCheck(idNums,recipiantId)
                    idNums = idCheck(idNums,yourId)
                    idNums[str(yourId)][0]["amount"] -= int(amount)
                    idNums[str(recipiantId)][0]["amount"] += int(amount)
                    write_json_file('TestDataHolding.json', idNums)
                    await ctx.respond(f"<@{yourId}> sent " + amount + " to " + f"<@{recipiantId}>" + " !")
                     
    else:
        recipiantId = nameinput.id
        if recipiantId == yourId:
            await ctx.respond("This is not Venezuela... or is it?")
        else:
            idNums = read_json_file('TestDataHolding.json')
            idNums = idCheck(idNums,recipiantId)
            idNums = idCheck(idNums,yourId)
            idNums[str(yourId)][0]["amount"] -= int(amount)
            idNums[str(recipiantId)][0]["amount"] += int(amount)
            write_json_file('TestDataHolding.json', idNums)
            await ctx.respond(f"<@{yourId}> sent " + amount + " to " + f"<@{recipiantId}>" + " !")

@bot.slash_command(name = "balance", description = "Check your own balance")
async def balance(ctx):
    yourId = ctx.author.id
    idNums = read_json_file('TestDataHolding.json')
    balanceAmount = idNums[str(yourId)][0]["amount"]
    await ctx.respond("Your balance is: $" + str(balanceAmount))


bot.run(os.getenv("apikey"))
