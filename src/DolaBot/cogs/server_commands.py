"""Server-affecting admin/mod commands cog."""
from typing import Optional, Union

from discord import Role, Guild, Member
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

    @commands.command(
        name='GetRoles',
        description="Get all the roles this server member has.",
        brief="Roles for a User.",
        aliases=['roles', 'getroles', 'get_roles'],
        help=f'{COMMAND_PREFIX}roles [member]',
        pass_ctx=True)
    async def roles(self, ctx: Context, user: Optional[Member]):
        guild: Optional[Guild] = ctx.guild
        if guild:
            await ctx.guild.fetch_roles()
            ctx.guild.fetch_members(limit=None)
            if not user:
                user = ctx.author
            roles = [f"{r.__str__()}".replace("@", "") for r in user.roles]
            await self.print_roles(ctx, roles)
        else:
            await ctx.send("Hmm... we're not in a server! 😅")

    @commands.command(
        name='HasRole',
        description="Get if the user has a role.",
        brief="Get if the user has a role",
        aliases=['hasrole', 'has_role'],
        help=f'{COMMAND_PREFIX}hasrole <role> [member]',
        pass_ctx=True)
    async def has_role(self, ctx: Context, role: str, user: Optional[Member]):
        guild: Optional[Guild] = ctx.guild
        if guild:
            await ctx.guild.fetch_roles()
            ctx.guild.fetch_members(limit=None)

            print(f"has_role: {ctx=} {role=} {user=}")

            if not role:
                role = "everyone"

            role = role.replace('@', '')

            if not user:
                user = ctx.author

            roles = [f"{r.__str__().replace('@', '')}" for r in user.roles]
            has_role = role.__str__() in roles

            await ctx.send(f"{user.display_name} has {role}!" if has_role else f"{user.display_name} does not have {role}!")

            if not has_role:
                await self.print_roles(ctx, roles)
        else:
            await ctx.send("Hmm... we're not in a server! 😅")

    @staticmethod
    async def print_roles(ctx, roles):
        await ctx.send(', '.join([f"`{r}`" for r in roles]))
