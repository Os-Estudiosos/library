from abc import ABC, abstractmethod


class Screen(ABC):
    @abstractmethod
    def build(*args, **kwargs):...
