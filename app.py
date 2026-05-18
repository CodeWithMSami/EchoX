import discord
from discord.ext import commands
from utils.database import get_command_prefix
from dotenv import load_dotenv
from utils.envs import DISCOR_TOKEN

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

bot.run(DISCOR_TOKEN)