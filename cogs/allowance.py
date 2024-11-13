from discord.ext import commands, tasks
from discord.commands import slash_command, Option
first_instance_loop = True

# Adding utils folder to system path for utilites to be accessible by this cog
#sys.path.append(os.path.join(os.getcwd(), 'utils'))
from utils.jsonutil import read_json_file, write_json_file

class Allowance(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.allowance.start()
        

    @tasks.loop(minutes=10)
    async def allowance(self):
        global first_instance_loop
        # This is to prevent the loop from running before the bot is ready, or when the bot is redeploying
        if not first_instance_loop:
          id_nums = read_json_file('DataHolding.json')
          print("Money added")
          #Adds 20 dollars per worker to each user
          for id in id_nums:
              worker_amount = id_nums[id][0]["workers"]
              id_nums[id][0]["amount"] += (20*worker_amount)
              write_json_file('DataHolding.json', id_nums)
        else:
              first_instance_loop = False

    

def setup(bot) -> None:
    bot.add_cog(Allowance(bot))