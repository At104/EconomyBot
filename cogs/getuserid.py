import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Getuserid(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @slash_command(description = "Get user IDs from mentions")
    async def getuserid(self, ctx, user: Option(discord.User, "The user you want to get the ID from", default = None)): # type: ignore
        your_id = ctx.author.id
        if not user:
            await ctx.respond("Please enter in a user!")
        else:
            user_id = user.id
        await ctx.respond(f"<@{your_id}> is stalking <@{user_id}> smh...")

def setup(bot) -> None:
    bot.add_cog(Getuserid(bot))