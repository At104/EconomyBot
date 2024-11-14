import os
import random
import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.ui import Button, View
from dotenv import load_dotenv
from utils.jsonutil import read_json_file, write_json_file

load_dotenv()
roulette_weight = list(map(int, os.getenv("roulette_weight").split(',')))
class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Play a game of roulette!")
    @commands.cooldown(1, 300, commands.BucketType.user)  # 1 use per 300 seconds (5 minutes) per user
    async def roulette(self, ctx, bet_amount: int):
        user_id = str(ctx.author.id)
        id_nums = read_json_file('DataHolding.json')

        if user_id not in id_nums or id_nums[user_id][0]["amount"] < bet_amount:
            await ctx.respond("You don't have enough money to place this bet.")
            return

        embed = discord.Embed(title="Roulette Game", description="Choose your bet!", color=discord.Color.green())
        view = RouletteView(ctx, bet_amount)
        await ctx.respond(embed=embed, view=view)

    @roulette.error
    async def roulette_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"Don't be a serial gambler! Try again in {int(error.retry_after)} seconds.")
        else:
            await ctx.respond("An error occurred while trying to play roulette.")

class RouletteView(View):
    def __init__(self, ctx, bet_amount):
        super().__init__(timeout=60)  # View will timeout after 60 seconds
        self.ctx = ctx
        self.bet_amount = bet_amount

    @discord.ui.button(label="Red", style=discord.ButtonStyle.danger)
    async def red_button(self, button: Button, interaction: discord.Interaction):
        await self.spin_wheel(interaction, "Red")

    @discord.ui.button(label="Black", style=discord.ButtonStyle.primary)
    async def black_button(self, button: Button, interaction: discord.Interaction):
        await self.spin_wheel(interaction, "Black")

    @discord.ui.button(label="Green", style=discord.ButtonStyle.success)
    async def green_button(self, button: Button, interaction: discord.Interaction):
        await self.spin_wheel(interaction, "Green")

    async def spin_wheel(self, interaction: discord.Interaction, bet: str):
        result = random.choices(["Red", "Black", "Green"], weights=roulette_weight, k=1)[0]
        user_id = str(self.ctx.author.id)
        id_nums = read_json_file('DataHolding.json')

        if bet == result:
            if result == "Green":
                winnings = self.bet_amount * 14  # Green pays 14:1
            else:
                winnings = self.bet_amount * 2  # Red and Black pay 2:1
            id_nums[user_id][0]["amount"] += winnings
            outcome = f"Congratulations! The wheel landed on {result}. You win ${winnings}!"
        else:
            id_nums[user_id][0]["amount"] -= self.bet_amount
            outcome = f"Sorry, the wheel landed on {result}. You lose ${self.bet_amount}."

        write_json_file('DataHolding.json', id_nums)

        embed = discord.Embed(title="Roulette Result", description=outcome, color=discord.Color.gold())
        await interaction.response.edit_message(embed=embed, view=None)

def setup(bot):
    bot.add_cog(Roulette(bot))