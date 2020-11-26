from aiogram import Bot

from datetime import timedelta

import asyncio
import random


BOT_TOKEN = ""
CHANNEL_ID = ""
bot = Bot(BOT_TOKEN)


async def post_message(message):
    await bot.send_message(CHANNEL_ID, message)


async def post():
    message = "Hello, World! Now="

    from datetime import datetime

    now = datetime.now()

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    message = message + dt_string
    # print(message)
    await post_message(message)


async def run_periodically(wait_time_bounds, func, *args, **kwargs):
    while True:
        await func(*args, **kwargs)
        wait_time = random.random() * (wait_time_bounds[1] - wait_time_bounds[0]) + wait_time_bounds[0]
        await asyncio.sleep(wait_time)


if __name__ == "__main__":
    wait_time_bounds = (timedelta(hours=4).seconds, timedelta(hours=5).seconds)
    asyncio.get_event_loop().run_until_complete(run_periodically(wait_time_bounds, post))
