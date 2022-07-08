from aiogram import types
from aiogram.dispatcher import FSMContext
from config.conf import ConfBot
from aiogram.dispatcher.filters.builtin import Command
from states import SearchState
from keyboards.default.keyboard import shownext_btns
from config.commands import CSearch
from config.keys import KSearch
from utils.search.type import SearchTags
from . import search
dp = ConfBot.DP


@dp.message_handler(text=KSearch.tags)
async def search_tags_btn(message: types.Message):
    await search_tags(message)


@dp.message_handler(Command(CSearch.tags))
async def search_tags(message: types.Message):
    await SearchState.s_tags.set()
    await message.answer('Search posts by tags...')


@dp.message_handler(state=SearchState.s_tags)
async def tags_input(message: types.Message, state: FSMContext):
    """
    Waiting for the tag name to be entered to search.

    :param message:
    :param state:
    :return:
    """
    if await search.__check_stop_search_input(message, state):
        return
    await state.reset_data()

    await message.answer(f'Search tags ➡ {message.text}', reply_markup=shownext_btns)
    urls = SearchTags([message.text]).get_data()
    await state.update_data(urls=urls)
    await state.reset_state(with_data=False)
    await search.shownext(message, state)