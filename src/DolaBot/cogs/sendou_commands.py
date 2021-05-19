"""Bot Utility commands cog."""
import asyncio
import functools
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Tuple
from urllib.parse import quote_plus

import requests
from discord.ext import commands
from discord.ext.commands import Context

from PyBot.constants.bot_constants import COMMAND_PREFIX
from PyBot.helpers.weapons import try_find_weapon


class SendouCommands(commands.Cog):
    """A grouping of commands around sendou.ink"""
    sendou_cache: Dict[str, Tuple[datetime, str]] = dict()

    @commands.command(
        name='Builds',
        description="Gets some common builds from Sendou for the weapon.",
        brief="Gets some common builds from Sendou for the weapon.",
        aliases=['build', 'builds'],
        help=f'{COMMAND_PREFIX}builds weapon',
        pass_ctx=True)
    async def builds(self, ctx: Context, *, weapon_to_get: str):
        resolved_weapon = try_find_weapon(weapon_to_get)
        if not resolved_weapon:
            await ctx.send(f"I don't know what {weapon_to_get} is.")
            return
        # else
        message = await self.get_or_fetch_weapon_build(resolved_weapon)
        await ctx.send(message)

    async def get_or_fetch_weapon_build(self, resolved_weapon) -> str:
        cache_hit = self.sendou_cache.get(resolved_weapon, None)
        if cache_hit:
            logging.info(f"{resolved_weapon=} cache hit.")
            cache_time = cache_hit[0]
            if cache_time + timedelta(hours=6) > datetime.utcnow():
                logging.info("... returning previous message.")
                return cache_hit[1]
            else:
                logging.info(f"... but it's expired ({cache_time + timedelta(hours=6)=} > {datetime.utcnow()=} failed)")

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            functools.partial(requests.get,
                              url="https://sendou.ink/api/bot/builds",
                              params={"weapon": resolved_weapon}
                              )
        )

        if response and response.text:
            result = json.loads(response.text)
            message = f"**{resolved_weapon}**\n"

            nodes_read = 0
            for node in result:
                headgear = node.get("headAbilities", [])
                clothing = node.get("clothingAbilities", [])
                shoes = node.get("shoesAbilities", [])
                message += ''.join([ability_to_emoji(h) for h in headgear])
                message += "\n"
                message += ''.join([ability_to_emoji(c) for c in clothing])
                message += "\n"
                message += ''.join([ability_to_emoji(s) for s in shoes])

                nodes_read += 1
                if nodes_read >= 3:
                    break

                message += "\n\n"

            message += "\n" + "<https://sendou.ink/builds?weapon=" + quote_plus(resolved_weapon) + ">"
            self.sendou_cache[resolved_weapon] = (datetime.utcnow(), message)

        else:
            # If the cache hit then use that rather than returning a not-useful error message.
            if cache_hit:
                return cache_hit[1]
            else:
                message = f"Bad response from Sendou.ink: {response=}"
        return message


def ability_to_emoji(ability: str) -> str:
    """Translate the ability to an emoji, otherwise return the specified ability string if not found."""
    from PyBot.constants.emojis import ABILITY_DOUBLER, BOMB_DEFENSE_UP_DX, COMEBACK, DROP_ROLLER, \
        HAUNT, INK_RECOVERY_UP, INK_RESISTANCE_UP, INK_SAVER_MAIN, INK_SAVER_SUB, \
        LAST_DITCH_EFFORT, MAIN_POWER_UP, NINJA_SQUID, OBJECT_SHREDDER, \
        OPENING_GAMBIT, QUICK_RESPAWN, QUICK_SUPER_JUMP, RESPAWN_PUNISHER, \
        RUN_SPEED_UP, SPECIAL_CHARGE_UP, SPECIAL_POWER_UP, SPECIAL_SAVER, \
        STEALTH_JUMP, SUB_POWER_UP, SWIM_SPEED_UP, TENACITY, THERMAL_INK

    switch = {
        "AD": ABILITY_DOUBLER,
        "BDU": BOMB_DEFENSE_UP_DX,
        "CB": COMEBACK,
        "DR": DROP_ROLLER,
        "H": HAUNT,
        "REC": INK_RECOVERY_UP,
        "RES": INK_RESISTANCE_UP,
        "ISM": INK_SAVER_MAIN,
        "ISS": INK_SAVER_SUB,
        "LDE": LAST_DITCH_EFFORT,
        "MPU": MAIN_POWER_UP,
        "NS": NINJA_SQUID,
        "OS": OBJECT_SHREDDER,
        "OG": OPENING_GAMBIT,
        "QR": QUICK_RESPAWN,
        "QSJ": QUICK_SUPER_JUMP,
        "RP": RESPAWN_PUNISHER,
        "RSU": RUN_SPEED_UP,
        "SCU": SPECIAL_CHARGE_UP,
        "SPU": SPECIAL_POWER_UP,
        "SS": SPECIAL_SAVER,
        "SJ": STEALTH_JUMP,
        "BRU": SUB_POWER_UP,  # BRU is bomb range up
        "SSU": SWIM_SPEED_UP,
        "T": TENACITY,
        "TI": THERMAL_INK,
    }
    return switch.get(ability, ability)
