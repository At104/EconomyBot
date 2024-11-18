from discord.ext import commands
from discord.commands import slash_command, Option

# Adding utils folder to system path for utilites to be accessible by this cog
#sys.path.append(os.path.join(os.getcwd(), 'utils'))
from utils.jsonutil import read_json_file, write_json_file
from utils.idcheck import id_check

class Initialize(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
   
    @slash_command(description = "Initialize your account before you can use the other methods")
    async def initialize(self, ctx):
        id = ctx.author.id
        id_nums = read_json_file('DataHolding.json')

        if (id_check(id_nums, [id])):
            await ctx.respond("You have already initialized your account!")
        # If ID does not exist in the database, add it to the database
        else:
            id_nums[str(id)] = [{"id": id,"amount": 500, "workers": 0, "income": 0, "gold": 0}]
            write_json_file('DataHolding.json', id_nums)
            await ctx.respond(f"<@{id}> has initialized their account!")
       

def setup(bot) -> None:
    bot.add_cog(Initialize(bot))