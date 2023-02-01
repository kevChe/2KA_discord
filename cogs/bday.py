from discord.ext import commands, tasks
import discord
from discord import File, app_commands
import pymysql
import datetime
import asyncio

class bday(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.connection = pymysql.connect(host="db-buf-02.sparkedhost.us",autocommit=True ,port=3306, user="u75662_RNokPhakPC", passwd="v4RL73jqIfS^1lkMc@mZrZkE", db="s75662_NNN")
        self.cursor = self.connection.cursor()

    @commands.Cog.listener()
    async def on_ready(self):
        print('BDAY ONLINE')
        self.send_channel = self.bot.get_channel(1021667971682287630)
        # self.send_channel = self.bot.get_channel(1026387611230670848)
        self.check.start()

    @app_commands.command(name="bday", description="請輸入你的生日日期")
    @app_commands.describe(
        month="生日月份",
        day="生日日子"
    )
    @app_commands.rename(
        month="月",
        day="日"
    )
    async def bday(self, interaction: discord.Interaction, month: app_commands.Range[int, 1, 12], day: app_commands.Range[int, 1, 31]) -> None:
        if interaction.channel_id == 1055393389463474239:
            if (month in [4, 6, 9, 11] and day == 31) or (month == 2 and day > 29):
                await interaction.response.send_message(f'{month}月並沒有{day}日<:angry_fox:1026061884304138321>', ephemeral=True)
            else:
                date = f'{month:02d}{day:02d}'
                print(date)
                sql = (f"INSERT INTO bday (id, name, month, day) VALUES ({interaction.user.id},'{interaction.user.name}' ,{month}, {day})"
                f"ON DUPLICATE KEY UPDATE name = '{interaction.user.name}', month={month}, day = {day}")
                self.cursor.execute(sql)
                await interaction.response.send_message(f'你的生日是{month}月{day}日')
        else:
            await interaction.response.send_message(f"請在<#1055393389463474239>使用此指令", ephemeral=True)

    @tasks.loop(hours=24.0)
    # @tasks.loop(seconds=10)
    async def check(self):
        await asyncio.sleep(self.seconds_until_midnight())
        date = datetime.datetime.now()
        # date = datetime.datetime(2022, 3, 2)
        month = date.strftime("%m")
        day = date.strftime("%d")
        result = self.cursor.execute(f'SELECT id FROM bday WHERE month = {month} AND day = {day}')
        print(result)
        if result != 0:
        # print(self.cursor.fetchall()[0][0])
            names = ' '.join(f'<@{id[0]}>' for id in self.cursor.fetchall())
            await self.send_channel.send(f"今天是{names}的生日<:peko_yeah:1044922712990171156>")


    def seconds_until_midnight(self):
        now = datetime.datetime.now()
        target = (now).replace(hour=0, minute=0, second=0, microsecond=0)
        diff = (target - now).total_seconds()
        if diff < 0:
            diff += 86400
        print(f"{target} - {now} = {diff}")
        return diff

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        bday(bot), 
        guild = discord.Object(id = 1021667971682287627))