# 2-Hour Training Configuration

## ⏱️ TRAINING TIME: ~2 HOURS EACH

Both plain and uneven terrain are now configured for **approximately 2 hours** of training time.

---

## 📊 NEW CONFIGURATION

### **Timesteps:**
```python
max_training_timesteps = int(3e5)   # 300,000 timesteps
```

### **Episodes:**
- Max timesteps per episode: 1,000
- Total episodes: **~300 episodes**
- Training time: **~2 hours** per version

### **Checkpoints:**
- Save model every **50,000 timesteps**
- You'll get **6 checkpoints** total:
  - 50K, 100K, 150K, 200K, 250K, 300K

---

## 🎯 WHAT YOU'LL GET

### **Plain Surface Training (2 hours):**
```bash
Location: final_phase/
Timesteps: 300,000
Episodes: ~300
Expected Result: Partial learning, some successful landings
Final Reward: ~+50 to +150 (not fully trained)
```

### **Uneven Terrain Training (2 hours):**
```bash
Location: final_phase/final_uneven_terrain/
Timesteps: 300,000
Episodes: ~300
Expected Result: Basic learning, harder than plain
Final Reward: ~0 to +100 (still learning)
```

---

## ⚠️ IMPORTANT NOTE

**300K timesteps is NOT enough for full training!**

- **Full training needs:** 3-6 million timesteps
- **You're doing:** 300K timesteps (10% of full training)
- **Why:** To save time and compare plain vs uneven quickly

### **What to Expect:**
- ✅ You'll see learning happening
- ✅ Rewards will improve
- ✅ Some successful landings
- ❌ Not optimal performance
- ❌ Agent still learning (not expert)

---

## 🚀 HOW TO RUN

### **Step 1: Train Plain Surface (2 hours)**
```bash
cd C:\Users\abhir\Desktop\rl_case\final_phase
python train.py
```
**Wait ~2 hours** ⏰

### **Step 2: Train Uneven Terrain (2 hours)**
```bash
cd C:\Users\abhir\Desktop\rl_case\final_phase\final_uneven_terrain
python train.py
```
**Wait ~2 hours** ⏰

**Total time: ~4 hours** for both

---

## 📈 EXPECTED LEARNING CURVE (300K timesteps)

### **Plain Surface:**
```
Start (0-50K):     -200 to -100 (crashing)
Early (50-100K):   -100 to 0    (learning)
Mid (100-200K):    0 to +50     (some landings)
End (200-300K):    +50 to +150  (improving)
```

### **Uneven Terrain:**
```
Start (0-50K):     -200 to -100 (crashing)
Early (50-100K):   -100 to -50  (harder learning)
Mid (100-200K):    -50 to 0     (struggling)
End (200-300K):    0 to +100    (some success)
```

---

## 📁 OUTPUT FILES

### **Plain Surface:**
- Models: `PPO_preTrained/RocketLanding/`
  - Checkpoints at 50K, 100K, 150K, 200K, 250K, 300K
- Logs: `PPO_logs/RocketLanding/`
  - CSV file with training data
- Graphs: Auto-generated after training

### **Uneven Terrain:**
- Models: `PPO_preTrained/RocketLanding_UnevenTerrain/`
  - Checkpoints at 50K, 100K, 150K, 200K, 250K, 300K
- Logs: `PPO_logs/RocketLanding_UnevenTerrain/`
  - CSV file with training data
- Graphs: Auto-generated after training

---

## 🔧 CHANGES MADE

### **Both Files Changed:**

**BEFORE:**
```python
max_training_timesteps = int(6e6)   # 6 million timesteps (~10-12 hours)
save_model_freq = int(1e5)          # Save every 100K
```

**AFTER:**
```python
max_training_timesteps = int(3e5)   # 300K timesteps (~2 hours)
save_model_freq = int(5e4)          # Save every 50K
```

---

## 📊 COMPARISON TABLE

| Aspect | Original | New (2 Hours) |
|--------|----------|---------------|
| **Timesteps** | 6,000,000 | 300,000 |
| **Episodes** | ~6,000 | ~300 |
| **Training Time** | ~10-12 hours | ~2 hours |
| **Checkpoints** | Every 100K | Every 50K |
| **Total Checkpoints** | 60 | 6 |
| **Expected Performance** | Excellent | Basic/Partial |
| **Fully Trained?** | ✅ Yes | ❌ No (10% trained) |

---

## 💡 WHAT YOU'LL SEE AFTER 2 HOURS

### **Console Output (End of Training):**
```
Episode : 300   Timestep : 300000   Average Reward : ~+100
Training completed!
Total training time: ~2 hours
```

### **Graphs Generated:**
- Reward vs Timesteps (similar to the one you showed)
- But only going up to 300K instead of 3.7M

### **Performance:**
- **Plain Surface:** Some successful landings, not perfect
- **Uneven Terrain:** Basic understanding, still learning

---

## 🎯 WHY THIS CONFIGURATION?

### **Advantages:**
✅ **Quick comparison** - See both in 4 hours total
✅ **See learning curve** - Watch improvement happen
✅ **Compare difficulty** - Plain vs uneven side-by-side
✅ **Save time** - Don't need full training for testing

### **Disadvantages:**
❌ **Not fully trained** - Won't see optimal performance
❌ **Lower rewards** - Won't reach +300 like the graph
❌ **Still learning** - Agent won't master landing

---

## 🔄 IF YOU WANT BETTER RESULTS LATER

After the 2-hour training, you can:

1. **Continue training:**
   ```python
   # Change back to longer training
   max_training_timesteps = int(3e6)  # 3 million
   ```

2. **Use the checkpoints:**
   - Load the 300K checkpoint
   - Continue from where you left off

3. **Compare the 2-hour results:**
   - Plain vs Uneven at same timesteps
   - Fair comparison!

---

## ✅ READY TO RUN!

**Everything is configured for 2-hour training runs.**

### **Next Steps:**
1. ✅ Run plain surface (2 hours)
2. ✅ Run uneven terrain (2 hours)
3. ✅ Compare results
4. ✅ Decide if you want longer training

**Total commitment: 4 hours (2 hours each)** 🚀

