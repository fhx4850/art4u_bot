from aiogram.dispatcher.filters import Text
from config.conf import ConfBot
from config.text import SearchText
from utils.bot_commands import set_custom_command
from utils.search.type import SearchCategories
from aiogram import types
from config.commands import CSearch
from aiogram.dispatcher import FSMContext
from keyboards.default.keyboard import shownext_btns
from config.keys import KSearch
from utils.search.processing import Categories
from . import search
dp = ConfBot.DP


categories_names_command = Categories().get_categories_names_command()
categories_names = Categories().get_categories_names()


@dp.message_handler(text=CSearch.searchcategories)
async def show_categories_list(message: types.Message):
    """
    Shows a list of all available categories (commands).

    :param message:
    :return:
    """
    await message.answer(SearchText().get_text())
    await set_custom_command(dp, categories_names_command)


@dp.message_handler(text=KSearch.category)
async def show_categories_btn(message: types.Message):
    await show_categories_list(message)


@dp.message_handler(Text(equals=categories_names_command))
async def catch_category(message: types.Message, state: FSMContext):
    """
    Category command processing.

    :param message:
    :param state:
    :return:
    """
    await message.answer(message.text, reply_markup=shownext_btns)
    category_index = categories_names_command.index(message.text)
    category_name = categories_names[category_index]

    urls = SearchCategories(category_name).get_data()
    await state.update_data(urls=urls)
    await state.reset_state(with_data=False)
    await search.shownext(message, state)