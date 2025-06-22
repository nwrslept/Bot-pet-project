import asyncio
import logging
import os
from dotenv import load_dotenv
from database.models import create_tables
from scheduler import schedule_jobs
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

#ініціалізація роутерів
from handlers import start, news, gemini, ideas_generator, user_profile, subscription, language
dp.include_routers(
    start.router,
    news.router,
    gemini.router,
    ideas_generator.router,
    user_profile.router,
    subscription.router,
    language.router
)


async def main():
    create_tables() #створення таблиць
    schedule_jobs(bot) #запуск розсилки
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
