from aiogram import Dispatcher
from .bot_commands import set_default_commands
import middlewares


async def startup_msg(dp: Dispatcher):
    await set_default_commands(dp)
    middlewares.setup(dp)