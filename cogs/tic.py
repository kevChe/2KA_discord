from discord.ext import commands
import discord
from discord import File, app_commands
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math

class tic(commands.Cog):

    CHANNEL_ID = 1051364945947799582
    started = False
    LEFT = 325
    MID_COL = 435
    RIGHT = 540
    TOP = 20
    MID_ROW = 125
    BOTTOM = 230

    position_coor = [ [LEFT, TOP], [MID_COL, TOP], [RIGHT, TOP], 
                [LEFT, MID_ROW], [MID_COL, MID_ROW], [RIGHT, MID_ROW],
                [LEFT, BOTTOM], [MID_COL, BOTTOM], [RIGHT, BOTTOM] ]

    position_list = []
    ox = "O"

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print('tic tac toe online')

    group = app_commands.Group(name="ox", description="圓圈交叉遊戲")

    @group.command(name="start", description="開始圓圈交叉遊戲") # we use the declared group to make a command.
    async def start(self, interaction: discord.Interaction) -> None:
        """ 開始OX遊戲 """
        if interaction.channel_id == self.CHANNEL_ID:
            if not self.started:
                self.position_list = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
                self.ox = "O"
                secret_channel = self.bot.get_channel(1026387611230670848)
                temp_message = await secret_channel.send(file=File("inaforehead.png"))
                # await interaction.response.send_message(f"OX遊戲開始", view=self.view([]), embed = self.embed(temp_message.attachments[0]))
                await interaction.response.send_message(f"OX遊戲開始，O請選擇 {temp_message.attachments[0]}", view= await self.view())
            else:
                await interaction.response.send_message("遊戲進行中...")


    # @group.command(name='fill')
    # async def fill(self, interaction: discord.Interaction):
    #     if interaction.channel_id == 1050255861630648340:

    async def view(self) -> discord.ui.View():
        view = discord.ui.View()
        # buttons = []
        for i in range(9):
            button = discord.ui.Button(label=self.position_list[i], row = math.floor(i / 3))
            async def cb(interaction: discord.Interaction, i = i):
                if self.position_list[i] == " ":
                    self.position_list[i] = self.ox
                    self.reverse_ox()
                    temp_pic = await self.draw_image()
                    # await interaction.response.send_message(i)
                    # self.counter += 1

                    if self.win_check():
                        await interaction.response.edit_message(content=f"{interaction.user.name}獲勝！{temp_pic}", view=None)
                        self.started = False
                    else:
                        await interaction.response.edit_message(content=f"{self.ox}請選擇 {temp_pic}", view=await self.view())
                else:
                    await interaction.response.send_message(content="不能選擇已被選擇的格子，請重新選擇", ephemeral=True)
            button.callback = cb
            view.add_item(button)
        return view

    def embed(self, img) -> discord.Embed():
        embed = discord.Embed()
        embed.set_image(url=f"{img}")
        return embed

    async def draw_image(self) -> None:
        img = Image.open('inaforehead.png')
        I1 =  ImageDraw.Draw(img)
        font = ImageFont.truetype('wt009.ttf', size=100)
        counter = 0
        for i, block in enumerate(self.position_list):
            I1.text(self.position_coor[i], block, font=font, fill=(0, 0, 0))
        img.save("tic_results.png")
        secret_channel = self.bot.get_channel(1026387611230670848)
        temp_message = await secret_channel.send(file=File("tic_results.png"))
        return temp_message.attachments[0]

    def reverse_ox(self) -> None:
        if self.ox == "O":
            self.ox = "X"
        else:
            self.ox = "O"

    def win_check(self) -> bool:
        #Check row
        for i in range(0, 9, 3):
            setlist = set( [self.position_list[i], self.position_list[i + 1], self.position_list[i + 2]] )
            print(f"Row {i} {setlist}")
            if len(setlist) == 1 and " " not in setlist:
                return True

        #Check column
        for i in range(3):
            setlist = set( [self.position_list[i], self.position_list[i + 3], self.position_list[i + 6]] )
            print(f"Column {i} {setlist}")
            if len(setlist) == 1 and " " not in setlist:
                return True


        #Check diagonal
        setlist = set( [self.position_list[0], self.position_list[4], self.position_list[8]] )
        print(f"Diagonal Left {setlist}")
        if len(setlist) == 1 and " " not in setlist:
            return True
        
        setlist = set( [self.position_list[2], self.position_list[4], self.position_list[6]] )
        print(f"Diagonal Right {setlist}")
        if len(setlist) == 1 and " " not in setlist:
            return True

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        tic(bot), 
        guild = discord.Object(id = 1021667971682287627))