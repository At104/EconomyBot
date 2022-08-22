import discord, sys, os
from discord.ext import commands
from discord.commands import slash_command, Option

# Adding utils folder to system path for utilites to be accessible by this cog
sys.path.append(os.path.join(os.getcwd(), 'utils'))
from jsonutil import read_json_file

class Balance(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @slash_command(description = "Check your own balance")
    async def balance(self, ctx):
        yourId = ctx.author.id
        id_nums = read_json_file('TestDataHolding.json')
        balanceAmount = id_nums[str(yourId)][0]["amount"]
        await ctx.respond("Your balance is: $" + str(balanceAmount))

def setup(bot) -> None:
    bot.add_cog(Balance(bot))

