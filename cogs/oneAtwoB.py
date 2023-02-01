from discord.ext import commands
import random

class oneAtwoB(commands.Cog):
    
    started = False
    targetNum = 0
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('1A2B online')

    @commands.command(name='1a2b')
    async def start(self, ctx: commands.Context, arg=None):
        if ctx.channel.id == 1050355043477495828:
            if(arg == 'end'):
                self.started = False
                await ctx.reply('遊戲結束')
            elif not self.started:
                self.started = True
                self.targetNum = random.sample('1234567890',4)
                print(self.targetNum)
                await ctx.reply("1A2B開始，請使用指令 !1a2b [輸入任意四位數]")
            elif arg is None or len(arg) != 4:
                await ctx.reply("請在!1A2B後 輸入任意四位數")
            else:
                a = 0
                for i in range(4):
                    #如果位置相同且數字相同 A+1
                    if(self.targetNum[i] == arg[i]):
                        a = a + 1 #A+1
                #檢查B 相同數字但不同位置
                b = 0
                for i in range(4):
                    #如果數字相同且位置不相同 B+1
                    if(arg[i] in self.targetNum and arg[i] != self.targetNum[i]):
                        b = b + 1 #B+1
                if a == 4:
                    self.started = False
                    await ctx.reply("好耶，全對了！")
                else:
                    await ctx.reply(f"{a}A{b}B")


async def setup(bot):
    await bot.add_cog(oneAtwoB(bot))