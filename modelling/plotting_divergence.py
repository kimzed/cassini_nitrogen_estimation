import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

def load_numpy_arrays(directory):
    """Load all NumPy arrays from .npy files in the specified directory."""
    npy_files = sorted([f for f in os.listdir(directory) if f.endswith('.npy')])
    data_list = []
    date_list = []

    for file in npy_files:
        file_path = os.path.join(directory, file)
        array = np.load(file_path)

        date_str = file.split('_')[-1].split('.')[0]
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        data_list.append(array)
        date_list.append(date)

    return data_list, date_list

def plot_data(no2, u_wind, v_wind, divergence, date, output_dir):
    """Create and save a plot of NO2, wind, and divergence data."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 8))

    # Plot NO2 data
    im1 = ax1.imshow(no2, cmap='YlOrRd', interpolation='nearest')
    plt.colorbar(im1, ax=ax1, label='NO2 Concentration')
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

    # Plot divergence data
    im3 = ax3.imshow(divergence, cmap='RdBu_r', interpolation='nearest')
    plt.colorbar(im3, ax=ax3, label='Divergence')
    ax3.set_title(f'Flux Divergence - {date}')
    ax3.set_xlabel('X coordinate')
    ax3.set_ylabel('Y coordinate')
    ax3.invert_yaxis()

    # Set integer ticks for all plots
    for ax in [ax1, ax2, ax3]:
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Adjust layout and save
    plt.tight_layout()
    output_file = os.path.join(output_dir, f'nox_emission_analysis_{date}.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    u_wind_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/u_wind_np"
    v_wind_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/v_wind_np"
    no2_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/no2_np"
    divergence_dir = "/home/cedric/repos/cassini_nitrogen_estimation/data/divergence_np"
    output_dir = "/home/cedric/repos/cassini_nitrogen_estimation/outputs/divergence_plots"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    u_wind_data, dates = load_numpy_arrays(u_wind_dir)
    v_wind_data, _ = load_numpy_arrays(v_wind_dir)
    no2_data, _ = load_numpy_arrays(no2_dir)
    divergence_data, _ = load_numpy_arrays(divergence_dir)

    for no2, u_wind, v_wind, divergence, date in zip(no2_data, u_wind_data, v_wind_data, divergence_data, dates):
        plot_data(no2, u_wind, v_wind, divergence, date, output_dir)
        print(f"Processed plot for {date}")

    print("All plots have been generated and saved.")