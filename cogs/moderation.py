from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Moderation(bot))