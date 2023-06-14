import asyncio
import logging
import os
import sys

import discord
from discord import RawReactionActionEvent
from discord.ext import commands
from discord.ext.commands import Bot, CommandNotFound, UserInputError, MissingRequiredArgument, Context

from DolaBot.cogs.bot_util_commands import BotUtilCommands
from DolaBot.cogs.meme_commands import MemeCommands
from DolaBot.cogs.mit_commands import MITCommands
from DolaBot.cogs.sendou_commands import SendouCommands
from DolaBot.cogs.server_commands import ServerCommands
from DolaBot.cogs.slapp_commands import SlappCommands
from DolaBot.cogs.splatoon_commands import SplatoonCommands
from DolaBot.constants.bot_constants import COMMAND_PREFIX
from DolaBot.helpers.channel_logger import ChannelLogHandler


class DolaBot(Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # Subscribe to the privileged members intent for roles and reactions.
        intents.message_content = True
        intents.messages = True
        intents.presences = False
        intents.typing = False
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            intents=intents
        )
        self.mit_commands = None
        self.slapp_commands = None

    async def setup_hook(self):
        # Load Cogs
        await self.try_add_cog(BotUtilCommands)
        await self.try_add_cog(MemeCommands)
        self.mit_commands: MITCommands = await self.try_add_cog(MITCommands)
        await self.try_add_cog(SendouCommands)
        await self.try_add_cog(ServerCommands)
        self.slapp_commands: SlappCommands = await self.try_add_cog(SlappCommands)
        await self.try_add_cog(SplatoonCommands)

    async def try_add_cog(self, cog: commands.cog):
        try:
            new_cog = cog(self)
            await self.add_cog(new_cog)
            return new_cog
        except Exception as e:
            logging.error(f"Failed to load {cog=}: {e=}")

    async def on_command_error(self, ctx: Context, error, **kwargs):
        if isinstance(error, CommandNotFound):
            return
        elif isinstance(error, UserInputError):
            await ctx.send(error.__str__())
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(error.__str__())
        else:
            raise error

    async def on_message(self, message: discord.Message, **kwargs):
        # We do not want the bot to reply to itself
        if message.author == self.user:
            return

        # self.process_commands ###
        # If it's the MIT webhook, do stuff.
        # else, don't respond to bot messages.
        if message.author.bot and message.channel.id.__str__() == os.getenv("MIT_WEBHOOK_CHANNEL") \
                and message.author.id.__str__() == os.getenv("MIT_WEBHOOK_USER_ID"):
            message_to_send = await self.mit_commands.handle_webhook(message)
            await message.channel.send(message_to_send)
        elif message.author.bot:
            return

        # Process the message
        ctx = await self.get_context(message)
        await self.invoke(ctx)
        ###

    async def on_ready(self):
        ChannelLogHandler(self)
        logging.info(f'Logged in as {self.user.name}, id {self.user.id}')

        # noinspection PyUnreachableCode
        if __debug__:
            logging.getLogger().setLevel(level="DEBUG")
            presence = "--=IN DEV=--"
        else:
            presence = "in the cloud ⛅"

        if 'pydevd' in sys.modules or 'pdb' in sys.modules or '_pydev_bundle.pydev_log' in sys.modules:
            presence += ' (Debug Attached)'

        await self.change_presence(activity=discord.Game(name=presence))

    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.user_id != self.user.id:
            await self.slapp_commands.handle_reaction(payload)

    def do_the_thing(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(
                self.initialise_slapp(),
                self.start(os.getenv("BOT_TOKEN"))
            )
        )

    async def initialise_slapp(self):
        while self.slapp_commands is None:
            await asyncio.sleep(3)
        assert isinstance(self.slapp_commands, SlappCommands)
        logging.info("Beginning slapp init.")
        await self.slapp_commands.initialise_slapp()
