from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
import psycopg2 as psycopg

T = TypeVar("T")


class BaseLoader(ABC, Generic[T]):
    """Base class for loading domain objects from database."""

    @abstractmethod
    def _extract(**kwargs) -> list[tuple[Any, ...]]:
        """Extract raw data from database."""
        pass

    @abstractmethod
    def _transform(rows: list[tuple[Any, ...]]) -> list[tuple[Any, ...]]:
        """Optional transformation step. Override if needed."""
        return rows

    @abstractmethod
    def _build(rows: list[tuple[Any, ...]]) -> list[T]:
        """Build domain objects from rows."""
        pass

    @abstractmethod
    def load_input(**kwargs) -> list[T]:
        """Main entry point: ex tract, transform, build."""
        rows = BaseLoader._extract(**kwargs)
        rows = BaseLoader._transform(rows, **kwargs)
        return BaseLoader._build(rows)


class BaseInputLoader(ABC):
    """Base class for aggregating multiple loaders into input objects."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_input(self, **kwargs):
        """Load and aggregate all inputs."""
        pass
