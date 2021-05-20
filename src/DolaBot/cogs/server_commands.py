"""Server-affecting admin/mod commands cog."""
from typing import Optional

from discord import Role, Guild
from discord.ext import commands
from discord.ext.commands import Context

from DolaBot.constants.bot_constants import COMMAND_PREFIX


class ServerCommands(commands.Cog):
    """A grouping of server-affecting admin/mod commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Members',
        description="Count number of members with a role specified, or leave blank for all in the server.",
        brief="Member counting.",
        aliases=['members', 'count_members'],
        help=f'{COMMAND_PREFIX}members [role]',
        pass_ctx=True)
    async def members(self, ctx: Context, role: Optional[Role]):
        guild: Optional[Guild] = ctx.guild
        if guild:
            await ctx.guild.fetch_roles()
            ctx.guild.fetch_members(limit=None)
            if role:
                count = sum(1 for user in guild.members if role in user.roles)
                await ctx.send(f"{count}/{guild.member_count} users are in this server with the role {role.name}!")
            else:
                await ctx.send(f"{guild.member_count} users are in the server!")
        else:
            await ctx.send("Hmm... we're not in a server! 😅")
