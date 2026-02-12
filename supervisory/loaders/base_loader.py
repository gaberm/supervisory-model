from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
import psycopg2 as psycopg

T = TypeVar("T")


class BaseLoader(ABC, Generic[T]):
    """Base class for loading domain objects from database."""

    @abstractmethod
    def _extract(*args, **kwargs) -> list[tuple[Any, ...]]:
        """Extract raw data from database."""
        pass

    @abstractmethod
    def _transform(
        rows: list[tuple[Any, ...]], *args, **kwargs
    ) -> list[tuple[Any, ...]]:
        """Optional transformation step. Override if needed."""
        return rows

    @abstractmethod
    def _build(rows: list[tuple[Any, ...]]) -> list[T]:
        """Build domain objects from rows."""
        pass

    @classmethod
    def load_input(cls, *args, **kwargs) -> list[T]:
        """Main entry point: extract, transform, build."""
        rows = cls._extract(*args, **kwargs)
        rows = cls._transform(rows, *args, **kwargs)
        return cls._build(rows)


class BaseInputLoader(ABC):
    """Base class for aggregating multiple loaders into input objects."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_input(self, **kwargs):
        """Load and aggregate all inputs."""
        pass
