import dataclasses
import h3
from typing import Any
from base import Geometry, SHAPE_TYPE
from base.output.dataset import Dataset


def assign_cells(output: Any, resolution: int) -> Any:
    if isinstance(output, list):
        return assign_model_output(output, resolution)
    elif isinstance(output, Dataset):
        return assign_external_dataset(output, resolution)
    else:
        raise TypeError(
            "Cannot assign cells to output of type: {}".format(type(output))
        )


def assign_external_dataset(dataset: Dataset, resolution: int) -> Dataset:
    if dataset.h3_index:
        dataset.data["cell_ids"] = dataset.data[dataset.geometry_column].apply(
            lambda geom: _cells_for_shape(geom, resolution)
        )
    return dataset


def assign_model_output(outputs: list[Geometry], resolution: int) -> list[Geometry]:
    results = []
    for output in outputs:
        shape = output.shape
        coords = output.coords_4326
        output = dataclasses.replace(
            output, h3_ids=_cells_for_shape(shape, coords, resolution)
        )
        results.append(output)
    return results


def _cells_for_shape(
    shape: SHAPE_TYPE,
    coords: tuple[float, float] | list[tuple[float, float]],
    resolution: int,
) -> list[str]:
    if shape == "POINT":
        return [h3.geo_to_h3(coords[1], coords[0], resolution)]

    if shape == "LINESTRING":
        ids = []
        for i in range(len(coords) - 1):
            start = h3.geo_to_h3(coords[i][1], coords[i][0], resolution)
            end = h3.geo_to_h3(coords[i + 1][1], coords[i + 1][0], resolution)
            ids.extend(h3.h3_line(start, end))
        return list(dict.fromkeys(ids))

    if shape == "POLYGON":
        geo = {
            "type": "Polygon",
            "coordinates": [coords],
        }
        return list(h3.polyfill_geojson(geo, resolution))

    raise ValueError(f"Unsupported shape type: {shape}")
