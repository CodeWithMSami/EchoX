import discord
from discord.ext import commands
from utils.database import get_command_prefix

def commands_help(bot: commands.AutoShardedBot):
    '''Help for all commands.'''
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

def command_help(bot: commands.AutoShardedBot, command: str):
    '''Help for single command.'''
    cmd = bot.get_command(command)
    
    if not cmd:
        embed = discord.Embed(
            title="Error",
            description=f"Command `{command}` not found.",
            color=discord.Colour.red()
        )
        return embed
    
    cmd_name = cmd.name
    cmd_description = cmd.description or cmd.help or "No description provided."
    cmd_aliases = cmd.aliases
    cmd_signature = cmd.signature
    
    required_args = []
    optional_args = []
    
    for param in cmd.clean_params.values():
        if param.default == param.empty:
            required_args.append(param.name)
        else:
            optional_args.append(f"{param.name} = {param.default}")
    
    embed = discord.Embed(
        title=f"Help: {cmd_name.capitalize()}",
        description=cmd_description,
        color=discord.Colour.green()
    )
    
    usage = f"`{bot.command_prefix()}{cmd_name}"
    if cmd_signature:
        usage += f" {cmd_signature}"
    usage += "`"
    embed.add_field(name="**Usage**", value=usage, inline=False)
    
    if cmd_aliases:
        aliases_str = ", ".join([f"`{alias}`" for alias in cmd_aliases])
        embed.add_field(name="**Aliases**", value=aliases_str, inline=False)
    
    if required_args:
        required_str = ", ".join([f"`{arg}`" for arg in required_args])
        embed.add_field(name="**Required Arguments**", value=required_str, inline=False)
    
    if optional_args:
        optional_str = ", ".join([f"`{arg}`" for arg in optional_args])
        embed.add_field(name="**Optional Arguments**", value=optional_str, inline=False)
    
    if cmd_signature:
        embed.add_field(name="**Parameters**", value=f"`{cmd_signature}`", inline=False)
    
    return embed

async def get_banned_users_embed(ctx: commands.Context, limit: int = 10):
    '''Returns an embed of banned users in the server'''
    
    banned_users = [entry async for entry in ctx.guild.bans()]
    
    if not banned_users:
        embed = discord.Embed(
            title="Banned Users",
            description="No banned users in this server.",
            color=discord.Colour.green()
        )
        return embed
    
    embed = discord.Embed(
        title=f"Banned Users ({len(banned_users)})",
        color=discord.Colour.red()
    )
    
    for i, entry in enumerate(banned_users[:limit], 1):
        user = entry.user
        reason = entry.reason or "No reason provided"
        
        if len(reason) > 50:
            reason = reason[:47] + "..."
        
        embed.add_field(
            name=f"{i}. {user} (ID: {user.id})",
            value=f"**Reason:** {reason}",
            inline=False
        )
    
    if len(banned_users) > limit:
        embed.set_footer(text=f"Showing {limit} of {len(banned_users)} banned users")
    
    return embed