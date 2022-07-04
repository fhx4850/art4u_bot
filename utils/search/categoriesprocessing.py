from config.conf import Env
import json


class Categories:
    def __init__(self):
        self._categories_load = self.__load_categories()
        self._replace = {'&': '_', ' ': '_', "'": '', '-': '_', ',': '_', '(': '', ')': ''}

    def __load_categories(self):
        with open(Env.CATEGORIES_PATH, 'r') as f:
            return json.load(f)

    def get_categories_names(self, format=False):
        if format:
            return self._format()
        else:
            return [i for i in self._categories_load.keys()]

    def get_categories_names_command(self):
        return ['/' + i.lower() for i in self._format()]

    def _format(self):
        format_list = []
        for i in self._categories_load:
            rep_i = i
            for key, value in self._replace.items():
                rep_i = rep_i.replace(key, value)
            format_list.append(rep_i)
        return format_list