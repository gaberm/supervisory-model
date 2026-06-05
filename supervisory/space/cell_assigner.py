import dataclasses
import h3
from shapely.geometry import Point, LineString, Polygon
from typing import Any
from base import Entity
from adapter.data_adapter import ExternalDataset


def assign_cells(entity: Any, resolution: int) -> Any:
    if isinstance(entity, list):
        return assign_model_output(entity, resolution)
    elif isinstance(entity, ExternalDataset):
        return assign_external_dataset(entity, resolution)
    else:
        raise TypeError(
            "Cannot assign cells to output of type: {}".format(type(entity))
        )


def assign_external_dataset(
    dataset: ExternalDataset, resolution: int
) -> ExternalDataset:
    if dataset.h3_index:
        dataset.data["cell_ids"] = dataset.data[dataset.geometry_column].apply(
            lambda geom: _cells_for_shape(geom, resolution)
        )
    return dataset


def assign_model_output(records: list[Entity], resolution: int) -> list[Entity]:
    result = []
    for record in records:
        geometry = getattr(record, "geometry", None)
        if geometry is not None and not isinstance(geometry, str):
            record = dataclasses.replace(
                record, cell_ids=_cells_for_shape(geometry, resolution)
            )
        result.append(record)
    return result


def _cells_for_shape(
    geometry: Point | LineString | Polygon, resolution: int
) -> list[str]:
    if isinstance(geometry, Point):
        return [h3.geo_to_h3(geometry.y, geometry.x, resolution)]

    if isinstance(geometry, LineString):
        coords = list(geometry.coords)
        cells = []
        for i in range(len(coords) - 1):
            start = h3.geo_to_h3(coords[i][1], coords[i][0], resolution)
            end = h3.geo_to_h3(coords[i + 1][1], coords[i + 1][0], resolution)
            cells.extend(h3.h3_line(start, end))
        return list(dict.fromkeys(cells))

    if isinstance(geometry, Polygon):
        geo = {
            "type": "Polygon",
            "coordinates": [list(geometry.exterior.coords)],
        }
        return list(h3.polyfill_geojson(geo, resolution))

    raise ValueError(f"Unsupported geometry type: {type(geometry)}")
