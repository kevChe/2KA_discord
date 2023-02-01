import sys
import discord
from discord.ext import commands, tasks
import pymysql
import datetime
import asyncio
from .rwarray import read_array, write_array

class NNN(commands.Cog):

    #########################
    ###########2KA###########
    #########################
    SERVER_NAME = '2KA的公園'
    BOT_ID = 1028125267727745174
    CHANNEL = 1036206588899381329
    YES = '<:peko_carrot:1035123960083402833>'
    NO = '<:peko_cool:1036561247237324851>'
    MESSAGE = "messages.txt"
    # messages = [1036671342361190410, 1037033275899781230, 1037397736686882846, 1037758428984123452, 1038120439253303307,  1038482827353800755, 1038845215294881862]

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.connection = pymysql.connect(host="db-buf-02.sparkedhost.us",autocommit=True ,port=3306, user="u75662_RNokPhakPC", passwd="v4RL73jqIfS^1lkMc@mZrZkE", db="s75662_NNN")
        self.cursor = self.connection.cursor()
        # self.day = datetime.datetime.now().strftime("%d")
        self.day = 31
        self.messages = read_array("messages.txt")

    @commands.Cog.listener()
    async def on_ready(self):
        print('NNN')
        self.nnn.start()
        self.update.start()

    # @tasks.loop(hours=24.0)
    # async def nnn(self):
    #     await asyncio.sleep(self.seconds_until_midnight())
    #     # self.day = datetime.datetime.now().strftime("%d")
    #     channel = self.bot.get_channel(self.CHANNEL)
    #     message = await channel.send(f'<@&1028510369917960202> 你今天（11月{int(self.day) + 1}日）尻了嗎？')
    #     self.messages.append(message.id)
    #     write_array(self.MESSAGE, self.messages)
    #     #print(self.messages)
    #     await message.add_reaction(self.YES)
    #     await message.add_reaction(self.NO)

    # @nnn.before_loop
    # async def before(self):
    #     await self.bot.wait_until_ready()
    #     print("Finished waiting")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        guild = discord.utils.get(self.bot.guilds, name=self.SERVER_NAME) #Get server name
        role = discord.utils.get(guild.roles, name="NNN參與者")
        emoji = str(payload.emoji) #Get custom emoji ID
        member = payload.member
        for date, message in enumerate(self.messages):
            # print(f"MESSAGE: {int(message)} MESSAGE_ID: {payload.message_id}")
            if payload.message_id == int(message) and member.id != self.BOT_ID:
                await member.add_roles(role)
                yesno = 1
                if emoji == self.NO: 
                    yesno = 0
                self.add_result(member.name, date + 1, yesno)

    def add_result(self, name, date, yesno):
        date = datetime.datetime(2022, 11, date).strftime("%B%d")
        # date = datetime.datetime.now().strftime("%B%d")
        #print(date)
        sql = (f'INSERT INTO NNN (user_name, {date}, `continue`) VALUES (\'{name}\', \'{yesno}\', \'{yesno}\')'
            f"ON DUPLICATE KEY UPDATE {date}='{yesno}'"
        )
        print(sql)
        self.cursor.execute(sql)

    def seconds_until_midnight(self):

        now = datetime.datetime.now()
        target = (now).replace(hour=16, minute=0, second=0, microsecond=0)
        diff = (target - now).total_seconds()
        if diff < 0:
            diff += 86400
        print(f"{target} - {now} = {diff}")
        return diff

    def dead_count(self):
        sql = ""
        for i in range(int(self.day)):
            if i + 1 == int(self.day):
                sql += f'November{i + 1:02d} = 1' 
            else:
                sql += f'November{i + 1:02d} = 1 OR '
        print(f'DEAD SQL {sql}')
        return (self.cursor.execute(f'SELECT * FROM NNN WHERE {sql}'))

    def alive_count(self):
        sql = ""
        # for i in range(int(self.day) - 1):
        #     if i + 1 == int(self.day) - 1:
        for i in range(int(self.day)):
            if i + 1 == int(self.day):
                sql += f'November{i + 1:02d} = 0' 
            else:
                sql += f'November{i + 1:02d} = 0 AND '
        print(f'ALIVE SQL {sql}')
        return (self.cursor.execute(f'SELECT * FROM NNN WHERE {sql}'))
    
    @commands.command()
    async def get_name(self, ctx):
        print("in")
        channel = self.bot.get_channel(self.CHANNEL)
        guild = discord.utils.get(self.bot.guilds, name=self.SERVER_NAME) #Get server name
        role = discord.utils.get(guild.roles, name="NNN參與者")
        for message in self.messages:
            message = await channel.fetch_message(message)
            for reaction in message.reactions:
                for user in reaction.users():
                    await user.add_roles(role)

    @commands.command()
    async def alive(self, ctx: commands.Context):
        if ctx.channel.id == 1044959934992875580:
            self.cursor.execute(f'SELECT * FROM NNN WHERE user_name = \'{ctx.author.name}\'')
            db = self.cursor.fetchone()
            dead = False
            deadDate = []
            empty = False
            emptyDate = []
            msg = "好耶，你還活著"
            for i in range(1, int(self.day)):
                if db[i] == 1:
                    dead = True
                    deadDate.append(i)
                elif db[i] is None:
                    empty = True
                    emptyDate.append(i)
            if empty:
                msg = f'你在11月{emptyDate}日沒有選擇'
            elif dead:
                msg = f"你在11月{deadDate}日死了"
            await ctx.reply(msg)

    @tasks.loop(hours=1.0)
    async def update(self):
        dead_channel = self.bot.get_channel(1037348849993388093)
        alive_channel = self.bot.get_channel(1037350849590079519)
        dead = self.dead_count()
        alive = self.alive_count()
        print(f'DEAD: {dead}  ALIVE: {alive}')
        await dead_channel.edit(name = f'nnn破戒人數：{dead}')
        await alive_channel.edit(name = f'nnn生存人數：{alive}')


async def setup(bot):
    await bot.add_cog(NNN(bot))