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
# from utils.searchprocessing import SearchProcessing

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
    await state.update_data(search_text=search_text)
    # SearchProcessing(search_text)
    await state.reset_state(with_data=False)
    await shownext(message, state)


@dp.message_handler(Command(CSearch.stopsearch))
async def stopsearch(message: types.Message):
    await start_bot(message)


@dp.message_handler(Command(CSearch.shownext))
async def shownext(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        search_text = data.get('search_text', None)
    if not search_text:
        await message.answer('No search query!')
        return


@dp.message_handler(text=KSearch.show5)
async def shownext_btn(message: types.Message, state: FSMContext):
    await message.delete()
    await shownext(message, state)