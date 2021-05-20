# Dola
Dola is a Python-based bot specialising in Splatoon and [Slapp](https://github.com/kjhf/SplatTag) but also comes with some utility functions.
Code on [Github](https://github.com/kjhf/DolaBot).

Import prefix is `DolaBot`.

## Requirements
- Python 3.9+

## Bot Setup 
* Create a `.env` in the repository root with the following values:

```py
# This is the bot's Discord token from the Developer API page.
BOT_TOKEN="xxxx.xxxx.xxxx"
# This is the bot's Discord Id.
CLIENT_ID=123456789
# This is your Discord Id.
OWNER_ID=123456789
# Path to SplatTagConsole for Slapp things
SLAPP_CONSOLE_PATH=".../SplatTagConsole.dll"
# Path to the Slapp App Data folder
SLAPP_DATA_FOLDER=".../SplatTag"  
```
