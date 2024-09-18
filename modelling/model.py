import numpy as np
from scipy import ndimage
import os
from datetime import datetime

def load_numpy_arrays(directory):
    """
    Load all NumPy arrays from .npy files in the specified directory.

    Args:
    directory (str): Path to the directory containing .npy files

    Returns:
    tuple: List of numpy arrays, List of dates
    """
    npy_files = sorted([f for f in os.listdir(directory) if f.endswith('.npy')])
    data_list = []
    date_list = []

    for file in npy_files:
        file_path = os.path.join(directory, file)
        array = np.load(file_path)

        # Extract date from filename (assuming format 'data_YYYY-MM-DD.npy')
        date_str = file.split('_')[-1].split('.')[0]
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        data_list.append(array)
        date_list.append(date)

    return data_list, date_list

def calculate_flux(no2, u_wind, v_wind):
    """Calculate NOx flux."""
    flux_u = no2 * u_wind
    flux_v = no2 * v_wind
    return flux_u, flux_v

def calculate_divergence(flux_u, flux_v):
    """Calculate divergence of the flux."""
    du_dx = ndimage.sobel(flux_u, axis=1)
    dv_dy = ndimage.sobel(flux_v, axis=0)
    return du_dx + dv_dy

def temporal_average(data_list):
    """Calculate temporal average of a list of arrays."""
    return np.mean(data_list, axis=0)

def save_numpy_array(array, output_dir, date):
    """Save numpy array with date in filename."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = f"divergence_{date.strftime('%Y-%m-%d')}.npy"
    file_path = os.path.join(output_dir, filename)
    np.save(file_path, array)

if __name__ == "__main__":
    u_wind_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/u_wind_np"
    v_wind_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/v_wind_np"
    no2_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/no2_np"
    output_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/divergence_np"

    u_wind_data, dates = load_numpy_arrays(u_wind_dir)
    v_wind_data, _ = load_numpy_arrays(v_wind_dir)
    no2_data, _ = load_numpy_arrays(no2_dir)

    divergence_maps = []

    for no2, u_wind, v_wind, date in zip(no2_data, u_wind_data, v_wind_data, dates):
        flux_u, flux_v = calculate_flux(no2, u_wind, v_wind)
        divergence = calculate_divergence(flux_u, flux_v)
        divergence_maps.append(divergence)
        save_numpy_array(divergence, output_dir, date)

    averaged_divergence = temporal_average(divergence_maps)
    save_numpy_array(averaged_divergence, output_dir, datetime.now().date())

    print("Divergence maps saved. Shape of averaged divergence map:", averaged_divergence.shape)