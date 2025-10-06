import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# Find the latest log file
log_files = glob.glob('PPO_logs/RocketLanding_UnevenTerrain/*.csv')
if not log_files:
    print("No log files found!")
    exit(1)

# Use the most recent log file
log_file = max(log_files, key=os.path.getctime)
print(f"Reading log file: {log_file}")

# Read the training log
df = pd.read_csv(log_file)

print(f"Total data points: {len(df)}")
print(f"Max timestep: {df['timestep'].max()}")
print(f"Max episode: {df['episode'].max()}")
print(f"Current reward range: {df['reward'].min():.2f} to {df['reward'].max():.2f}")
print("\nLast 5 entries:")
print(df.tail())

# Create the plot
plt.figure(figsize=(12, 6))

# Plot rewards vs timesteps
plt.subplot(1, 2, 1)
plt.plot(df['timestep'], df['reward'], alpha=0.3, color='blue', label='Raw Reward')

# Calculate moving average
window = 20
if len(df) >= window:
    moving_avg = df['reward'].rolling(window=window).mean()
    plt.plot(df['timestep'], moving_avg, color='red', linewidth=2, label=f'Moving Avg ({window} episodes)')

plt.xlabel('Timesteps')
plt.ylabel('Reward')
plt.title('Uneven Terrain Training: Reward vs Timesteps')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot rewards vs episodes
plt.subplot(1, 2, 2)
plt.plot(df['episode'], df['reward'], alpha=0.3, color='green', label='Raw Reward')

if len(df) >= window:
    moving_avg = df['reward'].rolling(window=window).mean()
    plt.plot(df['episode'], moving_avg, color='orange', linewidth=2, label=f'Moving Avg ({window} episodes)')

plt.xlabel('Episodes')
plt.ylabel('Reward')
plt.title('Uneven Terrain Training: Reward vs Episodes')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()

# Save the graph
output_path = 'training_graphs/uneven_terrain_current_progress.png'
os.makedirs('training_graphs', exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\n✅ Graph saved to: {output_path}")

plt.show()
