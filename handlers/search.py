from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from config.conf import ConfBot
from aiogram.dispatcher.filters.builtin import Command
from states import SearchState, TagsState
from utils.bot_commands import search_commands, pre_search_commands, set_custom_command
from keyboards.keyboard import search_btns, shownext_btns
from keyboards.inline import inline_url_post_btn
from handlers.start import start_bot
from config.commands import CSearch
from config.keys import KSearch
from utils.search.searchprocessing import ParsingSearchQuery, SearchPost, SearchCategories, SearchTags
from config.text import SearchText
from utils.search.categoriesprocessing import Categories

dp = ConfBot.DP


@dp.message_handler(Command(CSearch.search))
async def search(message: types.Message):
    await pre_search_commands(dp)
    await message.answer('Search...', reply_markup=search_btns)
    await SearchState.s_text.set()
    await message.delete()


@dp.message_handler(state=SearchState.s_text)
async def search_input(message: types.Message, state: FSMContext):
    await search_commands(dp)
    if await __check_stop_search_input(message, state):
        return
    search_text = message.text
    await message.answer(f'Search ➡️ {search_text}', reply_markup=shownext_btns)

    await state.reset_data()

    search_data = ParsingSearchQuery(search_text).get_search_data()
    urls = SearchPost(search_data).get_post()
    await state.update_data(urls=urls)
    await state.reset_state(with_data=False)
    await shownext(message, state)


async def __check_stop_search_input(message: types.Message, state):
    isstop = False
    if message.text == KSearch.category or message.text == '/' + CSearch.searchcategories:
        await state.reset_state()
        await show_categories_list(message)
        isstop = True

    if message.text == KSearch.stopsearch or message.text == '/' + CSearch.stopsearch:
        await state.reset_state()
        await stopsearch(message)
        isstop = True

    if message.text == KSearch.tags or message.text == '/' + CSearch.tags:
        await search_tags(message)
        isstop = True

    return isstop


@dp.message_handler(Command(CSearch.stopsearch))
async def stopsearch(message: types.Message):
    await start_bot(message)


@dp.message_handler(Command(CSearch.shownext))
async def shownext(message: types.Message, state: FSMContext):
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

categories_names_command = Categories().get_categories_names_command()
categories_names = Categories().get_categories_names()


@dp.message_handler(text=CSearch.searchcategories)
async def show_categories_list(message: types.Message):
    await message.answer(SearchText().get_text())
    await set_custom_command(dp, categories_names_command)


@dp.message_handler(text=KSearch.category)
async def show_categories_btn(message: types.Message):
    await show_categories_list(message)


@dp.message_handler(Text(equals=categories_names_command))
async def catch_category(message: types.Message, state: FSMContext):
    await message.answer(message.text, reply_markup=shownext_btns)
    category_index = categories_names_command.index(message.text)
    category_name = categories_names[category_index]

    urls = SearchCategories(category_name).get_data()
    await state.update_data(urls=urls)
    await state.reset_state(with_data=False)
    await shownext(message, state)


@dp.message_handler(text=KSearch.tags)
async def search_tags_btn(message: types.Message):
    await search_tags(message)


@dp.message_handler(Command(CSearch.tags))
async def search_tags(message: types.Message):
    await SearchState.s_tags.set()
    await message.answer('Search posts by tags...')


@dp.message_handler(state=SearchState.s_tags)
async def tags_input(message: types.Message, state: FSMContext):
    if await __check_stop_search_input(message, state):
        return
    await state.reset_data()

    await message.answer(f'Search tags ➡ {message.text}', reply_markup=shownext_btns)
    urls = SearchTags(message.text).get_data()
    await state.update_data(urls=urls)
    await state.reset_state(with_data=False)
    await shownext(message, state)