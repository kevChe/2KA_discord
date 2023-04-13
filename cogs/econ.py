from discord.ext import commands, tasks
import discord
from discord import File, app_commands
import pymysql
from .transaction import get_cardboards, update_cardboards

class econ(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.connection = pymysql.connect(host="db-buf-02.sparkedhost.us",autocommit=True ,port=3306, user="u75662_RNokPhakPC", passwd="v4RL73jqIfS^1lkMc@mZrZkE", db="s75662_NNN")
        self.cursor = self.connection.cursor()

    @commands.Cog.listener()
    async def on_ready(self):
        print('econ ONLINE')
        self.send_channel = self.bot.get_channel(1021667971682287630)

    @app_commands.command(name="我冷嗎", description="查看你有多少紙皮")
    async def check(self, interaction: discord.Interaction):
        result = self.cursor.execute(f'SELECT cardboards FROM cardboard WHERE id = {interaction.user.id}')
        print(result)
        await interaction.response.send_message(f'{self.cursor.fetchone()[0]}')

    @commands.command()
    async def give_money(self, ctx: commands.Context, who: discord.User, amount):
        # change_money(self.cursor, who.id, amount)
        await ctx.reply(f"Who: {who.id}, Amount: {amount}")

    @app_commands.command(name="轉移溫暖", description="把紙皮讓給別人")
    @app_commands.describe(
        to="把溫暖轉給誰，請用@用戶名",
        amount="要轉多少紙皮給對方"
    )
    async def transfer(self, interaction: discord.Interaction, to: discord.User, amount: app_commands.Range[int, 1]):
        sender = get_cardboards(self.cursor, interaction.user.id)
        receiver = get_cardboards(self.cursor, to.id)
        if sender - amount >= 0 :
            msg = "系統出錯"
            if update_cardboards(self.cursor, interaction.user.id, sender - amount) and update_cardboards(self.cursor, to.id, receiver + amount):
                    msg = f"{interaction.user.name}送了{amount}個紙皮給{to.name}"
            
        else:
            print("failed")
            msg = "紙皮不足"
        await interaction.response.send_message(msg)
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        econ(bot), 
        guild = discord.Object(id = 1021667971682287627))