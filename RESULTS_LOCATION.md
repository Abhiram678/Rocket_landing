# 📁 Training Results - File Locations

## 🎯 PLAIN SURFACE TRAINING RESULTS

### **Location:**
```
C:\Users\abhir\Desktop\rl_case\final_phase\
```

---

## 📊 1. TRAINING LOGS (CSV Files)

### **Path:**
```
C:\Users\abhir\Desktop\rl_case\final_phase\PPO_logs\RocketLanding\
```

### **Files:**
- `PPO_RocketLanding_log_0.csv` - Training progress data

### **What's Inside:**
- Timestep numbers
- Episode numbers
- Average rewards
- Training metrics

### **Use For:**
- Plotting graphs
- Analyzing training progress
- Comparing performance over time

---

## 🤖 2. MODEL CHECKPOINTS (Trained Models)

### **Path:**
```
C:\Users\abhir\Desktop\rl_case\final_phase\PPO_preTrained\RocketLanding\
```

### **Files:**
- `PPO_RocketLanding_0_0.pth` - Latest model checkpoint
- Additional checkpoints saved every 100K timesteps:
  - `PPO_RocketLanding_0_0.pth` (at 100K)
  - `PPO_RocketLanding_0_0.pth` (at 200K)
  - ... continues every 100K until 2.4M

### **What's Inside:**
- Actor network weights (policy)
- Critic network weights (value function)
- Optimizer state
- Training parameters

### **Use For:**
- Testing the trained agent
- Continuing training later
- Deploying the agent

---

## 📈 3. GRAPHS (Auto-Generated)

### **Path:**
```
C:\Users\abhir\Desktop\rl_case\final_phase\images\
```
(If `plot_graph.py` is run after training)

### **Files:**
- Reward vs Timesteps graph
- Episode length plots
- Performance metrics visualization

---

## 🏔️ UNEVEN TERRAIN TRAINING RESULTS (When You Run It)

### **Logs Path:**
```
C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain\PPO_logs\RocketLanding_UnevenTerrain\
```

### **Models Path:**
```
C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain\PPO_preTrained\RocketLanding_UnevenTerrain\
```

---

## 📋 QUICK REFERENCE TABLE

| Type | Plain Surface | Uneven Terrain |
|------|--------------|----------------|
| **Logs (CSV)** | `final_phase/PPO_logs/RocketLanding/` | `final_uneven_terrain/PPO_logs/RocketLanding_UnevenTerrain/` |
| **Models (.pth)** | `final_phase/PPO_preTrained/RocketLanding/` | `final_uneven_terrain/PPO_preTrained/RocketLanding_UnevenTerrain/` |
| **Graphs** | `final_phase/images/` | `final_uneven_terrain/images/` |
| **Log File Name** | `PPO_RocketLanding_log_0.csv` | `PPO_RocketLanding_UnevenTerrain_log_0.csv` |
| **Model File Name** | `PPO_RocketLanding_0_0.pth` | `PPO_RocketLanding_UnevenTerrain_0_0.pth` |

---

## 🔍 HOW TO ACCESS RESULTS

### **View Training Logs (CSV):**
```bash
# Plain Surface
notepad C:\Users\abhir\Desktop\rl_case\final_phase\PPO_logs\RocketLanding\PPO_RocketLanding_log_0.csv

# Uneven Terrain (after training)
notepad C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain\PPO_logs\RocketLanding_UnevenTerrain\PPO_RocketLanding_UnevenTerrain_log_0.csv
```

### **View Model Files:**
```bash
# Plain Surface
dir C:\Users\abhir\Desktop\rl_case\final_phase\PPO_preTrained\RocketLanding\

# Uneven Terrain (after training)
dir C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain\PPO_preTrained\RocketLanding_UnevenTerrain\
```

### **Generate Graphs:**
```bash
# Plain Surface
cd C:\Users\abhir\Desktop\rl_case\final_phase
python plot_graph.py

# Uneven Terrain
cd C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain
python plot_graph.py
```

---

## 📊 CHECKPOINT SCHEDULE

### **Plain Surface (2.4M timesteps):**
Checkpoints saved at:
- 100,000 timesteps
- 200,000 timesteps
- 300,000 timesteps
- 400,000 timesteps
- 500,000 timesteps
- ... every 100K up to 2,400,000

**Total checkpoints:** 24 files

---

## 💾 FILE SIZES (Approximate)

| File Type | Size | Description |
|-----------|------|-------------|
| `.pth` (Model) | ~2-5 MB | Neural network weights |
| `.csv` (Logs) | ~100-500 KB | Training data |
| Graphs (PNG) | ~100-200 KB | Visualization images |

---

## 🚀 TEST TRAINED MODEL

After training completes, test the agent:

```bash
# Plain Surface
cd C:\Users\abhir\Desktop\rl_case\final_phase
python test.py

# Uneven Terrain
cd C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain
python test.py
```

---

## 📂 FULL DIRECTORY STRUCTURE

```
final_phase/
├── PPO_logs/                        ← Training logs
│   └── RocketLanding/
│       └── PPO_RocketLanding_log_0.csv
│
├── PPO_preTrained/                  ← Trained models
│   └── RocketLanding/
│       └── PPO_RocketLanding_0_0.pth
│
├── images/                          ← Generated graphs
│   └── (graphs created after training)
│
└── final_uneven_terrain/            ← Uneven terrain version
    ├── PPO_logs/
    │   └── RocketLanding_UnevenTerrain/
    │       └── PPO_RocketLanding_UnevenTerrain_log_0.csv
    │
    ├── PPO_preTrained/
    │   └── RocketLanding_UnevenTerrain/
    │       └── PPO_RocketLanding_UnevenTerrain_0_0.pth
    │
    └── images/
        └── (graphs for uneven terrain)
```

---

## ✅ CURRENTLY SAVED (Plain Surface Running)

As of now:
- ✅ `PPO_logs/RocketLanding/PPO_RocketLanding_log_0.csv` - Being updated
- ✅ `PPO_preTrained/RocketLanding/PPO_RocketLanding_0_0.pth` - Latest checkpoint
- ⏳ Training in progress...

**Results will continue to update as training progresses!**

---

## 🎯 SUMMARY

### **Training Logs:**
- Plain: `C:\Users\abhir\Desktop\rl_case\final_phase\PPO_logs\RocketLanding\`
- Uneven: `C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain\PPO_logs\RocketLanding_UnevenTerrain\`

### **Trained Models:**
- Plain: `C:\Users\abhir\Desktop\rl_case\final_phase\PPO_preTrained\RocketLanding\`
- Uneven: `C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain\PPO_preTrained\RocketLanding_UnevenTerrain\`

**All results are automatically saved during training!** 📊
