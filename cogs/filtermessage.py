import os, re
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
        
        msg_content = message.content.lower().replace(" ", "")
        pattern = re.compile(r'p+o+k+e*r*|p+0+k+e*r*|p+o+k+3*r*|p+0+k+3*r*')
        pattern2 = re.compile(r'p+e+e*|p+3+e*|p+e+3*|p+3+e*|p+o+o*|p+0+o*|p+o+0*|p+0+0*|p+e+p+e*|p+o+p+o*')
        
        if message.author.id == certain_id and pattern.search(msg_content):
            await message.delete()
            await message.channel.send("no poker for you")
        
        elif message.author.id == certain_id and pattern2.search(msg_content):
            await message.delete()
            await message.channel.send("no just stop")
            
        if role in message.author.roles:     
            print("Checking words")  
            words = self.scan_for_words(msg_content, ["sell", "offer", "ticket", "coldplay", "bus", "pass", "concert", "concerts", "selling", "buy", "prep101", "hsr", "tutor", "taylor swift"])
            if words:
                await message.delete()  
                await message.author.send("Your message contained prohibited words and has been deleted.")

def setup(bot):
    bot.add_cog(FilterMessage(bot))