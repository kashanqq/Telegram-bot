import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv
from handlers import start_handler, meme_handler, roullete_handler, chat_handler

BOT = Bot(os.getenv("TOKEN_BOT"))
dp = Dispatcher()



async def main():
    dp.include_router(start_handler.router)
    dp.include_router(roullete_handler.router)
    dp.include_router(chat_handler.router)
    dp.include_router(meme_handler.router)
    await dp.start_polling(BOT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")