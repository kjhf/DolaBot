"""Meme commands cog."""
import logging
import os
import re
from typing import Union
import discord
import requests
from discord.ext import commands
from discord.ext.commands import Context

from DolaBot.constants.emojis import EEVEE

IMAGE_FORMATS = ["image/png", "image/jpeg", "image/jpg"]


class MemeCommands(commands.Cog):
    """A grouping of meme commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='slap',
        description='oops',
        pass_ctx=True
    )
    async def slap(self, ctx: Context):
        await ctx.message.add_reaction(EEVEE)

    @commands.command(
        name='jpg',
        description='jpgs your avatar',
        pass_ctx=True
    )
    async def jpg(self, ctx: Context, quality_or_url: Union[str, int] = 10, quality: int = 10):
        try:
            import tempfile
            (handle_int, filename) = tempfile.mkstemp('.jpg')
            if isinstance(quality_or_url, str) and re.match(r"[-+]?\d+$", quality_or_url) is None:
                with open(filename, 'wb') as handle:
                    r = requests.head(quality_or_url)
                    if r.headers["content-type"] not in IMAGE_FORMATS:
                        await ctx.send(f"Something went wrong 😔 (not an image)")
                        return

                    r = requests.get(quality_or_url, stream=True)
                    if r.status_code != 200:
                        await ctx.send(f"Something went wrong 😔 {r.__str__()}")
                        return

                    for block in r.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
                logging.info(f'Saved url {quality_or_url} temp to {filename}')
            else:
                quality = int(quality_or_url)
                await ctx.author.avatar_url.save(filename)
                logging.info(f'Saved {ctx.author} avatar at url {ctx.author.avatar_url} temp to {filename}')

            from PIL import Image
            im = Image.open(filename)
            im = im.convert("RGB")
            im.save(filename, format='JPEG', quality=quality)

            file = discord.File(fp=filename)
            await ctx.send(f"Here you go! (Quality: {quality})", file=file)
            os.close(handle_int)
            os.remove(filename)
        except Exception as e:
            await ctx.send(f"Something went wrong 😔 {e}")
