"""
Generate comparison graphs for SAC Plain vs Uneven Surface
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

def plot_sac_comparison():
    # Read both logs
    df_plain = pd.read_csv('../plain_sac/SAC_logs/training_log.csv')
    df_uneven = pd.read_csv('SAC_logs_uneven/training_log.csv')
    
    # Plain surface data
    timesteps_plain = df_plain['timestep'].values
    episodes_plain = df_plain['episode'].values
    rewards_plain = df_plain['reward'].values
    
    # Uneven surface data
    timesteps_uneven = df_uneven['timestep'].values
    episodes_uneven = df_uneven['episode'].values
    rewards_uneven = df_uneven['reward'].values
    
    # Calculate moving averages
    window = 50
    ma_rewards_plain = moving_average(rewards_plain, window)
    ma_timesteps_plain = timesteps_plain[window-1:] if len(rewards_plain) >= window else timesteps_plain
    
    ma_rewards_uneven = moving_average(rewards_uneven, window)
    ma_timesteps_uneven = timesteps_uneven[window-1:] if len(rewards_uneven) >= window else timesteps_uneven
    
    # Create output directory
    os.makedirs('training_graphs', exist_ok=True)
    
    # Calculate statistics
    stats_plain = {
        'episodes': int(episodes_plain[-1]),
        'timesteps': int(timesteps_plain[-1]),
        'peak_reward': np.max(rewards_plain),
        'peak_ma': np.max(ma_rewards_plain),
        'final_avg': np.mean(rewards_plain[-100:]) if len(rewards_plain) >= 100 else np.mean(rewards_plain)
    }
    
    stats_uneven = {
        'episodes': int(episodes_uneven[-1]),
        'timesteps': int(timesteps_uneven[-1]),
        'peak_reward': np.max(rewards_uneven),
        'peak_ma': np.max(ma_rewards_uneven),
        'final_avg': np.mean(rewards_uneven[-100:]) if len(rewards_uneven) >= 100 else np.mean(rewards_uneven)
    }
    
    print("="*70)
    print("SAC COMPARISON - Plain vs Uneven Surface")
    print("="*70)
    print(f"{'Metric':<30} {'Plain':<20} {'Uneven':<20}")
    print("-"*70)
    print(f"{'Total Episodes':<30} {stats_plain['episodes']:<20} {stats_uneven['episodes']:<20}")
    print(f"{'Total Timesteps':<30} {stats_plain['timesteps']:,<20} {stats_uneven['timesteps']:,<20}")
    print(f"{'Peak Episode Reward':<30} {stats_plain['peak_reward']:<20.2f} {stats_uneven['peak_reward']:<20.2f}")
    print(f"{'Peak 50-Episode MA':<30} {stats_plain['peak_ma']:<20.2f} {stats_uneven['peak_ma']:<20.2f}")
    print(f"{'Final 100-Episode Avg':<30} {stats_plain['final_avg']:<20.2f} {stats_uneven['final_avg']:<20.2f}")
    print("="*70)
    
    # Create comparison plot - Moving Averages
    fig, ax = plt.subplots(figsize=(16, 9))
    
    # Plot both moving averages
    ax.plot(ma_timesteps_plain/1000, ma_rewards_plain, color='darkblue', linewidth=3, 
            label=f'Plain Surface (Peak MA: {stats_plain["peak_ma"]:.1f})', marker='o', 
            markevery=max(len(ma_rewards_plain)//20, 1), markersize=4)
    
    ax.plot(ma_timesteps_uneven/1000, ma_rewards_uneven, color='darkgreen', linewidth=3, 
            label=f'Uneven Surface (Peak MA: {stats_uneven["peak_ma"]:.1f})', marker='s', 
            markevery=max(len(ma_rewards_uneven)//20, 1), markersize=4)
    
    # Add reference lines
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.6, linewidth=2, label='Zero Reward')
    ax.axhline(y=stats_plain['peak_ma'], color='blue', linestyle=':', alpha=0.5, linewidth=1.5)
    ax.axhline(y=stats_uneven['peak_ma'], color='green', linestyle=':', alpha=0.5, linewidth=1.5)
    
    # Add shaded regions for positive rewards
    ax.fill_between(ma_timesteps_plain/1000, 0, ma_rewards_plain, where=(ma_rewards_plain > 0), 
                     alpha=0.1, color='blue')
    ax.fill_between(ma_timesteps_uneven/1000, 0, ma_rewards_uneven, where=(ma_rewards_uneven > 0), 
                     alpha=0.1, color='green')
    
    ax.set_xlabel('Timesteps (×1000)', fontsize=14, fontweight='bold')
    ax.set_ylabel('50-Episode Moving Average Reward', fontsize=14, fontweight='bold')
    ax.set_title('SAC Training Comparison: Plain vs Uneven Surface\nContinuous Action Space Performance (~300K Timesteps)', 
                 fontsize=17, fontweight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=13, framealpha=0.95, shadow=True)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.tick_params(labelsize=12)
    
    # Add text box with comparison
    comparison_text = f"""SAC Performance Comparison:
    
