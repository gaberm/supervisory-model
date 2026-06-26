import pytest
from dataclasses import dataclass
from base import Timestamp


@dataclass(kw_only=True)
class SimpleTimestamp(Timestamp):
    pass


def test_bad_time_field():
    with pytest.raises(TypeError, match="time_field must be a field in"):

        @dataclass(kw_only=True)
        class BadTimestamp(Timestamp):
            time_field = "missing_field"


def test_bad_time_type():
    with pytest.raises(TypeError, match=".time must be a float or int"):
        SimpleTimestamp(time="bad_time")


def test_negative_time_raises():
    with pytest.raises(ValueError, match="must be non-negative"):
        SimpleTimestamp(time=-1.0)


def test_valid_record():
    record = SimpleTimestamp(time=1.0)
    assert record.time == 1.0
