from discord.ext import commands, tasks
import discord
from discord import File, app_commands
import pymysql
from .transaction import change_money

class econ(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.connection = pymysql.connect(host="db-buf-02.sparkedhost.us",autocommit=True ,port=3306, user="u75662_RNokPhakPC", passwd="v4RL73jqIfS^1lkMc@mZrZkE", db="s75662_NNN")
        self.cursor = self.connection.cursor()

    @commands.Cog.listener()
    async def on_ready(self):
        print('econ ONLINE')
        self.send_channel = self.bot.get_channel(1021667971682287630)

    # @app_commands.command(name="bday", description="請輸入你的生日日期")
    # @app_commands.describe(
    #     month="生日月份",
    #     day="生日日子"
    # )
    # @app_commands.rename(
    #     month="月",
    #     day="日"
    # )
    # async def bday(self, interaction: discord.Interaction, month: app_commands.Range[int, 1, 12], day: app_commands.Range[int, 1, 31]) -> None:
    #     if interaction.channel_id == 1055393389463474239:
    #         if (month in [4, 6, 9, 11] and day == 31) or (month == 2 and day > 29):
    #             await interaction.response.send_message(f'{month}月並沒有{day}日<:angry_fox:1026061884304138321>', ephemeral=True)
    #         else:
    #             date = f'{month:02d}{day:02d}'
    #             print(date)
    #             sql = (f"INSERT INTO bday (id, name, month, day) VALUES ({interaction.user.id},'{interaction.user.name}' ,{month}, {day})"
    #             f"ON DUPLICATE KEY UPDATE name = '{interaction.user.name}', month={month}, day = {day}")
    #             self.cursor.execute(sql)
    #             await interaction.response.send_message(f'你的生日是{month}月{day}日')
    #     else:
    #         await interaction.response.send_message(f"請在<#1055393389463474239>使用此指令", ephemeral=True)

    @app_commands.command(name="我冷嗎", description="查看你有多少紙皮")
    async def check(self, interaction: discord.Interaction):
        result = self.cursor.execute(f'SELECT cardboards FROM cardboard WHERE id = {interaction.user.id}')
        print(result)
        await interaction.response.send_message(f'{self.cursor.fetchone()[0]}')

    @commands.command()
    async def give_money(self, ctx: commands.Context, who: discord.User, amount):
        change_money(self.cursor, who.id, amount)
        await ctx.reply(f"Who: {who.id}, Amount: {amount}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        econ(bot), 
        guild = discord.Object(id = 1021667971682287627))