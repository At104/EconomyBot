import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.jsonutil import read_json_file

class Rankings(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @slash_command(description="Show the top 5 people with the highest money and gold!")
    async def rankings(self, ctx):  # type: ignore
        id_nums = read_json_file('DataHolding.json')
        
        # Create a list of tuples (user_id, amount) and sort it by amount in descending order
        sorted_users_by_money = sorted(id_nums.items(), key=lambda x: x[1][0]["amount"], reverse=True)
        
        # Get the top 5 users by money
        top5_users_by_money = sorted_users_by_money[:5]
        
        # Create a list of tuples (user_id, gold) and sort it by gold in descending order
        sorted_users_by_gold = sorted(id_nums.items(), key=lambda x: x[1][0].get("gold", 0), reverse=True)
        
        # Get the top 5 users by gold
        top5_users_by_gold = sorted_users_by_gold[:5]
        
        # Create an embed
        embed = discord.Embed(title="Top 5 Richest Users", color=discord.Color.gold())
        
        # Add top 5 users by money
        money_field_value = ""
        for i, (user_id, data) in enumerate(top5_users_by_money):
            user = await self.bot.fetch_user(int(user_id))
            money_field_value += f"{i+1}. {user.display_name}: ${data[0]['amount']}\n"
        embed.add_field(name="Top 5 by Money", value=money_field_value, inline=True)
        
        # Add top 5 users by gold
        gold_field_value = ""
        for i, (user_id, data) in enumerate(top5_users_by_gold):
            user = await self.bot.fetch_user(int(user_id))
            gold_field_value += f"{i+1}. {user.display_name}: {data[0].get('gold', 0)} gold\n"
        embed.add_field(name="Top 5 by Gold", value=gold_field_value, inline=True)
        
        await ctx.respond(embed=embed)

def setup(bot) -> None:
    bot.add_cog(Rankings(bot))