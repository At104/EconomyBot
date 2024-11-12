import discord, os
from dotenv import load_dotenv

# Slash command pain
load_dotenv()
testingservers = [os.getenv("serveridfsm"),os.getenv("serveridtest"),os.getenv("serveridbotify")]

class Bot(discord.Bot):
    def __init__(self):
        #intents = discord.Intents.default()
        #intents.message_content = True
        intents = discord.Intents.all()
        super().__init__(
            intents = intents,
            debug_guilds = testingservers
        )

# Bot object
bot = Bot()

# Bot ready
@bot.event
async def on_ready() -> None:
    await bot.change_presence(activity=discord.Game(name=" with the stonk market")) # Displays the "playing as" for the bot
    print('Bot is on!')
    

def load_cogs() -> None:
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            bot.load_extension(f'cogs.{file[:-3]}')

def main() -> None:
    load_cogs()
    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()