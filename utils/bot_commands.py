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


async def pre_search_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand(CSearch.searchcategories, 'Search categories')
    ])


async def set_custom_command(dp: Dispatcher, command):
    await dp.bot.set_my_commands([types.BotCommand(i[:32:].lower(), '.') for i in command])
    # cc = [types.BotCommand(i[:31:], '/') for i in command]
    # dd = [types.BotCommand('/Fantasy', '/'), types.BotCommand('/Concept_Art', '/'),]
    # await dp.bot.set_my_commands(cc)