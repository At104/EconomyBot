from discord.ext import commands
from discord.commands import slash_command
from utils.jsonutil import read_json_file, write_json_file

class Sell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="sell", description="Sell your gold for $7500 each (it is what it is)")
    async def sell(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        id_nums = read_json_file('DataHolding.json')

        if user_id not in id_nums:
            await ctx.respond("You don't have an account.", ephemeral=True)
            return

        user_data = id_nums[user_id][0]
        gold_amount = user_data.get("gold", 0)

        if amount > gold_amount:
            await ctx.respond("You don't have enough gold to sell.", ephemeral=True)
            return

        gold_value = 7500  # Value of each gold in money
        money_earned = amount * gold_value

        user_data["gold"] -= amount
        user_data["amount"] += money_earned

        write_json_file('DataHolding.json', id_nums)
        await ctx.respond(f"You sold {amount} gold.")

def setup(bot):
    bot.add_cog(Sell(bot))