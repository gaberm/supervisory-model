from __future__ import annotations
from dataclasses import dataclass, fields as dataclass_fields
from typing import Any, ClassVar
from base.entity.entity import Entity


@dataclass(frozen=True)
class Comparison:
    op: str
    value: Any


def Equal(value: Any) -> Comparison:
    return Comparison("=", value)


def NotEqual(value: Any) -> Comparison:
    return Comparison("!=", value)


def Less(value: Any) -> Comparison:
    return Comparison("<", value)


def LessEqual(value: Any) -> Comparison:
    return Comparison("<=", value)


def Greater(value: Any) -> Comparison:
    return Comparison(">", value)


def GreaterEqual(value: Any) -> Comparison:
    return Comparison(">=", value)


@dataclass(frozen=True)
class Filter:
    entity: type
    field: str
    cmp: Comparison


@dataclass(frozen=True)
class Join:
    left_entity: type
    left_field: str
    right_entity: type
    right_field: str


class Input:
    entity: ClassVar[type[Entity]]
    filters: ClassVar[list[Filter]] = []
    on: ClassVar[Join] = None
    row: ClassVar[type]

    entities: ClassVar[list[type]]
    is_join: ClassVar[bool]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "entity" not in {k for c in cls.__mro__ for k in vars(c)}:
            return
        _resolve_entities(cls)
        _resolve_filters(cls)


def _resolve_entities(cls) -> None:
    cls.entities = (
        list(cls.entity) if isinstance(cls.entity, (list, tuple)) else [cls.entity]
    )
    cls.is_join = len(cls.entities) > 1


def _resolve_filters(cls) -> None:
    valid = {e: _field_names(e) for e in cls.entities}
    cls.filters = [_make_filter(cls, f, valid) for f in getattr(cls, "filters", [])]
    if cls.on is not None:
        cls.on = _make_join(cls, cls.on, valid)
    elif cls.is_join:
        raise TypeError(
            f"{cls.__name__}: {len(cls.entities)} entities require an `on` join condition"
        )


def _field_names(entity: type) -> set[str]:
    try:
        return {f.name for f in dataclass_fields(entity)}
    except TypeError:
        raise TypeError(
            f"{getattr(entity, '__name__', entity)!r} is not a dataclass entity"
        )


def _check_field(owner: str, entity: type, field: str, valid: dict) -> None:
    if entity not in valid:
        raise TypeError(
            f"{owner}: references {entity.__name__}, "
            f"not in entity={[e.__name__ for e in valid]}"
        )
    if field not in valid[entity]:
        raise AttributeError(
            f"{owner}: {entity.__name__} has no field {field!r}. "
            f"Valid fields: {sorted(valid[entity])}"
        )


def _make_filter(cls, spec, valid) -> Filter:
    entity, field, cmp = (
        (spec.entity, spec.field, spec.cmp)
        if isinstance(spec, Filter)
        else _unpack(cls, spec, 3, "each filter must be (entity, field, Cmp)")
    )
    if not isinstance(cmp, Comparison):
        raise TypeError(
            f"{cls.__name__}: filter on {entity.__name__}.{field} needs a comparison "
            f"like Eq(...)/Lt(...); got {cmp!r}"
        )
    _check_field(cls.__name__, entity, field, valid)
    return Filter(entity, field, cmp)


def _make_join(cls, spec, valid) -> Join:
    le, lf, re_, rf = (
        (spec.left_entity, spec.left_field, spec.right_entity, spec.right_field)
        if isinstance(spec, Join)
        else _unpack(cls, spec, 4, "`on` must be (LeftEntity, 'lf', RightEntity, 'rf')")
    )
    _check_field(f"{cls.__name__}.on", le, lf, valid)
    _check_field(f"{cls.__name__}.on", re_, rf, valid)
    return Join(le, lf, re_, rf)


def _unpack(cls, spec, n, msg):
    if not isinstance(spec, (list, tuple)) or len(spec) != n:
        raise TypeError(f"{cls.__name__}: {msg}; got {spec!r}")
    return tuple(spec)
