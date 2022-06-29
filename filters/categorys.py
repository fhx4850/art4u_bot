from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


class CheckCategory(BoundFilter):
    async def check(self, message: types.Message):
        print('ddd')
        return message.text == ':test'