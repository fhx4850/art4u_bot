from aiogram.dispatcher.filters import CommandStart
from aiogram import types
from config.conf import ConfBot
from utils.bot_commands import set_default_commands
from keyboards.keyboard import base_btns
dp = ConfBot.DP


@dp.message_handler(CommandStart())
async def start_bot(message: types.Message):
    await message.answer(f'👋 {message.from_user.full_name}', reply_markup=base_btns)
    await set_default_commands(dp)
    # await message.bot.send_photo(message.chat.id, 'https://cdnb.artstation.com/p/assets/images/images/051/009/795/20220628040829/smaller_square/antoine-verney-carron-f03.jpg?1656407310')
