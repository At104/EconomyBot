import discord
from discord.ext import commands
from discord.commands import slash_command

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Show help information for all commands")
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="List of available commands", color=discord.Color.blue())

        for cog_name, cog in self.bot.cogs.items():
            commands_list = cog.get_commands()
            if commands_list:
                command_descriptions = "\n".join([f"/{command.name} - {command.description}" for command in commands_list])
                embed.add_field(name=cog_name, value=command_descriptions, inline=False)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))