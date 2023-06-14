from typing import Optional, Union, Tuple, List

import discord
from discord import Embed, Color, Colour
from slapp_py.helpers.str_helper import truncate

# LIMITS: See https://discord.com/developers/docs/resources/channel#embed-limits-limits
TITLE_LIMIT = 256
DESCRIPTION_LIMIT = 4096
NUMBER_OF_FIELDS_LIMIT = 25
FIELD_NAME_LIMIT = 256
FIELD_VALUE_LIMIT = 1024
FOOTER_TEXT_LIMIT = 2048
AUTHOR_NAME_LIMIT = 256
MESSAGE_TEXT_LIMIT = 2000
TOTAL_CHARACTER_LIMIT = 6000


def to_embed(
        message: str,
        colour: Union[None, Colour, Tuple[int, int, int]] = None,
        title: str = None,
        image_url: Optional[str] = None) -> Embed:
    """
    Convert string to embed with an optional title and colour.
    :exception Bad Request: Raised if any of the following are broken:
        - Embed titles are limited to 256 characters
        - Embed descriptions are limited to 4096 characters
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
        raise discord.InvalidData('Specify message or image_url')

    return discord.Embed(
        description=truncate(description, DESCRIPTION_LIMIT),
        colour=colour if not isinstance(colour, (int, int, int)) else Color.from_rgb(colour[0], colour[1], colour[2]),
        url=image_url,
        title=truncate(title, TITLE_LIMIT)  # Embed titles limited to 256 characters.
    )


def append_unrolled_list(
        builder: Embed,
        field_header: str,
        field_values: List[str],
        separator: str = '\n',
        max_unrolls: int = NUMBER_OF_FIELDS_LIMIT) -> None:
    """
    Append a list to the builder as strings that might append multiple fields.
    If an individual string would overflow the field, it will be truncated to fit.

    :param builder: The embed builder to append to.
    :param field_header: The title of the field. A count will be automatically added.
    :param field_values: The list of strings to add to the field(s).
    :param separator: The separator between strings. Newline by default.
    :param max_unrolls: The maximum number of fields to add. Will max out at NUMBER_OF_FIELDS_LIMIT.
    """
    max_unrolls = min(max_unrolls, NUMBER_OF_FIELDS_LIMIT)

    if len(field_values):
        for batch in range(0, max_unrolls):
            values_length = len(field_values)
            this_batch_message = ''
            j = 0
            for j in range(0, values_length):
                # Check if we'd overrun the field by adding this message.
                single_value_to_add = field_values[j] + separator
                if len(this_batch_message) + len(single_value_to_add) >= FIELD_VALUE_LIMIT:
                    # Check if we're going to loop indefinitely
                    if j == 0:
                        # Bite the bullet and truncate-add otherwise we'd get stuck
                        this_batch_message += truncate(field_values[j], FIELD_VALUE_LIMIT, "…" + separator)
                    break
                else:
                    this_batch_message += field_values[j] + separator
            field_values = field_values[min(values_length, (j + 1)):]
            no_more = len(field_values) <= 0
            only_field = no_more and batch == 0
            header = f'{field_header}:' if only_field else f'{field_header} ({(batch + 1)}):'
            builder.add_field(name=header,
                              value=truncate(this_batch_message, FIELD_VALUE_LIMIT),
                              inline=False)
            if no_more:
                break
