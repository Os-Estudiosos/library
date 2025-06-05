from abc import ABC, abstractmethod

class Table(ABC):

    @abstractmethod
    def create(self, *values): ...

    @abstractmethod
    def read(self, filter=None): ...

    @abstractmethod
    def update(self, *values): ...

    @abstractmethod
    def delete(self, *values): ...
