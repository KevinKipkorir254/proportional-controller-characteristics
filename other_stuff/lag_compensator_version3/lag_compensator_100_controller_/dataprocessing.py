import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the folders (replace these with your actual folder paths)
folders = ['filtered_velocity_1', 'filtered_velocity_2', 'filtered_velocity_3', 'filtered_velocity_4', 'filtered_velocity_5', 'filtered_velocity_6', 'filtered_velocity_7', 'filtered_velocity_8', 'filtered_velocity_9', 'filtered_velocity_10', 'filtered_velocity_11', 'filtered_velocity_12', 'filtered_velocity_13', 'filtered_velocity_14', 'filtered_velocity_15', 'filtered_velocity_16', 'filtered_velocity_17', 'filtered_velocity_18', 'filtered_velocity_19', 'filtered_velocity_20']

# Colors for each folder's data in the plot
colors = ['blue', 'green', 'red', 'purple', 'yellow', 'orange', 'pink', 'brown', 'black', 'turquoise', 'gray', 'cyan', 'magenta', 'lime', 'indigo', 'violet', 'teal', 'gold', 'silver', 'maroon']
labels = ['filtered_velocity_1', 'filtered_velocity_2', 'filtered_velocity_3', 'filtered_velocity_4', 'filtered_velocity_5', 'filtered_velocity_6', 'filtered_velocity_7', 'filtered_velocity_8', 'filtered_velocity_9', 'filtered_velocity_10', 'filtered_velocity_11', 'filtered_velocity_12', 'filtered_velocity_13', 'filtered_velocity_14', 'filtered_velocity_15', 'filtered_velocity_16', 'filtered_velocity_17', 'filtered_velocity_18', 'filtered_velocity_19', 'filtered_velocity_20']

# Initialize a figure for plotting
plt.figure(figsize=(10, 6))

# Process each folder
for folder, color, label in zip(folders, colors, labels):
    # Define the path to the CSV file
    csv_path = os.path.join(folder, 'step_response_data.csv')
    
    # Check if the file exists
    if not os.path.exists(csv_path):
        print(f"File {csv_path} not found. Skipping...")
        continue
    
    # Read the CSV file
    data = pd.read_csv(csv_path)
    
    # Rename columns for clarity (based on the image format)
    data.columns = ['Time', 'Output']
    
    # Step 1: Extract the first 4 seconds
    data_4sec = data[data['Time'] <= 4.0]
    
    # Step 2: Filter out negative values in the Output column
    data_filtered = data_4sec[data_4sec['Output'] >= 0]
    
    # Step 3: Subsample by taking every 2nd row
    data_subsampled = data_filtered - data_filtered.iloc[0]
    
    # Step 4: remove data points with negative values
    data_subsampled = data_subsampled[data_subsampled['Output'] >= 0]
    
    #step 5: set up the first sample to have time 0 by subtracting all the data points with th time of the first
    data_subsampled['Time'] = data_subsampled['Time'] - data_subsampled['Time'].iloc[0]
  
    # Step 4: Save the processed data to a new file in the same folder
    output_path = os.path.join(folder, 'processed_step_response_data.csv')
    data_subsampled.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")
    
    # Step 5: Plot the data
    plt.plot(data_subsampled['Time'], data_subsampled['Output'], 
             color=color, label=label, marker='o', markersize=3)

# Customize the plot
plt.title('Step Response Data (First 4 Seconds, Subsampled, Non-Negative)')
plt.xlabel('Time (s)')
plt.ylabel('Output')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
#plt.savefig("Time_series_data")