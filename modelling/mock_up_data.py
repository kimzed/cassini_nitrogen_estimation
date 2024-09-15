import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from conf import DASHBOARD_DIR

# Set random seed for reproducibility
np.random.seed(42)

# Generate dates for one year
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(365)]

# Generate base emissions data (kg/day)
base_emissions = 5000 + np.random.normal(0, 500, 365)

# Add seasonal variation
seasonal_variation = 1000 * np.sin(np.arange(365) * 2 * np.pi / 365)
emissions = base_emissions + seasonal_variation

# Ensure non-negative emissions
emissions = np.maximum(emissions, 0)

# Generate confidence levels (%)
confidence_levels = 95 + np.random.normal(0, 1, 365)
confidence_levels = np.clip(confidence_levels, 90, 99)

# Calculate error bounds (kg/day)
error_bounds = emissions * (1 - confidence_levels/100) / 2

# Set permitted level (kg/day)
permitted_level = 6000

# Create DataFrame
df = pd.DataFrame({
    'Date': dates,
    'NOx_Emissions_kg_per_day': emissions.round(2),
    'Confidence_Level_percent': confidence_levels.round(2),
    'Error_Bound_kg_per_day': error_bounds.round(2),
    'Permitted_Level_kg_per_day': permitted_level
})

# Add some random anomalies (unusual emission events)
anomaly_days = np.random.choice(365, 10, replace=False)
df.loc[anomaly_days, 'NOx_Emissions_kg_per_day'] *= np.random.uniform(1.5, 2.5, 10)

# Calculate exceedances
df['Exceedance_kg_per_day'] = np.maximum(df['NOx_Emissions_kg_per_day'] - permitted_level, 0)

# Save to CSV
df.to_csv(DASHBOARD_DIR/'daily_nox_emissions.csv', index=False)

print("CSV file 'daily_nox_emissions.csv' has been created.")

# Display first few rows
print(df.head())

# Display summary statistics
print(df.describe())