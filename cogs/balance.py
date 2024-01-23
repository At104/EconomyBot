import discord
from discord.ext import commands
from discord.commands import slash_command, Option

# Adding utils folder to system path for utilites to be accessible by this cog
#sys.path.append(os.path.join(os.getcwd(), 'utils'))
from utils.jsonutil import read_json_file

class Balance(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @slash_command(description = "Check your own balance")
    async def balance(self, ctx):
        embed = discord.Embed(
        title="Balance",
        description="Your current balance and workers",
        color=discord.Colour.blurple(), 
        )
        yourId = ctx.author.id
        id_nums = read_json_file('DataHolding.json')
        balance_amount = id_nums[str(yourId)][0]["amount"]
        workers_amount = id_nums[str(yourId)][0]["workers"]
        embed.add_field(name="*Balance*:money_with_wings: :", value="$" + str(balance_amount))
        embed.add_field(name="*Workers*:construction_worker: :", value= str(workers_amount))
        embed.set_author(name="EconomyBot", icon_url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/90ad8232-4e09-4675-b9e7-bc2898960870/deq5chq-8aabc40f-a1ba-4762-9583-638b4382e93a.png/v1/fill/w_1032,h_774/mr__krabs_holding_a_dollar_by_jcp_johncarlo_deq5chq-pre.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9OTYwIiwicGF0aCI6IlwvZlwvOTBhZDgyMzItNGUwOS00Njc1LWI5ZTctYmMyODk4OTYwODcwXC9kZXE1Y2hxLThhYWJjNDBmLWExYmEtNDc2Mi05NTgzLTYzOGI0MzgyZTkzYS5wbmciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.fLjXDR7qP8PiVKxq3oQat78QZbNA3ze3SJT_3na75jc")
        await ctx.respond("",embed=embed)

def setup(bot) -> None:
    bot.add_cog(Balance(bot))

