from aiogram.dispatcher.filters.state import StatesGroup, State


class SearchState(StatesGroup):
    s_text = State()