import discord, asyncio, sys, os, time
from discord.ext import commands
from discord.commands import slash_command, Option

# Adding utils folder to system path for utilites to be accessible by this cog
sys.path.append(os.path.join(os.getcwd(), 'utils'))
from jsonutil import *
from idcheck import *

class Send(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @slash_command(description = "Send another person money")
    async def send(self, ctx, nameinput: Option(discord.User, "The name of the recipiant", required = True), amount: Option(int, "The amount of currency you want to send", required = True)):
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
                amount = await self.bot.wait_for(thing_being_waited, check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=15.0)

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
                        idNums = id_check(idNums,recipiantId)
                        idNums = id_check(idNums,yourId)
                        idNums[str(yourId)][0]["amount"] -= amount
                        idNums[str(recipiantId)][0]["amount"] += amount
                        write_json_file('TestDataHolding.json', idNums)
                        await ctx.respond(f"<@{yourId}> sent " + str(amount) + " to " + f"<@{recipiantId}>" + " !")
                        
        else:
            recipiantId = nameinput.id
            if recipiantId == yourId:
                await ctx.respond("This is not Venezuela... or is it?")
            else:
                idNums = read_json_file('TestDataHolding.json')
                idNums = id_check(idNums,recipiantId)
                idNums = id_check(idNums,yourId)
                idNums[str(yourId)][0]["amount"] -= amount
                idNums[str(recipiantId)][0]["amount"] += amount
                write_json_file('TestDataHolding.json', idNums)
                await ctx.respond(f"<@{yourId}> sent " + str(amount) + " to " + f"<@{recipiantId}>" + " !")

def setup(bot):
    bot.add_cog(Send(bot))