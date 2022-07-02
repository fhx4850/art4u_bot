from aiogram import types
from aiogram import Dispatcher
from config.commands import CSearch


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Bot start'),
        types.BotCommand(CSearch.search, 'Search posts')
    ])

async def search_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand(CSearch.stopsearch, 'Stop search')
    ])
