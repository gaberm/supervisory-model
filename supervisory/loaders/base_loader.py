from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
import psycopg2 as psycopg

T = TypeVar("T")


class BaseLoader(ABC, Generic[T]):
    """Base class for loading domain objects from database."""

    @abstractmethod
    def _extract(self, **kwargs) -> list[tuple[Any, ...]]:
        """Extract raw data from database."""
        pass

    def _transform(self, rows: list[tuple[Any, ...]]) -> list[tuple[Any, ...]]:
        """Optional transformation step. Override if needed."""
        return rows

    @abstractmethod
    def _build(self, rows: list[tuple[Any, ...]]) -> list[T]:
        """Build domain objects from rows."""
        pass

    def load_input(self, **kwargs) -> list[T]:
        """Main entry point: extract, transform, build."""
        rows = self._extract(**kwargs)
        rows = self._transform(rows)
        return self._build(rows)


class BaseInputLoader(ABC):
    """Base class for aggregating multiple loaders into input objects."""

    def __init__(self, conn: psycopg.extensions.connection):
        self.conn = conn

    @abstractmethod
    def load_input(self, **kwargs):
        """Load and aggregate all inputs."""
        pass
