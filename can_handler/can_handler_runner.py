from kelly_handler import LeftKellyHandler, RightKellyHandler
from bms_handler import BMSHandler
import asyncio

# Getting the instance of all the converters
leftKelly = LeftKellyHandler()
rightKelly = RightKellyHandler()
bms = BMSHandler()

# Function to run all the can converters concurrences on paralel
async def main():
    await asyncio.gather(leftKelly.run_daemon(), rightKelly.run_daemon(), bms.run_daemon())

# Final run instruction
asyncio.run(main())
