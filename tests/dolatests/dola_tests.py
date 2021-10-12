import asyncio
import base64
import json
import logging
import os
import timeit
import unittest
from time import time

import dotenv

from slapp_py.slapp_runner.slapipes import initialise_slapp


class DolaSlappTests(unittest.IsolatedAsyncioTestCase):

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
                await asyncio.wait_for(initialise_slapp(self.receive_slapp_response, mode=''), timeout=60.0)
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
                # Test data in the testdata folder, which is generated directly from Slapp and copied with
                # SplatTagConsole.exe --query "e" --verbose >slapp_result.txt 2>&1
                with open("../testdata/slapp_result.txt", 'r', encoding='utf-8') as infile:
                    response = infile.read()
                decoded_bytes = base64.b64decode(response)
                response = json.loads(str(decoded_bytes, "utf-8"))

                # Establish a connection
                await SlappCommands.receive_slapp_response("Nothing", {})

                # Push this request into queue
                slapp_ctx_queue.append((None, "slapp"))

                # And get a response from Slapp
                start_time = time()
                await asyncio.wait_for(SlappCommands.receive_slapp_response("OK", response), timeout=600.0)
                print(f'Time taken to process response: {time() - start_time:0.3f}s')
            except asyncio.TimeoutError:
                self.fail(f"Timed out waiting for Dola to build the message from the Slapp response.")
        except Exception as ex:
            self.fail(f"Not expecting an exception: {ex}")


if __name__ == '__main__':
    unittest.main()
