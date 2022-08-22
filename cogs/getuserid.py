import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Getuserid(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @slash_command(description = "Get user IDs from mentions")
    async def getuserid(self, ctx, user: Option(discord.User, "The user you want to get the ID from", default = None)):
        yourId = ctx.author.id
        if not user:
            await ctx.respond("Please enter in a user!")
        else:
            userId = user.id
        await ctx.respond(f"<@{yourId}> is stalking <@{userId}> smh...")

def setup(bot):
    bot.add_cog(Getuserid(bot))