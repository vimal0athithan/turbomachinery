import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats  # For outlier detection using z-score

# Assumptions based on research:
# - Air density (rho) = 1.225 kg/m^3 (standard value at sea level)
# - Rotor diameter = 117 m (assumed for a typical 3.6 MW turbine, e.g., similar to Vestas V117-3.6 MW; adjust if exact specs are known)
# - Swept area A = pi * (d/2)^2
# - Data file: 'T1.csv' from your dataset
# - Columns: 'Date/Time', 'LV ActivePower (kW)', 'Wind Speed (m/s)', 'Theoretical_Power_Curve (KWh)', 'Wind Direction (°)'

# Note: The 'Theoretical_Power_Curve (KWh)' is likely mislabeled and represents theoretical power in kW.
# If it is energy (KWh) for 10-min intervals, convert by multiplying by 6 to get average power in kW.

# Load the data (using read_csv for CSV files)
data_file = 'Wind_Turbine_Performance_Data_Analyzer\\T1.csv'  # Correct relative path with extension
df = pd.read_csv(data_file)

# Rename columns for ease
df.columns = ['datetime', 'power', 'wind_speed', 'theoretical_power', 'wind_direction']

# Parse datetime
df['datetime'] = pd.to_datetime(df['datetime'], format='%d %m %Y %H:%M')

# Feature 1: Data cleaning & filtering
# Drop rows with missing values
df = df.dropna()

# Remove invalid values (negative power or wind speed)
df = df[(df['power'] >= 0) & (df['wind_speed'] >= 0)]

# Filter unrealistic values (power exceeding theoretical by a large margin, e.g., 10%)
df = df[df['power'] <= df['theoretical_power'] * 1.1]

# Outlier detection using z-score within wind speed bins (threshold = 3)
bins = np.arange(0, df['wind_speed'].max() + 0.5, 0.5)
df['wind_speed_bin'] = pd.cut(df['wind_speed'], bins=bins)

# Function to remove outliers in each bin
def remove_outliers(group):
    if len(group) > 1:
        z_scores = np.abs(stats.zscore(group['power']))
        return group[z_scores < 3]
    return group

df = df.groupby('wind_speed_bin', observed=False).apply(remove_outliers).reset_index(drop=True)

# Engineering data validation: Assume cut-in ~3 m/s, cut-out ~25 m/s (typical values; adjust based on specs)
cut_in = 3.0
cut_out = 25.0
df = df[(df['wind_speed'] >= cut_in) & (df['wind_speed'] <= cut_out)]

print(f"Data after cleaning: {df.shape[0]} rows")

# Calculate available wind power and Cp
rho = 1.225  # kg/m^3
rotor_diameter = 117.0  # meters (assumed; change based on actual turbine specs)
A = np.pi * (rotor_diameter / 2) ** 2  # swept area in m^2

# Available kinetic power in kW (divide by 1000)
df['available_power'] = 0.5 * rho * A * df['wind_speed'] ** 3 / 1000

# Avoid division by zero
df = df[df['available_power'] > 0]

# Measured Cp
df['measured_cp'] = df['power'] / df['available_power']

# Theoretical Cp
df['theoretical_cp'] = df['theoretical_power'] / df['available_power']

# Cap Cp at Betz limit (0.593) for sanity check
df['measured_cp'] = df['measured_cp'].clip(upper=0.593)
df['theoretical_cp'] = df['theoretical_cp'].clip(upper=0.593)

# Feature 2: Calculate power curves (binned averages)
grouped = df.groupby('wind_speed_bin', observed=False)
mean_power = grouped['power'].mean()
std_power = grouped['power'].std()
mean_theoretical = grouped['theoretical_power'].mean()
mean_measured_cp = grouped['measured_cp'].mean()
mean_theoretical_cp = grouped['theoretical_cp'].mean()

# Bin midpoints for plotting
bin_mid = grouped['wind_speed'].mean()

# Feature 3: Compare measured vs. theoretical Cp
# Plot Cp curves
plt.figure(figsize=(12, 6))
plt.plot(bin_mid, mean_measured_cp, label='Measured Cp', color='blue')
plt.plot(bin_mid, mean_theoretical_cp, label='Theoretical Cp', color='red', linestyle='--')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Power Coefficient (Cp)')
plt.title('Measured vs Theoretical Power Coefficient (Cp)')
plt.legend()
plt.grid(True)
plt.savefig('cp_comparison.png')
plt.show()

# Feature 4: Visualization of efficiency losses due to wind speed variability
# Plot power curves with variability (std dev as shading for losses due to variability)
plt.figure(figsize=(12, 6))
plt.plot(bin_mid, mean_power, label='Measured Power Curve', color='blue')
plt.fill_between(bin_mid, mean_power - std_power, mean_power + std_power, color='blue', alpha=0.2, label='Variability (Std Dev)')
plt.plot(bin_mid, mean_theoretical, label='Theoretical Power Curve', color='red', linestyle='--')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Power (kW)')
plt.title('Power Curves with Efficiency Losses due to Wind Speed Variability')
plt.legend()
plt.grid(True)
plt.savefig('power_curves_with_variability.png')
plt.show()

# Additional visualization: Efficiency loss (difference in power)
loss = mean_theoretical - mean_power
plt.figure(figsize=(12, 6))
plt.bar(bin_mid, loss, width=0.4, label='Power Loss (kW)', color='orange')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Average Power Loss (kW)')
plt.title('Average Efficiency Losses per Wind Speed Bin')
plt.legend()
plt.grid(True)
plt.savefig('efficiency_losses.png')
plt.show()

# Summary statistics
print("Summary of Efficiency Losses:")
print(loss.describe())

# Skills Showcased: Python (pandas, matplotlib), engineering data validation, renewable energy performance assessment.
# References: Methods inspired from research papers on SCADA data analysis, such as "Exploratory Analysis of SCADA Data from Wind Turbines Using the K-Means Clustering Algorithm" and "Performance Assessment of a Wind Turbine Using SCADA based Gaussian Process Model".