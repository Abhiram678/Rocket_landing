"""
Generate PREMIUM comparison graphs for SAC Plain vs Uneven Surface
Enhanced color schemes and professional formatting
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

def plot_premium_comparison():
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
    print("PREMIUM SAC COMPARISON - Plain vs Uneven Surface")
    print("="*70)
    
    # Set style for better visuals
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # ==================== GRAPH 1: Elegant Comparison ====================
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    # Define premium color palette
    color_plain = '#2E86AB'      # Ocean blue
    color_uneven = '#A23B72'     # Magenta/purple
    color_plain_fill = '#87CEEB' # Sky blue
    color_uneven_fill = '#DDA0DD' # Plum
    
    # Plot both moving averages with enhanced styling
    line1 = ax.plot(ma_timesteps_plain/1000, ma_rewards_plain, 
                    color=color_plain, linewidth=3.5, 
                    label=f'Plain Surface (Peak: {stats_plain["peak_ma"]:.1f})',
                    marker='o', markevery=max(len(ma_rewards_plain)//15, 1), 
                    markersize=6, markerfacecolor='white', markeredgewidth=2,
                    markeredgecolor=color_plain, alpha=0.9, zorder=3)
    
    line2 = ax.plot(ma_timesteps_uneven/1000, ma_rewards_uneven, 
                    color=color_uneven, linewidth=3.5,
                    label=f'Uneven Surface (Peak: {stats_uneven["peak_ma"]:.1f})',
                    marker='s', markevery=max(len(ma_rewards_uneven)//15, 1), 
                    markersize=6, markerfacecolor='white', markeredgewidth=2,
                    markeredgecolor=color_uneven, alpha=0.9, zorder=3)
    
    # Add shaded confidence regions
    ax.fill_between(ma_timesteps_plain/1000, 0, ma_rewards_plain, 
                     where=(ma_rewards_plain > 0), 
                     alpha=0.15, color=color_plain_fill, zorder=1)
    ax.fill_between(ma_timesteps_uneven/1000, 0, ma_rewards_uneven, 
                     where=(ma_rewards_uneven > 0), 
                     alpha=0.15, color=color_uneven_fill, zorder=1)
    
    # Reference lines with better styling
    ax.axhline(y=0, color='#E63946', linestyle='--', alpha=0.7, linewidth=2.5, 
               label='Zero Baseline', zorder=2)
    ax.axhline(y=stats_plain['peak_ma'], color=color_plain, 
               linestyle=':', alpha=0.4, linewidth=2)
    ax.axhline(y=stats_uneven['peak_ma'], color=color_uneven, 
               linestyle=':', alpha=0.4, linewidth=2)
    
    # Enhanced labels and title
    ax.set_xlabel('Training Timesteps (×1000)', fontsize=16, fontweight='bold', color='#2d3436')
    ax.set_ylabel('50-Episode Moving Average Reward', fontsize=16, fontweight='bold', color='#2d3436')
    ax.set_title('SAC Algorithm Performance Comparison\nPlain vs Uneven Terrain (~300K Timesteps)', 
                 fontsize=19, fontweight='bold', pad=25, color='#2d3436')
    
    # Enhanced legend
    legend = ax.legend(loc='lower right', fontsize=13, framealpha=0.98, 
                       shadow=True, fancybox=True, edgecolor='#636e72')
    legend.get_frame().set_facecolor('#f8f9fa')
    legend.get_frame().set_linewidth(2)
    
    # Enhanced grid
    ax.grid(True, alpha=0.25, linestyle='--', linewidth=1.2, color='#636e72')
    ax.tick_params(labelsize=13, colors='#2d3436')
    
    # Statistics box with premium styling
    stats_text = f"""Performance Metrics:
    
Plain Surface:
  Episodes: {stats_plain['episodes']:,}
  Timesteps: {stats_plain['timesteps']:,}
  Peak MA: {stats_plain['peak_ma']:.2f}
  
