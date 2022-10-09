import discord
from discord.ext import commands
import os
import asyncio

from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("ONLINE")

async def load_extension():
    for f in os.listdir("./cogs"):
        if f.endswith('.py'):
            await bot.load_extension('cogs.' + f[:-3])

async def main():
    await load_extension()
    await bot.start(os.getenv("TOKEN"))

asyncio.run(main())