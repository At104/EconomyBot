import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class FilterMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def scan_for_words(self, content, words_list):
        return any(word in content for word in words_list)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        guild = self.bot.get_guild(int(self.bot.debug_guilds[0]))
        if message.author.bot:
            return
        
        # Fetch the role using the correct role ID
        role_id = int(os.getenv("new_member_role_id_test"))  
        certain_id = int(os.getenv("certain_someone_id"))
        role = guild.get_role(role_id)
        
        msg_content = message.content.lower()
        if message.author.id == certain_id and "poker" in msg_content:
            await message.delete()
            await message.channel.send("no poker for you")
       
        if role in message.author.roles:     
            print("Checking words")  
            words = self.scan_for_words(msg_content, ["sell", "offer", "tickets"])
            if words:
                await message.delete()  
                await message.author.send("Your message contained prohibited words and has been deleted.")
                return
def setup(bot):
    bot.add_cog(FilterMessage(bot))