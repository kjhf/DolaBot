def wrap_in_backticks(string: str) -> str:
    if '`' in string:
        string = f"```{string}```"
    else:
        string = f"`{string}`"
    return string


def safe_backticks(string: str) -> str:
    if '`' in string:
        string = f"```{string}```"
    elif '_' in string or '*' in string:
        string = f"`{string}`"
    return string


def close_backticks_if_unclosed(string: str) -> str:
    if (string.count('```') % 2) == 1:  # If we have an unclosed ```
        string += '```'
    return string
