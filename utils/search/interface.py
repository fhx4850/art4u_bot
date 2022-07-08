from abc import abstractmethod, ABCMeta


class Filter(metaclass=ABCMeta):
    @abstractmethod
    def _open_sours_file(self):
        pass

    @abstractmethod
    def get_filtered_data(self):
        pass

    @abstractmethod
    def filter(self, search_data):
        pass


class Search(metaclass=ABCMeta):
    @abstractmethod
    def get_data(self):
        pass