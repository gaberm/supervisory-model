from __future__ import annotations
import dataclasses
from typing import Type
from records.base_record import BaseRecord


class ModelOutput:
    def __init__(self):
        self._batches: dict[Type, list] = {}

    def add(self, record) -> ModelOutput:
        record_cls = type(record)
        if not issubclass(record_cls, BaseRecord):
            raise ValueError(f"{record_cls.__name__} does not inherit from BaseRecord.")
        if record_cls not in self._batches:
            self._batches[record_cls] = []
        self._batches[record_cls].append(record)
        return self

    def add_many(self, records) -> ModelOutput:
        for record in records:
            self.add(record)
        return self

    def all_records(self):
        for records in self._batches.values():
            yield from records

    def to_dict(self) -> dict:
        return {
            cls.__name__: [dataclasses.asdict(r) for r in records]
            for cls, records in self._batches.items()
        }

    @classmethod
    def from_dict(cls, d: dict, registry: dict[str, Type]) -> ModelOutput:
        output = cls()
        for class_name, records in d.items():
            record_cls = registry.get(class_name)
            if record_cls is None:
                raise ValueError(
                    f"Unknown record class '{class_name}'. " f"Add it to the registry."
                )
            for record_data in records:
                output.add(record_cls.from_dict(record_data))
        return output

    def __repr__(self) -> str:
        summary = ", ".join(
            f"{cls.__name__}: {len(records)}" for cls, records in self._batches.items()
        )
        return f"ModelOutput({summary})"
