from aiogram import types
from config.conf import ConfBot
from handlers.search import stopsearch
from config.keys import KSearch
dp = ConfBot.DP


@dp.message_handler(text=KSearch.stopsearch)
async def stopsearch_btn_click(message: types.Message):
    await stopsearch(message)