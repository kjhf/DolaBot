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
    If the string contains an _ or *, it is wrapped in `.
    """
    if '`' in string:
        string = f"```{string}```"
    elif '_' in string or '*' in string:
        string = f"`{string}`"
    return string


def close_backticks_if_unclosed(string: str) -> str:
    if (string.count('```') % 2) == 1:  # If we have an unclosed ```
        string += '```'
    return string
