from evaluator.evaluate_model import create_evaluator, predict

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from datetime import timedelta

import asyncio
import os
import random


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = None
bot = Bot(BOT_TOKEN)


async def post_message(message):
    await bot.send_message(CHANNEL_ID, message)


evaluator = None
DEFAULT_PROMPT = "олег"


async def post():
    generate = True
    while generate:
        message = predict(evaluator, DEFAULT_PROMPT)
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


dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    HELLO_MESSAGE = "Привет!\nЯ умею генерировать нейро пирожки. Хочешь один?\nОтправь мне начало пирожка и я сгенерирую тебе его продолжение"
    await message.reply(HELLO_MESSAGE)


@dp.message_handler()
async def echo(message: types.Message):
    generate = True
    while generate:
        reply_message = predict(evaluator, message.text)
        generate = not reply_message.startswith(message.text)
    await message.reply(reply_message)


if __name__ == "__main__":
    evaluator = create_evaluator()

    loop = asyncio.get_event_loop()
    if os.environ["POST_TO_CHANNEL"] == "True":
        CHANNEL_ID = os.environ["CHANNEL_ID"]
        wait_time_bounds = (int(os.environ["MIN_TIME"]), int(os.environ["MAX_TIME"]))
        loop.create_task(run_periodically(wait_time_bounds, post))

    executor.start_polling(dp, skip_updates=True, loop=loop)
