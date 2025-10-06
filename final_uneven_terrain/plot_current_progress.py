import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the training log
df = pd.read_csv('PPO_logs/RocketLanding/PPO_RocketLanding_log_0.csv')

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
plt.title('Training Progress: Reward vs Timesteps')
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
plt.title('Training Progress: Reward vs Episodes')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()

# Save the graph
output_path = 'training_graphs/current_training_progress.png'
import os
os.makedirs('training_graphs', exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\nGraph saved to: {output_path}")

plt.show()
