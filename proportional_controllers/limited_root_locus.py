import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Function to calculate poles from natural frequency and damping ratio
def calculate_poles(wn, zeta):
    real_part = -zeta * wn
    imag_part = wn * np.sqrt(1 - zeta**2) if zeta < 1 else 0
    return complex(real_part, imag_part), complex(real_part, -imag_part)

# Manually enter folder paths where 'transient_metrics.csv' is located
folder_paths = [
    r"C:\Users\HP\Desktop\filtered_velocity\proportional_controllers\P_100_controller",
    r"C:\Users\HP\Desktop\filtered_velocity\proportional_controllers\P_120_controller_",
    r"C:\Users\HP\Desktop\filtered_velocity\proportional_controllers\P_140_controller_",
    r"C:\Users\HP\Desktop\filtered_velocity\proportional_controllers\P_160_controller_",
    r"C:\Users\HP\Desktop\filtered_velocity\proportional_controllers\P_180_controller_",
    r"C:\Users\HP\Desktop\filtered_velocity\proportional_controllers\P_200_controller_"
]  # Replace with actual paths

# Define colors for each dataset
colors = ["red", "blue", "green", "purple", "orange", "black"]

# Process each file named 'transient_metrics.csv' in specified folders
data_frames = []
poles = []
pole_colors = []
labels = []
for i, folder in enumerate(folder_paths):
    file_path = os.path.join(folder, "transient_metrics.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df["Poles"] = df.apply(lambda row: calculate_poles(row["Undamped Natural Freq (rad/s)"], row["Damping Ratio"]), axis=1)
        data_frames.append(df)
        for p in df["Poles"]:
            poles.extend(p)
            pole_colors.extend([colors[i % len(colors)]] * 2)  # Assign color to each pole
            labels.extend([folder] * 2)  # Store folder label for legend

# Concatenate all results into one DataFrame
final_data = pd.concat(data_frames, ignore_index=True)

# Save to a new CSV file
output_file = "poles_output.csv"
final_data.to_csv(output_file, index=False)

# Plot the poles on a limited root locus
plt.figure(figsize=(10, 6))
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, linestyle='--', linewidth=0.5)

# Plot each dataset with its assigned color and label
unique_labels = list(set(labels))
for label, color in zip(unique_labels, colors[:len(unique_labels)]):
    indices = [i for i, lbl in enumerate(labels) if lbl == label]
    #plt.scatter([real_parts[i] for i in indices], [imag_parts[i] for i in indices], c=color, label=label)
    plt.scatter([poles[i].real for i in indices], [poles[i].imag for i in indices], c=color, label=label)

plt.xlabel("Real Axis")
plt.ylabel("Imaginary Axis")
plt.title("Limited Root Locus")
plt.legend()
plt.show()
plt.savefig("limited root locus")

# Print the first few rows to verify output
#print(final_data.head())
