from discord.ext import commands, tasks
from utils.jsonutil import read_json_file, write_json_file
first_instance_loop = True
class Taxes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.taxes.start()  

    @tasks.loop(hours=1)
    async def taxes(self):
         
        global first_instance_loop
        if not first_instance_loop:
            id_nums = read_json_file('DataHolding.json')
            tax_rate = 0.1  # 10% tax
            
            for data in id_nums.values():
                amount = data[0]["amount"]
                tax_amount = int(amount * tax_rate)
                data[0]["amount"] -= tax_amount

            write_json_file('DataHolding.json', id_nums)
            print("Taxed all users")
        else:
            first_instance_loop = False

    @taxes.before_loop
    async def before_taxes(self):
        await self.bot.wait_until_ready()  # Wait until the bot is ready
  
def setup(bot):
    bot.add_cog(Taxes(bot))