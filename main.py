from aiogram import executor
from handlers import dp
from utils import startup_msg
# from utils.set_bot_commands import set_default_commands


# async def on_startup(dp):
#     # import filters
#     # import middlewares
#     # filters.setup(dp)
#     # middlewares.setup(dp)
#
#     # from utils.notify_admins import on_startup_notify
#     # await on_startup_notify(dp)
#     await set_default_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=startup_msg)