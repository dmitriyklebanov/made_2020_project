from evaluator.evaluate_model import create_evaluator, predict

from aiogram import Bot

from datetime import timedelta

import asyncio
import os
import random


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
bot = Bot(BOT_TOKEN)


async def post_message(message):
    await bot.send_message(CHANNEL_ID, message)


evaluator = None
default_prompt = "олег"


async def post():
    '''
    message = "Hello, World! Now="

    from datetime import datetime

    now = datetime.now()

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    message = message + dt_string
    # print(message)
    '''
    global evaluator
    global prompt

    if evaluator is None:
        evaluator = create_evaluator()

    generate = True
    while generate:
        message = predict(evaluator, default_prompt)
        prompt = message.split('\n')[-1]
        message = predict(evaluator, prompt)
        message = message[:message.rfind('\n')]
        generate = message.count('\n') < 2

    await post_message(message)


async def run_periodically(wait_time_bounds, func, *args, **kwargs):
    while True:
        await func(*args, **kwargs)
        wait_time = random.random() * (wait_time_bounds[1] - wait_time_bounds[0]) + wait_time_bounds[0]
        await asyncio.sleep(wait_time)


if __name__ == "__main__":
    wait_time_bounds = (int(os.environ["MIN_TIME"]), int(os.environ["MAX_TIME"]))
    asyncio.get_event_loop().run_until_complete(run_periodically(wait_time_bounds, post))
