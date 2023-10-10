import logging
import os

import anyio
from dotenv import load_dotenv
from nintendo.nex.ranking import RankingClient

from mk8boards.mk8.boards_client import MK8Client
from mk8boards.mk8.timesheet import get_timesheet

logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# --- Device Information ---
DEVICE_ID = int(os.getenv("DEVICE_ID"), base=16)
SERIAL_NUMBER = os.getenv("SERIAL_NUMBER")
SYSTEM_VERSION = int(os.getenv("SYSTEM_VERSION"), base=16)
# --- Region and Language Information ---
COUNTRY_ID = int(os.getenv("COUNTRY_ID"))
COUNTRY_NAME = os.getenv("COUNTRY_NAME")
REGION_ID = int(os.getenv("REGION_ID"))
REGION_NAME = os.getenv("REGION_NAME")
LANGUAGE = os.getenv("LANGUAGE")
# --- Account Information ---
USERNAME = os.getenv("NNID_USERNAME")
PASSWORD = os.getenv("PASSWORD")

# To get a player's timesheet, we need their Nintendo Network ID
PLAYER_NNID = "dorasa15"
# ----------------------------------


async def main():
    client = MK8Client()
    client.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION)
    client.set_locale(REGION_ID, REGION_NAME, COUNTRY_ID, COUNTRY_NAME, LANGUAGE)

    await client.login(USERNAME, PASSWORD)
    async with client.backend_login() as bc:
        rc = RankingClient(bc)
        for time in (await get_timesheet(rc, PLAYER_NNID)).to_string_array():
            print(time)


if __name__ == "__main__":
    anyio.run(main)
    # input("Press Enter to exit...")
