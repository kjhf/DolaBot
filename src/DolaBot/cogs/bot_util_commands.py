"""Bot Utility commands cog."""
from discord.ext import commands
from discord.ext.commands import Context

from PyBot.constants.bot_constants import COMMAND_PREFIX
from tokens import CLIENT_ID


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
        await ctx.send(f"https://discordapp.com/oauth2/authorize?client_id={CLIENT_ID}&scope=bot")
