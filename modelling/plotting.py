import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from scipy.interpolate import RegularGridInterpolator


def load_wind_data(u_wind_dir, v_wind_dir):
    """Load U and V wind component rasters and their dates."""
    u_files = sorted(glob.glob(os.path.join(u_wind_dir, '*.tif')))
    v_files = sorted(glob.glob(os.path.join(v_wind_dir, '*.tif')))

    if len(u_files) != len(v_files):
        raise ValueError("Mismatch in number of U and V wind files")

    dates = [os.path.basename(file).split('_')[-1].split('.')[0] for file in u_files]

    wind_data = []
    for u_file, v_file in zip(u_files, v_files):
        with rasterio.open(u_file) as u_src, rasterio.open(v_file) as v_src:
            u_wind = u_src.read(1)
            v_wind = v_src.read(1)

        # Replace NaN values with 0
        u_wind = np.nan_to_num(u_wind, nan=0.0)
        v_wind = np.nan_to_num(v_wind, nan=0.0)

        wind_data.append((u_wind, v_wind))

    return wind_data, dates


def load_no2_data(no2_dir):
    """Load NO2 rasters and their dates."""
    no2_files = sorted(glob.glob(os.path.join(no2_dir, '*.tif')))
    dates = [os.path.basename(file).split('_')[-1].split('.')[0] for file in no2_files]

    no2_data = []
    for no2_file in no2_files:
        with rasterio.open(no2_file) as src:
            no2 = src.read(1)

        # Replace NaN values with 0
        no2 = np.nan_to_num(no2, nan=0.0)
        no2_data.append(no2)

    return no2_data, dates


def plot_no2_and_wind(no2_data, u_wind, v_wind, date, output_dir):
    """Create and save a side-by-side plot of NO2 concentration and wind data."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 8))

    # Plot NO2 data
    im1 = ax1.imshow(no2_data, cmap='YlOrRd', interpolation='nearest')
    cbar1 = plt.colorbar(im1, ax=ax1)
    cbar1.set_label('NO2 Concentration')
    ax1.set_title(f'NO2 Concentration - {date}')
    ax1.set_xlabel('X coordinate')
    ax1.set_ylabel('Y coordinate')
    ax1.invert_yaxis()

    # Plot wind data
    Y, X = np.mgrid[:u_wind.shape[0], :u_wind.shape[1]]
    q = ax2.quiver(X, Y, u_wind, v_wind, scale=3, scale_units='inches')
    ax2.quiverkey(q, X=0.9, Y=1.05, U=10, label='10 m/s', labelpos='E')
    ax2.set_title(f'Wind Direction and Speed - {date}')
    ax2.set_xlabel('X coordinate')
    ax2.set_ylabel('Y coordinate')
    ax2.invert_yaxis()

    # Set integer ticks for both plots
    for ax in [ax1, ax2]:
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.tight_layout()
    output_file = os.path.join(output_dir, f'no2_and_wind_map_{date}.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()



def interpolate_wind_to_no2_grid(u_wind, v_wind, no2_shape):
    """Interpolate wind data to match NO2 data shape using RegularGridInterpolator."""
    old_shape = u_wind.shape
    old_y = np.arange(old_shape[0])
    old_x = np.arange(old_shape[1])

    new_y = np.linspace(0, old_shape[0] - 1, no2_shape[0])
    new_x = np.linspace(0, old_shape[1] - 1, no2_shape[1])

    # Create meshgrid for new coordinates
    new_xx, new_yy = np.meshgrid(new_x, new_y)
    new_points = np.column_stack([new_yy.ravel(), new_xx.ravel()])

    # Create interpolation functions for u and v components
    interp_u = RegularGridInterpolator((old_y, old_x), u_wind)
    interp_v = RegularGridInterpolator((old_y, old_x), v_wind)

    # Apply interpolation
    u_wind_interp = interp_u(new_points).reshape(no2_shape)
    v_wind_interp = interp_v(new_points).reshape(no2_shape)

    return u_wind_interp, v_wind_interp


def plot_wind_arrows(u_wind, v_wind, date, output_dir):
    """Create and save a wind arrow map for given U and V components."""
    Y, X = np.mgrid[:u_wind.shape[0], :u_wind.shape[1]]

    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot arrows for all grid points
    q = ax.quiver(X, Y, u_wind, v_wind, scale=3, scale_units='inches')
    ax.quiverkey(q, X=0.9, Y=1.05, U=10, label='10 m/s', labelpos='E')

    ax.set_title(f'Wind Direction and Speed - {date}')
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')

    # Invert y-axis to match the typical GIS raster orientation
    ax.invert_yaxis()

    # Set integer ticks
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    output_file = os.path.join(output_dir, f'wind_map_{date}.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


def plot_no2(no2_data, date, output_dir):
    """Create and save a NO2 concentration map."""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot NO2 data as a heatmap
    im = ax.imshow(no2_data, cmap='YlOrRd', interpolation='nearest')

    # Add a colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('NO2 Concentration')

    ax.set_title(f'NO2 Concentration - {date}')
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')

    # Invert y-axis to match the typical GIS raster orientation
    ax.invert_yaxis()

    # Set integer ticks
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    output_file = os.path.join(output_dir, f'no2_map_{date}.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


def main():
    u_wind_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/wind_poland/u_wind"
    v_wind_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/wind_poland/v_wind"
    output_dir = "/home/cedric/repos/cassini_nitrogen_estimation/outputs/maps"
    no2_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/no2_poland"

    u_wind_output_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/u_wind_np"
    v_wind_output_dir= "/home/cedric/repos/cassini_nitrogen_estimation/data/v_wind_np"
    no2_output_dir= "/home/cedric/repos/cassini_nitrogen_estimation/data/no2_np"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(u_wind_output_dir, exist_ok=True)
    os.makedirs(v_wind_output_dir, exist_ok=True)
    os.makedirs(no2_output_dir, exist_ok=True)

    wind_data, wind_dates = load_wind_data(u_wind_dir, v_wind_dir)
    no2_data, no2_dates = load_no2_data(no2_dir)

    # Ensure wind and NO2 data have matching dates
    if wind_dates != no2_dates:
        raise ValueError("Mismatch in dates between wind and NO2 data")

    for (u_wind, v_wind), no2, date in zip(wind_data, no2_data, wind_dates):
        # Interpolate wind data to match NO2 grid
        u_wind_interp, v_wind_interp = interpolate_wind_to_no2_grid(u_wind, v_wind, no2.shape)

        np.save(os.path.join(u_wind_output_dir, f'u_wind_interp_{date}.npy'), u_wind_interp)
        np.save(os.path.join(v_wind_output_dir, f'v_wind_interp_{date}.npy'), v_wind_interp)
        np.save(os.path.join(no2_output_dir, f'no2_{date}.npy'), no2)

        plot_wind_arrows(u_wind_interp, v_wind_interp, date, output_dir)
        plot_no2(no2, date, output_dir)
        plot_no2_and_wind(no2, u_wind_interp, v_wind_interp, date, output_dir)
        print(f"Processed wind and NO2 maps for {date}")


if __name__ == "__main__":
    main()