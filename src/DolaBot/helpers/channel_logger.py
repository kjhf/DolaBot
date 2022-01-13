import asyncio
import logging
import os
import platform
from logging import StreamHandler

from discord.ext.commands import Bot

from DolaBot.helpers.embed_helper import MESSAGE_TEXT_LIMIT


class ChannelLogHandler(StreamHandler):
    def __init__(self, bot: Bot):
        StreamHandler.__init__(self)
        self.bot = bot
        self.log_channel = os.getenv("LOGS_CHANNEL", None)
        if self.log_channel:
            self.log_channel = self.bot.get_channel(int(self.log_channel))
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            self.setLevel(logging.INFO)
            computer_name = os.getenv("COMPUTERNAME", platform.node())
            formatter = logging.Formatter('[' + computer_name + '] [%(levelname)s]: %(message)s')
            self.setFormatter(formatter)
            logger.addHandler(self)

    def emit(self, record):
        msg = self.format(record)
        while len(msg) > MESSAGE_TEXT_LIMIT:
            truncated_send = msg[:MESSAGE_TEXT_LIMIT]
            asyncio.create_task(self.log_channel.send(truncated_send))
            msg = msg[MESSAGE_TEXT_LIMIT:]
        asyncio.create_task(self.log_channel.send(msg))
