import os
import dotenv
import logging

if __name__ == '__main__':
    dotenv.load_dotenv()
    if not os.getenv("BOT_TOKEN", None):
        assert False, "BOT_TOKEN is not defined, please check the .env file is present and correct."

    # Import must be after the env loading
    from DolaBot.entry.DolaBot import DolaBot

    logging.basicConfig(level=logging.INFO)
    dola = DolaBot()
    dola.do_the_thing()
    logging.info("Main exited!")
