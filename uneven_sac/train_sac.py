"""
Train SAC agent for rocket landing - Uneven Terrain
Uses Stable-Baselines3 implementation
"""

import os
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.logger import configure
import matplotlib.pyplot as plt
from rocket_env import RocketLandingEnv
import random


class TrainingCallback(BaseCallback):
    """Callback for logging training progress"""
    
    def __init__(self, check_freq=1000, log_dir='./SAC_logs_uneven/'):
        super().__init__()
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.episode_rewards = []
        self.episode_lengths = []
        self.current_episode_reward = 0
        self.current_episode_length = 0
        
    def _on_step(self):
        self.current_episode_reward += self.locals['rewards'][0]
        self.current_episode_length += 1
        
        if self.locals['dones'][0]:
            self.episode_rewards.append(self.current_episode_reward)
            self.episode_lengths.append(self.current_episode_length)
            self.current_episode_reward = 0
            self.current_episode_length = 0
            
            # Log to file
            if len(self.episode_rewards) % 10 == 0:
                log_file = os.path.join(self.log_dir, 'training_log.csv')
                with open(log_file, 'a') as f:
                    f.write(f"{self.num_timesteps},{len(self.episode_rewards)},{self.episode_rewards[-1]}\n")
        
        return True


def train_sac():
    # Set random seeds
    seed = 42
    np.random.seed(seed)
    random.seed(seed)
    
    # Create directories
    log_dir = './SAC_logs_uneven/'
    model_dir = './SAC_preTrained_uneven/'
    graph_dir = './training_graphs/'
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(graph_dir, exist_ok=True)
    
    # Initialize log file
    log_file = os.path.join(log_dir, 'training_log.csv')
    with open(log_file, 'w') as f:
        f.write('timestep,episode,reward\n')
    
    print("=" * 50)
    print("SAC Training - Uneven Terrain")
    print("=" * 50)
    print(f"Algorithm: SAC (Soft Actor-Critic)")
    print(f"Action Space: Continuous [thrust, nozzle_angle_velocity]")
    print(f"Terrain: Enabled (Difficulty: moderate)")
    print(f"Total Timesteps: 500,000")
    print(f"Expected Time: ~1-2 hours")
    print("=" * 50)
    
    # Create environment with uneven terrain
    env = RocketLandingEnv(
        max_steps=1000, 
        task='landing', 
        rocket_type='starship',
        enable_terrain=True,
        terrain_difficulty='moderate'
    )
    
    # Create SAC model
    model = SAC(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        buffer_size=100000,
        learning_starts=1000,
        batch_size=256,
        tau=0.005,
        gamma=0.99,
        train_freq=1,
        gradient_steps=1,
        ent_coef='auto',
        verbose=1,
        tensorboard_log=log_dir,
        seed=seed
    )
    
    # Create callback
    callback = TrainingCallback(check_freq=1000, log_dir=log_dir)
    
    # Train the model
    print("\nStarting training...")
    total_timesteps = 500000
    save_freq = 50000
    
    for i in range(0, total_timesteps, save_freq):
        remaining = min(save_freq, total_timesteps - i)
        model.learn(
            total_timesteps=remaining,
            callback=callback,
            reset_num_timesteps=False,
            progress_bar=True
        )
        
        # Save model checkpoint
        checkpoint_path = os.path.join(model_dir, f'sac_rocket_uneven_{i+remaining}.zip')
        model.save(checkpoint_path)
        print(f"\nCheckpoint saved: {checkpoint_path}")
    
    # Save final model
    final_model_path = os.path.join(model_dir, 'sac_rocket_uneven_final.zip')
    model.save(final_model_path)
    print(f"\nFinal model saved: {final_model_path}")
    
    # Plot training progress
    plot_training_results(log_file, graph_dir)
    
    print("\n" + "=" * 50)
    print("Training Complete!")
    print("=" * 50)
    print(f"Total Episodes: {len(callback.episode_rewards)}")
    print(f"Average Reward (last 100): {np.mean(callback.episode_rewards[-100:]):.2f}")
    print(f"Max Reward: {np.max(callback.episode_rewards):.2f}")
    print(f"Models saved in: {model_dir}")
    print(f"Graphs saved in: {graph_dir}")
    print("=" * 50)
    
    env.close()


def plot_training_results(log_file, save_dir):
    """Generate training progress graphs"""
    
    # Read log file
    timesteps, episodes, rewards = [], [], []
    with open(log_file, 'r') as f:
        lines = f.readlines()[1:]  # Skip header
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 3:
                timesteps.append(int(parts[0]))
                episodes.append(int(parts[1]))
                rewards.append(float(parts[2]))
    
    if len(rewards) == 0:
        print("No training data to plot")
        return
    
    # Calculate moving average
    window = min(20, len(rewards))
    moving_avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Timesteps vs Rewards
    ax1.plot(timesteps, rewards, alpha=0.3, color='green', label='Episode Reward')
    if len(moving_avg) > 0:
        ax1.plot(timesteps[window-1:], moving_avg, color='red', linewidth=2, label=f'{window}-Episode Moving Avg')
    ax1.set_xlabel('Timesteps', fontsize=12)
    ax1.set_ylabel('Reward', fontsize=12)
    ax1.set_title('SAC Training Progress - Uneven Terrain (Timesteps)', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Episodes vs Rewards
    ax2.plot(episodes, rewards, alpha=0.3, color='green', label='Episode Reward')
    if len(moving_avg) > 0:
        ax2.plot(episodes[window-1:], moving_avg, color='red', linewidth=2, label=f'{window}-Episode Moving Avg')
    ax2.set_xlabel('Episodes', fontsize=12)
    ax2.set_ylabel('Reward', fontsize=12)
    ax2.set_title('SAC Training Progress - Uneven Terrain (Episodes)', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    save_path = os.path.join(save_dir, 'sac_uneven_training_progress.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nTraining graph saved: {save_path}")
    
    plt.close()


if __name__ == "__main__":
    train_sac()
