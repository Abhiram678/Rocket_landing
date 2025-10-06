# SAC Rocket Landing Training

This folder contains the **SAC (Soft Actor-Critic)** implementation for rocket landing on **plain surface**.

## Algorithm: SAC vs PPO

**SAC Advantages:**
- **Continuous Actions**: Thrust [0.2g, 2.0g] and Nozzle Angle [-30°, +30°] - more realistic control
- **Sample Efficiency**: 5-10x more sample efficient than PPO
- **Off-Policy**: Can learn from past experiences stored in replay buffer
- **Better Final Performance**: Expected to achieve similar/better results in less time

**PPO (for comparison):**
- **Discrete Actions**: Only 9 action combinations (3 thrust × 3 nozzle positions)
- **On-Policy**: Requires fresh data for each update
- **Required**: 2.4M timesteps (~8 hours) to achieve +75-95 rewards

## Training Configuration

- **Total Timesteps**: 500,000 (vs 2.4M for PPO)
- **Expected Time**: 1-2 hours (vs 8 hours for PPO)
- **Action Space**: Continuous Box([thrust, nozzle_velocity])
- **Observation Space**: [x, y, vx, vy, theta, vtheta, t, phi]
- **Learning Rate**: 3e-4
- **Batch Size**: 256
- **Buffer Size**: 100,000
- **Target**: Achieve similar/better performance than PPO in less time

## Files

- `rocket_env.py`: Gymnasium-compatible continuous environment
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

Based on SAC's superior sample efficiency:
- **Convergence**: Faster than PPO (500K vs 2.4M timesteps)
- **Final Reward**: +80-100 (similar or better than PPO's +75-95)
- **Training Time**: ~1-2 hours (vs 8 hours for PPO)
- **Success Rate**: Higher landing success rate

## Output

- **Models**: Saved in `SAC_preTrained/` every 50K timesteps
- **Logs**: CSV logs in `SAC_logs/training_log.csv`
- **Graphs**: Training progress saved in `training_graphs/sac_plain_training_progress.png`

## Comparison with PPO

| Metric | PPO (Plain) | SAC (Plain) |
|--------|-------------|-------------|
| Timesteps | 2.4M | 500K |
| Training Time | ~8 hours | ~1-2 hours |
| Action Space | Discrete (9) | Continuous |
| Final Reward | +75 to +95 | TBD |
| Episodes | 11,721 | TBD |
| Sample Efficiency | 1x | 5-10x |

---

**Note**: SAC is theoretically superior for continuous control tasks like rocket landing. The continuous action space allows for finer control of thrust and nozzle angle, leading to smoother and more precise landings.
