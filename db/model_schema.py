from abc import ABC, abstractmethod
from typing import Dict, Iterable


class ModelSchema(ABC):
    """
    Abstract base class describing the complete database
    schema owned by a model.
    """

    @abstractmethod
    def model_name(self) -> str:
        """Human-readable model identifier (e.g. 'transport')."""
        pass

    @abstractmethod
    def tables(self) -> Dict[str, "TableSchema"]:
        """
        Return all tables owned by this model,
        keyed by logical table name.
        """
        pass

    def get_table(self, name: str) -> "TableSchema":
        """Convenience lookup with validation."""
        tables = self.tables()
        if name not in tables:
            raise KeyError(f"Model '{self.model_name()}' has no table '{name}'")
        return tables[name]
