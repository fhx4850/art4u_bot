from aiogram import types
from aiogram.dispatcher import FSMContext
from config.conf import ConfBot
from aiogram.dispatcher.filters.builtin import Command
from states import SearchState
from utils.bot_commands import search_commands, pre_search_commands
from keyboards.default.keyboard import search_btns, shownext_btns
from keyboards.inline import inline_url_post_btn
from handlers.start import start_bot
from config.commands import CSearch
from config.keys import KSearch
from utils.search.type import SearchQuery
from utils.search.processing import ParsingSearchQuery, Categories
from . import categories
from . import tags

dp = ConfBot.DP


@dp.message_handler(Command(CSearch.search))
async def search(message: types.Message):
    """
    Processing the search start command.

    :param message:
    :return:
    """
    await pre_search_commands(dp)
    await message.answer('Search...', reply_markup=search_btns)
    await SearchState.s_text.set()
    await message.delete()


@dp.message_handler(state=SearchState.s_text)
async def search_input(message: types.Message, state: FSMContext):
    """
    The handler expects a message with text to search from the user.

    :param message:
    :param state:
    :return:
    """
    await search_commands(dp)
    if await __check_stop_search_input(message, state):
        return
    search_text = message.text
    await message.answer(f'Search ➡️ {search_text}', reply_markup=shownext_btns)

    await state.reset_data()

    search_data = ParsingSearchQuery(search_text).get_search_data()
    urls = SearchQuery(search_data).get_data()
    await state.update_data(urls=urls)
    await state.reset_state(with_data=False)
    await shownext(message, state)


async def __check_stop_search_input(message: types.Message, state):
    """
    Checking if the search should be stopped.

    :param message:
    :param state:
    :return:
    """
    isstop = False
    if message.text == KSearch.category or message.text == '/' + CSearch.searchcategories:
        await state.reset_state()
        await categories.show_categories_list(message)
        isstop = True

    if message.text == KSearch.stopsearch or message.text == '/' + CSearch.stopsearch:
        await state.reset_state()
        await stopsearch(message)
        isstop = True

    if message.text == KSearch.tags or message.text == '/' + CSearch.tags:
        await tags.search_tags(message)
        isstop = True

    return isstop


@dp.message_handler(text=KSearch.stopsearch)
async def stopsearch_btn_click(message: types.Message):
    await stopsearch(message)


@dp.message_handler(text=KSearch.search)
async def search_btn_click(message: types.Message):
    await search(message)


@dp.message_handler(Command(CSearch.stopsearch))
async def stopsearch(message: types.Message):
    await start_bot(message)


@dp.message_handler(Command(CSearch.shownext))
async def shownext(message: types.Message, state: FSMContext):
    """
    Sends messages with the following posts.

    :param message:
    :param state:
    :return:
    """
    await search_commands(dp)
    async with state.proxy() as data:
        urls = data.get('urls', None)
    if not urls:
        await message.answer('No search query!')
        return
    current_url = list()
    for x, url in enumerate(urls):
        if x == 5:
            await __remove_send_url(current_url, urls, state)
            return
        else:
            try:
                await message.bot.send_photo(message.chat.id, url[0], reply_markup=inline_url_post_btn(url[2], url[1]))
            except Exception as ex:
                print(ex)
            current_url.append(url)
    await __remove_send_url(current_url, urls, state)


async def __remove_send_url(current_url, urls, state):
    for i in current_url:
        urls.remove(i)
    await state.update_data(urls=urls)


@dp.message_handler(text=KSearch.show5)
async def shownext_btn(message: types.Message, state: FSMContext):
    await message.delete()
    await shownext(message, state)
