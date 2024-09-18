import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import ndimage
import os
from datetime import datetime
from scipy import ndimage, optimize

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


def gaussian_2d(xy, amplitude, x0, y0, sigma_x, sigma_y, theta, offset):
    """2D Gaussian function."""
    x, y = xy
    a = (np.cos(theta) ** 2) / (2 * sigma_x ** 2) + (np.sin(theta) ** 2) / (2 * sigma_y ** 2)
    b = -(np.sin(2 * theta)) / (4 * sigma_x ** 2) + (np.sin(2 * theta)) / (4 * sigma_y ** 2)
    c = (np.sin(theta) ** 2) / (2 * sigma_x ** 2) + (np.cos(theta) ** 2) / (2 * sigma_y ** 2)
    return amplitude * np.exp(-(a * (x - x0) ** 2 + 2 * b * (x - x0) * (y - y0) + c * (y - y0) ** 2)) + offset


def fit_gaussian_2d(data):
    """Fit a 2D Gaussian to the data."""
    height, width = data.shape
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    xy = np.vstack((x.ravel(), y.ravel()))

    # Initial guess for parameters
    amplitude = data.max()
    x0, y0 = np.unravel_index(data.argmax(), data.shape)
    sigma_x = sigma_y = np.sqrt(data.sum() / amplitude) / 2

    popt, _ = optimize.curve_fit(gaussian_2d, xy, data.ravel(),
                                 p0=[amplitude, x0, y0, sigma_x, sigma_y, 0, 0])
    return popt


def quantify_emissions(peaks, pixel_area):
    """Convert fitted peaks to emission rates."""
    emissions = []
    for peak_pos, popt in peaks:
        amplitude, _, _, sigma_x, sigma_y, _, _ = popt
        # Emission rate proportional to amplitude and area of the Gaussian
        emission_rate = amplitude * 2 * np.pi * sigma_x * sigma_y * pixel_area
        emissions.append((peak_pos, emission_rate))
    return emissions


def visualize_results(divergence_map, emissions, lats, lons, output_dir):
    """Create a map of divergence with identified point sources."""
    plt.figure(figsize=(12, 8))
    m = Basemap(projection='mill', llcrnrlat=lats.min(), urcrnrlat=lats.max(),
                llcrnrlon=lons.min(), urcrnrlon=lons.max(), resolution='l')

    x, y = m(*np.meshgrid(lons, lats))
    m.pcolormesh(x, y, divergence_map, cmap='RdYlBu_r', shading='auto')

    for (y, x), emission_rate in emissions:
        m.plot(lons[x], lats[y], 'ko', markersize=5)
        plt.text(lons[x], lats[y], f'{emission_rate:.2f}', fontsize=8)

    m.drawcoastlines()
    m.drawcountries()
    plt.colorbar(label='Divergence')
    plt.title('NOx Emissions from Point Sources')

    plt.savefig(os.path.join(output_dir, 'nox_emissions_map.png'))
    plt.close()


def save_emissions_report(emissions, lats, lons, output_dir):
    """Save a report of quantified emissions."""
    df = pd.DataFrame(emissions, columns=['Position', 'Emission Rate'])
    df['Latitude'] = df['Position'].apply(lambda x: lats[x[0]])
    df['Longitude'] = df['Position'].apply(lambda x: lons[x[1]])
    df = df.drop('Position', axis=1)
    df.to_csv(os.path.join(output_dir, 'nox_emissions_report.csv'), index=False)


def detect_and_fit_peaks(divergence_map, threshold=0.5, max_peaks=10):
    """Detect peaks in the divergence map and fit Gaussians."""
    peaks = []
    remaining_map = divergence_map.copy()

    for _ in range(max_peaks):
        if remaining_map.max() < threshold:
            break

        peak_pos = np.unravel_index(remaining_map.argmax(), remaining_map.shape)
        peak_region = remaining_map[max(0, peak_pos[0] - 10):peak_pos[0] + 11,
                      max(0, peak_pos[1] - 10):peak_pos[1] + 11]

        try:
            popt = fit_gaussian_2d(peak_region)
            peaks.append((peak_pos, popt))

            # Remove fitted peak from the map
            y, x = np.ogrid[-peak_pos[0]:divergence_map.shape[0] - peak_pos[0],
                   -peak_pos[1]:divergence_map.shape[1] - peak_pos[1]]
            remaining_map -= gaussian_2d((x, y), *popt)
            remaining_map = np.maximum(remaining_map, 0)
        except RuntimeError:
            print(f"Failed to fit Gaussian at position {peak_pos}")

    return peaks


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

    lats = np.load("/home/cedric/repos/cassini_nitrogen_estimation/data/latitudes.npy")
    lons = np.load("/home/cedric/repos/cassini_nitrogen_estimation/data/longitudes.npy")

    pixel_area = (lats[1] - lats[0]) * (lons[1] - lons[0]) * 111000 * 111000  # in m^2

    peaks = detect_and_fit_peaks(averaged_divergence)

    emissions = quantify_emissions(peaks, pixel_area)

    visualize_results(averaged_divergence, emissions, lats, lons, output_dir)

    save_emissions_report(emissions, lats, lons, output_dir)

    print("Analysis complete. Results saved in the output directory.")