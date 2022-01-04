from typing import Optional, List

from discord import Guild, Role, Member


def wrap_in_backticks(string: str) -> str:
    """
    Wrap the string in backticks.
    If the string contains an `, it is wrapped in ```.
    Otherwise, only one ` is used either side.
    """
    if '`' in string:
        string = f"```{string}```"
    else:
        string = f"`{string}`"
    return string


def safe_backticks(string: str) -> str:
    """
    Wrap the string in backticks if and ony if it requires it.
    If the string contains an `, it is wrapped in ```.
    If the string contains an _ or *, or starts or ends with a space, it is wrapped in `.
    """
    if '`' in string:
        string = f"```{string}```"
    elif '_' in string or '*' in string or string.startswith(' ') or string.endswith(' '):
        string = f"`{string}`"
    return string


def close_backticks_if_unclosed(string: str) -> str:
    if (string.count('```') % 2) == 1:  # If we have an unclosed ```
        string += '```'
    return string


async def get_members(guild: Guild, role: Optional[Role] = None) -> List[Member]:
    await guild.fetch_roles()
    guild.fetch_members(limit=None)
    if role:
        return [member for member in guild.members if role in member.roles]
    return guild.members
