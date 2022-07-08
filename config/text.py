# This file contains texts for output.

from utils.search.processing import Categories


class SearchText:
    def __init__(self):
        self._categories_init = Categories()
        self.categories_name = self._categories_init.get_categories_names()

    def __set_categories_name_list(self):
        text = ''
        for i in self._categories_init.get_categories_names_command():
            text += i + '\n'
        return text

    def get_text(self):
        return self.__set_categories_name_list()