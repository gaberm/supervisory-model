from typing import ClassVar, Literal

SHAPE_TYPE = Literal["POINT", "LINESTRING", "POLYGON"]


class Entity:
    """Base class defining the table schema and adapter output structure."""

    table_name: ClassVar[str]
    primary_key: ClassVar[tuple[str, ...]]
    indexed: ClassVar[tuple[str, ...]] = ()
    diagnostic: ClassVar[bool] = False

    time: float
    coord: tuple[float, float] | list[tuple[float, float]]
    geometry: SHAPE_TYPE
    h3: str

    def __post_init__(self):
        if self.geometry == "POINT":
            assert isinstance(
                self.coord, tuple
            ), "POINT geometry must have a single coordinate tuple."
        else:
            assert isinstance(
                self.coord, list
            ), f"{self.geometry} geometry must have a list of coordinate tuples."
