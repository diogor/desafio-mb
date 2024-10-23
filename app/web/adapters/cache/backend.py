from abc import ABCMeta, abstractmethod


class BaseBackend(metaclass=ABCMeta):
    def __init__(self):
        self.cache = {}

    @abstractmethod
    def create(self, resp, key: str, ex: int = 60):
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, key: str):
        raise NotImplementedError

    @abstractmethod
    def invalidate(self, key: str):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError
