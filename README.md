# Rocket Landing on Rough Surfaces using Reinforcement Learning

A comprehensive comparison of Proximal Policy Optimization (PPO) and Soft Actor-Critic (SAC) algorithms for autonomous rocket landing in both flat and uneven terrain scenarios.

## 🚀 Overview

This project implements and compares two state-of-the-art reinforcement learning algorithms for autonomous rocket landing control. The study demonstrates SAC's superior sample efficiency and performance compared to PPO, achieving 8.4× faster training and 2.3× higher peak rewards.

## 📊 Key Results

- **Sample Efficiency**: SAC requires 8.4× fewer timesteps (300K vs 2.4M)
- **Training Speed**: SAC trains in 21 minutes vs PPO's 8 hours
- **Peak Performance**: SAC achieves 2.3× higher single-episode rewards (+690 vs +305)
- **Terrain Robustness**: SAC retains 82.7% performance, PPO retains 67.8%
- **Action Precision**: Continuous actions enable smoother control

## 🏗️ Project Structure

```
Rocket_landing/
├── PPO.py                          # PPO algorithm implementation
├── train.py                        # PPO training script
├── test.py                         # Testing script
├── requirements.txt                # Dependencies
├── plain_sac/                     # SAC implementation for plain terrain
├── uneven_sac/                     # SAC implementation for uneven terrain
├── final_uneven_terrain/          # PPO uneven terrain training
├── training_graphs/               # Generated plots and visualizations
└── PPO_logs/                      # Training logs and checkpoints
```

## 🎯 Algorithms

### PPO (Proximal Policy Optimization)
- **Type**: On-policy
- **Actions**: Discrete (9 combinations)
- **Strengths**: Stable, low variance
- **Use Case**: Final validation, safety-critical applications

### SAC (Soft Actor-Critic)
- **Type**: Off-policy
- **Actions**: Continuous
- **Strengths**: Sample efficient, high performance
- **Use Case**: Rapid development, prototyping

## 🌍 Environments

- **Plain Surface**: Flat landing pad for baseline testing
- **Uneven Terrain**: Procedurally generated with ±25m variation and 5 features

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PyTorch 1.9+
- Stable-Baselines3 2.0+
- NumPy, Matplotlib

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Abhiram678/Rocket_landing.git
cd Rocket_landing
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Training

#### Train PPO (Plain Surface)
```bash
python train.py
```

#### Train PPO (Uneven Terrain)
```bash
cd final_uneven_terrain
python train.py
```

#### Train SAC (Plain Surface)
```bash
cd plain_sac
python train_sac.py
```

#### Train SAC (Uneven Terrain)
```bash
cd uneven_sac
python train_sac_uneven.py
```

### Testing
```bash
python test.py
```

### Generate Results
```bash
# SAC Plain
cd plain_sac
python plot_sac_final.py

# SAC Uneven
cd uneven_sac
python plot_sac_uneven_final.py

# Comparison plots
cd uneven_sac
python plot_premium_comparison.py
```

## 📈 Environment Details

### State Space
8-dimensional continuous observations:
- Position (x, y) in meters
- Velocity (vx, vy) in m/s
- Body angle θ in radians
- Angular velocity θ̇ in rad/s
- Timestep counter t
- Gimbal angle φ in radians

### Action Space
- **PPO**: 9 discrete actions (3 thrust levels × 3 gimbal angles)
- **SAC**: Continuous actions (thrust: 0.2g-2.0g, angle: ±30°)

### Physics Parameters
- Rocket height: 50m
- Gravity: 9.8 m/s²
- Simulation timestep: 0.05s
- World bounds: x ∈ [-300, 300]m, y ∈ [-30, 570]m

## 🔧 Hyperparameters

### PPO Configuration
- Learning rate: 3×10⁻⁴
- Discount factor: 0.99
- GAE parameter: 0.95
- Batch size: 4000 timesteps
- Optimization epochs: 80

### SAC Configuration
- Learning rate: 3×10⁻⁴
- Discount factor: 0.99
- Replay buffer: 1M transitions
- Batch size: 256
- Target update rate: 0.005

## 📊 Performance Metrics

| Metric | PPO Plain | PPO Uneven | SAC Plain | SAC Uneven |
|--------|-----------|------------|-----------|------------|
| Training Time | 8 hours | 8 hours | 21 min | 25 min |
| Peak Reward | +305.2 | +215.8 | +690.34 | +896.42 |
| Convergence | 1.5M steps | 1.8M steps | 250K steps | 200K steps |
| Success Rate | 65% | 45% | 70% | 60% |

## 🎓 Academic Context

This project implements a comprehensive case study comparing PPO and SAC algorithms for autonomous rocket landing. The research demonstrates:

- Superior sample efficiency of off-policy learning
- Impact of action space design on control precision
- Terrain robustness evaluation through procedural generation
- Practical feasibility for resource-constrained development

## 📄 Citation

```bibtex
@misc{rocket-landing-rl-2025,
  author = {Suravarapu Abhiram},
  title = {Rocket Landing on Rough Surfaces using Reinforcement Learning},
  year = {2025},
  url = {https://github.com/Abhiram678/Rocket_landing}
}
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or feedback, please open an issue in this repository.

---

**Made with ❤️ for autonomous aerospace control** 🚀