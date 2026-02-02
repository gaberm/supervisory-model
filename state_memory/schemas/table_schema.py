from abc import ABC, abstractmethod


class TableSchema(ABC):
    """
    Abstract base class describing a single database table
    owned by a model.
    """

    @abstractmethod
    def name(self) -> str:
        """Return the table name."""
        pass

    @abstractmethod
    def create_sql(self) -> str:
        """Return the SQL statement to create the table."""
        pass

    @abstractmethod
    def insert_sql(self) -> str:
        """
        Return a parametrized INSERT statement and parameters.

        This method encodes table-specific insertion semantics.
        """
        pass
