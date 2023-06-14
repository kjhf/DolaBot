import os
import sys

import dotenv
import logging

if __name__ == '__main__':
    dotenv_path = dotenv.find_dotenv()
    if not dotenv_path:
        assert False, ".env file not found. Please check the .env file is present in the root folder."
    sys.path.insert(0, os.path.dirname(dotenv_path))
    print(sys.path)

    dotenv.load_dotenv(dotenv_path)

    # Import must be after the env loading
    if not os.getenv("BOT_TOKEN", None):
        assert False, "BOT_TOKEN is not defined, please check the .env file is present and correct."

    # Import must be after the env loading
    from DolaBot.entry.DolaBot import DolaBot

    logging.basicConfig(level=logging.INFO)
    dola = DolaBot()
    dola.do_the_thing()
    logging.info("Main exited!")
