import json
from config.conf import Env


class ParsingSearchQuery:
    def __init__(self, search_text):
        self._search_text = str(search_text)
        self._last_index = 0
        self._categories = None
        self._tags = None
        self._body = None

    def _parse_query(self):
        """
        Processing a request with a definition of its type.
        :return:
        """
        query_format = self._search_text.replace(' ', '')
        if self._search_text.startswith('#-'):
            self.__execute_tags(query_format)
            self.__execute_body(query_format)
        elif self._search_text.startswith('@-'):
            self.__execute_categories(query_format)
            self.__execute_body(query_format)
        else:
            self.__execute_body(query_format)

    def __execute_categories(self, query_format):
        """

        :param query_format:
        :return:
        """
        if query_format.find('@-') != -1:
            categories_text = ''
            categories_start_index = query_format.find('@-').as_integer_ratio()[0]
            for x, i in enumerate(query_format):
                if x >= categories_start_index:
                    if i == '/':
                        self._last_index = x+1
                        break
                    else:
                        categories_text += i
            c = categories_text.split('-')
            categories = c[1].split(',')
            self._categories = categories

    def __execute_tags(self, query_format):
        tags_text = ''
        if query_format.find('#-') != -1:
            tags_start_index = query_format.find('#-').as_integer_ratio()[0]
            for x, i in enumerate(query_format):
                if x > tags_start_index:
                    if i == '/':
                        self._last_index = x+1
                        break
                    else:
                        tags_text += i
            t = tags_text.split('-')
            tags = t[1].split(',')
            self._tags = tags

    def __execute_body(self, query_format):
        body = query_format[self._last_index::]
        self._body = body

    def get_search_data(self):
        self._parse_query()
        return {'categories': self._categories, 'tags': self._tags, 'body': self._body}


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