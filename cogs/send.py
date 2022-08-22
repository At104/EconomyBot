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
        your_id = ctx.author.id
        recipiant_id = nameinput.id

        if (amount == "" or not nameinput):
            await ctx.respond("One of the command parameters has an invalid value! Please try again.")
        else:
            if recipiant_id == your_id:
                await ctx.respond("This is not Venezuela... or is it?")
            else:
                id_nums = read_json_file('TestDataHolding.json')
                if id_nums == {}:
                    await ctx.respond("Something went wrong with the JSON parsing.")
                else:
                    id_nums = id_check(id_nums, [your_id, recipiant_id])
                
                    id_nums[str(your_id)][0]["amount"] -= amount
                    id_nums[str(recipiant_id)][0]["amount"] += amount

                    write_json_file('TestDataHolding.json', id_nums)
                    await ctx.respond(f"<@{your_id}> sent " + str(amount) + " to " + f"<@{recipiant_id}>" + " !")

def setup(bot) -> None:
    bot.add_cog(Send(bot))