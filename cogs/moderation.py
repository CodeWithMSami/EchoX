import discord
import datetime
from discord.ext import commands
from utils.database import get_command_prefix, set_command_prefix
from utils.embeds import get_banned_users_embed

class Moderation(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author):
            return True
        
        user_roles = [role.name for role in ctx.author.roles]

        allowed_roles = ["Admin", "Moderator", "Bot"]

        if any(role in user_roles for role in allowed_roles):
            return True

        return False

    @commands.command(name = "get_prefix", aliases=["prefix"])
    async def  get_prefix(self, ctx:commands.Context):
        '''Command to get prefix for commands usage.'''
        await ctx.send(f"Use `{get_command_prefix()}` before commands.")

    @commands.command(name = "set_prefix", aliases=["setPrefix"])
    async def  set_prefix(self, ctx:commands.Context, prefix: str):
        '''Command to set prefix for commands usage.'''
        result = set_command_prefix(prefix)
        if result:
            await ctx.send(f"Command prefix set to `{prefix}`")
        else:
            await ctx.send(f"Please retry.")

    @commands.command(name = "ban", aliases=["ban_member"])
    @commands.has_permissions(ban_members=True)
    async def  ban_member(self, ctx:commands.Context, member: discord.Member, *, reason: str | None = None):
        '''Ban a user by mentioning member.'''
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} banned.\n{f'for: {reason}' if reason is not None else ''}")

    @commands.command(name = "unban", aliases=["unban_member"])
    @commands.has_permissions(ban_members=True)
    async def  unban_member(self, ctx:commands.Context, *, member_name: str):
        '''Unban a user by their Username'''
        banned_users = [entry async for entry in ctx.guild.bans()]
        for entry in banned_users:
            if entry.user.name == member_name:
                await ctx.guild.unban(entry.user)
                await ctx.send(f"Unbanned {member_name}")
                return
        await ctx.send(f"User {member_name} not found in bans")

    @commands.command(name = "show_banned", aliases=["banned"])
    async def  show_banned(self, ctx:commands.Context, limit: int = 10):
        "Display first 10 banned members. Increase limit to get more."
        embed = await get_banned_users_embed(ctx=ctx, limit=limit)
        await ctx.send(embed=embed)

    @commands.command(name = "kick", aliases=["kick_member"])
    @commands.has_permissions(kick_members=True)
    async def  kick_member(self, ctx: commands.Context, member: discord.Member, *, reason: str | None = None):
        '''Kick the member command.'''
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked!{f'\n**for:** {reason}' if reason is not None else ''}")

    @commands.command(name = "mute", aliases=['mute_member'])
    @commands.has_permissions(moderate_members=True)
    async def mute_member(self, ctx: commands.Context, member: discord.Member, duration: str, *, reason: str | None = None):
        '''Mute a member using timeout.'''
        ctx.guild.fetch_members()

        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="❌ Error",
                description="You cannot mute someone with an equal or higher role!",
                color=discord.Colour.red()
            )
            return await ctx.send(embed=embed)
        
        time_units = {
            's': 1, 'm': 60, 'h': 3600, 'd': 86400
        }

        unit = duration[-1]
        amount = int(duration[:-1])

        if unit not in time_units:
            embed = discord.Embed(
                title="❌ Error",
                description="Invalid duration format! Use: `10s`, `5m`, `2h`, `1d`",
                color=discord.Colour.red()
            )
            return await ctx.send(embed=embed)
        
        seconds = amount * time_units[unit]

        reason_text = reason or "No reason provided"

        await member.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=seconds), reason=reason_text)

        embed = discord.Embed(
            title="🔇 Member Muted",
            description=f"{member.mention} has been muted for **{duration}**",
            color=discord.Colour.orange()
        )
        embed.add_field(name="Reason", value=reason_text)
        embed.set_footer(text=f"Moderator: {ctx.author}")
    
        await ctx.send(embed=embed)

    @commands.command(name = "unmute", aliases=["unmute_member"])
    @commands.has_permissions(moderate_members=True)
    async def  unmute_member(self, ctx:commands.Context, member: discord.Member):
        '''Remove timeout from a member'''

        await member.timeout(None)

        embed = discord.Embed(
            title="🔊 Member Unmuted",
            description=f"{member.mention} has been unmuted",
            color=discord.Colour.green()
        )

        await ctx.send(embed=embed)

    @commands.command(name = "warn", aliases=["warn_member"])
    @commands.has_permissions(kick_members=True)
    async def  warn_member(self, ctx:commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
        '''Warn a member.'''

        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="❌ Error",
                description="You cannot warn someone with an equal or higher role!",
                color=discord.Colour.red()
            )

            return await ctx.send(embed=embed)
        
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Error",
                description="You cannot warn yourself!",
                color=discord.Colour.red()
            )

            return await ctx.send(embed=embed)

        try:
            dm_embed = discord.Embed(
                title=f"⚠️ Warning from {ctx.guild.name}",
                description=f"**Reason:** {reason}",
                color=discord.Colour.red()
            )
            dm_embed.set_footer(text=f"Moderator: {ctx.author}")
            await member.send(embed=dm_embed)
        except:
            pass

        embed = discord.Embed(
            title="⚠️ Member Warned",
            description=f"{member.mention} has been warned",
            color=discord.Colour.orange()
        )
        embed.add_field(name="Reason", value=reason)
        embed.set_footer(text=f"Moderator: {ctx.author}")

        await ctx.send(embed=embed)

    @commands.command(name = "clear", aliases=["clear_messages"])
    @commands.has_permissions(manage_messages=True)
    async def  clear_messages(self, ctx:commands.Context, amount: int = 1):
        '''Delete multiple messages at once'''

        if amount < 1:
            embed = discord.Embed(
                title="❌ Error",
                description="You must delete at least 1 message!",
                color=discord.Colour.red()
            )
            return await ctx.send(embed=embed)

        if amount > 100:
            embed = discord.Embed(
                title="❌ Error",
                description="You can only delete up to 100 messages at once!",
                color=discord.Colour.red()
            )
            return await ctx.send(embed=embed)
        
        deleted = await ctx.channel.purge(limit=amount + 1)

        embed = discord.Embed(
            title="🗑️ Messages Cleared",
            description=f"Deleted {len(deleted) - 1} messages",
            color=discord.Colour.green()
        )
        msg = await ctx.send(embed=embed)
        await msg.delete(delay=3)

    @commands.command(name = "lockdown", aliases=["lockdown_channel"])
    @commands.has_permissions(manage_channels=True)
    async def  lockdown_channel(self, ctx:commands.Context, channel: discord.TextChannel = None):
        '''Lock a channel.'''

        channel = channel or ctx.channel

        await channel.set_permissions(ctx.guild.default_role, send_messages=False)

        embed = discord.Embed(
            title="🔒 Channel Locked",
            description=f"{channel.mention} has been locked",
            color=discord.Colour.red()
        )
        embed.add_field(name="Locked by", value=ctx.author.mention)

        await ctx.send(embed=embed)

    @commands.command(name = "unlock", aliases=["unlock_channel"])
    async def  unlock_channel(self, ctx:commands.Context, channel: discord.TextChannel = None):
        '''Unlock a channel'''

        channel = channel or ctx.channel

        await channel.set_permissions(ctx.guild.default_role, send_messages=None)

        embed = discord.Embed(
            title="🔓 Channel Unlocked",
            description=f"{channel.mention} has been unlocked",
            color=discord.Colour.green()
        )
        embed.add_field(name="Unlocked by", value=ctx.author.mention)

        await ctx.send(embed=embed)

    @commands.command(name = "slowmode", aliases=["slowmode_channel"])
    async def  slowmode_channel(self, ctx:commands.Context, seconds: int = 0):
        '''Set cooldown between messages'''

        if seconds < 0:
            embed = discord.Embed(
                title="❌ Error",
                description="Slowmode cannot be negative!",
                color=discord.Colour.red()
            )
            return await ctx.send(embed=embed)
        
        if seconds > 21600:
            embed = discord.Embed(
                title="❌ Error",
                description="Slowmode cannot exceed 6 hours (21600 seconds)!",
                color=discord.Colour.red()
            )
            return await ctx.send(embed=embed)

        await ctx.channel.edit(slowmode_delay=seconds)

        if seconds == 0:
            embed = discord.Embed(
                title="⏩ Slowmode Disabled",
                description=f"Slowmode has been removed in {ctx.channel.mention}",
                color=discord.Colour.green()
            )
        else:
            embed = discord.Embed(
                title="🐢 Slowmode Enabled",
                description=f"Members can now send a message every **{seconds}** seconds",
                color=discord.Colour.orange()
            )
    
        await ctx.send(embed=embed)

    async def cog_command_error(self, ctx: commands.Context, error):
        '''Handles errors for all commands in this cog'''
        
        if isinstance(error, commands.CommandNotFound):
            return
        
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Missing Permissions",
                description=f"You need: `{', '.join(error.missing_permissions)}`",
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed, delete_after=5)
        
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="❌ Bot Missing Permissions",
                description=f"I need: `{', '.join(error.missing_permissions)}`",
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed, delete_after=5)
        
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⏰ Command on Cooldown",
                description=f"Try again in `{error.retry_after:.1f}` seconds",
                color=discord.Colour.orange()
            )
            await ctx.send(embed=embed, delete_after=5)
        
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                title="❌ Member Not Found",
                description=f"Could not find member: `{error.argument}`",
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed, delete_after=5)
        
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="❌ Missing Argument",
                description=f"Missing: `{error.param.name}`\nUse `{get_command_prefix()}help {ctx.command.name}` for usage",
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed, delete_after=10)
        
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="❌ Invalid Argument",
                description=str(error),
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed, delete_after=5)
        
        elif isinstance(error, commands.CommandError):
            embed = discord.Embed(
                title="❌ Error",
                description=str(error),
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(
                title="❌ Unexpected Error",
                description=f"```py\n{error}\n```",
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed)
            print(f"Error in {ctx.command}: {error}")

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Moderation(bot))