import os
import glob
import numpy as np
import rasterio


def fill_top_row_and_save(input_dir, output_dir):
    """
    Fill the top row of NaN values in wind rasters with values from the second row,
    and save the modified rasters in a new folder.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all .tif files in the input directory
    tif_files = glob.glob(os.path.join(input_dir, '*.tif'))

    for tif_file in tif_files:
        with rasterio.open(tif_file) as src:
            # Read the raster data
            data = src.read(1)

            # Check if the top row contains NaN values
            if np.isnan(data[0]).any():
                # Fill the top row with values from the second row
                data[0] = data[1]

            # Prepare the output file path
            output_file = os.path.join(output_dir, os.path.basename(tif_file))

            # Create a new raster file with the modified data
            with rasterio.open(
                    output_file,
                    'w',
                    driver='GTiff',
                    height=src.height,
                    width=src.width,
                    count=1,
                    dtype=data.dtype,
                    crs=src.crs,
                    transform=src.transform,
            ) as dst:
                dst.write(data, 1)

        print(f"Processed and saved: {output_file}")


def main():
    # Define input and output directories for u_wind and v_wind
    u_wind_input_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/wind_poland/u_wind"
    v_wind_input_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/wind_poland/v_wind"
    u_wind_output_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/wind_poland/u_wind_filled"
    v_wind_output_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/wind_poland/v_wind_filled"

    # Process u_wind rasters
    print("Processing u_wind rasters...")
    fill_top_row_and_save(u_wind_input_dir, u_wind_output_dir)

    # Process v_wind rasters
    print("Processing v_wind rasters...")
    fill_top_row_and_save(v_wind_input_dir, v_wind_output_dir)

    print("All rasters have been processed and saved.")


if __name__ == "__main__":
    main()