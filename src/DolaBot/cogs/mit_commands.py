import asyncio
import logging
import os
import re
from typing import Optional

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
            command = command_parts[1]
            switch = {
                "001": await self.upload_discord_ids_to_sheet(message),
            }
            command_result = switch.get(command, None)
            if not command_result:
                result = f"Discarding webhook message because I don't understand the command: {command}"
                logging.warning(result)
            else:
                return command_result
        else:
            logging.warning(f"Discarding webhook message that does not start with a 🤖 emoji.")
        return result

    async def upload_discord_ids_to_sheet(self, message) -> str:
        if self.connector.valid:
            # Get the discord columns
            tag_regex = re.compile(r"(Discord Tag).*")
            id_regex = re.compile(r"(Discord Id).*")
            try:
                discord_tag_col = self.connector.sheet.findall(tag_regex)[0].col
                discord_id_col = self.connector.sheet.findall(id_regex)[0].col
                logging.debug(f"{discord_tag_col=} {discord_id_col=}")
            except Exception as ex:
                return f"Could not find the Discord tag/id column: {ex}. Columns loaded: {self.connector.sheet.col_count}"

            # Get the members in this server
            members = await get_members(message.guild)
            
            # Foreach discord tag in the column that doesn't already have an id, find a match in the server.
            tag_count = 0
            near_count = 0
            failed_count = 0
            cache_sheet = self.connector.sheet.get_values()

            await asyncio.sleep(1)  # 60 requests / min (1 a second); note it's Read requests per minute per user.
            logging.debug(f"{len(cache_sheet)} rows cached")

            for row in range(1, len(cache_sheet)):
                if not cache_sheet[row - 1][discord_id_col - 1]:
                    discord_tag = cache_sheet[row - 1][discord_tag_col - 1].strip().lower()
                    if not discord_tag:
                        continue

                    # Find the discord name from the server
                    match = next((member for member in members if member._user and member._user.__str__().strip().lower() == discord_tag), None)
                    if match:
                        cache_sheet[row - 1][discord_id_col - 1] = match._user.id.__str__()
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
                            cache_sheet[row - 1][discord_id_col - 1] = f"Id for {match._user.__str__()}: {match._user.id}"
                            near_count += 1
                        else:
                            logging.info(f"Could not find a match for {discord_tag=}")
                            failed_count += 1
            # Commit
            cells = [Cell(row=row_i + 1, col=discord_id_col, value=row_list[discord_id_col - 1]) for row_i, row_list in enumerate(cache_sheet)]
            self.connector.sheet.update_cells(cells)
            return f"{tag_count} found tags, {near_count} found by discrim and first char, and {failed_count} members could not be found."
        else:
            return f"Cannot connect to Google Sheets."


class GSheetConnector:
    def __init__(self):
        try:
            google_creds_file = os.getenv("MIT_GOOGLE_CREDS_FILE_PATH")
            self.service = gspread.service_account(filename=google_creds_file)
        except FileNotFoundError:
            logging.error("Google creds file not found, will not complete sheet requests.")
            self.sheet = None
        else:
            self.sheet = self.service.open_by_key(os.getenv("MIT_GOOGLE_SHEET_ID")).get_worksheet(int(os.getenv("MIT_GOOGLE_SHEET_PAGE")))
            logging.debug("Loaded GSheetConnector")

    @property
    def valid(self):
        return self.sheet is not None
