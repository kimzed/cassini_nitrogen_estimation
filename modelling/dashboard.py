import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from conf import DASHBOARD_DIR

# Load the CSV file
df = pd.read_csv(DASHBOARD_DIR/'daily_nox_emissions.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Set up the plot style
plt.style.use('ggplot')  # Changed from 'seaborn' to 'ggplot'
fig, axes = plt.subplots(3, 2, figsize=(20, 20))
fig.suptitle('NOx Emissions Dashboard', fontsize=16)

# 1. Total NOx emissions over time
axes[0, 0].plot(df['Date'], df['NOx_Emissions_kg_per_day'])
axes[0, 0].set_title('Daily NOx Emissions')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('NOx Emissions (kg/day)')

# 2. Emissions with error bounds
axes[0, 1].plot(df['Date'], df['NOx_Emissions_kg_per_day'], color='red', label='Emissions')
axes[0, 1].fill_between(df['Date'],
                        df['NOx_Emissions_kg_per_day'] - df['Error_Bound_kg_per_day'],
                        df['NOx_Emissions_kg_per_day'] + df['Error_Bound_kg_per_day'],
                        color='blue', alpha=0.3, label='Error Bounds')
axes[0, 1].axhline(y=df['Permitted_Level_kg_per_day'].iloc[0], color='green', linestyle='--', label='Permitted Level')
axes[0, 1].set_title('NOx Emissions with Error Bounds')
axes[0, 1].set_xlabel('Date')
axes[0, 1].set_ylabel('NOx Emissions (kg/day)')
axes[0, 1].legend()

# To make the y-axis scale more appropriate
y_max = max(df['NOx_Emissions_kg_per_day'] + df['Error_Bound_kg_per_day']) * 1.1
axes[0, 1].set_ylim(0, y_max)

# 3. Temporal patterns (weekly averages)
df['Week'] = df['Date'].dt.to_period('W')
weekly_avg = df.groupby('Week')['NOx_Emissions_kg_per_day'].mean().reset_index()
weekly_avg['Week'] = weekly_avg['Week'].dt.to_timestamp()
axes[1, 0].plot(weekly_avg['Week'], weekly_avg['NOx_Emissions_kg_per_day'])
axes[1, 0].set_title('Weekly Average NOx Emissions')
axes[1, 0].set_xlabel('Week')
axes[1, 0].set_ylabel('Average NOx Emissions (kg/day)')

# 4. Regulatory compliance
exceedance_days = (df['NOx_Emissions_kg_per_day'] > df['Permitted_Level_kg_per_day']).sum()
compliance_rate = ((365 - exceedance_days) / 365) * 100
axes[1, 1].bar(['Compliant', 'Non-Compliant'], [compliance_rate, 100-compliance_rate])
axes[1, 1].set_title('Annual Compliance Rate')
axes[1, 1].set_ylabel('Percentage')
for i, v in enumerate([compliance_rate, 100-compliance_rate]):
    axes[1, 1].text(i, v, f'{v:.1f}%', ha='center', va='bottom')

# 5. Anomaly detection
threshold = df['NOx_Emissions_kg_per_day'].mean() + 2 * df['NOx_Emissions_kg_per_day'].std()
df['Anomaly'] = df['NOx_Emissions_kg_per_day'] > threshold
axes[2, 0].scatter(df['Date'], df['NOx_Emissions_kg_per_day'], c=df['Anomaly'], cmap='coolwarm')
axes[2, 0].set_title('Anomaly Detection in NOx Emissions')
axes[2, 0].set_xlabel('Date')
axes[2, 0].set_ylabel('NOx Emissions (kg/day)')

# 6. Confidence levels distribution
sns.histplot(df['Confidence_Level_percent'], kde=True, ax=axes[2, 1])
axes[2, 1].set_title('Distribution of Confidence Levels')
axes[2, 1].set_xlabel('Confidence Level (%)')
axes[2, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig(DASHBOARD_DIR/'nox_emissions_dashboard.png')
plt.close()

# Generate summary statistics
summary_stats = df['NOx_Emissions_kg_per_day'].describe()
total_emissions = df['NOx_Emissions_kg_per_day'].sum()
total_exceedances = df['Exceedance_kg_per_day'].sum()

print("Summary Statistics:")
print(summary_stats)
print(f"\nTotal Annual NOx Emissions: {total_emissions:.2f} kg")
print(f"Total Annual Exceedances: {total_exceedances:.2f} kg")
print(f"Annual Compliance Rate: {compliance_rate:.2f}%")
print(f"Number of Anomalies Detected: {df['Anomaly'].sum()}")