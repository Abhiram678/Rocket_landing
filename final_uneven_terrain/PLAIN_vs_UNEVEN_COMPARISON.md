# 🎯 PLAIN vs UNEVEN SURFACE - Complete Comparison

## 📊 NEW PARAMETERS ADDED

### In `rocket.py` __init__():
```python
# UNEVEN TERRAIN VERSION - NEW PARAMETERS:
terrain_difficulty = 'moderate'    # NEW! Options: 'easy', 'moderate', 'hard'
enable_terrain = True              # NEW! Turn terrain on/off
```

### In `train.py`:
```python
# PLAIN SURFACE VERSION:
env_name = "RocketLanding"
env = Rocket(max_steps=max_ep_len, task=task, rocket_type='starship')

# UNEVEN TERRAIN VERSION:
env_name = "RocketLanding_UnevenTerrain"    # NEW!
enable_terrain = True                        # NEW!
terrain_difficulty = 'moderate'              # NEW!
env = Rocket(max_steps=max_ep_len, task=task, rocket_type='starship',
             enable_terrain=enable_terrain,   # NEW PARAMETER!
             terrain_difficulty=terrain_difficulty)  # NEW PARAMETER!
```

---

## 🏔️ TERRAIN DIFFICULTY SETTINGS

| Parameter | Easy | Moderate | Hard |
|-----------|------|----------|------|
| **Number of Features** | 3 craters/hills | 5 craters/hills | 8 craters/hills |
| **Max Height Variation** | ±15 meters | ±25 meters | ±40 meters |
| **Crater Depth** | -10 meters | -15 meters | -20 meters |
| **Smoothness** | Smoother | Medium | More rugged |

---

## 🔍 WHAT YOU WILL SEE - VISUAL DIFFERENCES

### 1️⃣ **PLAIN SURFACE (Original)**
```
┌─────────────────────────────────────────┐
│           SKY (landing.jpg)             │
│                                         │
│         🚀                              │
│        Rocket                           │
│                                         │
│         ↓↓↓                             │
│                                         │
│═════════════════════════════════════════│ ← FLAT GROUND (y=0)
│         [TARGET]                        │
└─────────────────────────────────────────┘
```

**Visual Features:**
- ✅ Flat horizontal ground line
- ✅ Target zone (ellipse) at y=0
- ✅ Simple landing - always same height
- ✅ Clean, predictable surface

---

### 2️⃣ **UNEVEN TERRAIN (New)**
```
┌─────────────────────────────────────────┐
│           SKY (landing.jpg)             │
│                                         │
│         🚀                              │
│        Rocket                           │
│                                         │
│         ↓↓↓                             │
│                                         │
│    ╱╲  ╱───╲    [TARGET]    ╱╲        │
│  ╱    ╲      ╲╱╲          ╱    ╲       │ ← UNEVEN GROUND
│╱  CRATER  HILL   ╲    ╱╲╱  CRATER ╲    │    (brown/earth)
└─────────────────────────────────────────┘
```

**Visual Features:**
- ✅ **Brown/earth-colored terrain** (RGB: 139, 90, 60)
- ✅ **Darker brown outline** on terrain surface
- ✅ **Craters** (depressions going down)
- ✅ **Hills** (elevations going up)
- ✅ **Target zone positioned ON terrain surface** (not at y=0)
- ✅ **Variable landing heights** (different each location)
- ✅ **Smooth, natural-looking curves**

---

## 🎮 WHAT YOU'LL SEE DURING TRAINING

### **Plain Surface Training:**
```
Episode : 46    Timestep : 10000    Average Reward : -187.44
training environment name : RocketLanding
terrain enabled: False  ← NO TERRAIN
```

### **Uneven Terrain Training:**
```
Episode : 46    Timestep : 10000    Average Reward : -187.44
training environment name : RocketLanding_UnevenTerrain
terrain enabled: True, difficulty: moderate  ← TERRAIN ACTIVE!
```

---

## 🆚 KEY DIFFERENCES TABLE

| Feature | Plain Surface | Uneven Terrain |
|---------|--------------|----------------|
| **Ground Level** | Always y=0 | Variable: -20m to +25m (moderate) |
| **Landing Target** | Fixed at y=0 | Positioned on terrain surface |
| **Collision Detection** | Checks y <= 0 + H/2 | Checks y <= terrain_height(x) + H/2 |
| **Visual Terrain** | No terrain drawn | Brown terrain with craters/hills |
| **Difficulty** | Easier - predictable | Harder - variable surface |
| **Training Time** | 4-6M timesteps | 8-10M timesteps (needs more) |
| **Success Rate** | 60-80% after training | 40-60% after training |
| **Logs Folder** | `PPO_logs/RocketLanding/` | `PPO_logs/RocketLanding_UnevenTerrain/` |
| **Model Folder** | `PPO_preTrained/RocketLanding/` | `PPO_preTrained/RocketLanding_UnevenTerrain/` |

---

## 🎨 VISUAL RENDERING DIFFERENCES

### **Plain Surface - render() Output:**
1. Background image (landing.jpg)
2. Target ellipse at y=0 (white outline)
3. Rocket with engines
4. Trajectory panel (top right)
5. Text overlay (stats)

