from aiogram.dispatcher.filters import CommandStart
from aiogram import types
from config.conf import ConfBot
from utils.bot_commands import set_default_commands
from keyboards.default.keyboard import base_btns
dp = ConfBot.DP


@dp.message_handler(CommandStart())
async def start_bot(message: types.Message):
    await message.answer(f'👋 {message.from_user.full_name}', reply_markup=base_btns)
    await set_default_commands(dp)
