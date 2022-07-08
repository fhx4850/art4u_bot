from aiogram import executor
from handlers import dp
from utils import startup_msg


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=startup_msg)