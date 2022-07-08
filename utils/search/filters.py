from .interface import Filter
from config.conf import Env
import json
import pandas as pd
from . import type as t


class SearchQueryFilter(Filter):
    def __init__(self, path_to_file):
        self._path_to_file = path_to_file
        self._tags_data = self._open_sours_file()
        self._post_data_filter = PostDataFilter(Env.POSTS_PATH)
        self._filtered_data = None

    def _open_sours_file(self):
        with open(self._path_to_file) as f:
            return json.load(f)

    def filter(self, search_data):
        if search_data['tags']:
            t_search = t.SearchTags(search_data['tags']).get_data()
            tags_titles = [i[2] for i in t_search]
            posts = t.SearchPost(title=search_data['body']).get_data()
            urls = []
            for post in posts:
                if post[2] in tags_titles:
                    urls.append(post)
            self._filtered_data = urls
            return self
        else:
            self._filtered_data = t.SearchPost(title=search_data['body']).get_data()
            return self

    def get_filtered_data(self):
        return self._filtered_data


class TagsFilter(Filter):
    def __init__(self, path_to_file):
        self._path_to_file = path_to_file
        self._tags_data = self._open_sours_file()
        self._post_data_filter = PostDataFilter(Env.POSTS_PATH)
        self._filtered_data = None

    def _open_sours_file(self):
        with open(self._path_to_file) as f:
            return json.load(f)

    def filter(self, search_data):
        for i in search_data:
            t = i.split(',')
        tags = [i.strip(' ') for i in t]
        tags_pd_series = pd.Series(list(self._tags_data.keys()))
        filter_tags = []
        for i in tags:
             filter_tags.append(tags_pd_series[tags_pd_series.str.contains(i, case=False)].tolist())
        hid = []
        for i in filter_tags[0]:
            hid += [i for i in self._tags_data[i]]
        urls = []
        for h in hid:
            urls.append(self._post_data_filter.filter(hash_id=h).get_filtered_data()[0])
        self._filtered_data = urls
        return self

    def get_filtered_data(self):
        return self._filtered_data


class CategoriesFilter(Filter):
    def __init__(self, path_to_file):
        self._path_to_file = path_to_file
        self._categories_data = self._open_sours_file()
        self._post_data_filter = PostDataFilter(Env.POSTS_PATH)
        self._filtered_data = None

    def _open_sours_file(self):
        with open(self._path_to_file) as f:
            return json.load(f)

    def filter(self, search_data):
        cd = self._categories_data
        hash_ids = cd[search_data]

        urls = []

        for hid in hash_ids:
            urls.append(self._post_data_filter.filter(hash_id=hid).get_filtered_data()[0])
        self._filtered_data = urls
        return self

    def get_filtered_data(self):
        return self._filtered_data


class PostDataFilter(Filter):
    def __init__(self, path_to_file):
        self._path_to_file = path_to_file
        self._df_posts_data = self._open_sours_file()
        self._filtered_data = None

    def _open_sours_file(self):
        with open(self._path_to_file) as f:
            posts = json.load(f)
            df = pd.DataFrame(posts)
        return df

    def filter(self, **kwargs):
        df = self._df_posts_data
        kk = list(kwargs.keys())[0]
        kv = list(kwargs.values())[0]
        df_filter = df[df[kk].str.contains(kv, case=False)][['cover_url', 'permalink', 'title']].values.tolist()
        self._filtered_data = df_filter
        return self

    def get_filtered_data(self):
        return self._filtered_data
