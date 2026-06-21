from typing import Literal

SHAPE_TYPE = Literal["POINT", "LINESTRING", "POLYGON"]


class Geometry:
    coords: tuple[float, float] | list[tuple[float, float]]
    epsg_code: int = 4326
    shape: SHAPE_TYPE
    h3_ids: str | list[str] | None = None
    coords_4326: tuple[float, float] | list[tuple[float, float]] | None = None

    def _validate_shape(self):
        if self.shape == "POINT":
            assert isinstance(
                self.coords, tuple
            ), "POINT geometry must have a single coordinate tuple."
        else:
            assert isinstance(
                self.coords, list
            ), f"{self.shape} geometry must have a list of coordinate tuples."
