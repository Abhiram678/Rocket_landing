# 🚀 Quick Start Guide - Uneven Terrain Rocket Landing

## Location
```
C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain\
```

## Run Training (6 Million Timesteps)
```bash
cd C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain
python train.py
```

## What You'll See
1. Training starts with terrain enabled
2. Progress updates every 10,000 timesteps
3. Model checkpoints saved every 100,000 timesteps
4. Graphs automatically generated (same as flat surface version)
5. Logs saved to `PPO_logs/RocketLanding_UnevenTerrain/`

## Change Terrain Difficulty
Edit `train.py` line 22:
```python
terrain_difficulty = 'easy'      # Easy terrain
terrain_difficulty = 'moderate'  # Default - moderate difficulty  
terrain_difficulty = 'hard'      # Hard terrain with many features
```

## Disable Terrain (Switch to Flat)
Edit `train.py` line 21:
```python
enable_terrain = False  # Flat surface like original
```

## Key Differences from Flat Surface
- ✅ Procedurally generated terrain with craters and hills
- ✅ Variable landing surface heights
- ✅ Requires more training time (8-10M timesteps recommended)
- ✅ More challenging but more realistic

## Training Expected Time
- **CPU**: ~12-15 hours for 6M timesteps
- **GPU**: Not required (discrete actions)

## Output Files
- `PPO_preTrained/RocketLanding_UnevenTerrain/*.pth` - Model checkpoints
- `PPO_logs/RocketLanding_UnevenTerrain/*.csv` - Training logs
- Graphs will be plotted automatically (existing code)

## That's It!
No need to change anything else. The graphs and visualization are already built-in from the original code.

Just run `python train.py` and let it train! 🎯
