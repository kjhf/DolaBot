"""Splatoon commands cog."""
from discord.ext import commands
from discord.ext.commands import Context

from DolaBot.constants.bot_constants import COMMAND_PREFIX
from DolaBot.helpers.weapons import get_random_weapon
from DolaBot.translators.GameModeTranslator import GameModeTranslator
from DolaBot.translators.StageTranslator import StageTranslator


class SplatoonCommands(commands.Cog):
    """A grouping of Splatoon commands."""
    stage_translator = StageTranslator()
    mode_translator = GameModeTranslator()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Weapon',
        description="Draws a random Splatoon 2 weapon.",
        brief="Draws a random Splatoon 2 weapon.",
        aliases=['weapon'],
        help=f'{COMMAND_PREFIX}weapon.',
        pass_ctx=True)
    async def weapon(self, ctx: Context):
        await ctx.send(get_random_weapon())

    @commands.command(
        name='Stage',
        description='Lists the translations for the specified English stage in other languages',
        brief="Translates the specified stage into other languages",
        aliases=['stage', 'map'],
        help=f'{COMMAND_PREFIX}stage the_stage_name_to_translate',
        pass_ctx=True
    )
    async def stage(self, ctx: Context, *, stage_to_translate):
        if not stage_to_translate:
            await ctx.send_help(self)
        else:
            result = self.stage_translator.get_from_query(stage_to_translate) or "I don't know what that is."
            await ctx.send(result)

    @commands.command(
        name='Game Mode',
        description='Lists the translations for the specified English game mode in other languages',
        brief="Translates the specified stage into other languages",
        aliases=['mode', 'gamemode'],
        help=f'{COMMAND_PREFIX}mode the_mode_name_to_translate',
        pass_ctx=True
    )
    async def mode(self, ctx: Context, *, mode_to_translate):
        if not mode_to_translate:
            await ctx.send_help(self)
        else:
            result = self.mode_translator.get_from_query(mode_to_translate) or "I don't know what that is."
            await ctx.send(result)
