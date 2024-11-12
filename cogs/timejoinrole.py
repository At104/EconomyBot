import os
from discord.ext import commands,tasks
from discord.utils import utcnow
from dotenv import load_dotenv

load_dotenv()


class TimeJoinRole(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.time_join_role.start()
    
    @tasks.loop(minutes = 30)
    async def time_join_role(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(int(self.bot.debug_guilds[0]))
        #members = guild.members
        #role = guild.get_role(int(os.getenv("new_member_role_id_test")))
        #new_role = guild.get_role(int(os.getenv("member_role_id_test")))
        
        role = guild.get_role(os.getenv("fsm_newmember_id"))
        new_role = guild.get_role(os.getenv("fsm_member_id"))
        
        members_with_role = [member for member in guild.members if role in member.roles]
        
        for member in members_with_role:
            joined_at = member.joined_at
            print(f"{member.display_name} joined at {joined_at}")   
            duration = utcnow() - joined_at
            if duration.days >= 3:
                await member.remove_roles(role)
                await member.add_roles(new_role)
            else:
                #message = f"{member.display_name} has been here for less than 3 days.\n"
                pass
    
'''
    @slash_command(description = "time join")
    async def time_join_role(self,ctx):
        guild = self.bot.get_guild(int(self.bot.debug_guilds[0]))
        #members = guild.members
        role = guild.get_role(1279588290890174516)
        new_role = guild.get_role(1279639178203758694)
        
        members_with_role = [member for member in guild.members if role in member.roles]
        
        for member in members_with_role:
            joined_at = member.joined_at
            duration = utcnow() - joined_at
            if duration.days >= 3:
                message = f"{member.display_name} has been here for {duration.days} days.\n"
                await member.remove_roles(role)
                await member.add_roles(new_role)
                await ctx.respond(message)
            else:
                message = f"{member.display_name} has been here for less than 3 days.\n"
                await ctx.respond(message)
            
    # Send the message to a specific channel
        #channel = Bot.get_channel(1279572272956309544)  # Replace with your channel ID
    '''
            
         
  
def setup(bot) -> None:
    bot.add_cog(TimeJoinRole(bot))