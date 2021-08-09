from typing import Dict, Optional

from discord import Embed, Colour

from slapp_py.slapp_runner.slapp_response_object import SlappResponseObject


class ProcessedSlappObject:

    def __init__(self, embed: Optional[Embed], colour: Colour, reacts):
        self.embed: Optional[Embed] = embed
        self.colour: Colour = colour or Colour.dark_magenta()
        self.reacts: Dict[str, SlappResponseObject] = reacts or {}
        """Keyed by the reaction emoji"""
