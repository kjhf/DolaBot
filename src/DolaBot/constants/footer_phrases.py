"""
This page contains the footer phrases that go onto the Slapp commands.
That is it.
Reading it may **spoil** the fun in seeing all the phrases for the first time.
You have been warned :)
"""
import random

from DolaBot.helpers import weapons


def get_random_footer_phrase() -> str:
    return random\
        .choice(FOOTER_PHRASES)\
        .replace('%weapon%', weapons.get_random_weapon())


FOOTER_PHRASES = [
    # General and for the morale
    "Slate says hi. ",
    "Slate loves Wug. ",
    "Has anyone told you that you're awesome? 🥰 ",
    "Don't shoot the messenger. ",
    "Be kind to one another. ",
    "Keep it up! You're doing great! ",
    "Coffee time? ",
    "I'm just here to make your verification slightly easier. ",
    "The real journey was the friends we made along the way. ",
    "Are you looking after yourself? ",
    "Stay hydrated, human. I'll pass on it though. ",
    "http://aws.random.cat 🐱 ",
    "https://random.dog/ 🐕 ",
    "I'm written in Python, Slapp is written in C#, but Slate is written in cups of tea and base 4 GCAT. ",
    "This sentence was written past 3am. ",
    "Just ignore when I used to tell you how long a query took. I lied about it. ",
    "You can join the dev server at https://discord.gg/wZZv2Cr",
    "Did you know that I have a ~jpg function? ",
    "The answer is... yes, that one. ",
    "The answer is... no. ",

    # LGBT+
    "Imagine a computer program to be non-binary. Haha. ",
    "Trans rights! ",

    # Splatoon and tournament shout-outs
    "You should Step Up, Europe. ",
    "Play LowInk. ",
    "Thank your TOs. ",
    "#SaveMelee ",
    "A Minnow is a small freshwater fish and also a tourney that you should join. ",
    "SPLATOON 3! ",
    "Please don't enter entire song lyrics as your name. ",
    "Do you remember when Nintendo released the SOS 2020 poster? Good times. ",
    "Thanks Inkipedia! ",
    "Your weapon of the day is... %weapon%! ",
    "The spirits tell me... %weapon%! ",

    # Internet memes and other game references
    "Other... games...? ",
    "Peace was never an option. 🔪 ",
    "BINGO! ",
    "*You hear Megalovania playing off in the distance* ",
    "Sus. ",
    "I'll have two number 9s, a number 6 with extra dip, a number 7, two number 45s, one with cheese, and a large soda. ",
    "You will be baked. And then there will be cake. ",
    "The square root of rope is string. ",
    "At some point in their lives 1 in 6 children will be abducted by the Dutch. ",
    "Humans can survive underwater. But not for very long. ",
    "Baba is you. You is win. ",
    "I hope you brought pancakes. ",
    "OBJECTION‼ 👉 ",
    "Nice drip ~ PERFECT! ",
    "Life is like a hurricane... Here in Duckburg... ",
    "Wake up, Mr Freeman. ",
    "Stonks. ",
    "*Sweats nervously* ",

    # TV, Film, and Music references
    "Orange is the new black. ",
    "Let's go to the Winchester, have a nice cold pint, and wait for this all to blow over. ",
    "SSWWAAAAAANN 🦢 ",
    "Check out 'is 'arse 🐴 ",
    "Did you take the red pill or the blue pill? ",
    "42. ",
    "We're only human after all. ",
    "Do not be sad because they left, be happy because they existed. ",
    "Buy it, use it, break it, fix it, trash it, change it, mail, upgrade it... ",
    "Soon may the Wellerman come, to bring us sugar and tea and rum... ",
    "What is love? ",
    "Ceci n'est pas une pipe. ",

    # Streamer parodies (YouTubers and Twitch)
    "We BOUNCE THAT BOI ",
    "I do not say poggies. ",
    "Doing it for the fans! Fans love it! ",
    "Alright so we're checking out the only place that does Splatoon verifications coming at you from a sentient AI... It's Dola. ",
    "More Splatoon content, goddammit. ",
    "Hello it is Dola bringing you yet another Slapp result. ",
    "Not sponsored by any mobile game or VPN software. ",

]
