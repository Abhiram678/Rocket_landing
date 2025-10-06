"""
Generate publication-quality graphs for SAC Plain Surface training
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def moving_average(data, window_size=50):
    """Calculate moving average"""
    if len(data) < window_size:
        return data
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def plot_sac_plain():
    # Read training log
    log_file = 'SAC_logs/training_log.csv'
    df = pd.read_csv(log_file)
    
    timesteps = df['timestep'].values
    episodes = df['episode'].values
    rewards = df['reward'].values
    
    # Calculate moving average
    window = 50
    if len(rewards) >= window:
        ma_rewards = moving_average(rewards, window)
        ma_episodes = episodes[window-1:]
        ma_timesteps = timesteps[window-1:]
    else:
        ma_rewards = rewards
        ma_episodes = episodes
        ma_timesteps = timesteps
    
    # Create output directory
    os.makedirs('training_graphs', exist_ok=True)
    
    # Calculate statistics
    max_reward = np.max(rewards)
    max_ma_reward = np.max(ma_rewards) if len(ma_rewards) > 0 else 0
    final_avg = np.mean(rewards[-100:]) if len(rewards) >= 100 else np.mean(rewards)
    total_episodes = int(episodes[-1])
    total_timesteps = int(timesteps[-1])
    
    print("="*60)
    print("SAC PLAIN SURFACE - Training Statistics")
    print("="*60)
    print(f"Total Episodes: {total_episodes}")
    print(f"Total Timesteps: {total_timesteps:,}")
    print(f"Peak Episode Reward: {max_reward:.2f}")
    print(f"Peak 50-Episode MA: {max_ma_reward:.2f}")
    print(f"Final 100-Episode Average: {final_avg:.2f}")
    print("="*60)
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Reward vs Episodes
    ax1.plot(episodes, rewards, alpha=0.3, color='steelblue', linewidth=0.8, label='Episode Reward')
    if len(ma_rewards) > 0:
        ax1.plot(ma_episodes, ma_rewards, color='darkblue', linewidth=2.5, label=f'{window}-Episode Moving Average')
    ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1.5, label='Zero Line')
    ax1.axhline(y=max_ma_reward, color='green', linestyle=':', alpha=0.7, linewidth=1.5, 
                label=f'Peak MA: {max_ma_reward:.1f}')
    
    ax1.set_xlabel('Episode', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Reward', fontsize=13, fontweight='bold')
    ax1.set_title('SAC Training - Plain Surface (Reward vs Episodes)', fontsize=15, fontweight='bold', pad=15)
    ax1.legend(loc='lower right', fontsize=10, framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(labelsize=11)
    
    # Plot 2: Reward vs Timesteps
    ax2.plot(timesteps, rewards, alpha=0.3, color='coral', linewidth=0.8, label='Episode Reward')
    if len(ma_rewards) > 0:
        ax2.plot(ma_timesteps, ma_rewards, color='darkred', linewidth=2.5, label=f'{window}-Episode Moving Average')
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1.5, label='Zero Line')
    ax2.axhline(y=max_ma_reward, color='green', linestyle=':', alpha=0.7, linewidth=1.5,
                label=f'Peak MA: {max_ma_reward:.1f}')
    
    # Add timestep markers
    for ts in [50000, 100000, 150000, 200000, 250000, 287000]:
        if ts <= total_timesteps:
            ax2.axvline(x=ts, color='gray', linestyle=':', alpha=0.4, linewidth=1)
    
    ax2.set_xlabel('Timesteps', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Reward', fontsize=13, fontweight='bold')
    ax2.set_title('SAC Training - Plain Surface (Reward vs Timesteps)', fontsize=15, fontweight='bold', pad=15)
    ax2.legend(loc='lower right', fontsize=10, framealpha=0.9)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.tick_params(labelsize=11)
    
    # Format x-axis for timesteps
    ax2.ticklabel_format(axis='x', style='plain')
    
    plt.tight_layout()
    
    # Save at different DPIs
    plt.savefig('training_graphs/sac_plain_training_300dpi.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: training_graphs/sac_plain_training_300dpi.png")
    
    plt.savefig('training_graphs/sac_plain_training_600dpi.png', dpi=600, bbox_inches='tight')
    print(f"✓ Saved: training_graphs/sac_plain_training_600dpi.png")
    
    plt.close()
    
    # Create single consolidated graph
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.plot(timesteps/1000, rewards, alpha=0.3, color='steelblue', linewidth=0.8, label='Episode Reward')
    if len(ma_rewards) > 0:
        ax.plot(ma_timesteps/1000, ma_rewards, color='darkblue', linewidth=3, label=f'{window}-Episode Moving Average')
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1.5, label='Zero Reward')
    ax.axhline(y=max_ma_reward, color='green', linestyle=':', alpha=0.7, linewidth=2,
               label=f'Peak Performance: {max_ma_reward:.1f}')
    
    # Add annotations
    ax.text(0.98, 0.05, f'Total Episodes: {total_episodes}\nTotal Timesteps: {total_timesteps:,}\nPeak Reward: {max_reward:.1f}\nFinal Avg (100ep): {final_avg:.1f}',
            transform=ax.transAxes, fontsize=11, verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    ax.set_xlabel('Timesteps (×1000)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Episode Reward', fontsize=14, fontweight='bold')
    ax.set_title('SAC Training Performance - Plain Surface\nContinuous Action Space (300K Timesteps)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=12, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.tick_params(labelsize=12)
    
    plt.tight_layout()
    plt.savefig('training_graphs/sac_plain_consolidated_300dpi.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: training_graphs/sac_plain_consolidated_300dpi.png")
    
    plt.savefig('training_graphs/sac_plain_consolidated_600dpi.png', dpi=600, bbox_inches='tight')
    print(f"✓ Saved: training_graphs/sac_plain_consolidated_600dpi.png")
    
    plt.close()
    
    print("\n✓ All SAC plain surface graphs generated successfully!")
    
    return {
        'total_episodes': total_episodes,
        'total_timesteps': total_timesteps,
        'peak_reward': max_reward,
        'peak_ma': max_ma_reward,
        'final_avg': final_avg
    }

if __name__ == "__main__":
    stats = plot_sac_plain()
