# SAC Rocket Landing Training - Uneven Terrain

This folder contains the **SAC (Soft Actor-Critic)** implementation for rocket landing on **uneven terrain**.

## Algorithm: SAC vs PPO

**SAC Advantages:**
- **Continuous Actions**: Thrust [0.2g, 2.0g] and Nozzle Angle [-30°, +30°] - more realistic control
- **Sample Efficiency**: 5-10x more sample efficient than PPO
- **Off-Policy**: Can learn from past experiences stored in replay buffer
- **Better Final Performance**: Expected to achieve similar/better results in less time
- **Adaptability**: Should handle terrain variations better with continuous control

**PPO (for comparison):**
- **Discrete Actions**: Only 9 action combinations (3 thrust × 3 nozzle positions)
- **On-Policy**: Requires fresh data for each update
- **Required**: 2.4M timesteps (~8 hours) to achieve +40-150 rewards on uneven terrain

## Training Configuration

- **Total Timesteps**: 500,000 (vs 2.4M for PPO)
- **Expected Time**: 1-2 hours (vs 8 hours for PPO)
- **Terrain**: Enabled (Difficulty: moderate)
  - 5 terrain features (craters and hills)
  - Height variation: ±25 meters
  - Crater depth: up to 15 meters
- **Action Space**: Continuous Box([thrust, nozzle_velocity])
- **Observation Space**: [x, y, vx, vy, theta, vtheta, t, phi]
- **Learning Rate**: 3e-4
- **Batch Size**: 256
- **Buffer Size**: 100,000

## Terrain Features

The environment generates procedural uneven terrain:
- **Random Generation**: New terrain for each episode
- **Features**: Craters and hills using Gaussian distributions
- **Difficulty**: Moderate (5 features, ±25m variation)
- **Physics**: Collision detection with terrain interpolation

## Files

- `rocket_env.py`: Gymnasium-compatible continuous environment with terrain
- `train_sac.py`: SAC training script using Stable-Baselines3
- `utils.py`: Utility functions
- `landing.jpg`, `hover.jpg`: Background images
- `requirements.txt`: Python dependencies

## How to Run

```bash
# Install dependencies (if needed)
pip install -r requirements.txt

# Start training
python train_sac.py
```

## Expected Results

Based on SAC's superior sample efficiency and continuous control:
- **Convergence**: Faster than PPO (500K vs 2.4M timesteps)
- **Final Reward**: +50-120 (potentially better than PPO's +40-150)
- **Training Time**: ~1-2 hours (vs 8 hours for PPO)
- **Terrain Handling**: Better adaptation due to continuous control
- **Variance**: Lower variance in performance due to better control precision

## Output

- **Models**: Saved in `SAC_preTrained_uneven/` every 50K timesteps
- **Logs**: CSV logs in `SAC_logs_uneven/training_log.csv`
- **Graphs**: Training progress saved in `training_graphs/sac_uneven_training_progress.png`

## Comparison with PPO

| Metric | PPO (Uneven) | SAC (Uneven) |
|--------|--------------|--------------|
| Timesteps | 2.4M | 500K |
| Training Time | ~8 hours | ~1-2 hours |
| Action Space | Discrete (9) | Continuous |
| Final Reward | +40 to +150 | TBD |
| Episodes | 11,917 | TBD |
| Sample Efficiency | 1x | 5-10x |
| Terrain | Moderate | Moderate |

## Why SAC Should Perform Better on Uneven Terrain

1. **Continuous Control**: Fine-grained thrust adjustments for terrain adaptation
2. **Sample Efficiency**: Learns faster from diverse terrain experiences
3. **Off-Policy Learning**: Replay buffer helps generalize across terrain variations
4. **Precise Landing**: Smoother control for navigating craters and hills
5. **Exploration**: Automatic entropy tuning for better terrain exploration

---

**Note**: Uneven terrain is significantly harder than plain surface. The continuous action space of SAC should provide better control for precise landings on varied terrain heights.
