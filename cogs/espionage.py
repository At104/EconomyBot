import random
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands import BucketType, cooldown

from utils.jsonutil import read_json_file, write_json_file

class Espionage(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @slash_command(description="Remove workers from another person!")
    @cooldown(1, 7200, BucketType.user)  # 2 hour cooldown per user
    async def espionage(self, ctx, target: Option(discord.User, "Enter the person's name!", required=True)):  # type: ignore
        
        author_id = ctx.author.id
        target_id = target.id
        
        if author_id == target_id:
            await ctx.respond("Do you enjoy removing your own workers? Seek help.")
            return
        
        id_nums = read_json_file('DataHolding.json')
        workers_target = id_nums[str(target_id)][0]["workers"]
        
        if workers_target <= 1:
            await ctx.respond(f"{target.display_name} has no workers to remove.")
            return
        
        workers_removed = random.randint(1, int(workers_target*0.65))  # Random amount of workers to remove
        id_nums[str(target_id)][0]["workers"] -= workers_removed
        id_nums[str(target_id)][0]["income"] = id_nums[str(target_id)][0]["workers"]*60

        # Write new data to the database and return confirmation that the workers were removed
        write_json_file('DataHolding.json', id_nums)
        
        await ctx.respond(f"<@{author_id}> removed " + str(workers_removed) + " workers from " + f"<@{target_id}>" + " !")

    @espionage.error
    async def espionage_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"This command is on cooldown. Try again in {int(error.retry_after)} seconds.")
        else:
            await ctx.respond("An error occurred while trying to remove workers.")

def setup(bot) -> None:
    bot.add_cog(Espionage(bot))