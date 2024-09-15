import numpy as np
import matplotlib.pyplot as plt
import rasterio
from conf import DATA_DIR, DASHBOARD_DIR

# Path to your GeoTIFF file
tif_path = DATA_DIR/'NO2_plant_larger.tif'

# Open the GeoTIFF file and get its shape
with rasterio.open(tif_path) as src:
    height = src.height
    width = src.width

# Calculate the aspect ratio
aspect_ratio = width / height

# Create a grid matching the GeoTIFF dimensions
X, Y = np.mgrid[:width, :height]

# Calculate U and V components for the desired angle (23 degrees up from horizontal)
angle = np.radians(-20)  # 23 degrees up from horizontal
U = np.cos(angle) * np.ones_like(X) + np.random.normal(0, 0.05, X.shape)
V = -np.sin(angle) * np.ones_like(Y) + np.random.normal(0, 0.05, Y.shape)  # Negative to go upwards

# Normalize U and V to maintain consistent arrow lengths
magnitude = np.sqrt(U**2 + V**2)
U /= magnitude
V /= magnitude

# Add slight randomness to arrow lengths
lengths = 1 + np.random.normal(0, 0.05, X.shape)
U *= lengths
V *= lengths

# Create the plot with the correct aspect ratio
fig, ax = plt.subplots(figsize=(20, 20/aspect_ratio))

# Plot slightly randomized arrows for every 4th pixel
ax.quiver(X[::4, ::4], Y[::4, ::4], U[::4, ::4], V[::4, ::4],
          scale=0.5, scale_units='xy', angles='xy', color='blue', width=0.002)

# Set the limits and invert the y-axis to match image coordinates
ax.set_xlim(0, width)
ax.set_ylim(height, 0)

# Remove ticks
ax.set_xticks([])
ax.set_yticks([])

# Add a title
plt.title("Wind raster")

# Ensure the layout is tight and save the figure with the correct aspect ratio
plt.tight_layout()
plt.savefig(DASHBOARD_DIR/"wind_raster.png", dpi=300, bbox_inches='tight')

# Show the plot
plt.show()