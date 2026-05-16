from discord.ext import commands
from utils.embeds import commands_help

class Help(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

        self.bot.remove_command('help')

    @commands.command(name = "Help", aliases=["h","help"])
    async def  help(self, ctx:commands.Context, command: str | None = None):
        if command:
            command_help = self.bot.get_command(command)
        else:
            embed = commands_help(self.bot)
            await ctx.send(embed=embed)

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Help(bot))