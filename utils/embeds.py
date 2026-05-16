import discord
from discord.ext import commands
from utils.database import get_command_prefix

def commands_help(bot: commands.AutoShardedBot):
    embed = discord.Embed(title="Help", description="Help for bot commands.", color=discord.Colour.green())
    
    categories = {}
    for cmd in bot.commands:
        if cmd.cog:
            category = cmd.cog.__class__.__name__
        else:
            category = "General"
        
        if category not in categories:
            categories[category] = []
        categories[category].append(f"`{cmd.name}`")
    
    for category, commands in categories.items():
        embed.add_field(
            name=category,
            value=", ".join(commands),
            inline=False
        )
    
    embed.set_footer(text=f"Total Commands: {len(bot.commands)}\nUse {get_command_prefix()}\n{get_command_prefix()}help <command> for details")
    return embed

