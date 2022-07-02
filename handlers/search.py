from aiogram import types
from aiogram.dispatcher import FSMContext
from config.conf import ConfBot
from aiogram.dispatcher.filters.builtin import Command
from states import SearchState
from utils.bot_commands import search_commands, set_default_commands
from keyboards.keyboard import search_btns, shownext_btns
from handlers.start import start_bot
from config.commands import CSearch
from config.keys import KSearch
from utils.searchprocessing import SearchProcessing, SearchPost

dp = ConfBot.DP


@dp.message_handler(Command(CSearch.search))
async def search(message: types.Message):
    await message.answer('Search...', reply_markup=search_btns)
    await search_commands(dp)
    await SearchState.s_text.set()
    await message.delete()


@dp.message_handler(state=SearchState.s_text)
async def test(message: types.Message, state: FSMContext):
    search_text = message.text
    await message.answer(f'Search ➡️ {search_text}', reply_markup=shownext_btns)

    search_data = SearchProcessing(search_text).get_search_data()
    urls = SearchPost(search_data).get_post()
    # await message.answer(urls)
    await state.update_data(urls=urls)
    # await message.bot.send_photo(message.chat.id, url)
    await state.reset_state(with_data=False)
    await shownext(message, state)


@dp.message_handler(Command(CSearch.stopsearch))
async def stopsearch(message: types.Message):
    await start_bot(message)


@dp.message_handler(Command(CSearch.shownext))
async def shownext(message: types.Message, state: FSMContext):
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
            if url != 'nan':
                await message.bot.send_photo(message.chat.id, url)
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