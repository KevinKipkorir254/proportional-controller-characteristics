import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Define the folders (replace these with your actual folder paths)
folders = ['filtered_velocity_1', 'filtered_velocity_2', 'filtered_velocity_3', 'filtered_velocity_4']

# Colors and labels for each folder's data in the plot
colors = ['blue', 'green', 'red', 'purple']
labels = ['filtered_velocity_1', 'filtered_velocity_2', 'filtered_velocity_3', 'filtered_velocity_4']

# Initialize a figure for plotting
plt.figure(figsize=(10, 6))

# Dictionary to store metrics for the table
metrics = {
    'System': [],
    'Rise Time (s)': [],
    'Rise Time start (s)': [],
    'Rise Time end (s)': [],
    'Threshhold 10 %': [],
    'Threshhold 90 %': [],
    'Settling Time (s)': [],
    'Overshoot (%)': [],
    'Steady-State Value': [],
    'Undamped Natural Freq (rad/s)': [],
    'Damping Ratio': []
}

# Process each folder's processed data
for folder, color, label in zip(folders, colors, labels):
    # Define the path to the processed CSV file
    csv_path = os.path.join(folder, 'processed_step_response_data.csv')
    
    # Check if the file exists
    if not os.path.exists(csv_path):
        print(f"File {csv_path} not found. Skipping...")
        continue
    
    # Read the processed CSV file
    data = pd.read_csv(csv_path)
    
    # Ensure columns are named correctly
    data.columns = ['Time', 'Output']
    
    # Step 1: Plot the data
    plt.plot(data['Time'], data['Output'], 
             color=color, label=label, marker='o', markersize=3)
    
    # Step 2: Calculate step response metrics
    output = data['Output']
    time = data['Time']
    
    # Estimate steady-state value (average of last 10% of data points)
    steady_state_value = output.iloc[-int(len(output) * 0.1):].mean()
    
    # Rise Time (10% to 90% of steady-state value)
    threshold_10 = 0.1 * steady_state_value
    threshold_90 = 0.9 * steady_state_value
    rise_time_start = time[output >= threshold_10].iloc[0] if any(output >= threshold_10) else np.nan
    rise_time_end = time[output >= threshold_90].iloc[0] if any(output >= threshold_90) else np.nan
    rise_time = rise_time_end - rise_time_start if not np.isnan(rise_time_end) and not np.isnan(rise_time_start) else np.nan
    
    # Settling Time (within 2% of steady-state value)
    settling_threshold = 0.02 * steady_state_value
    within_settling = (output >= steady_state_value - settling_threshold) & (output <= steady_state_value + settling_threshold)
    settling_time = time[within_settling].iloc[0] if any(within_settling) else np.nan
    
    # Overshoot (as a percentage of steady-state value)
    max_value = output.max()
    overshoot = ((max_value - steady_state_value) / steady_state_value) * 100 if steady_state_value != 0 else np.nan
    
    # Step 3: Calculate Undamped Natural Frequency and Damping Ratio
    # Damping Ratio (from overshoot)
    if not np.isnan(overshoot) and overshoot > 0:
        # Overshoot (%) = exp(-ζπ / sqrt(1-ζ^2)) * 100
        zeta = np.log(overshoot / 100) / np.sqrt(np.pi**2 + (np.log(overshoot / 100))**2)
        zeta = -zeta  # Since log(overshoot/100) is negative
    else:
        zeta = np.nan  # If no overshoot, damping ratio cannot be determined this way
    
    # Undamped Natural Frequency (from the period of oscillation)
    # Find peaks to estimate the period of oscillation
    peaks = []
    for i in range(1, len(output) - 1):
        if output.iloc[i] > output.iloc[i-1] and output.iloc[i] > output.iloc[i+1]:
            peaks.append((time.iloc[i], output.iloc[i]))
    
    omega_n = np.nan  # Default value if we can't compute it
    if len(peaks) >= 2:  # Need at least two peaks to estimate the period
        # Calculate the period as the time difference between consecutive peaks
        periods = [peaks[i+1][0] - peaks[i][0] for i in range(len(peaks)-1)]
        period = np.mean(periods)  # Average period
        # Damped frequency: ω_d = 2π / T
        omega_d = 2 * np.pi / period
        # Undamped natural frequency: ω_n = ω_d / sqrt(1 - ζ^2)
        if not np.isnan(zeta) and zeta < 1:
            omega_n = omega_d / np.sqrt(1 - zeta**2)
    
    # Store metrics for the table
    metrics['System'].append(label)
    metrics['Rise Time (s)'].append(rise_time)
    metrics['Rise Time start (s)'].append(rise_time_start)
    metrics['Rise Time end (s)'].append(rise_time_end)
    metrics['Threshhold 10 %'].append(threshold_10)
    metrics['Threshhold 90 %'].append(threshold_90)
    metrics['Settling Time (s)'].append(settling_time)
    metrics['Overshoot (%)'].append(overshoot)
    metrics['Steady-State Value'].append(steady_state_value)
    metrics['Undamped Natural Freq (rad/s)'].append(omega_n)
    metrics['Damping Ratio'].append(zeta)

# Customize and display the plot
plt.title('Processed Step Response Data (Transient Analysis)')
plt.xlabel('Time (s)')
plt.ylabel('Output')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Create and display the comparison table
metrics_df = pd.DataFrame(metrics)
# Round the values for better readability
metrics_df = metrics_df.round(3)
print("\nStep Response Metrics Comparison Table:")
print(metrics_df)

# Optionally, save the table to a CSV file
metrics_df.to_csv('transient_metrics.csv', index=False)
print("\nMetrics table saved to 'transient_metrics.csv'")