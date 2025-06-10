from abc import ABC, abstractmethod

class Table(ABC):

    @abstractmethod
    def create(self, *values): ...

    @abstractmethod
    def read(self, qtd=15, filter=None): ...

    @abstractmethod
    def read_one(self, id): ...

    @abstractmethod
    def update(self, *values): ...

    @abstractmethod
    def delete(self, *values): ...

    @abstractmethod
    def close(self): ...
