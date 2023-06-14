import asyncio
import datetime
import logging
import os
import re
from typing import Optional, Tuple, List

import discord
from discord.ext import commands
import gspread
from gspread import Cell

from DolaBot.helpers.discord_helper import get_members


class MITCommands(commands.Cog):
    """A grouping of Mulloway Institute of Turfing commands."""
    def __init__(self, bot):
        self.bot = bot
        self.connector = GSheetConnector()

    async def handle_webhook(self, message: discord.Message) -> Optional[str]:
        result = None
        content = message.content
        command_parts = content.split('-')
        if content.startswith('🤖') and command_parts[0] == '🤖':
            if command_parts[1] == "001":
                return await self.upload_discord_ids_to_sheet(message)
            elif command_parts[1] == "002":
                return await self.upload_friend_codes_to_sheet()
            else:
                result = f"Discarding webhook message because I don't understand the command: {content}"
                logging.warning(result)
        else:
            logging.warning(f"Discarding webhook message that does not start with a 🤖 emoji.")
        return result

    async def upload_discord_ids_to_sheet(self, message) -> str:
        if self.connector.valid and self.connector.mit_cycle_sheet:
            cache_sheet = self.connector.mit_cycle_sheet.get_values()
            
            # Get the discord columns
            try:
                discord_tag_index, discord_tag_col = self._find_col_from_cache(cache_sheet, re.compile(r"(Discord Tag).*", re.I))
                discord_id_index, discord_id_col = self._find_col_from_cache(cache_sheet, re.compile(r"(Discord Id).*", re.I))
                logging.debug(f"{discord_tag_col=} {discord_id_col=}")
            except Exception as ex:
                return f"Could not find the Discord tag/id column: {ex}. Columns loaded: {self.connector.mit_cycle_sheet.col_count}"

            # Get the members in this server
            members = await get_members(message.guild)
            
            # Foreach discord tag in the column that doesn't already have an id, find a match in the server.
            tag_count = 0
            near_count = 0
            skipped_count = 0
            failed_count = 0

            await asyncio.sleep(1)  # 60 requests / min (1 a second); note it's Read requests per minute per user.
            logging.debug(f"{len(cache_sheet)} rows cached")

            for row in range(1, len(cache_sheet)):
                if not cache_sheet[row - 1][discord_id_index]:
                    discord_tag = cache_sheet[row - 1][discord_tag_index].strip().lower()
                    if not discord_tag:
                        continue

                    # Find the discord name from the server
                    match = next((member for member in members if member._user and member._user.__str__().strip().lower() == discord_tag), None)
                    if match:
                        cache_sheet[row - 1][discord_id_index] = match._user.id.__str__()
                        logging.debug(f"Found a match for {discord_tag=}, {match._user.id=}")
                        tag_count += 1
                    else:
                        parts = discord_tag.rpartition('#')
                        username_lower = parts[0] or " "
                        discrim = parts[2] if len(parts) >= 2 else ''
                        match = next((member for member in members if member._user.name and member._user.name[0].lower() == username_lower[0]
                                      and member._user.discriminator == discrim), None)
                        if match:
                            logging.info(f"Near-matched {discord_tag=}: {discrim=}, {match._user.id=}")
                            cache_sheet[row - 1][discord_id_index] = f"Id for {match._user.__str__()}: {match._user.id}"
                            near_count += 1
                        else:
                            logging.info(f"Could not find a match for {discord_tag=}")
                            failed_count += 1
                else:
                    skipped_count += 1
            # Commit
            cells = [Cell(row=row_i + 1, col=discord_id_col, value=row_list[discord_id_index]) for row_i, row_list in enumerate(cache_sheet)]
            self.connector.mit_cycle_sheet.update_cells(cells)
            return f"{len(cells)} cells updated: {tag_count} new found tags, {near_count} found by discrim and first char, and {failed_count} members could not be found. {skipped_count} skipped. For a total of {tag_count+near_count+failed_count+skipped_count}."
        else:
            return f"Cannot connect to Google Sheets."

    async def upload_friend_codes_to_sheet(self) -> str:
        if self.connector.valid and self.connector.friend_code_sheet:
            cache_sheet = self.connector.friend_code_sheet.get_values()
            new_entries = []

            # Get the columns from the sheet
            try:
                server_id_index, server_id_col = self._find_col_from_cache(cache_sheet, re.compile(r"(Server Id).*"))
                channel_id_index, channel_id_col = self._find_col_from_cache(cache_sheet, re.compile(r"(Channel Id).*"))
                discord_id_index, discord_id_col = self._find_col_from_cache(cache_sheet, re.compile(r"(Discord Id).*"))
                discord_name_index, discord_name_col = self._find_col_from_cache(cache_sheet, re.compile(r"(Discord Name).*"))
                fc_index, fc_col = self._find_col_from_cache(cache_sheet, re.compile(r"(FC).*"))
                timestamp_index, timestamp_col = self._find_col_from_cache(cache_sheet, re.compile(r"(Timestamp).*"))
                logging.debug(f"{server_id_col=} {channel_id_col=} {discord_id_col=} "
                              f"{discord_name_col=} {fc_col=} {timestamp_col=}")
            except Exception as ex:
                return f"Could not find all the columns: {ex}. Columns loaded: {self.connector.friend_code_sheet.col_count}"

            # For each server the bot is in, find a friend code channel
            # For each post in that, parse an FC and assume it's the sender's - unless it's from a BOT account (Spyke),
            # in which case, check the previous message for the sender.

            logging.debug(f"{len(self.bot.guilds)=} guild(s) to search!")
            for guild in self.bot.guilds:
                from discord import TextChannel
                # regex testing -- https://regexr.com/6d6tf
                channels: List[TextChannel] = [channel for channel in guild.channels if isinstance(channel, TextChannel) and re.search(r"(^|\W|\s)f(riend)?([\w -]?)c(ode)?s?($|\W|\s)", channel.name, re.IGNORECASE)]
                logging.debug(f"Found {len(channels)=} friend code channel(s) in {guild.__str__()}! {channels!r}")
                for channel in channels:
                    bot_perms_for_channel = guild.me.permissions_in(channel)
                    if bot_perms_for_channel.read_messages and bot_perms_for_channel.read_message_history:
                        latest_for_this_channel = self._find_latest_for_channel_cache(cache_sheet, channel_id_index, timestamp_index, channel.id)

                        is_bot_fc_request = None
                        async for message in channel.history(limit=None, after=latest_for_this_channel):
                            fc_str = message.content
                            timestamp_ordinal = message.created_at.toordinal()
                            if message.author.bot:
                                if is_bot_fc_request:
                                    user = is_bot_fc_request
                                else:
                                    continue
                            elif message.content.endswith("getfc"):
                                is_bot_fc_request = message.author
                                continue
                            else:
                                user = message.author

                            from slapp_py.core_classes.friend_code import FriendCode
                            try:
                                fc = FriendCode.from_serialized(fc_str)
                            except (ValueError, AttributeError) as _:
                                logging.debug(f"Binned {message.content=} because it had no code.")
                                continue

                            if fc.no_code:
                                logging.debug(f"Binned {message.content=} because it had no code.")
                            else:
                                new_entries.append(self._make_new_fc_sheet_entry(
                                    server_id_index, guild.id,
                                    channel_id_index, channel.id,
                                    discord_id_index, user.id,
                                    discord_name_index, user.name,
                                    fc_index, fc.__str__(),
                                    timestamp_index, timestamp_ordinal))
                                logging.debug(f"Added new entry {fc.__str__()}!")
                            is_bot_fc_request = None
                    else:
                        logging.debug(f"Cannot read messages in this channel :(")

            # Commit all
            self.connector.friend_code_sheet.append_rows(new_entries)
            return f"{len(new_entries)} new rows!"
        else:
            return f"Cannot connect to Google Sheets."

    @staticmethod
    def _find_latest_for_channel_cache(cache, channel_id_index: int, timestamp_index: int, channel_id_to_find: int) -> Optional[datetime.datetime]:
        ordinal_datetime: Optional[int] = None
        if cache:
            try:
                for row_i, row_list in enumerate(cache):
                    if row_i == 0:
                        continue

                    if int(row_list[channel_id_index]) == channel_id_to_find:
                        if not ordinal_datetime:
                            ordinal_datetime = row_list[timestamp_index] or None
                        elif row_list[timestamp_index]:
                            if ordinal_datetime < int(row_list[timestamp_index]):
                                ordinal_datetime = int(row_list[timestamp_index])
            except Exception as ex:
                logging.error(f"_find_latest_for_channel_cache failed.", exc_info=ex)
        else:
            raise RuntimeError(f"Nothing in the cache to search for {channel_id_to_find=}.")
        return datetime.datetime.fromordinal(ordinal_datetime) if ordinal_datetime else None

    @staticmethod
    def _find_col_from_cache(cache, query: re) -> Tuple[int, int]:
        """Find the column with the specified regex from cache. Returns the index, and sheet's col id as a tuple"""
        if cache:
            for col in range(0, len(cache[0])):
                if query.search(cache[0][col]):
                    return col, (col + 1)
            else:
                raise RuntimeError(f"Unable to find {query.pattern=} in the cache sheet first row ({len(cache)=}")
        else:
            raise RuntimeError(f"Nothing in the cache to search for {query.pattern=}.")

    @staticmethod
    def _make_new_fc_sheet_entry(
            server_id_index: int, server_id: int,
            channel_id_index: int, channel_id: int,
            discord_id_index: int, discord_id: int,
            discord_name_index: int, discord_name: str,
            fc_index: int, fc: str,
            timestamp_index: int, timestamp: int):
        new_row = [""] * (max(server_id_index, channel_id_index, discord_id_index, discord_name_index, fc_index, timestamp_index) + 1)
        new_row[server_id_index] = server_id.__str__()
        new_row[channel_id_index] = channel_id.__str__()
        new_row[discord_id_index] = discord_id.__str__()
        new_row[discord_name_index] = discord_name
        new_row[fc_index] = fc
        new_row[timestamp_index] = timestamp.__str__()
        return new_row


class GSheetConnector:
    def __init__(self):
        try:
            google_creds_file = os.getenv("MIT_GOOGLE_CREDS_FILE_PATH")
            self.service = gspread.service_account(filename=google_creds_file)
        except FileNotFoundError:
            logging.error("Google creds file not found, will not complete sheet requests.")
            self.mit_cycle_sheet = None
            self.friend_code_sheet = None
        else:
            mit_workbook = self.service.open_by_key(os.getenv("MIT_GOOGLE_SHEET_ID"))
            if os.getenv("MIT_FC_PAGE_ID"):
                self.friend_code_sheet = mit_workbook.get_worksheet_by_id(int(os.getenv("MIT_FC_PAGE_ID")))
            else:
                logging.warning("MIT sheet was found but the MIT_FC_PAGE_ID was not specified.")
                self.friend_code_sheet = None
            self.mit_cycle_sheet = mit_workbook.get_worksheet(int(os.getenv("MIT_GOOGLE_SHEET_PAGE_INDEX")))
            logging.debug("Loaded GSheetConnector")

    @property
    def valid(self):
        return self.mit_cycle_sheet is not None
