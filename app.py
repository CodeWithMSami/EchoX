import discord
from discord.ext import commands
from utils.database import get_command_prefix
from dotenv import load_dotenv
from utils.envs import DISCOR_TOKEN

import asyncio
import uvicorn

from utils.api import app, set_bot

intents = discord.Intents.all()
intents.message_content = True
intents.bans = True
intents.moderation = True

bot = commands.AutoShardedBot(intents=intents, command_prefix=get_command_prefix)

@bot.event
async def on_ready():
    await bot.load_extension("cogs.ai")
    await bot.load_extension("cogs.help")
    await bot.load_extension("cogs.moderation")
    print(f'{bot.user} is ready!')

async def start_api():
    set_bot(bot)

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000
    )

    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        bot.start(DISCOR_TOKEN),
        start_api()
    )

asyncio.run(main())