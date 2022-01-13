import asyncio
import base64
import inspect
import json
import logging
import unittest
from time import time
from typing import Any, Callable

import dotenv
from discord.ext.commands import Bot

from slapp_py.core_classes.player import Player
from slapp_py.core_classes.team import Team
from slapp_py.slapp_runner.slapipes import SlapPipe

from error_flagger_logger import ErrorFlaggerLogger


class DolaSlappTests(unittest.IsolatedAsyncioTestCase):
    flagger: ErrorFlaggerLogger

    def setUp(self):
        self.flagger = ErrorFlaggerLogger()

    def tearDown(self):
        if self.flagger:
            errors = self.flagger.errors
            self.fail(f"Error Flagger caught {len(errors)} error(s):\n" + '\n'.join(errors))

    @staticmethod
    async def receive_slapp_response(success_message: str, response: dict):
        logging.info(f"Slapp response: {success_message=} {response=}")
        pass

    async def test_verify_slapp_starts(self):
        dotenv.load_dotenv()
        logging.basicConfig(level=logging.DEBUG)

        try:
            try:
                # Mode '' will poke slapp but not actually do anything
                slappipe = SlapPipe()
                await asyncio.wait_for(slappipe.initialise_slapp(self.receive_slapp_response, mode=''), timeout=60.0)
            except asyncio.TimeoutError:
                self.fail(f"Timed out waiting for slapp.")
        except Exception as ex:
            self.fail(f"Not expecting an exception: {ex}")

    async def test_dola_receive_slapp_function(self):
        dotenv.load_dotenv()
        logging.basicConfig(level=logging.DEBUG)

        try:
            try:
                from DolaBot.cogs.slapp_commands import SlappCommands, slapp_ctx_queue
                commands = SlappCommands(Bot(None))

                # Test data in the testdata folder, which is generated directly from Slapp and copied with
                # SplatTagConsole.exe --query "e" --verbose >slapp_result.txt 2>&1
                with open("../testdata/slapp_result.txt", 'r', encoding='utf-8') as infile:
                    response = infile.read()
                decoded_bytes = base64.b64decode(response)
                response = json.loads(str(decoded_bytes, "utf-8"))

                # Establish a connection
                await commands.receive_slapp_response("Connection established.", {})

                # Push this request into queue
                slapp_ctx_queue.append((None, "slapp"))

                # And get a response from Slapp
                start_time = time()
                await asyncio.wait_for(commands.receive_slapp_response("OK", response), timeout=600.0)
                print(f'Time taken to process response: {time() - start_time:0.3f}s')
            except asyncio.TimeoutError:
                self.fail(f"Timed out waiting for Dola to build the message from the Slapp response.")
        except Exception as ex:
            self.fail(f"Not expecting an exception: {ex}")

    def test_empty_player_sanity(self):
        from slapp_py.core_classes.player import Player
        self._sanity_check_class(Player())

    def test_empty_team_sanity(self):
        from slapp_py.core_classes.team import Team
        self._sanity_check_class(Team())

    def test_empty_source_sanity(self):
        from slapp_py.core_classes.source import Source
        self._sanity_check_class(Source())

    def test_empty_response_sanity(self):
        from slapp_py.slapp_runner.slapp_response_object import SlappResponseObject
        self._sanity_check_class(SlappResponseObject({}))

    def test_populated_response_sanity(self):
        # Test data in the testdata folder, which is generated directly from Slapp and copied with
        # SplatTagConsole.exe --query "e" --verbose >slapp_result.txt 2>&1
        with open("../testdata/slapp_result.txt", 'r', encoding='utf-8') as infile:
            response = infile.read()
        decoded_bytes = base64.b64decode(response)
        from slapp_py.slapp_runner.slapp_response_object import SlappResponseObject
        response = SlappResponseObject(json.loads(str(decoded_bytes, "utf-8")))
        self._sanity_check_class(response)

    def test_serialize_populated_response(self):
        # Test data in the testdata folder, which is generated directly from Slapp and copied with
        # SplatTagConsole.exe --query "e" --verbose >slapp_result.txt 2>&1
        with open("../testdata/slapp_result.txt", 'r', encoding='utf-8') as infile:
            response = infile.read()
        decoded_bytes = base64.b64decode(response)
        from slapp_py.slapp_runner.slapp_response_object import SlappResponseObject
        response = SlappResponseObject(json.loads(str(decoded_bytes, "utf-8")))
        # Serialise the players, teams, and brackets
        player_dicts = [p.to_dict() for p in response.matched_players]
        team_dicts = [t.to_dict() for t in response.matched_teams]
        bracket_dicts = [[b.to_dict() for b in brackets] for s, brackets in response.get_brackets_for_player(response.matched_players[0]).items()]
        self.assertTrue(player_dicts)
        self.assertTrue(team_dicts)
        self.assertTrue(bracket_dicts, "No bracket information for players in response?")

        # Try to filter to a source, which will test the sources linking to the players and teams as well as internals
        player = response.matched_players[0]
        source = player.sources[0]
        player_filtered = player.filter_to_source(source)
        self.assertIsNotNone(player_filtered)

        team = response.matched_teams[0]
        source = team.sources[0]
        team_filtered = team.filter_to_source(source)
        self.assertIsNotNone(team_filtered)

        # Check divs in sources
        luti_player = next((player for player in response.matched_players if any('LUTI-' in s.name for s in player.sources)), None)
        self.assertIsNotNone(luti_player, f"No LUTI source found in response? Player sources: {[player.sources for player in response.matched_players]!r}")
        division = response.get_best_division_for_player(luti_player)
        self.assertIsNotNone(division, "get_best_division_for_player unexpectedly returned None")
        self.assertFalse(division.is_unknown, f"get_best_division_for_player unexpectedly returned {division.__str__()}")

    def test_serialize_deserialize_is_reversible(self):
        # Test data in the testdata folder, which is generated directly from Slapp and copied with
        # SplatTagConsole.exe --query "e" --verbose >slapp_result.txt 2>&1
        with open("../testdata/slapp_result.txt", 'r', encoding='utf-8') as infile:
            response = infile.read()
        decoded_bytes = base64.b64decode(response)
        from slapp_py.slapp_runner.slapp_response_object import SlappResponseObject
        response_dict = json.loads(str(decoded_bytes, "utf-8"))
        response = SlappResponseObject(response_dict)
        self.maxDiff = None
        player_dict = response.matched_players[0].to_dict()
        player_dict_2 = Player.from_dict(player_dict).to_dict()
        self.assertEqual(player_dict, player_dict_2)
        team_dict = response.matched_teams[0].to_dict()
        team_dict_2 = Team.from_dict(team_dict).to_dict()
        self.assertEqual(team_dict, team_dict_2)

    def _sanity_check_class(self, instance: Any):
        dotenv.load_dotenv()
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel("DEBUG")

        attrs = inspect.getmembers(instance, lambda o: isinstance(o, Callable))
        methods = list(attrs)

        if not methods:
            logging.error(f"No methods to call.")
        else:
            logging.info(f"Calling {len(methods)=} methods")

        for name, method in methods:
            try:
                logging.info(f"Running {name=}")
                method()
            except TypeError as tex:
                message = tex.__str__()
                if ("missing" in message
                    or "takes exactly" in message
                    or "expected" in message
                    or "not enough" in message) \
                        and "argument" in message:
                    logging.info(f"Missing argument(s) in {name=}. Ignoring. {tex=}")
                else:
                    self.fail(f"TypeError raised in {name=}. {tex=}")
            except Exception as ex:
                self.fail(f"Exception raised for {type(instance)=}: {ex}")

        # By logging the attrs, we can evaluate all properties. Any that cause an exception will
        # therefore fail the test.
        try:
            print(inspect.getmembers(instance))
        except Exception as ex:
            self.fail(f"Exception raised when evaluating all attributes. Is a property bad? {type(instance)=}: {ex}")


if __name__ == '__main__':
    unittest.main()
