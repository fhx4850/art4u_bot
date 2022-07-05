from aiogram.dispatcher.filters.state import StatesGroup, State


class SearchState(StatesGroup):
    s_text = State()
    s_tags = State()


class TagsState(StatesGroup):
    s_tags = State()