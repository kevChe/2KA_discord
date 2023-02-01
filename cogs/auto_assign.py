from discord.ext import commands
import discord
import json

class AutoAssign(commands.Cog):

    SERVER_NAME = "2KA的公園"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.roles = self.read_json()

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.get(self.bot.guilds, name=self.SERVER_NAME)
        print(self.guild)
        print('AUTO　ASSIGN ONLINE')
    
    def read_json(self):
        with open('roles.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        member = payload.member

        async def add_roles(role_name):
            print(f"add roles {role_name}")
            role = discord.utils.get(self.guild.roles, name=role_name)
            await member.add_roles(role)
        
        for role in self.roles:
            if payload.message_id == role['id']:
                for emoji in role['emojis']:
                    if emoji['emoji'] == str(payload.emoji):
                        await add_roles(emoji['role'])


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        guild = discord.utils.get(self.bot.guilds, name=self.SERVER_NAME) #Get server name
        member = guild.get_member(payload.user_id)

        async def remove_roles(role_name):
            print(f"REMOVING {role_name}")
            role = discord.utils.get(guild.roles, name=role_name)
            await member.remove_roles(role)

        for role in self.roles:
            if payload.message_id == role['id']:
                for emoji in role['emojis']:
                    if emoji['emoji'] == str(payload.emoji):
                        await remove_roles(emoji['role'])


async def setup(bot):
    await bot.add_cog(AutoAssign(bot))