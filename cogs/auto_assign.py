from discord.ext import commands
import discord

class AutoAssign(commands.Cog):

    #ID of messages
    WELCOME_MESSAGE = 1028191165150937088
    LOLI_OR_ANE = 1028204989937614848

    #ID of emojis
    PEKO_CRY = "<:peko_cry:1028191345900265573>"
    SHION = "<:shion:1028204235080343562>"
    NOEL = '<:noel:1028204232425357342>'

    #Name of roles
    LOLI = "shion"
    ANE = "noel"
    HENTAI = "變態"

    def __init__(self, bot):
        self.bot = bot
        print("AUTO ASSIGN ONLINE")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        #print("REACTION GET")

        guild = discord.utils.get(self.bot.guilds, name="Bot") #Get server name
        emoji = str(payload.emoji) #Get custom emoji ID
        member = payload.member

        async def add_roles(role_name):
            role = discord.utils.get(guild.roles, name=role_name)
            await member.add_roles(role)

        if payload.message_id == self.WELCOME_MESSAGE and emoji == self.PEKO_CRY:
            await add_roles("test 1")
        elif payload.message_id == self.LOLI_OR_ANE:
            if emoji == self.SHION:
                await add_roles(self.LOLI)
            elif emoji == self.NOEL:
                await add_roles(self.ANE)
        elif payload.message_id == self.HENTAI:
            if emoji == self.MARINE:
                await add_roles(self.HENTAI)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        print("REACTION REMOVED")

        guild = discord.utils.get(self.bot.guilds, name="Bot") #Get server name
        emoji = str(payload.emoji) #Get custom emoji ID
        member = guild.get_member(payload.user_id)

        async def remove_roles(role_name):
            print("REMOVING ROLE")
            role = discord.utils.get(guild.roles, name=role_name)
            await member.remove_roles(role)

        if payload.message_id == self.WELCOME_MESSAGE and emoji == self.PEKO_CRY:
            await remove_roles("test 1")
        elif payload.message_id == self.LOLI_OR_ANE:
            if emoji == self.SHION:
                await remove_roles(self.LOLI)
            elif emoji == self.NOEL:
                await remove_roles(self.ANE)
        elif payload.message_id == self.HENTAI:
            if emoji == self.MARINE:
                await remove_roles(self.HENTAI)

async def setup(bot):
    await bot.add_cog(AutoAssign(bot))