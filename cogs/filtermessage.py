import os
from discord.ext import commands
from dotenv import load_dotenv
from filter_config import BLOCKED_WORDS, check_pattern

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
        
        # Check for meow variations for everyone
        if check_pattern(message.content):
            await message.delete()
            return
        # Fetch the role using the correct role ID
        role_id = int(os.getenv("new_member_role_id_test"))  
        role = guild.get_role(role_id)
        
        msg_content = message.content.lower().replace(" ", "")
       
        if role in message.author.roles:     
            print("Checking words")  
            words = self.scan_for_words(msg_content, BLOCKED_WORDS)
            if words:
                await message.delete()  
                await message.author.send("Your message contained prohibited words and has been deleted.")
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return
        
        # Check if the edited message contains meow
        if check_pattern(after.content):
            await after.delete()

def setup(bot):
    bot.add_cog(FilterMessage(bot))