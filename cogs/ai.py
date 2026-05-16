from discord.ext import commands

class Ai(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Ai(bot))