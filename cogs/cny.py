import discord
from discord.ext import commands
from .rwarray import read_array, write_array

class CNY(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.list = read_array("cny_list.txt")
        print(self.list)

    @commands.Cog.listener()
    async def on_ready(self):
        print('CNY')

    @commands.command(name="我要抽獎")
    async def enter(self, ctx: commands.Context):
        if ctx.channel.id == 1066657764669145129:
            id = str(ctx.author.id)
            print(id)
            print(self.list)
            if id in self.list:
                await ctx.reply("你已經參加抽獎了！")
            else:
                self.list.append(id)
                write_array("cny_list.txt", self.list)
                await ctx.reply("成功參加抽獎！祝你好運！")
                # await ctx.reply(await self.bot.fetch_user(ctx.author.id))

async def setup(bot):
    await bot.add_cog(CNY(bot))