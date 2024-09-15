import ee
import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union
from pathlib import Path
from utils import get_spatial_mean
from pandas import DataFrame

MODEL_NASA = "CNRM-ESM2-1"


def generate_time_series(
    image_collection_id: str,
    band: str,
    polygon_location: Path,
    start_date: str,
    end_date: str,
) -> DataFrame:
    # Initialize the Earth Engine API.
    ee.Initialize()

    polygon_location = gpd.read_file(polygon_location)
    polygon_location = polygon_location.geometry.to_list()[0]
    merged_polygon = unary_union(polygon_location)
    coords_water_basin = list(merged_polygon.exterior.coords)

    ee_water_basin_polygon = ee.Geometry.Polygon(coords_water_basin)

    image_collection = ee.ImageCollection(image_collection_id)

    if image_collection_id == "NASA/GDDP-CMIP6":
        filtered_collection = (
            image_collection.filterBounds(ee_water_basin_polygon).filterDate(
                start_date, end_date
            )
        ).filter(ee.Filter.eq("model", MODEL_NASA))
    else:
        filtered_collection = image_collection.filterBounds(
            ee_water_basin_polygon
        ).filterDate(start_date, end_date)

    daily_mean = filtered_collection.map(
        lambda image: get_spatial_mean(image, ee_water_basin_polygon, band)
    )

    # Reduce the collections to lists
    time_series = (
        daily_mean.reduceColumns(
            ee.Reducer.toList(2), ["system:time_start", "daily_mean_temp"]
        )
        .values()
        .get(0)
    )

    # Get the results as a Python list.
    values = time_series.getInfo()

    df_time_series = pd.DataFrame(values, columns=["timestamp", "mean_daily"])
    df_time_series["timestamp"] = pd.to_datetime(df_time_series["timestamp"], unit="ms")
    df_time_series.set_index("timestamp", inplace=True)

    return df_time_series


path_water_basin = Path("/home/cedric/repos/cassini_data/villeret_water_basin.gpkg")

precipitation_time_series = generate_time_series(
    "NASA/GDDP-CMIP6",
    "pr",
    path_water_basin,
    "2000-01-01",
    "2001-01-01",
)

temperature_time_series = generate_time_series(
    "NASA/GDDP-CMIP6",
    "tas",
    path_water_basin,
    "2000-01-01",
    "2001-01-01",
)


evapotranspiration_time_series = generate_time_series(
    "ECMWF/ERA5_LAND/DAILY_AGGR",
    "potential_evaporation_sum",
    path_water_basin,
    "2000-01-01",
    "2001-01-01",
)

precipitation_time_series.to_csv(
    "/home/cedric/repos/cassini_data/precipitation_time_series.csv"
)
temperature_time_series.to_csv(
    "/home/cedric/repos/cassini_data/temperature_time_series.csv"
)
evapotranspiration_time_series.to_csv(
    "/home/cedric/repos/cassini_data/evapotranspiration_time_series.csv"
)