Plain Surface:
  • Episodes: {stats_plain['episodes']}
  • Timesteps: {stats_plain['timesteps']:,}
  • Peak MA: {stats_plain['peak_ma']:.1f}
  
Uneven Surface:
  • Episodes: {stats_uneven['episodes']}
  • Timesteps: {stats_uneven['timesteps']:,}
  • Peak MA: {stats_uneven['peak_ma']:.1f}"""
    
    ax.text(0.02, 0.98, comparison_text, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top', horizontalalignment='left',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, edgecolor='black', linewidth=1.5),
            family='monospace')
    
    plt.tight_layout()
    plt.savefig('training_graphs/sac_comparison_300dpi.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: training_graphs/sac_comparison_300dpi.png")
    
    plt.savefig('training_graphs/sac_comparison_600dpi.png', dpi=600, bbox_inches='tight')
    print(f"✓ Saved: training_graphs/sac_comparison_600dpi.png")
    
    plt.close()
    
    # Create side-by-side comparison with raw data
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    
    # Plain surface
    ax1.plot(timesteps_plain/1000, rewards_plain, alpha=0.3, color='steelblue', linewidth=0.8)
    ax1.plot(ma_timesteps_plain/1000, ma_rewards_plain, color='darkblue', linewidth=3, 
             label=f'{window}-Episode MA')
    ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
    ax1.axhline(y=stats_plain['peak_ma'], color='green', linestyle=':', alpha=0.7, linewidth=2)
    ax1.set_xlabel('Timesteps (×1000)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Reward', fontsize=12, fontweight='bold')
    ax1.set_title(f'Plain Surface\nPeak MA: {stats_plain["peak_ma"]:.1f}', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Uneven surface
    ax2.plot(timesteps_uneven/1000, rewards_uneven, alpha=0.3, color='mediumseagreen', linewidth=0.8)
    ax2.plot(ma_timesteps_uneven/1000, ma_rewards_uneven, color='darkgreen', linewidth=3, 
             label=f'{window}-Episode MA')
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
    ax2.axhline(y=stats_uneven['peak_ma'], color='blue', linestyle=':', alpha=0.7, linewidth=2)
    ax2.set_xlabel('Timesteps (×1000)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Reward', fontsize=12, fontweight='bold')
    ax2.set_title(f'Uneven Surface\nPeak MA: {stats_uneven["peak_ma"]:.1f}', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle('SAC Training: Plain vs Uneven Surface (Side-by-Side)', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig('training_graphs/sac_sidebyside_300dpi.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: training_graphs/sac_sidebyside_300dpi.png")
    
    plt.savefig('training_graphs/sac_sidebyside_600dpi.png', dpi=600, bbox_inches='tight')
    print(f"✓ Saved: training_graphs/sac_sidebyside_600dpi.png")
    
    plt.close()
    
    print("\n✓ All SAC comparison graphs generated successfully!")

if __name__ == "__main__":
    plot_sac_comparison()
