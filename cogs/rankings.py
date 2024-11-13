import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.jsonutil import read_json_file

class Rankings(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @slash_command(description="Show the top 5 people with the highest money!")
    async def rankings(self, ctx):  # type: ignore
        id_nums = read_json_file('DataHolding.json')
        
        # Create a list of tuples (user_id, amount) and sort it by amount in descending order
        sorted_users = sorted(id_nums.items(), key=lambda x: x[1][0]["amount"], reverse=True)
        
        # Get the top 5 users
        top5_users = sorted_users[:5]
        
        # Create an embed
        embed = discord.Embed(title="Top 5 Richest Users", color=discord.Color.gold())
        
        for i, (user_id, data) in enumerate(top5_users, start=1):
            user = await self.bot.fetch_user(int(user_id))
            embed.add_field(name=f"{i}. {user.display_name}", value=f"${data[0]['amount']}", inline=False)
        
        await ctx.respond("",embed=embed)

def setup(bot) -> None:
    bot.add_cog(Rankings(bot))