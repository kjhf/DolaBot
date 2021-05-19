from typing import Optional, Union, Tuple

import discord
from discord import Embed, Color, Colour
from slapp_py.helpers.str_helper import truncate


def to_embed(
        message: str,
        colour: Union[None, Colour, Tuple[int, int, int]] = None,
        title: str = None,
        image_url: Optional[str] = None) -> Embed:
    """
    Convert string to embed with an optional title and colour.

    :exception Bad Request: Raised if any of the following are broken:
        - Embed titles are limited to 256 characters
        - Embed descriptions are limited to 2048 characters
        - There can be up to 25 fields
        - A field's name is limited to 256 characters and its value to 1024 characters
        - The footer text is limited to 2048 characters
        - The author name is limited to 256 characters
        - In addition, the sum of all characters in an embed structure must not exceed 6000 characters
    :param message: The message content string
    :param colour: Embed discord colour or an RGB tuple.
    :param title: Embed title
    :param image_url: Optional image url to embed
    :return: The embed object built

    """
    if message is not None:
        description = message
    elif image_url is not None:
        description = image_url
    else:
        raise discord.InvalidArgument('Specify message or image_url')

    return discord.Embed(
        description=truncate(description, 2048, "…"),  # Embed descriptions limited to 2048 characters
        colour=colour if not isinstance(colour, (int, int, int)) else Color.from_rgb(colour[0], colour[1], colour[2]),
        image_url=image_url,
        title=truncate(title, 256, "…")  # Embed titles limited to 256 characters.
    )
