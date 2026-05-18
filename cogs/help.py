from discord.ext import commands
from utils.embeds import commands_help, command_help

class Help(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

        self.bot.remove_command('help')

    @commands.command(name = "help", aliases=["h"])
    async def  help(self, ctx:commands.Context, command: str | None = None):
        '''Command for getting help.'''
        if command is not None:
            embed = command_help(self.bot, command=command)
        else:
            embed = commands_help(self.bot)
        await ctx.send(embed=embed)

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Help(bot))