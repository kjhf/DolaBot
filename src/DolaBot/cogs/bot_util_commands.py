"""Bot Utility commands cog."""
import os

import discord
from discord.ext import commands
from discord.ext.commands import Context

from DolaBot.constants.bot_constants import COMMAND_PREFIX
from slapp_py.helpers.str_helper import truncate


class BotUtilCommands(commands.Cog):
    """A grouping of bot utility commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Hello',
        description="Says hello.",
        brief="Says hi.",
        aliases=['hello', 'hi', 'hey'],
        help=f'{COMMAND_PREFIX}hello.',
        pass_ctx=True)
    async def hello(self, ctx: Context):
        await ctx.send("Hello, {}".format(ctx.message.author.mention))

    @commands.command(
        name='Invite',
        description="Grab an invite link.",
        brief="Grab an invite link.",
        aliases=['invite'],
        help=f'{COMMAND_PREFIX}invite',
        pass_ctx=True)
    async def invite(self, ctx: Context):
        await ctx.send(f"https://discordapp.com/oauth2/authorize?client_id={os.getenv('CLIENT_ID')}&scope=bot")

    @commands.command(
        name='DebugDetails',
        description="Posts some debugging information.",
        brief="Posts some debugging information.",
        aliases=['debug', 'debugdetails'],
        help=f'{COMMAND_PREFIX}debug.',
        pass_ctx=True)
    async def debugdetails(self, ctx: Context):
        from DolaBot.cogs.slapp_commands import SlappCommands

        try:
            is_owner = await ctx.bot.is_owner(ctx.author)
            console_path = os.getenv('SLAPP_CONSOLE_PATH')
            slapp_sources = os.getenv('SLAPP_DATA_FOLDER')

            if slapp_sources:
                slapp_sources_count = len([f for f in os.listdir(slapp_sources) if os.path.isfile(os.path.join(slapp_sources, f))])
            else:
                slapp_sources_count = -1

            await ctx.send(f"Slapp started: {SlappCommands.has_slapp_started()}\n"
                           f"Slapp caching finished: {SlappCommands.has_slapp_caching_finished()}\n"
                           f"Slapp queue length: {SlappCommands.get_slapp_queue_length()}\n"
                           f"Slapp console path: {console_path} (IsFile: {os.path.isfile(console_path)})\n"
                           f"Slapp sources: {slapp_sources} (IsDir: {os.path.isdir(slapp_sources)}) ({slapp_sources_count} files)\n"
                           f"Owner check: {is_owner}\n"
                           )
        except Exception as e:
            await ctx.send(f"Something went wrong compiling debug details! {truncate(e.__str__(), 900, '…')}")
