from abc import ABC, abstractmethod
from typing import Dict
from .table_schema import TableSchema


class ModelSchema(ABC):
    @abstractmethod
    def tables(self) -> Dict[str, TableSchema]:
        """
        Return all tables owned by this model,
        keyed by logical table name.
        """
        pass
