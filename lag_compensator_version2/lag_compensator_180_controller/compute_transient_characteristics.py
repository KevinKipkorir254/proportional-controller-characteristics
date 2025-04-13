import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import os

# Define the folders (replace these with your actual folder paths)
folders = [ 'filtered_velocity_2', 'filtered_velocity_3', 'filtered_velocity_4', 'filtered_velocity_5', 'filtered_velocity_6', 'filtered_velocity_7', 'filtered_velocity_8', 'filtered_velocity_9', 'filtered_velocity_10', 'filtered_velocity_11', 'filtered_velocity_12', 'filtered_velocity_13', 'filtered_velocity_14', 'filtered_velocity_15', 'filtered_velocity_16', 'filtered_velocity_17', 'filtered_velocity_18', 'filtered_velocity_19', 'filtered_velocity_20']

# Colors and labels for each folder's data in the plot
colors = ['green', 'red', 'purple', 'yellow', 'orange', 'pink', 'brown', 'black', 'turquoise', 'gray', 'cyan', 'magenta', 'lime', 'indigo', 'violet', 'teal', 'gold', 'silver', 'maroon']
labels = [ 'filtered_velocity_2', 'filtered_velocity_3', 'filtered_velocity_4', 'filtered_velocity_5', 'filtered_velocity_6', 'filtered_velocity_7', 'filtered_velocity_8', 'filtered_velocity_9', 'filtered_velocity_10', 'filtered_velocity_11', 'filtered_velocity_12', 'filtered_velocity_13', 'filtered_velocity_14', 'filtered_velocity_15', 'filtered_velocity_16', 'filtered_velocity_17', 'filtered_velocity_18', 'filtered_velocity_19', 'filtered_velocity_20']

# Initialize a figure for plotting
plt.figure(figsize=(10, 6))

# Dictionary to store metrics for the table
metrics = {
    'System': [],
    'Rise Time (s)': [],
    #'Rise Time start (s)': [],
    #'Rise Time end (s)': [],
    #'Threshhold 10 %': [],
    #'Threshhold 90 %': [],
    'Settling Time (s)': [],
    'Overshoot (%)': [],
    'Steady-State Value': [],
    'Undamped Natural Freq (rad/s)': [],
    'Damping Ratio': [],
    #'damping ration log': [],
}


def estimate_damping_log_dec(y, t):
    """
    Estimate damping ratio using logarithmic decrement method.
    
    :param y: System response (time-series data)
    :param t: Corresponding time values
    :return: Estimated damping ratio ζ
    """
    peaks, _ = find_peaks(y)  # Find peak indices
    
    if len(peaks) < 2:
        raise ValueError("At least two peaks are needed.")

    # Peak values
    A1, A2 = y[peaks[0]], y[peaks[1]]
    
    # Logarithmic decrement
    delta = np.log(A1 / A2)
    
    # Damping ratio formula
    zeta = 1 / np.sqrt(1 + (2 * np.pi / delta) ** 2)
    
    return zeta


def compute_settling_time(time, output, steady_state_value, threshold=0.05):
    settling_threshold = threshold * steady_state_value
    within_settling = (output >= steady_state_value - settling_threshold) & (output <= steady_state_value + settling_threshold)

    # Find the first index where the output enters the threshold
    indices = np.where(within_settling)[0]

    if len(indices) == 0:
        return np.nan  # Never enters the threshold

    for i in range(len(indices)):
        if np.all(within_settling[indices[i]:]):  # Check if it stays within afterward
            return time.iloc[indices[i]]

    return np.nan  # No valid settling time found


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
    #rise_time_start = time[output >= threshold_10].iloc[0] if any(output >= threshold_10) else np.nan
    #rise_time_end = time[output >= threshold_90].iloc[0] if any(output >= threshold_90) else np.nan
    rise_time_start = np.interp(threshold_10, output, time)  # Interpolated time for 10%
    rise_time_end = np.interp(threshold_90, output, time)  # Interpolated time for 90%
    rise_time = rise_time_end - rise_time_start if not np.isnan(rise_time_end) and not np.isnan(rise_time_start) else np.nan
    
    # Settling Time (within 5% of steady-state value)
    #settling_threshold = 0.05 * steady_state_value
    #within_settling = (output >= steady_state_value - settling_threshold) & (output <= steady_state_value + settling_threshold)
    #settling_time = time[within_settling].iloc[0] if any(within_settling) else np.nan
    settling_time = compute_settling_time( time, output,steady_state_value)
    #print(settling_threshold)
    
    # Overshoot (as a percentage of steady-state value)
    max_value = output.max()
    overshoot = ((max_value - steady_state_value) / steady_state_value) * 100 if steady_state_value != 0 else np.nan
    
    # Step 3: Calculate Undamped Natural Frequency and Damping Ratio
    # Damping Ratio (from overshoot)
    if not np.isnan(overshoot) and overshoot > 0:
        zeta = estimate_damping_log_dec( output, time) 
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
    metrics['Settling Time (s)'].append(settling_time)
    metrics['Overshoot (%)'].append(overshoot)
    metrics['Steady-State Value'].append(steady_state_value)
    metrics['Undamped Natural Freq (rad/s)'].append(omega_n)
    metrics['Damping Ratio'].append(zeta) #'damping ration low'
    #metrics['damping ration log'].append(zeta_log)
    

# Customize and display the plot
plt.title('Processed Step Response Data (Transient Analysis)')
plt.xlabel('Time (s)')
plt.ylabel('Output')
plt.grid(True)
#plt.legend()
plt.tight_layout()
plt.savefig('Time_series_data.png', dpi=200, bbox_inches='tight')

# Create and display the comparison table
metrics_df = pd.DataFrame(metrics)
# Round the values for better readability
metrics_df = metrics_df.round(3)
print("\nStep Response Metrics Comparison Table:")
print(metrics_df)

# Optionally, save the table to a CSV file
metrics_df.to_csv('transient_metrics.csv', index=False)
print("\nMetrics table saved to 'transient_metrics.csv'")