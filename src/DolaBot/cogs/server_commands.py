"""Server-affecting admin/mod commands cog."""
from typing import Optional, Union

import discord
from discord import Role, Guild, Member
from discord.ext import commands
from discord.ext.commands import Context

from DolaBot.constants.bot_constants import COMMAND_PREFIX
from DolaBot.helpers.discord_helper import get_members


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
            guild_members = await get_members(guild, role)
            count = len(guild_members)
            if role:
                await ctx.send(f"{count}/{guild.member_count} users are in this server with the role {role.name}!")
            else:
                await ctx.send(f"{count} users are in the server!")
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

            if not role:
                role = "everyone"

            role = role.lstrip('@')

            if not user:
                user = ctx.author

            roles = [f"{r.__str__().lstrip('@')}" for r in user.roles]
            has_role = role.__str__() in roles

            await ctx.send(f"{user.display_name} has {role}!" if has_role else f"{user.display_name} does not have {role}!")

            if not has_role:
                await self.print_roles(ctx, roles)
        else:
            await ctx.send("Hmm... we're not in a server! 😅")

    @commands.command(
        name='ColourMe',
        description="Give the user a coloured role.",
        brief="Give the user a coloured role.",
        aliases=['colorme', 'colourme', 'color_me', 'colour_me'],
        help=f'{COMMAND_PREFIX}colourme [_colour_|random|remove]. The colour may be a common English name or hex code.',
        pass_ctx=True)
    async def colour_me(self, ctx: Context, *, colour_str: Optional[str]):
        if not colour_str:
            await ctx.send_help(self.colour_me)
            return

        colour: Optional[discord.Colour] = None
        colour_str = colour_str.strip('#').replace(" ", "_").lower()

        # First, test if the colour was given as three separate numbers
        parts = colour_str.split('_')
        if len(parts) == 3:
            # Assume hex, unless any numbers are above 3 digits.
            try:
                if any((len(s) == 3 for s in parts)):
                    hit = [int(part) for part in parts]
                else:
                    hit = [int(part, 16) for part in parts]
            except (ValueError, IndexError, TypeError):
                pass
            else:
                colour = discord.Colour.from_rgb(*hit)

        try:
            # First try some missing colours from discord's library
            lookup = {
                "aqua":       [190, 211, 229],
                "beige":      [245, 245, 220],
                "black":        [0,   0,   1],
                "brown":      [153, 102,  51],
                "cyan":         [0, 255, 255],
                "generic":      [0, 153, 255],  # Inkipedia
                "grello":     [170, 220,   0],  # Inkipedia
                "indigo":     [111,   0, 255],
                "lime":       [191, 255,   0],
                "maroon":     [128,   0,   0],
                "niwa":       [255, 128,   0],  # Inkipedia
                "octo":       [174,  21, 102],  # Inkipedia
                "olive":      [128, 128,   0],
                "peach":      [255, 229, 180],
                "pink":       [255, 192, 203],
                "salmon":     [255, 128, 128],
                "silver":     [192, 192, 192],
                "splatoon":   [170, 220,   0],  # Inkipedia
                "splatoon_2": [240,  60, 120],  # Inkipedia
                "splatoon_3": [235, 238,  61],  # Inkipedia
                "tan":        [210, 180, 140],
                "turquoise":   [64, 224, 208],
                "violet":     [143,   0, 255],
                "white":      [255, 255, 255],
                "yellow":     [255, 255,   0],

                # Special
                "remove": [0, 0, 0],
            }
            hit = lookup.get(colour_str, None)

            if hit is None:
                # Get from discord's library (including random())
                colour = getattr(discord.Colour, colour_str)()
            else:
                colour = discord.Colour.from_rgb(hit[0], hit[1], hit[2])

        except AttributeError:
            # Try parse a hex-code
            try:
                if len(colour_str) == 6:
                    colour = discord.Colour.from_rgb(
                        int(colour_str[0:2], 16),
                        int(colour_str[2:4], 16),
                        int(colour_str[4:6], 16))
                elif len(colour_str) == 3:
                    colour = discord.Colour.from_rgb(
                        int(f"{colour_str[0]}{colour_str[0]}", 16),
                        int(f"{colour_str[1]}{colour_str[1]}", 16),
                        int(f"{colour_str[2]}{colour_str[2]}", 16))
            except (ValueError, IndexError, TypeError):
                pass

        if not isinstance(colour, discord.Colour):
            await ctx.send("I didn't understand your colour. "
                           "Please specify an English colour, `random`, or a 3-digit or 6-digit hex code")
            return

        guild: Optional[Guild] = ctx.guild
        if guild:
            if not guild.me.guild_permissions.manage_roles:
                await ctx.send("I can't do that as I don't have the manage roles permission.")
                return

            await ctx.guild.fetch_roles()
            ctx.guild.fetch_members(limit=None)
            user: Union[discord.User, discord.Member] = ctx.author
            user_colour_roles = [r for r in user.roles if r.__str__().startswith('dola_')]
            request_role_name = f'dola_{colour.value}'
            matched_guild_role = next((r for r in guild.roles if r.__str__().lstrip('@') == request_role_name), None)

            # If the user has colour roles already, remove it
            if user_colour_roles:
                for role in user_colour_roles:
                    await user.remove_roles(role, reason=f"Dola (Requested change by {user.id}")

            # Remove roles that no longer have any users
            for role in user_colour_roles:
                if not any(True for user in guild.members if role in user.roles):
                    await role.delete(reason=f"Dola (No more users with this role)")

            # Add the requested role to the user
            if colour != discord.Colour.default():
                if matched_guild_role:
                    await user.add_roles(matched_guild_role, reason=f"Dola (Requested by {user.id}")
                else:
                    try:
                        new_role = await guild.create_role(name=request_role_name,
                                                           reason=f"Requested by {user.id}",
                                                           colour=colour)
                        await user.add_roles(new_role, reason=f"Dola (Requested by {user.id}")
                    except discord.errors.HTTPException:
                        await ctx.send("Discord rejected your request... did you give me a bad value?")
        else:
            await ctx.send("Hmm... we're not in a server! 😅")

    @staticmethod
    async def print_roles(ctx, roles):
        await ctx.send(', '.join([f"`{r}`" for r in roles]))
