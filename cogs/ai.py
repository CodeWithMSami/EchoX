from discord.ext import commands
from utils.envs import OPEN_ROUTER_API

class Ai(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command(name = "echox", aliases=["ai"])
    async def  commandName(self, ctx:commands.Context):
        '''Ask Ai for anything.'''
        await ctx.send("Ai answer.")

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Ai(bot))