from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.keys import KSearch

base_btns = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=KSearch.search)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

search_btns = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=KSearch.tags),
        KeyboardButton(text=KSearch.category)
    ],
    [
        KeyboardButton(text=KSearch.stopsearch)
    ]
],
    resize_keyboard=True,
    one_time_keyboard=False
)

shownext_btns = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=KSearch.stopsearch),
        KeyboardButton(text=KSearch.show5)

    ],
    [
        KeyboardButton(text=KSearch.search)
    ]
],
    resize_keyboard=True,
    one_time_keyboard=False
)