import random
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands import BucketType, cooldown

from utils.jsonutil import read_json_file, write_json_file

class Steal(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @slash_command(description="Steal money from another person!")
    @cooldown(1, 3600, BucketType.user)  # 1 hour cooldown per user
    async def steal(self, ctx, target: Option(discord.User, "Enter the person's name!", required=True)):  # type: ignore
        
        author_id = ctx.author.id
        target_id = target.id
        
        if author_id == target_id:
            await ctx.respond("You can't steal from yourself! What are you into?")
            return
        
        id_nums = read_json_file('DataHolding.json')
        balance_target = id_nums[str(target_id)][0]["amount"]
        
        if balance_target <= 0:
            await ctx.respond(f"{target.display_name} has no money to steal.")
            return
        
        amount = random.randint(1, int(balance_target*0.75))  # Random amount between 1 and 100
        id_nums[str(target_id)][0]["amount"] -= amount
        id_nums[str(author_id)][0]["amount"] += amount

        # Write new data to the database and return confirmation that the money is sent
        write_json_file('DataHolding.json', id_nums)
        
        await ctx.respond(f"<@{author_id}> stole " + "$"+ str(amount) + " from " + f"<@{target_id}>" + " !")

    @steal.error
    async def steal_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"This command is on cooldown. Try again in {int(error.retry_after)} seconds.")
        else:
            await ctx.respond("An error occurred while trying to steal money.")

def setup(bot) -> None:
    bot.add_cog(Steal(bot))