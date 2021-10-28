from typing import Dict, Optional, Union

from discord import Embed, Colour

from slapp_py.core_classes.player import Player
from slapp_py.core_classes.team import Team


class ProcessedSlappObject:

    def __init__(self, embed: Optional[Embed], colour: Colour, reacts):
        self.embed: Optional[Embed] = embed
        self.colour: Colour = colour or Colour.dark_magenta()
        self.reacts: Dict[str, Union[Player, Team]] = reacts or {}
        """Keyed by the reaction emoji"""
