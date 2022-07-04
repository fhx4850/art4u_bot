from abc import abstractmethod, ABCMeta


class Filter(metaclass=ABCMeta):
    @abstractmethod
    def _open_sours_file(self):
        pass

    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass