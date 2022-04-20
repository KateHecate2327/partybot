# coding: utf-8

import asyncio
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

# Читаем конфигурацию
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")


async def echo(event: types.Message):
    print(event)
    await event.answer(
        event.text,
        parse_mode=types.ParseMode.HTML,
    )


async def main():
    tg_bot = Bot(token=BOT_TOKEN)
    me = await tg_bot.get_me()
    print(f"🤖 Hello, I'm {me.first_name}.\nHave a nice Day!")

    try:
        disp = Dispatcher(bot=tg_bot)
        disp.register_message_handler(echo)
        await disp.start_polling()
    finally:
        await tg_bot.close()


asyncio.run(main())
