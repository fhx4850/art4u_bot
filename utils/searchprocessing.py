import json
import pandas as pd
from config.conf import Env


class SearchProcessing:
    def __init__(self, search_text):
        self._search_text = str(search_text)
        self._last_index = 0
        self._categories = None
        self._tags = None
        self._body = None

    def _parse_query(self):
        query_format = self._search_text.replace(' ', '')
        if self._search_text.startswith('!'):
            self.__execute_categories(query_format)
            self.__execute_tags(query_format)
            self.__execute_body(query_format)
        else:
            self.__execute_body(query_format)

    def __execute_categories(self, query_format):
        if query_format.find('categories:') != -1:
            categories_text = ''
            categories_start_index = query_format.find('categories:').as_integer_ratio()[0]
            for x, i in enumerate(query_format):
                if x >= categories_start_index:
                    if i == ';':
                        self._last_index = x+1
                        break
                    else:
                        categories_text += i
            c = categories_text.split(':')
            categories = c[1].split(',')
            self._categories = categories
            print(categories)

    def __execute_tags(self, query_format):
        tags_text = ''
        if query_format.find('tags:') != -1:
            tags_start_index = query_format.find('tags:').as_integer_ratio()[0]
            for x, i in enumerate(query_format):
                if x > tags_start_index:
                    if i == ';':
                        self._last_index = x+1
                        break
                    else:
                        tags_text += i
            t = tags_text.split(':')
            tags = t[1].split(',')
            self._tags = tags
            print(tags)

    def __execute_body(self, query_format):
        body = query_format[self._last_index::]
        self._body = body

    def get_search_data(self):
        self._parse_query()
        return {'categories': self._categories, 'tags': self._tags, 'body': self._body}


class SearchPost:
    def __init__(self, search_data: dict):
        self._ps = _PostData(Env.POSTS_PATH).get_data(title=search_data['body'])

    def get_post(self):
        return self._ps


class _PostData:
    def __init__(self, path_to_file):
        self._path_to_file = path_to_file
        self._df_posts_data = self._open_sours_file()

    def _open_sours_file(self):
        posts = None
        with open(self._path_to_file) as f:
            posts = json.load(f)
            df = pd.DataFrame(posts)
        return df

    def get_data(self, **kwargs):
        df = self._df_posts_data
        kk = list(kwargs.keys())[0]
        kv = list(kwargs.values())[0]
        df_filter = df[df[kk].str.contains(kv, case=False)]['cover_url'].values.tolist()
        return df_filter
