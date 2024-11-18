import random
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands import BucketType, cooldown
from utils.jsonutil import read_json_file, write_json_file

class Steal(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.first_attempt = True

    @slash_command(description="Steal money from another person!")
    @cooldown(1, 3600, BucketType.user)  # 1 hour cooldown per user
    async def steal(self, ctx, target: Option(discord.User, "Enter the person's name!", required=True)):  # type: ignore
        author_id = ctx.author.id
        target_id = target.id
        
        #Check this first before reading the json file to avoid unnecessary reads
        if author_id == target_id:
            await ctx.respond("You can't steal from yourself! What are you into?")
            if self.first_attempt:
                self.steal.reset_cooldown(ctx)
            return

        
        id_nums = read_json_file('DataHolding.json')
        balance_target = id_nums[str(target_id)][0]["amount"]
        
        if balance_target <= 0:
            await ctx.respond(f"{target.display_name} has no money to steal.")
            if self.first_attempt:
                self.steal.reset_cooldown(ctx)
            return

        amount = random.randint(1, int(balance_target * 0.70))  # Random amount between 1 and 70% of target's balance
        id_nums[str(target_id)][0]["amount"] -= amount
        id_nums[str(author_id)][0]["amount"] += amount

        # Write new data to the database and return confirmation that the money is sent
        write_json_file('DataHolding.json', id_nums)

        self.first_attempt = False  # Set the flag to False after a successful attempt
        await ctx.respond(f"<@{author_id}> stole ${amount} from <@{target_id}>!")

    @steal.error
    async def steal_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"This command is on cooldown. Try again in {int(error.retry_after)} seconds.")
            self.first_attempt = True  # Reset the flag after the cooldown is triggered
        else:
            await ctx.respond("An error occurred while trying to steal money.")
            self.first_attempt = True
            
    

def setup(bot) -> None:
    bot.add_cog(Steal(bot))