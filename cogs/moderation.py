import discord
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

        allowed_roles = ["Admin", "Moderator", "Developer", "Bot"]

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

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Moderation(bot))