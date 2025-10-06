# Rocket Landing on Uneven Terrain - PPO Implementation

## Overview
This folder contains a modified version of the PPO rocket landing environment that includes **uneven terrain** support. The rocket must now land on a procedurally generated surface with craters and hills, making the landing task significantly more challenging.

## New Features

### 1. Uneven Terrain Generation
- **Procedural terrain**: Each episode generates a new random terrain with craters and hills
- **Difficulty levels**: 
  - `easy`: 3 features, max 15m height variation
  - `moderate`: 5 features, max 25m height variation  
  - `hard`: 8 features, max 40m height variation

### 2. Enhanced Physics
- **Terrain collision detection**: Rocket detects collision with terrain surface at different heights
- **Adaptive landing zone**: Target landing area positioned at actual terrain height
- **Variable landing surface**: Each x-position has different ground height

### 3. Training Configuration
Located in `train.py`:
```python
enable_terrain = True
terrain_difficulty = 'moderate'  # 'easy', 'moderate', 'hard'
```

## Files Modified

### rocket.py
- Added `generate_terrain()` method for procedural terrain generation
- Added `get_terrain_height(x_pos)` for terrain height interpolation
- Modified `check_crash()` to account for terrain height
- Modified `check_landing_success()` for terrain-aware landing
- Added `draw_terrain()` for visual rendering of terrain
- Updated collision detection and reward calculations

### train.py
- Environment name changed to `RocketLanding_UnevenTerrain`
- Added terrain parameters: `enable_terrain`, `terrain_difficulty`
- Updated environment initialization with terrain parameters

## How to Use

### Training
```bash
python train.py
```

The training will:
- Generate new random terrain for each episode
- Train the PPO agent to land on varying surfaces
- Save checkpoints to `PPO_preTrained/RocketLanding_UnevenTerrain/`
- Log training progress to `PPO_logs/RocketLanding_UnevenTerrain/`

### Testing
```bash
python test.py
```

## Key Differences from Flat Surface

1. **Increased Difficulty**: Agent must learn to:
   - Identify terrain features visually
   - Adjust landing approach based on surface slope
   - Land precisely within safe zone despite varying heights

2. **State Space**: Same 8-dimensional state (x, y, vx, vy, theta, vtheta, t, phi)
   - Agent must learn terrain awareness from position feedback

3. **Reward Shaping**: Rewards consider:
   - Distance to target (now at terrain level)
   - Landing velocity and angle
   - Successful landing on uneven surface

## Expected Training Time
- Uneven terrain requires **longer training** than flat surface
- Recommended: 8-10 million timesteps for good performance
- Agent needs to see diverse terrain configurations

## Visualization
When rendering (`render=True`):
- Brown terrain with craters and hills
- Target landing zone positioned at terrain surface
- Rocket dynamics with terrain interaction

## Tips for Best Results
1. Start with `difficulty='easy'` for initial training
2. Increase difficulty after achieving 50%+ success rate
3. Monitor landing success rate in logs
4. Adjust `max_training_timesteps` based on convergence

## Future Enhancements
- Variable terrain styles (rocky, icy, dusty)
- Wind and atmospheric effects
- Multiple landing zones
- Fuel constraints
