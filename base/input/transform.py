from abc import ABC, abstractmethod


class Transform(ABC):
    @abstractmethod
    def __call__(self, rows: list[dict]) -> list[dict]: ...
