import pandas as pd
import matplotlib.pyplot as plt
from modelling.conf import DASHBOARD_DIR

# Load the CSV file
df = pd.read_csv(DASHBOARD_DIR/'daily_nox_emissions.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Calculate yearly emissions
df['Year'] = df['Date'].dt.year
yearly_emissions = df.groupby('Year')['NOx_Emissions_kg_per_day'].sum().reset_index()
yearly_emissions = yearly_emissions.rename(columns={'NOx_Emissions_kg_per_day': 'Yearly_NOx_Emissions_kg'})

# Assume CSRD regulation defines a yearly maximum (you'll need to replace this with the actual value)
CSRD_YEARLY_MAX = 1500000

# Set up the plot style
plt.style.use('ggplot')
fig, axes = plt.subplots(2, 2, figsize=(20, 15))
fig.suptitle('NOx Emissions Dashboard', fontsize=16)

# (Plotting code remains the same)

plt.tight_layout()
plt.savefig(DASHBOARD_DIR/'nox_emissions_dashboard.png')
plt.close()

# Calculate and save yearly summary data
yearly_summary = yearly_emissions.copy()
yearly_summary['Compliance'] = yearly_summary['Yearly_NOx_Emissions_kg'] <= CSRD_YEARLY_MAX
yearly_summary['Exceedance_kg'] = (yearly_summary['Yearly_NOx_Emissions_kg'] - CSRD_YEARLY_MAX).clip(lower=0)

# Print debug information
print("Yearly Summary:")
print(yearly_summary)
print("\nCompliance by year:")
print(yearly_summary['Compliance'])

# Generate overall summary statistics
total_emissions = yearly_summary['Yearly_NOx_Emissions_kg'].sum()
total_exceedances = yearly_summary['Exceedance_kg'].sum()
compliant_years = yearly_summary['Compliance'].sum()
total_years = len(yearly_summary)
compliance_rate = (compliant_years / total_years) * 100
num_anomalies = df['Anomaly'].sum()

# Print more debug information
print(f"\nCompliant years: {compliant_years}")
print(f"Total years: {total_years}")
print(f"Calculated compliance rate: {compliance_rate}%")

# Save overall summary to a text file
with open(DASHBOARD_DIR/'overall_nox_summary.txt', 'w') as f:
    f.write(f"Total NOx Emissions (all years): {total_emissions:.2f} kg\n")
    f.write(f"Total Exceedances (all years): {total_exceedances:.2f} kg\n")
    f.write(f"Overall Yearly Compliance Rate: {compliance_rate:.2f}%\n")
    f.write(f"Number of Anomalies Detected (daily): {num_anomalies}\n")
    f.write(f"\nYearly Breakdown:\n")
    f.write(yearly_summary.to_string())

print("Dashboard updated and summary data saved.")