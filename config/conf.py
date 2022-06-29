from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv
load_dotenv()


class Env:
    TOKEN = os.getenv("BOT_TOKEN")
    ADMINS = [5572275744]
    IP = os.getenv("ip")


class ConfBot:
    BOT = Bot(token=Env.TOKEN, parse_mode=types.ParseMode.HTML)
    STORAGE = RedisStorage2(
        port=6379
    )
    DP = Dispatcher(BOT, storage=STORAGE)
    RATE_LIMIT = 1

