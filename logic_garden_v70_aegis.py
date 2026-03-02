"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v70_aegis_fixed.py
MODE:   Retro (VIC-II Emulation)
TARGET: AEGIS Weapon System (Saturation Defense)
STYLE:  "The Shield" | 30s | Mass Raid | C64 Palette
STATUS: PATCHED (Fixed Palette Vectors)

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

# --- 1. THE C64 PALETTE (Vectorized) ---
C64 = np.array([
    [0.00, 0.00, 0.00], # 0: Black
    [1.00, 1.00, 1.00], # 1: White (Interceptors)
    [0.53, 0.00, 0.00], # 2: Red (Vampires)
    [0.45, 0.75, 0.79], # 3: Cyan
    [0.55, 0.17, 0.55], # 4: Purple
    [0.37, 0.65, 0.29], # 5: Green (Radar Grid)
    [0.21, 0.16, 0.47], # 6: Blue
    [0.93, 0.94, 0.46], # 7: Yellow (Explosions)
    [0.55, 0.31, 0.08], # 8: Orange
    [0.28, 0.20, 0.00], # 9: Brown
    [0.75, 0.42, 0.43], # 10: Light Red
    [0.33, 0.33, 0.33], # 11: Dark Grey
    [0.47, 0.47, 0.47], # 12: Grey (Ocean)
    [0.63, 0.95, 0.61], # 13: Light Green
    [0.42, 0.37, 0.71], # 14: Light Blue
    [0.70, 0.70, 0.70]  # 15: Light Grey
])

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 30
TOTAL_FRAMES = FPS * DURATION
W, H = 320, 200 # Native Resolution
CX, CY = W//2, H//2

class Entity:
    def __init__(self, x, y, dx, dy, color_idx, type_):
        self.x = float(x); self.y = float(y)
        self.dx = float(dx); self.dy = float(dy)
        self.color_idx = color_idx
        self.type = type_ # "VAMPIRE", "BIRD", "DEBRIS"
        self.alive = True
        self.target = None # For homing
        self.life = 100

