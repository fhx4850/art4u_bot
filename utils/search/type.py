from .base import SearchItem, AdvancedSearchItem
from config.conf import Env
from . import filters as f


class SearchQuery(SearchItem):
    """
    Search by regular or advanced query.
    """
    def __init__(self, search_data):
        super().__init__(search_data, Env.TAGS_PATH, f.SearchQueryFilter)


class SearchTags(SearchItem):
    def __init__(self, search_data):
        super().__init__(search_data, Env.TAGS_PATH, f.TagsFilter)


class SearchCategories(SearchItem):
    def __init__(self, search_data):
        super().__init__(search_data, Env.CATEGORIES_PATH, f.CategoriesFilter)


class SearchPost(AdvancedSearchItem):
    def __init__(self, **kwargs):
        super().__init__(Env.POSTS_PATH, f.PostDataFilter, **kwargs)
