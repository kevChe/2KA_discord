import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

class Bot(commands.Bot):

    ignore = ['rwarray.py', 'nnn.py', 'oneAtwoB.py', 'tic.py', 'auto_assign.py', 'bday.py', 'cny.py', 'twitter.py', 'transaction.py']

    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents = discord.Intents.all(),
            application_id = 1028125267727745174
        )

    async def load(self):
        for f in os.listdir("./cogs"):
            if f.endswith('.py') and f not in self.ignore:
                cog_name = f'cogs.{f[:-3]}'
                print(cog_name)
                await self.load_extension(cog_name)

    async def setup_hook(self):
        await self.load()
        await bot.tree.sync(guild = discord.Object(id = 1021667971682287627))

    async def on_ready(self):
        print(f'Park Online')

bot = Bot()
bot.run(os.getenv("TOKEN"))