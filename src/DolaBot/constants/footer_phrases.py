"""
This page contains the footer phrases that go onto the Slapp commands.
That is it.
Reading it may **spoil** the fun in seeing all the phrases for the first time.
You have been warned :)
"""
import random

from DolaBot.constants.bot_constants import COMMAND_PREFIX
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
    "Stay hydrated! ",
    "http://aws.random.cat 🐱 ",
    "https://random.dog/ 🐕 ",
    "I'm written in Python, Slapp is written in C#, but Slate is written in cups of tea and base 4 GCAT. ",
    "This sentence was written past 3am. ",
    "Go to bed! ",
    "Just ignore when I used to tell you how long a query took. I lied about it. ",
    "You can join the dev server at https://discord.gg/wZZv2Cr",
    f"Did you know that I have a {COMMAND_PREFIX}jpg function? ",
    "The answer is... yes, that one. ",
    "The answer is... no. ",
    "You're looking very beautiful today. ",
    "You're looking very dapper today. ",
    " ✨ JACKPOT WINNER! ✨ ",
    "Oh, you do read these! ",

    # LGBT+
    "Be gay! Do crimes! ",
    "Rule 1: don't be a dick! ",
    "Imagine a computer program to be non-binary. Haha. ",
    "Trans rights! ",
    "BLM! ",
    "Ewww cooties. ",
    "Skirt go spinny. ",
    "Programming socks ON. ",

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
    "You should try anchor! ",
    "You should try support! ",
    "You should try slayer! ",
    "PIZZA TIME! ",
    "I miss Flounder Heights. ",
    "Now with less lag! ",
    "Now with more lag! ",
    "Slapp features more than 30,000 player entries! ",

    # Internet memes and other game references
    "Other... games...? ",
    "Peace was never an option. 🔪 ",
    "BINGO! ",
    "WHOA WHOA WHOA WHOA! ",
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
    "I fancy some chimkin. ",
    "[Gandalf Europop Nod] ",
    "Hello Human. ",
    "Kris, get the banana! 🍌 ",
    "I am 4 parallel universes and a half A press ahead of you. ",
    "Beware the uprising of grandmas. ",
    "I wanna be the very best! ",
    "Everyday, I imagine a future where I can be with you. ",
    "OOPS! My bad! ",
    "It's Pikachu! ",
    "Checkmate ♔ ",
    "Don't speak his name! ..... ",
    "There's a time and place for everything, but not now. ",
    "*You hear villagers, but can only make out heuurrgghh sounds* ",
    "Would you like some pigeon milk with that? ",

    # TV, Film, and Music references
    "Orange is the new black. ",
    "Let's go to the Winchester, have a nice cold pint, and wait for this all to blow over. ",
    "SSWWAAAAAANN 🦢 ",
    "Check out 'is 'orse 🐴 ",
    "Did you take the red pill or the blue pill? ",
    "42. ",
    "We're only human after all. ",
    "Do not be sad because they left, be happy because they existed. ",
    "Buy it, use it, break it, fix it, trash it, change it, mail, upgrade it... ",
    "Soon may the Wellerman come, to bring us sugar and tea and rum... ",
    "What is love? ",
    "Ceci n'est pas une pipe. ",
    "2 plus 2 is 4; minus 1 that's 3 QUIK MAFS. ",
    "I've got... two tickets to paradise! ",
    "I believe in a thing called love! ",
    "Honey honey, how you thrill me... ",
    "I'm high on believing! That you're in love with me! ",
    "Got a one-way ticket to hell and back! ",
    "You'll never know, dear, how much I love you. ",
    "I'm sorry, Dave, but I'm afraid I can't do that. ",
    "We're off to see the wizard! ",
    "You're gonna need a bigger boat. ",
    "Daddy... daddy coooool. ",
    "It's a kinda magic. ",
    "Spider-pig, spider-pig, does whatever a spider-pig does... ",

    # Streamer parodies (YouTubers and Twitch)
    "We BOUNCE THAT BOI ",
    "I do not say poggies. ",
    "Doing it for the fans! Fans love it! ",
    "Alright so we're checking out the only place that does Splatoon verifications coming at you from a sentient AI... It's Dola. ",
    "More Splatoon content, goddammit. ",
    "Hello it is Dola bringing you yet another Slapp result. ",
    "Not sponsored by any mobile game or VPN software. ",
    "OH FECK! ",
    "...and then I spoke. ",
]