def generate_aegis_frames():
    out_dir = "logic_garden_aegis_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[AEGIS] ACQUIRING TARGETS...")
    
    # SYSTEM STATE
    vampires = []
    birds = []
    debris = []
    
    vls_cells = 64 # Ammo count
    rad_angle = 0.0
    
    # RAID PLAN: (Frame, Count)
    raid_plan = [
        (10, 2),   # Wave 1: Probe
        (60, 8),   # Wave 2: Saturation
        (180, 16), # Wave 3: Massive
        (350, 6)   # Wave 4: Leakers
    ]
    
    for f in range(TOTAL_FRAMES):
        # 1. SPAWN LOGIC (Vampires)
        for trig, count in raid_plan:
            if f == trig:
                print(f"  > WARNING: RAID DETECTED ({count} INBOUND)")
                for _ in range(count):
                    angle = random.uniform(0, 6.28)
                    dist = 140 # Outside screen radius (approx)
                    spawn_x = CX + np.cos(angle) * dist
                    spawn_y = CY + np.sin(angle) * dist
                    
                    speed = random.uniform(0.6, 1.2)
                    angle_in = np.arctan2(CY - spawn_y, CX - spawn_x)
                    vx = np.cos(angle_in) * speed
                    vy = np.sin(angle_in) * speed
                    
                    vampires.append(Entity(spawn_x, spawn_y, vx, vy, 2, "VAMPIRE"))
        
        # 2. FIRE CONTROL LOGIC
        # Identify threats without assigned interceptors
        tracked_ids = {id(b.target) for b in birds if b.alive and b.target and b.target.alive}
        
        for v in vampires:
            if v.alive and id(v) not in tracked_ids:
                # Engagement Envelope check
                dist_sq = (v.x - CX)**2 + (v.y - CY)**2
                if dist_sq < 130**2: # Open fire
                    if vls_cells > 0:
                        vls_cells -= 1
                        # Lead computation? No, direct intercept logic
                        spd = 2.8 # Birds are faster than vamps
                        b_angle = np.arctan2(v.y - CY, v.x - CX)
                        bx = np.cos(b_angle) * spd
                        by = np.sin(b_angle) * spd
                        
                        bird = Entity(CX, CY, bx, by, 1, "BIRD")
                        bird.target = v
                        birds.append(bird)

        # 3. PHYSICS
        # Vampires
        active_v = []
        for v in vampires:
            if v.alive:
                v.x += v.dx; v.y += v.dy
                # Impact Ship?
                if abs(v.x - CX) < 5 and abs(v.y - CY) < 5:
                    v.alive = False # Detonate
                    # Debris
                    for _ in range(10):
                        debris.append(Entity(CX, CY, random.uniform(-2,2), random.uniform(-2,2), 8, "DEBRIS"))
                else:
                    active_v.append(v)
        vampires = active_v
        
        # Birds
        active_b = []
        for b in birds:
            if b.alive:
                if b.target and b.target.alive:
                    # Guided Flight (Proportional Nav)
                    tx, ty = b.target.x, b.target.y
                    curr_angle = np.arctan2(b.dy, b.dx)
                    des_angle = np.arctan2(ty - b.y, tx - b.x)
                    
                    # Turn rate
                    diff = (des_angle - curr_angle + np.pi) % (2*np.pi) - np.pi
                    curr_angle += np.clip(diff, -0.25, 0.25) # High G turn
                    
                    spd = 3.0
                    b.dx = np.cos(curr_angle) * spd
                    b.dy = np.sin(curr_angle) * spd
                    b.x += b.dx; b.y += b.dy
                    
                    # Fuse
                    if (b.x - tx)**2 + (b.y - ty)**2 < 25: # 5px radius
                        b.alive = False
                        b.target.alive = False
                        # Boom
                        for _ in range(5):
                            debris.append(Entity(tx, ty, random.uniform(-1,1), random.uniform(-1,1), 7, "DEBRIS"))
                else:
                    b.alive = False # Self destruct
            if b.alive: active_b.append(b)
        birds = active_b
        
        # Debris
        active_d = []
        for d in debris:
            d.x += d.dx; d.y += d.dy
            d.life -= 4
            d.dx *= 0.9; d.dy *= 0.9
            if d.life > 0: active_d.append(d)
        debris = active_d

        # 4. RENDER
        buffer = np.zeros((H, W, 3))
        # Background Black
        
        # Radar Crosshair (Dim Green)
        c_green = C64[5]
        buffer[CY, :] = c_green * 0.3
        buffer[:, CX] = c_green * 0.3
        
        # Radar Sweep
        rad_angle += 0.2
        # Draw sweep line?
        # Let's map polar to cartesian
        sw_x = CX + np.cos(rad_angle) * 100
        sw_y = CY + np.sin(rad_angle) * 100
        # Bresenham line for sweep?
        # Simple for loop for clarity
        for r in range(0, 100, 2):
            rx = int(CX + np.cos(rad_angle) * r)
            ry = int(CY + np.sin(rad_angle) * r)
            if 0 <= rx < W and 0 <= ry < H:
                buffer[ry, rx] = c_green * 0.6

        # Ship
        buffer[CY-1:CY+2, CX-1:CX+2] = C64[3]
        
        # Entities
        for v in vampires:
            if 0 <= int(v.x) < W and 0 <= int(v.y) < H:
                buffer[int(v.y), int(v.x)] = C64[v.color_idx]
                
        for b in birds:
            if 0 <= int(b.x) < W and 0 <= int(b.y) < H:
                 buffer[int(b.y), int(b.x)] = C64[b.color_idx]
                 
        for d in debris:
            if 0 <= int(d.x) < W and 0 <= int(d.y) < H:
                # Fade Yellow to Red
                col = C64[7] if d.life > 30 else C64[2]
                buffer[int(d.y), int(d.x)] = col

        # 5. OVERLAY
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        
        ax.imshow(buffer, interpolation='nearest', aspect='auto')
        
        # HUD Text
        v_col = "white" if vls_cells > 0 else "red"
        ax.text(W/2, H-10, f"AMMO: {vls_cells} | THREATS: {len(vampires)}", color=v_col, 
                ha='center', fontfamily='monospace', fontweight='bold', fontsize=18)
        
        ax.text(10, 10, "LOGIC GARDEN 70: AEGIS", color="#55ff55", 
                ha='left', fontfamily='monospace', fontweight='bold', fontsize=15)
        
        filename = os.path.join(out_dir, f"aegis_{f:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if f % 60 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES}")

if __name__ == "__main__":
    generate_aegis_frames()
