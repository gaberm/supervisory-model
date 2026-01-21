from abc import ABC, abstractmethod

class TableSchema(ABC):
    def __init__(self, table_name: str):
        self.table_name = table_name

    @abstractmethod
    def create_table_query(self) -> str:
        pass