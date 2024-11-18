import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.ui import Button, View
from utils.jsonutil import read_json_file, write_json_file

class Store(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Open the store to buy items!")
    async def store(self, ctx):
        embed = discord.Embed(title="Store", description="Buy items by pressing the buttons below!", color=discord.Color.red())
        embed.add_field(name="Rich Boi", value="Price: $100,000", inline=False)
        embed.add_field(name="Gold", value="Price: $10,000", inline=False)

        view = StoreView(ctx)
        await ctx.respond(embed=embed, view=view)

class StoreView(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)  # View will timeout after 60 seconds
        self.ctx = ctx

    @discord.ui.button(label="Rich Boi", style=discord.ButtonStyle.success)
    async def buy_rich_boi_role(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return  # Ignore interaction from other users
        await self.buy_item(interaction, "Rich Boi", 100000)

    @discord.ui.button(label="Buy Gold", style=discord.ButtonStyle.primary)
    async def buy_gold(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return  # Ignore interaction from other users
        await self.buy_item(interaction, "Gold", 10000)

    async def buy_item(self, interaction: discord.Interaction, item_name: str, price: int):
        user_id = str(self.ctx.author.id)
        id_nums = read_json_file('DataHolding.json')

        if user_id not in id_nums or id_nums[user_id][0]["amount"] < price:
            await interaction.response.send_message("You don't have enough money to buy this item.", ephemeral=True)
            return

        if item_name == "Rich Boi":
            role = discord.utils.get(interaction.guild.roles, name=item_name)
            if role in interaction.user.roles:
                await interaction.response.send_message("You already have the Rich Boi role.", ephemeral=True)
                return
            elif role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"You bought {item_name} role for ${price}!", ephemeral=True)
            else:
                await interaction.response.send_message("The Rich Boi role does not exist in this server.", ephemeral=True)

        id_nums[user_id][0]["amount"] -= price

        if item_name == "Gold":
            id_nums[user_id][0]["gold"] += 1
            await interaction.response.send_message(f"You bought 1 Gold for ${price}!", ephemeral=True)

            

        write_json_file('DataHolding.json', id_nums)
        # Disable all buttons after a purchase
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

def setup(bot):
    bot.add_cog(Store(bot))