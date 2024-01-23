from discord.ext import commands
from discord.commands import slash_command, Option

class Hello(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @slash_command(description = "Say hello to a person!")
    async def hello(self, ctx, nameinput: Option(str, "Enter the person's name!", required = True)):
        name = nameinput 
        await ctx.respond(f"Hello {name}!")
    
def setup(bot) -> None:
    bot.add_cog(Hello(bot))