import discord
from discord.ext import commands
from utils.database import get_command_prefix
from dotenv import load_dotenv
from utils.envs import DISCOR_TOKEN

import uvicorn
import threading

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

def start_api():
    set_bot(bot)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=12459
    )


if __name__ == "__main__":
    api_thread = threading.Thread(
        target=start_api,
        daemon=True
    )
    api_thread.start()

    bot.run(str(DISCOR_TOKEN))