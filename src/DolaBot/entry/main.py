import os

import dotenv

if __name__ == '__main__':
    dotenv.load_dotenv()
    if not os.getenv("BOT_TOKEN", None):
        assert False, "BOT_TOKEN is not defined, please check the .env file is present and correct."

    # Import must be after the env loading
    from DolaBot.entry.DolaBot import DolaBot
    dola = DolaBot()
    dola.do_the_thing()
    print("Main exited!")
