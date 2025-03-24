import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file (replace 'your_file.csv' with the actual file path)
df = pd.read_csv('transient_metrics.csv')

# Drop the 'System' column since it's just labels
df_numeric = df.drop(columns=['System'])

# Set up the plot grid
plt.figure(figsize=(15, 10))
for i, column in enumerate(df_numeric.columns, 1):
    plt.subplot(3, 2, i)  # 3 rows, 2 columns
    sns.histplot(df_numeric[column], kde=True, bins=10, color='skyblue', stat='density')
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Density')

# Adjust layout and display
plt.tight_layout()
plt.show()