from config.conf import ConfBot
from ..search import search
from aiogram import types
from config.keys import KSearch

dp = ConfBot.DP


@dp.message_handler(text=KSearch.search)
async def search_btn_click(message: types.Message):
    await search(message)