Uneven Terrain:
  Episodes: {stats_uneven['episodes']:,}
  Timesteps: {stats_uneven['timesteps']:,}
  Peak MA: {stats_uneven['peak_ma']:.2f}"""
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            fontsize=11, verticalalignment='top', horizontalalignment='left',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#fffef7', 
                     alpha=0.95, edgecolor='#636e72', linewidth=2),
            family='monospace', color='#2d3436')
    
    # Add watermark
    ax.text(0.98, 0.02, 'SAC Training Analysis', transform=ax.transAxes,
            fontsize=10, alpha=0.3, ha='right', va='bottom',
            style='italic', color='#636e72')
    
    plt.tight_layout()
    plt.savefig('training_graphs/sac_premium_comparison_300dpi.png', dpi=300, 
                bbox_inches='tight', facecolor='#f8f9fa')
    print(f"✓ Saved: training_graphs/sac_premium_comparison_300dpi.png")
    
    plt.savefig('training_graphs/sac_premium_comparison_600dpi.png', dpi=600, 
                bbox_inches='tight', facecolor='#f8f9fa')
    print(f"✓ Saved: training_graphs/sac_premium_comparison_600dpi.png")
    
    plt.close()
    
    # ==================== GRAPH 2: Modern Dark Theme ====================
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('#1a1a1a')
    ax.set_facecolor('#2d2d2d')
    
    # Dark theme colors
    color_plain_dark = '#00D9FF'    # Cyan
    color_uneven_dark = '#FF6B9D'   # Pink
    
    # Plot with glow effect
    ax.plot(ma_timesteps_plain/1000, ma_rewards_plain, 
            color=color_plain_dark, linewidth=4, 
            label=f'Plain Surface (Peak: {stats_plain["peak_ma"]:.1f})',
            alpha=0.9, zorder=3, path_effects=[])
    
    ax.plot(ma_timesteps_uneven/1000, ma_rewards_uneven, 
            color=color_uneven_dark, linewidth=4,
            label=f'Uneven Terrain (Peak: {stats_uneven["peak_ma"]:.1f})',
            alpha=0.9, zorder=3)
    
    # Add glow effect layers
    for width in [8, 6, 4]:
        ax.plot(ma_timesteps_plain/1000, ma_rewards_plain, 
                color=color_plain_dark, linewidth=width, alpha=0.1, zorder=2)
        ax.plot(ma_timesteps_uneven/1000, ma_rewards_uneven, 
                color=color_uneven_dark, linewidth=width, alpha=0.1, zorder=2)
    
    # Fill areas
    ax.fill_between(ma_timesteps_plain/1000, 0, ma_rewards_plain, 
                     where=(ma_rewards_plain > 0), 
                     alpha=0.2, color=color_plain_dark, zorder=1)
    ax.fill_between(ma_timesteps_uneven/1000, 0, ma_rewards_uneven, 
                     where=(ma_rewards_uneven > 0), 
                     alpha=0.2, color=color_uneven_dark, zorder=1)
    
    # Reference lines
    ax.axhline(y=0, color='#FFD700', linestyle='--', alpha=0.6, linewidth=2.5, 
               label='Zero Baseline', zorder=2)
    
    # Labels
    ax.set_xlabel('Training Timesteps (×1000)', fontsize=16, fontweight='bold', color='#ffffff')
    ax.set_ylabel('50-Episode Moving Average Reward', fontsize=16, fontweight='bold', color='#ffffff')
    ax.set_title('SAC Performance: Plain vs Uneven Terrain\nContinuous Action Space Comparison', 
                 fontsize=19, fontweight='bold', pad=25, color='#ffffff')
    
    # Legend
    legend = ax.legend(loc='lower right', fontsize=13, framealpha=0.9, 
                       fancybox=True, edgecolor='#00D9FF')
    legend.get_frame().set_facecolor('#1a1a1a')
    legend.get_frame().set_linewidth(2)
    
    # Grid
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=1, color='#666666')
    ax.tick_params(labelsize=13, colors='#ffffff')
    
    plt.tight_layout()
    plt.savefig('training_graphs/sac_dark_comparison_300dpi.png', dpi=300, 
                bbox_inches='tight', facecolor='#1a1a1a')
    print(f"✓ Saved: training_graphs/sac_dark_comparison_300dpi.png")
    
    plt.savefig('training_graphs/sac_dark_comparison_600dpi.png', dpi=600, 
                bbox_inches='tight', facecolor='#1a1a1a')
    print(f"✓ Saved: training_graphs/sac_dark_comparison_600dpi.png")
    
    plt.close()
    
    # ==================== GRAPH 3: Scientific Publication Style ====================
    plt.style.use('seaborn-v0_8-paper')
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Scientific colors (colorblind-friendly)
    color_plain_sci = '#0173B2'    # Blue
    color_uneven_sci = '#DE8F05'   # Orange
    
    # Plot with publication styling
    ax.plot(ma_timesteps_plain/1000, ma_rewards_plain, 
            color=color_plain_sci, linewidth=2.5, 
            label=f'Plain Surface',
            marker='o', markevery=max(len(ma_rewards_plain)//20, 1), 
            markersize=4, zorder=3)
    
    ax.plot(ma_timesteps_uneven/1000, ma_rewards_uneven, 
            color=color_uneven_sci, linewidth=2.5,
            label=f'Uneven Terrain',
            marker='s', markevery=max(len(ma_rewards_uneven)//20, 1), 
            markersize=4, zorder=3)
    
    # Reference line
    ax.axhline(y=0, color='#333333', linestyle='--', alpha=0.5, linewidth=1.5, 
               label='Zero Reward', zorder=2)
    
    # Labels - publication style
    ax.set_xlabel('Timesteps (×10³)', fontsize=14, fontweight='normal')
    ax.set_ylabel('Reward (50-episode moving average)', fontsize=14, fontweight='normal')
    ax.set_title('Training Performance Comparison: SAC on Plain and Uneven Terrain', 
                 fontsize=15, fontweight='bold', pad=15)
    
    # Legend - scientific
    legend = ax.legend(loc='best', fontsize=12, frameon=True, 
                       edgecolor='black', fancybox=False)
    legend.get_frame().set_linewidth(1.5)
    
    # Grid - minimal
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.8, color='#cccccc')
    ax.tick_params(labelsize=12)
    
    # Spines
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')
        spine.set_linewidth(1.5)
    
    plt.tight_layout()
    plt.savefig('training_graphs/sac_publication_comparison_300dpi.png', dpi=300, 
                bbox_inches='tight', facecolor='white')
    print(f"✓ Saved: training_graphs/sac_publication_comparison_300dpi.png")
    
    plt.savefig('training_graphs/sac_publication_comparison_600dpi.png', dpi=600, 
                bbox_inches='tight', facecolor='white')
    print(f"✓ Saved: training_graphs/sac_publication_comparison_600dpi.png")
    
    plt.close()
    
    # ==================== GRAPH 4: Vibrant Presentation Style ====================
    plt.style.use('seaborn-v0_8-bright')
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('#FFF8E7')
    ax.set_facecolor('#FFFEF9')
    
    # Vibrant colors
    color_plain_vib = '#FF1744'    # Red
    color_uneven_vib = '#00BCD4'   # Cyan
    
    # Plot with bold styling
    ax.plot(ma_timesteps_plain/1000, ma_rewards_plain, 
            color=color_plain_vib, linewidth=4.5, 
            label=f'🔴 Plain Surface (Peak: {stats_plain["peak_ma"]:.1f})',
            alpha=0.85, zorder=3, linestyle='-')
    
    ax.plot(ma_timesteps_uneven/1000, ma_rewards_uneven, 
            color=color_uneven_vib, linewidth=4.5,
            label=f'🔷 Uneven Terrain (Peak: {stats_uneven["peak_ma"]:.1f})',
            alpha=0.85, zorder=3, linestyle='-')
    
    # Gradient fills
    ax.fill_between(ma_timesteps_plain/1000, 0, ma_rewards_plain, 
                     where=(ma_rewards_plain > 0), 
                     alpha=0.25, color=color_plain_vib, zorder=1)
    ax.fill_between(ma_timesteps_uneven/1000, 0, ma_rewards_uneven, 
                     where=(ma_rewards_uneven > 0), 
                     alpha=0.25, color=color_uneven_vib, zorder=1)
    
    # Reference line
    ax.axhline(y=0, color='#424242', linestyle='--', alpha=0.6, linewidth=3, 
               label='⚠ Zero Baseline', zorder=2)
    
    # Labels - vibrant
    ax.set_xlabel('Training Timesteps (×1000)', fontsize=17, fontweight='bold', color='#212121')
    ax.set_ylabel('Reward (50-Episode Average)', fontsize=17, fontweight='bold', color='#212121')
    ax.set_title('🚀 SAC Training Results: Terrain Comparison\nContinuous Action Space Performance', 
                 fontsize=20, fontweight='bold', pad=25, color='#212121')
    
    # Legend - vibrant
    legend = ax.legend(loc='lower right', fontsize=14, framealpha=0.95, 
                       shadow=True, fancybox=True, edgecolor='#FF1744')
    legend.get_frame().set_facecolor('#FFF8E7')
    legend.get_frame().set_linewidth(3)
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=1.5, color='#9E9E9E')
    ax.tick_params(labelsize=14, colors='#212121')
    
    plt.tight_layout()
    plt.savefig('training_graphs/sac_vibrant_comparison_300dpi.png', dpi=300, 
                bbox_inches='tight', facecolor='#FFF8E7')
    print(f"✓ Saved: training_graphs/sac_vibrant_comparison_300dpi.png")
    
    plt.savefig('training_graphs/sac_vibrant_comparison_600dpi.png', dpi=600, 
                bbox_inches='tight', facecolor='#FFF8E7')
    print(f"✓ Saved: training_graphs/sac_vibrant_comparison_600dpi.png")
    
    plt.close()
    
    print("\n" + "="*70)
    print("✓ ALL PREMIUM COMPARISON GRAPHS GENERATED!")
    print("="*70)
    print("\nGenerated 4 different styles:")
    print("  1. Premium/Elegant (Ocean Blue vs Magenta)")
    print("  2. Dark Theme (Cyan vs Pink with glow)")
    print("  3. Scientific Publication (Colorblind-friendly)")
    print("  4. Vibrant Presentation (Red vs Cyan)")
    print("\nEach style available in 300 DPI and 600 DPI")
    print("="*70)

if __name__ == "__main__":
    plot_premium_comparison()
