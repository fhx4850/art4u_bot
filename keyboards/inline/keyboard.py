from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_url_post_btn(title, url):
    inline_url = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(text=title, url=url)
        ]
    ])
    return inline_url
