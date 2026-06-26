import pytest
from dataclasses import dataclass
from base import Record


def test_missing_primary_key_field():
    with pytest.raises(
        ValueError, match="BadRecord: primary_key field 'column_1' is not declared"
    ):

        @dataclass(kw_only=True)
        class BadRecord(Record):
            table_name = "bad_record"
            primary_key = ("column_1",)


def test_missing_indexed_field():
    with pytest.raises(
        ValueError, match="BadRecord: indexed field 'column_2' is not declared"
    ):

        @dataclass(kw_only=True)
        class BadRecord(Record):
            table_name = "bad_record"
            primary_key = ("column_1",)
            indexed = "column_2"

            column_1: str


def test_invalid_on_conflict_type():
    with pytest.raises(
        ValueError,
        match=".on_conflict must be 'IGNORE' or 'UPDATE'; got",
    ):

        @dataclass(kw_only=True)
        class BadRecord(Record):
            table_name = "bad_record"
            primary_key = ("column_1",)
            indexed = ()
            on_conflict = "bad_value"

            column_1: str


def test_invalid_diagnostic_type():
    with pytest.raises(
        TypeError,
        match=".diagnostic must be a boolean; got",
    ):

        @dataclass(kw_only=True)
        class BadRecord(Record):
            table_name = "bad_record"
            primary_key = ("column_1",)
            indexed = ()
            diagnostic = "bad_value"

            column_1: str


def test_valid_record():

    @dataclass(kw_only=True)
    class ValidRecord(Record):
        table_name = "valid_record"
        primary_key = ("column_1",)
        indexed = ()
        diagnostic = False

        column_1: str

    assert ValidRecord.primary_key == ("column_1",)
    ValidRecord(column_1="v1")
