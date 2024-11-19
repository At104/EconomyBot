from discord.ext import commands
from discord.commands import slash_command, Option

# Adding utils folder to system path for utilites to be accessible by this cog
#sys.path.append(os.path.join(os.getcwd(), 'utils'))
from utils.jsonutil import read_json_file, write_json_file
from utils.idcheck import id_check

workers_cost = 500

class BuyWorkers(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @slash_command(description = "Purchase workers to increase your income")
    async def buyworkers(self, ctx, amount: Option(int, "How many workers you want to buy, 500 per worker", required=True)): # type: ignore
        global workers_cost
        id = ctx.author.id
        workers_amount = amount
        if amount <= 0:
            await ctx.respond("You cannot buy negative workers... bozo")
            return
        id_nums = read_json_file('DataHolding.json')
        if (id_check(id_nums, [id])): 
            # Checks if the user has enough money to buy the workers
            cost = workers_cost*workers_amount
            if (id_nums[str(id)][0]["amount"] >= (cost)):
                
                id_nums[str(id)][0]["amount"] -= (cost)
                id_nums[str(id)][0]["workers"] += workers_amount
                id_nums[str(id)][0]["income"] = id_nums[str(id)][0]["workers"]*60
                
                write_json_file('DataHolding.json', id_nums)
                await ctx.respond(f"<@{id}> has bought {workers_amount} worker(s) for {cost} dollars!")
            else:
                await ctx.respond(f"<@{id}> does not have enough money to buy {workers_amount} worker(s)!")


def setup(bot) -> None:
    bot.add_cog(BuyWorkers(bot))