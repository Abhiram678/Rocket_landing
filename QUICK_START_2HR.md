# 🚀 Quick Start - 2 Hour Training

## ⏱️ CONFIGURATION SUMMARY

**Both plain and uneven terrain set to:**
- **300,000 timesteps** (~300 episodes)
- **~2 hours training time** each
- **6 checkpoints** (every 50K timesteps)

---

## 🏃 RUN TRAINING

### **Option 1: Run Plain Surface First (Recommended)**
```bash
cd C:\Users\abhir\Desktop\rl_case\final_phase
python train.py
```
⏰ **Wait ~2 hours**

Then run:
```bash
cd C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain
python train.py
```
⏰ **Wait ~2 hours**

---

### **Option 2: Run Uneven Terrain First**
```bash
cd C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain
python train.py
```
⏰ **Wait ~2 hours**

Then run:
```bash
cd C:\Users\abhir\Desktop\rl_case\final_phase
python train.py
```
⏰ **Wait ~2 hours**

---

## 📊 WHAT YOU'LL GET

### **Plain Surface Results:**
- Starting reward: -200 (crashing)
- Final reward: ~+50 to +150 (partial learning)
- Models saved in: `PPO_preTrained/RocketLanding/`
- Logs saved in: `PPO_logs/RocketLanding/`

### **Uneven Terrain Results:**
- Starting reward: -200 (crashing)
- Final reward: ~0 to +100 (harder, still learning)
- Models saved in: `PPO_preTrained/RocketLanding_UnevenTerrain/`
- Logs saved in: `PPO_logs/RocketLanding_UnevenTerrain/`

---

## ⚠️ IMPORTANT

**This is PARTIAL training only!**
- 300K timesteps = 10% of full training
- You'll see improvement but not optimal performance
- Good for quick comparison of plain vs uneven

**For full training, change to:**
```python
max_training_timesteps = int(3e6)  # 3 million (~10 hours)
```

---

## 🎯 AFTER TRAINING

Both will generate:
- ✅ Model checkpoints
- ✅ Training logs (CSV)
- ✅ Graphs (auto-generated)

**Total time investment: 4 hours (2 + 2)**

**Ready to start? Just run the commands above!** 🚀
