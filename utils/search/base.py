from .interface import Search


class SearchItem(Search):
    """
    The base representation of all search types.
    """
    def __init__(self, search_data, path, sfilter):
        self._data = sfilter(path).filter(search_data).get_filtered_data()

    def get_data(self):
        return self._data


class AdvancedSearchItem(Search):
    """
    Basic advanced view of all search types.
    """
    def __init__(self, path, filter, **kwargs):
        self._data = filter(path).filter(**kwargs).get_filtered_data()

    def get_data(self):
        return self._data