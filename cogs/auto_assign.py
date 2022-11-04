from discord.ext import commands
import discord

class AutoAssign(commands.Cog):

    #BOT - for testing
    #ID of messages / ID of emojis / Name of roles

    # SERVER_NAME = "Bot"
    
    # WELCOME_MESSAGE = 1028191165150937088
    # LOLI_OR_ANE = 1028204989937614848

    # OK = "<:peko_cry:1028191345900265573>"
    # SHION = "<:shion:1028204235080343562>"
    # NOEL = '<:noel:1028204232425357342>'

    # LOLI = "shion"
    # ANE = "noel"
    # HENTAI = "變態"

    #2KA - actual

    SERVER_NAME = "2KA的公園"
    
    WELCOME_MESSAGE = 1026394566036832297
    LOLI_OR_ANE = 1028503172576182332
    HENTAI_MESSAGE = 1028503145069936762
    BOING_OR_PETTAN = 1030738203054981190

    OK = '<:ok:1026368346565922916>'
    SHION = '<:shion:1026061891694497792>'
    NOEL = '<:noel:1026063540659966022>'
    MARINE = '<:marineexcited:1022351580680433694>'
    BOING_EMOJI = '<:boing:1030690357710688286>'
    PETTAN_EMOJI = '<:pettan:1022351578734284801>'

    NORMAL = "公園住民"
    LOLI = "蘿莉控"
    ANE = "禦姐控"
    HENTAI = "變態"
    BOING = "巨乳控"
    PETTAN = "貧乳控"

    def __init__(self, bot):
        self.bot = bot
        print("AUTO ASSIGN ONLINE")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        #print("REACTION GET")

        guild = discord.utils.get(self.bot.guilds, name=self.SERVER_NAME) #Get server name
        emoji = str(payload.emoji) #Get custom emoji ID
        member = payload.member

        async def add_roles(role_name):
            print(f"add roles {role_name}")
            role = discord.utils.get(guild.roles, name=role_name)
            await member.add_roles(role)

        if payload.message_id == self.WELCOME_MESSAGE and emoji == self.OK:
            await add_roles(self.NORMAL)
        elif payload.message_id == self.LOLI_OR_ANE:
            if emoji == self.SHION:
                await add_roles(self.LOLI)
            elif emoji == self.NOEL:
                await add_roles(self.ANE)
        elif payload.message_id == self.HENTAI_MESSAGE:
            if emoji == self.MARINE:
                await add_roles(self.HENTAI)
        elif payload.message_id == self.BOING_OR_PETTAN:
            if emoji == self.BOING_EMOJI:
                await add_roles(self.BOING)
            elif emoji == self.PETTAN_EMOJI:
                await add_roles(self.PETTAN)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        #print("REACTION REMOVED")

        guild = discord.utils.get(self.bot.guilds, name=self.SERVER_NAME) #Get server name
        emoji = str(payload.emoji) #Get custom emoji ID
        member = guild.get_member(payload.user_id)

        async def remove_roles(role_name):
            print(f"REMOVING {role_name}")
            role = discord.utils.get(guild.roles, name=role_name)
            await member.remove_roles(role)

        if payload.message_id == self.WELCOME_MESSAGE and emoji == self.OK:
            await remove_roles(self.NORMAL)
        elif payload.message_id == self.LOLI_OR_ANE:
            if emoji == self.SHION:
                await remove_roles(self.LOLI)
            elif emoji == self.NOEL:
                await remove_roles(self.ANE)
        elif payload.message_id == self.HENTAI_MESSAGE:
            if emoji == self.MARINE:
                await remove_roles(self.HENTAI)
        elif payload.message_id == self.BOING_OR_PETTAN:
            if emoji == self.BOING_EMOJI:
                await remove_roles(self.BOING)
            elif emoji == self.PETTAN_EMOJI:
                await remove_roles(self.PETTAN)

async def setup(bot):
    await bot.add_cog(AutoAssign(bot))