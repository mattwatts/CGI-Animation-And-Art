"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v70_c64_tank.py
MODE:   Retro (VIC-II Emulation)
TARGET: The Little Tank (8-Bit Demake)
STYLE:  "The 8-Bit War" | 30s | C64 Palette | Nearest Neighbor

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

# --- 1. THE VIC-II PALETTE ---
# Authentic RGB values
C64 = [
    [0.00, 0.00, 0.00], # 0: Black
    [1.00, 1.00, 1.00], # 1: White
    [0.53, 0.00, 0.00], # 2: Red
    [0.45, 0.75, 0.79], # 3: Cyan
    [0.55, 0.17, 0.55], # 4: Purple
    [0.37, 0.65, 0.29], # 5: Green
    [0.21, 0.16, 0.47], # 6: Blue (Border)
    [0.93, 0.94, 0.46], # 7: Yellow
    [0.55, 0.31, 0.08], # 8: Orange
    [0.28, 0.20, 0.00], # 9: Brown
    [0.75, 0.42, 0.43], # 10: Light Red
    [0.33, 0.33, 0.33], # 11: Dark Grey
    [0.47, 0.47, 0.47], # 12: Grey
    [0.63, 0.95, 0.61], # 13: Light Green
    [0.42, 0.37, 0.71], # 14: Light Blue
    [0.70, 0.70, 0.70]  # 15: Light Grey
]

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 30
TOTAL_FRAMES = FPS * DURATION
W, H = 320, 200 # Native Resolution

class Sprite:
    def __init__(self, x, y, dx, dy, color, type_):
        self.x = float(x)
        self.y = float(y)
        self.dx = float(dx)
        self.dy = float(dy)
        self.color = color
        self.type = type_ # "TANK", "ENEMY", "BULLET", "DEBRIS"
        self.alive = True
        self.life = 100

