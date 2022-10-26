from discord.ext import commands
import discord

class NNN(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("NNN bot online")

    @task.loop(days = 1)
    async def notif(self):
        channel = self.bot.channel()
        await channel.send("")


async def setup(bot):
    await bot.add_cog(AutoAssign(bot))