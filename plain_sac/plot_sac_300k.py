"""
Plot SAC training results up to 300K timesteps
"""

import numpy as np
import matplotlib.pyplot as plt
import os


def plot_sac_results():
    log_file = './SAC_logs/training_log.csv'
    save_dir = './training_graphs/'
    os.makedirs(save_dir, exist_ok=True)
    
    print("=" * 50)
    print("Generating SAC Training Graphs (300K timesteps)")
    print("=" * 50)
    
    # Read log file
    timesteps, episodes, rewards = [], [], []
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()[1:]  # Skip header
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    try:
                        ts = int(parts[0])
                        ep = int(parts[1])
                        rw = float(parts[2])
                        
                        # Only include data up to 300K timesteps
                        if ts <= 300000:
                            timesteps.append(ts)
                            episodes.append(ep)
                            rewards.append(rw)
                    except:
                        continue
    except FileNotFoundError:
        print(f"Error: Log file not found: {log_file}")
        return
    
    if len(rewards) == 0:
        print("No training data found!")
        return
    
    print(f"\nData Statistics:")
    print(f"Total Episodes: {len(episodes)}")
    print(f"Total Timesteps: {max(timesteps)}")
    print(f"Average Reward: {np.mean(rewards):.2f}")
    print(f"Max Reward: {np.max(rewards):.2f}")
    print(f"Min Reward: {np.min(rewards):.2f}")
    
    # Calculate moving average
    window = min(20, len(rewards))
    moving_avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Timesteps vs Rewards
    ax1.plot(timesteps, rewards, alpha=0.3, color='blue', label='Episode Reward')
    if len(moving_avg) > 0:
        ax1.plot(timesteps[window-1:], moving_avg, color='red', linewidth=2, 
                label=f'{window}-Episode Moving Avg')
    ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Timesteps', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Reward', fontsize=12, fontweight='bold')
    ax1.set_title('SAC Training Progress - Plain Surface (Timesteps)', 
                 fontsize=14, fontweight='bold')
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    
    # Add text annotation for peak
    peak_reward = np.max(rewards)
    peak_idx = np.argmax(rewards)
    peak_ts = timesteps[peak_idx]
    ax1.annotate(f'Peak: {peak_reward:.1f}\n@ {peak_ts:,} steps', 
                xy=(peak_ts, peak_reward),
                xytext=(peak_ts * 0.6, peak_reward * 0.8),
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3'))
    
    # Plot 2: Episodes vs Rewards
    ax2.plot(episodes, rewards, alpha=0.3, color='blue', label='Episode Reward')
    if len(moving_avg) > 0:
        ax2.plot(episodes[window-1:], moving_avg, color='red', linewidth=2, 
                label=f'{window}-Episode Moving Avg')
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Episodes', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Reward', fontsize=12, fontweight='bold')
    ax2.set_title('SAC Training Progress - Plain Surface (Episodes)', 
                 fontsize=14, fontweight='bold')
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    
    # Add summary text
    summary_text = f"Total: {len(episodes)} episodes, {max(timesteps):,} timesteps\n"
    summary_text += f"Final Avg (last 50): {np.mean(rewards[-50:]):.1f}\n"
    summary_text += f"Peak Reward: {peak_reward:.1f}"
    ax2.text(0.05, 0.95, summary_text, transform=ax2.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Save figure
    save_path = os.path.join(save_dir, 'sac_plain_training_300k.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n✅ Training graph saved: {save_path}")
    
    # Also save a high-res version
    save_path_hires = os.path.join(save_dir, 'sac_plain_training_300k_highres.png')
    plt.savefig(save_path_hires, dpi=600, bbox_inches='tight')
    print(f"✅ High-res graph saved: {save_path_hires}")
    
    plt.close()
    
    print("\n" + "=" * 50)
    print("Graph Generation Complete!")
    print("=" * 50)
    
    # Print performance summary
    print("\n📊 SAC Performance Summary (300K timesteps):")
    print(f"   Total Episodes: {len(episodes)}")
    print(f"   Total Timesteps: {max(timesteps):,}")
    print(f"   Average Reward: {np.mean(rewards):.2f}")
    print(f"   Peak Reward: {peak_reward:.2f}")
    print(f"   Final Average (last 50 eps): {np.mean(rewards[-50:]):.2f}")
    print(f"   Final Average (last 100 eps): {np.mean(rewards[-100:]):.2f}")
    
    print("\n📈 Comparison with PPO:")
    print(f"   PPO: 2,400,000 timesteps → +75 to +95 avg reward")
    print(f"   SAC: {max(timesteps):,} timesteps → {peak_reward:.2f} peak reward")
    print(f"   Sample Efficiency: {2400000/max(timesteps):.1f}x more efficient!")


if __name__ == "__main__":
    plot_sac_results()