def draw_pixel_line(buffer, x0, y0, x1, y1, color_idx):
    # Bresenham's implementation for scanning the buffer
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    while True:
        if 0 <= x0 < W and 0 <= y0 < H:
            buffer[y0, x0] = C64[color_idx]
        if x0 == x1 and y0 == y1: break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def generate_demake():
    out_dir = "logic_garden_8bit_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[C64] Loading Sprite Data into $D000...")

    # GAME STATE
    hero_angle = 0.0
    projectiles = []
    enemies = []
    debris = []
    
    kills = 0
    cooldown = 0
    
    # Border Logic
    border_w = 40
    border_h = 25
    
    for i in range(TOTAL_FRAMES):
        # 1. INIT VIDEO RAM
        # Fill Border Color (Blue or Black? Let's go Black for space feels)
        # Actually classic C64 looks cool with Blue border
        buffer = np.zeros((H, W, 3))
        buffer[:, :] = C64[6] # Blue Border
        
        # Screen Area (Black)
        buffer[border_h:H-border_h, border_w:W-border_w] = C64[0]
        
        # 2. HERO LOGIC (Center)
        cx, cy = W//2, H//2
        
        # Find Target
        target = None
        min_d = 9999
        for e in enemies:
            d = (e.x - cx)**2 + (e.y - cy)**2
            if d < min_d:
                min_d = d
                target = e
        
        # Aim
        if target:
            target_a = np.arctan2(target.y - cy, target.x - cx)
            # Instant snap for 8-bit responsiveness
            hero_angle = target_a
            
            # Fire?
            if cooldown <= 0:
                # Shoot
                p_dx = np.cos(hero_angle) * 4.0 # Fast bullet
                p_dy = np.sin(hero_angle) * 4.0
                projectiles.append(Sprite(cx, cy, p_dx, p_dy, 1, "BULLET")) # White Bullet
                cooldown = 5
        
        cooldown -= 1
        
        # 3. SPAWN ENEMIES
        if i % 15 == 0:
            # Spawn at screen edge
            side = random.randint(0, 3)
            ex, ey = 0,0
            if side == 0: ex, ey = border_w, random.randint(border_h, H-border_h) # Left
            elif side == 1: ex, ey = W-border_w-1, random.randint(border_h, H-border_h) # Right
            elif side == 2: ex, ey = random.randint(border_w, W-border_w), border_h # Top
            elif side == 3: ex, ey = random.randint(border_w, W-border_w), H-border_h-1 # Bottom
            
            # Velocity towards center
            ea = np.arctan2(cy - ey, cx - ex)
            vel = 1.0 # Pixel speed
            enemies.append(Sprite(ex, ey, np.cos(ea)*vel, np.sin(ea)*vel, 2, "ENEMY")) # Red Enemy
            
        # 4. PHYSICS UPDATE
        # Projectiles
        active_proj = []
        for p in projectiles:
            p.x += p.dx; p.y += p.dy
            # Hit check
            hit = False
            for e in enemies:
                if abs(p.x - e.x) < 4 and abs(p.y - e.y) < 4:
                    e.alive = False
                    hit = True
                    kills += 1
                    # Spawn Debris
                    for _ in range(5):
                        debris.append(Sprite(e.x, e.y, random.uniform(-2,2), random.uniform(-2,2), 7, "DEBRIS")) # Yellow sparks
                    break
            
            if not hit and border_w < p.x < W-border_w and border_h < p.y < H-border_h:
                active_proj.append(p)
        projectiles = active_proj
        
        # Enemies
        active_enemies = []
        for e in enemies:
            if e.alive:
                e.x += e.dx; e.y += e.dy
                # Hit Hero?
                if abs(e.x - cx) < 6 and abs(e.y - cy) < 6:
                     # Impact! (Shake screen?)
                     e.alive = False 
                
                # Boundary check (if they slide past center)
                if border_w < e.x < W-border_w and border_h < e.y < H-border_h:
                    active_enemies.append(e)
        enemies = active_enemies
        
        # Debris
        active_debris = []
        for d in debris:
            d.x += d.dx; d.y += d.dy
            d.life -= 5
            if d.life > 0: active_debris.append(d)
        debris = active_debris
            
        # 5. RENDER SPRITES
        
        # Draw Hero (Cyan Block + Barrel)
        # Body
        c = C64[3]
        for y in range(cy-3, cy+3):
            for x in range(cx-3, cx+3):
                buffer[y, x] = c
        # Barrel
        bx = cx + np.cos(hero_angle) * 8
        by = cy + np.sin(hero_angle) * 8
        draw_pixel_line(buffer, cx, cy, bx, by, 3)
        
        # Draw Enemies (Red X shape)
        for e in enemies:
            color = C64[e.color]
            px, py = int(e.x), int(e.y)
            if 0 <= px < W and 0 <= py < H:
                buffer[py, px] = color
                # Make it look like a little Invader
                try:
                    buffer[py, px-1] = color; buffer[py, px+1] = color
                    buffer[py-1, px] = color; buffer[py+1, px] = color
                except: pass
                
        # Draw Projectiles (White Dot)
        for p in projectiles:
            color = C64[p.color]
            px, py = int(p.x), int(p.y)
            if 0 <= px < W and 0 <= py < H:
                buffer[py, px] = color
                
        # Draw Debris (Yellow Dot)
        for d in debris:
            color = C64[d.color]
            px, py = int(d.x), int(d.y)
            if 0 <= px < W and 0 <= py < H:
                buffer[py, px] = C64[7] if d.life > 50 else C64[8] # Fade Yellow->Orange
        
        # 6. TEXT OVERLAY (PETSCII)
        # Using Matplotlib text but placing it relative to the buffer
        # Plot Frame
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        
        ax.imshow(buffer, interpolation='nearest') # The 8-bit look
        
        # Score HUD
        score_str = f"SCORE: {kills:06d}"
        ax.text(border_w, border_h - 5, score_str, color="#aaaaFF", ha='left', 
                fontfamily='monospace', fontweight='bold', fontsize=20)
        
        ax.text(W/2, H - border_h + 15, "LOGIC GARDEN 70: 8-BIT WAR", color="#aaaaFF", ha='center', 
                fontfamily='monospace', fontweight='bold', fontsize=18)
        
        filename = os.path.join(out_dir, f"c64_tank_{i:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES} | Kills: {kills}")

if __name__ == "__main__":
    generate_demake()
