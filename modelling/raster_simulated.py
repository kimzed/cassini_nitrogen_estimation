import rasterio
import numpy as np
import geopandas as gpd
from rasterio.transform import from_origin
from scipy.spatial.distance import cdist
from conf import DATA_DIR


def create_concentrated_decay_raster(input_raster_path, point_gpkg_path, output_raster_path, decay_factor=0.1,
                                     concentration_factor=2):
    # Read the input raster
    with rasterio.open(input_raster_path) as src:
        raster_data = src.read(1)  # Assuming single band raster
        metadata = src.meta.copy()

    # Read the point from the GeoPackage
    gdf = gpd.read_file(point_gpkg_path)
    point = gdf.geometry.iloc[0]

    # Convert point to pixel coordinates
    col, row = ~src.transform * (point.x, point.y)

    # Create a grid of coordinates
    height, width = raster_data.shape
    y, x = np.ogrid[0:height, 0:width]

    # Calculate distances from each pixel to the point
    distances = np.sqrt((x - col) ** 2 + (y - row) ** 2)

    # Create concentrated decay raster
    decay_raster = np.exp(-decay_factor * distances ** concentration_factor)

    # Normalize the decay raster to match the range of the original raster
    original_min, original_max = np.nanmin(raster_data), np.nanmax(raster_data)
    decay_raster = (decay_raster - np.min(decay_raster)) / (np.max(decay_raster) - np.min(decay_raster))
    decay_raster = decay_raster * (original_max - original_min) + original_min

    # Mask out areas where the original raster had no data
    if np.isnan(raster_data).any():
        decay_raster[np.isnan(raster_data)] = np.nan

    # Update metadata for the new raster
    metadata.update(dtype=rasterio.float32, count=1)

    # Write the new raster
    with rasterio.open(output_raster_path, 'w', **metadata) as dst:
        dst.write(decay_raster.astype(rasterio.float32), 1)

    print(f"Concentrated decay raster saved to {output_raster_path}")


# Usage
input_raster_path = DATA_DIR/'NO2_plant_larger.tif'
point_gpkg_path = '/home/cedric/plant_point_2.gpkg'
output_raster_path = DATA_DIR/'NO2_simulated.tif'

create_concentrated_decay_raster(input_raster_path, point_gpkg_path, output_raster_path)