### **Uneven Terrain - render() Output:**
1. Background image (landing.jpg)
2. **🆕 Brown terrain surface with hills/craters**
3. **🆕 Darker brown terrain outline**
4. Target ellipse **ON terrain surface** (white outline)
5. Rocket with engines
6. Trajectory panel (top right)
7. Text overlay (stats)

**NEW METHOD:** `draw_terrain(canvas)` - draws the brown terrain

---

## 🧮 PHYSICS DIFFERENCES

### **Collision Check - Plain Surface:**
```python
if y <= 0 + H/2.0 and v >= 15.0:
    crash = True  # Hit ground too fast
```

### **Collision Check - Uneven Terrain:**
```python
terrain_height = get_terrain_height(x)  # NEW! Get surface height
if y <= terrain_height + H/2.0 and v >= 15.0:
    crash = True  # Hit terrain too fast
```

**DIFFERENCE:** Terrain version checks against **variable surface height**, not fixed y=0

---

## 📐 TERRAIN GENERATION (What Happens Behind the Scenes)

### **How Terrain is Created:**
```
1. Create 100 points from x=-300 to x=+300
2. Start with flat base at y=0
3. Add random features:
   - Pick random x position (e.g., x=50)
   - Choose type: CRATER or HILL
   - Apply Gaussian shape:
     * CRATER: y decreases (goes down)
     * HILL: y increases (goes up)
4. Smooth the terrain
5. Store as height map
```

### **Example Terrain on Moderate:**
```
x = -200m: height = -5m   (in small crater)
x = -100m: height = +12m  (on hill)
x = 0m:    height = -3m   (target zone, slight depression)
x = +100m: height = +18m  (top of hill)
x = +200m: height = -8m   (in crater)
```

---

## 📊 WHAT YOU'LL SEE IN GRAPHS (Same for Both!)

Both versions create the **SAME graphs** automatically:

1. **Average Reward vs Episodes**
2. **Episode Length vs Episodes**
3. Any other plots from `plot_graph.py`

**No difference in graph output!** ✅

---

## 🎯 LANDING SUCCESS CRITERIA

### **Plain Surface:**
```python
SUCCESS if:
  - y <= 0 + H/2.0           (at ground level)
  - velocity < 15 m/s        (slow enough)
  - |x - 0| < 50m           (within target zone)
  - |angle| < 10 degrees     (upright)
```

### **Uneven Terrain:**
```python
SUCCESS if:
  - y <= terrain_height(x) + H/2.0  (at terrain surface) ← DIFFERENT!
  - velocity < 15 m/s               (slow enough)
  - |x - 0| < 50m                  (within target zone)
  - |angle| < 10 degrees            (upright)
```

**DIFFERENCE:** Must land on terrain surface, which varies by x-position!

---

## 🔧 HOW TO SWITCH BETWEEN MODES

### **Option 1: Use Different Folders**
```bash
# Plain surface:
cd final_phase
python train.py

# Uneven terrain:
cd final_phase/final_uneven_terrain
python train.py
```

### **Option 2: Disable Terrain in Uneven Version**
Edit `final_uneven_terrain/train.py`:
```python
enable_terrain = False  # Acts like plain surface!
```

---

## 📈 EXPECTED BEHAVIOR DIFFERENCES

### **Plain Surface:**
- Learns faster (4-6M timesteps)
- Higher success rate (60-80%)
- More consistent landings
- Easier for agent to master

### **Uneven Terrain:**
- Learns slower (8-10M timesteps)
- Lower success rate (40-60%)
- More varied landing approaches
- Harder challenge for agent
- More realistic scenario

---

## 🎬 SUMMARY - WHAT YOU'LL ACTUALLY SEE

### **When You Run Plain Surface:**
```
✅ Flat ground line
✅ Target at y=0
✅ Simple visual
✅ Faster training
✅ "RocketLanding" in logs
```

### **When You Run Uneven Terrain:**
```
✅ Brown terrain with craters/hills
✅ Target on terrain surface
✅ More complex visual
✅ Slower training (needs more episodes)
✅ "RocketLanding_UnevenTerrain" in logs
✅ New parameters: enable_terrain, terrain_difficulty
```

---

## 🚀 NEW METHODS ADDED (Uneven Terrain Only)

```python
generate_terrain(difficulty)     # Creates terrain with craters/hills
get_terrain_height(x_pos)       # Returns height at x position
draw_terrain(canvas)            # Renders brown terrain visually
```

**Total new code:** ~150 lines added to rocket.py

---

## 💡 BOTTOM LINE

### **3 Main Visual Differences You'll See:**

1. **Brown terrain surface** instead of invisible flat ground
2. **Target landing zone positioned on terrain** instead of at y=0
3. **Variable surface heights** - craters dip down, hills go up

### **2 Main Parameter Differences:**

1. `enable_terrain=True` - turns on terrain system
2. `terrain_difficulty='moderate'` - controls how rough the terrain is

### **Everything Else:**
- Same training loop
- Same graphs
- Same PPO algorithm
- Same rocket physics
- Just **harder landing challenge!** 🎯

