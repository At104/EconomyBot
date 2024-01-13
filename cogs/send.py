import discord, asyncio, sys, os, time
from discord.ext import commands
from discord.commands import slash_command, Option

# Adding utils folder to system path for utilites to be accessible by this cog
#sys.path.append(os.path.join(os.getcwd(), 'utils'))
from utils.jsonutil import read_json_file, write_json_file
from utils.idcheck import id_check

class Send(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @slash_command(description = "Send another person money")
    async def send(self, ctx, nameinput: Option(discord.User, "The name of the recipiant", required = True), amount: Option(int, "The amount of currency you want to send", required = True)):
        your_id = ctx.author.id
        recipiant_id = nameinput.id

        # In case either name or amount inputs are empty
        if (not amount or not nameinput):
            await ctx.respond("One of the command parameters has an invalid value! Please try again.")

        # Else continue on            
        else:
            # Cannot send money to yourself :(
            if recipiant_id == your_id:
                await ctx.respond("This is not Venezuela... or is it?")

            # Else continue on
            else:
                # Reads database from database
                id_nums = read_json_file('DataHolding.json')

                # If ID database is blank, respond with an error message
                if id_nums == {}:
                    await ctx.respond("Something went wrong with the JSON parsing.")
                    
                else:
                    # Check if IDs exist in the database
                    if (id_check(id_nums, [your_id, recipiant_id]) == False):
                        await ctx.respond("One of the IDs does not exist in the database. Please initialize your account before sending money.")
                    
                    else:
                        # Check if you have enough money to send
                        if (id_nums[str(your_id)][0]["amount"] < amount):
                            await ctx.respond("You do not have enough money to send...bozo")
                        else:
                            # Currency transfer
                            id_nums[str(your_id)][0]["amount"] -= amount
                            id_nums[str(recipiant_id)][0]["amount"] += amount

                            # Write new data to the database and return confirmation that the money is sent
                            write_json_file('DataHolding.json', id_nums)
                            await ctx.respond(f"<@{your_id}> sent " + str(amount) + " to " + f"<@{recipiant_id}>" + " !")

def setup(bot) -> None:
    bot.add_cog(Send(bot))