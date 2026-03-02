"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v70_c64_madman.py
MODE:   Retro (VIC-II Emulation)
TARGET: 4-Way Tank Deathmatch (C64 Port)
STYLE:  "The Madman" | 30s | C64 Palette | 4K Upscale

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

# --- 1. THE VIC-II PALETTE ---
C64 = {
    0:  [0.00, 0.00, 0.00], # Black
    1:  [1.00, 1.00, 1.00], # White
    2:  [0.53, 0.00, 0.00], # Red
    3:  [0.45, 0.75, 0.79], # Cyan
    4:  [0.55, 0.17, 0.55], # Purple
    5:  [0.37, 0.65, 0.29], # Green
    6:  [0.21, 0.16, 0.47], # Blue
    7:  [0.93, 0.94, 0.46], # Yellow
    8:  [0.55, 0.31, 0.08], # Orange
    9:  [0.28, 0.20, 0.00], # Brown
    10: [0.75, 0.42, 0.43], # Light Red
    11: [0.33, 0.33, 0.33], # Dark Grey
    12: [0.47, 0.47, 0.47], # Grey
    13: [0.63, 0.95, 0.61], # Light Green
    14: [0.42, 0.37, 0.71], # Light Blue
    15: [0.70, 0.70, 0.70]  # Light Grey
}

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 30
TOTAL_FRAMES = FPS * DURATION
W, H = 320, 200 # Native Resolution
BORDER_W, BORDER_H = 35, 25

class PixelTank:
    def __init__(self, uid, x, y, color_idx):
        self.uid = uid
        self.x = float(x)
        self.y = float(y)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.angle = random.uniform(0, 6.28)
        self.color = color_idx
        self.alive = True
        self.hp = 100
        self.turret_angle = self.angle
        self.cooldown = 0
    
    def update(self, targets):
        if not self.alive: return None
        
        # AI: MADMAN (Nearest Neighbor Aggression)
        target = None
        min_d = 100000
        
        for t in targets:
            if t.uid == self.uid or not t.alive: continue
            d = (t.x - self.x)**2 + (t.y - self.y)**2
            if d < min_d:
                min_d = d
                target = t
        
        action = None
        if target:
            # Move Logic: Orbit / Ram
            dx = target.x - self.x
            dy = target.y - self.y
            dist = np.sqrt(dx*dx + dy*dy)
            
            # Desired Heading
            dh = np.arctan2(dy, dx)
            
            # Strafe?
            if dist < 60: # Too close, strafe/retreat
                dh += 1.5 # 90 deg
            
            # Smooth Turn
            diff = (dh - self.angle + np.pi) % (2*np.pi) - np.pi
            self.angle += np.clip(diff, -0.2, 0.2)
            
            # Thrust
            speed = 1.5
            self.vel_x += np.cos(self.angle) * 0.2
            self.vel_y += np.sin(self.angle) * 0.2
            
            # Turret Logic (Lead)
            lead_x = target.x + target.vel_x * 5
            lead_y = target.y + target.vel_y * 5
            aim_angle = np.arctan2(lead_y - self.y, lead_x - self.x)
            
            t_diff = (aim_angle - self.turret_angle + np.pi) % (2*np.pi) - np.pi
            self.turret_angle += np.clip(t_diff, -0.4, 0.4)
            
            # Fire
            self.cooldown -= 1
            if abs(t_diff) < 0.3 and self.cooldown <= 0:
                self.cooldown = random.randint(10, 20)
                action = "FIRE"

        # Physics (Friction)
        self.vel_x *= 0.92
        self.vel_y *= 0.92
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Bounds (Bounce)
        if self.x < BORDER_W: self.x = BORDER_W; self.vel_x *= -0.8
        if self.x > W-BORDER_W: self.x = W-BORDER_W; self.vel_x *= -0.8
        if self.y < BORDER_H: self.y = BORDER_H; self.vel_y *= -0.8
        if self.y > H-BORDER_H: self.y = H-BORDER_H; self.vel_y *= -0.8
        
        return action

def draw_line(buffer, x0, y0, x1, y1, color):
    # Bresenham
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    while True:
        if 0 <= x0 < W and 0 <= y0 < H:
            buffer[y0, x0] = color
        if x0 == x1 and y0 == y1: break
        e2 = 2 * err
        if e2 > -dy: err -= dy; x0 += sx
        if e2 < dx: err += dx; y0 += sy

def generate_madman():
    out_dir = "logic_garden_madman_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[C64] Loading MADMAN Protocol...")
    
    # 4 Tanks
    tanks = [
        PixelTank(0, BORDER_W+20, BORDER_H+20, 3), # Cyan
        PixelTank(1, W-BORDER_W-20, BORDER_H+20, 4), # Magenta (Purple)
        PixelTank(2, W-BORDER_W-20, H-BORDER_H-20, 7), # Yellow
        PixelTank(3, BORDER_W+20, H-BORDER_H-20, 5) # Green
    ]
    
    projectiles = []
    debris = []
    # Persistent track layer (Video RAM)
    vram_tracks = np.zeros((H, W), dtype=int) 
    
    border_color = 6 # Blue default
    shake = 0
    
    for i in range(TOTAL_FRAMES):
        # 1. INIT BUFFER
        buffer = np.zeros((H, W, 3))
        
        # Shake effect
        off_x = random.randint(-shake, shake) if shake > 0 else 0
        off_y = random.randint(-shake, shake) if shake > 0 else 0
        shake = max(0, shake - 1)
        
        if border_color != 6: border_color = 6 # Reset border flash
        
        # Fill Border
        buffer[:, :] = C64[border_color]
        
        # Fill Play Area (Black)
        # Apply shake offset to view window? No, just shake border?
        # Let's keep play area fixed relative to buffer indices for simplicity
        # Track layer
        
        # Composite Tracks onto Play Area
        # We manually check bounds
        for y in range(BORDER_H, H-BORDER_H):
            for x in range(BORDER_W, W-BORDER_W):
                if vram_tracks[y, x] > 0:
                    buffer[y, x] = C64[vram_tracks[y, x]]
                else:
                    buffer[y, x] = C64[0] # Black BG
                    
        # 2. UPDATE TANKS
        for t in tanks:
            act = t.update(tanks)
            
            if t.alive:
                # Deposit Tracks (Grey dots)
                if i % 3 == 0:
                    tx, ty = int(t.x), int(t.y)
                    if BORDER_H < ty < H-BORDER_H and BORDER_W < tx < W-BORDER_W:
                        vram_tracks[ty, tx] = 11 # Dark Grey
                        # Jitter for width
                        vram_tracks[ty+1, tx] = 11
                
                # Fire
                if act == "FIRE":
                    # Velocity
                    spd = 4.0
                    vx = np.cos(t.turret_angle) * spd + t.vel_x * 0.5
                    vy = np.sin(t.turret_angle) * spd + t.vel_y * 0.5
                    # Offset muzzle
                    mx = t.x + np.cos(t.turret_angle) * 8
                    my = t.y + np.sin(t.turret_angle) * 8
                    projectiles.append({'x':mx, 'y':my, 'vx':vx, 'vy':vy, 'owner':t.uid, 'color':1}) # White bullet

        # 3. PROJECTILES
        active_proj = []
        for p in projectiles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Hit Check
            hit = False
            for t in tanks:
                if t.alive and t.uid != p['owner']:
                    if abs(p['x'] - t.x) < 6 and abs(p['y'] - t.y) < 6:
                        # HIT
                        hit = True
                        t.hp -= 15
                        # Debris (Sparks)
                        for _ in range(4):
                            debris.append({'x':p['x'], 'y':p['y'], 'vx':random.uniform(-2,2), 'vy':random.uniform(-2,2), 'life':10, 'color':t.color})
                        
                        if t.hp <= 0:
                            t.alive = False
                            # BIG BOOM
                            shake = 5
                            border_color = 2 # RED FLASH
                            for _ in range(30):
                                debris.append({'x':t.x, 'y':t.y, 'vx':random.uniform(-4,4), 'vy':random.uniform(-4,4), 'life':30, 'color':t.color})
                                debris.append({'x':t.x, 'y':t.y, 'vx':random.uniform(-4,4), 'vy':random.uniform(-4,4), 'life':20, 'color':7}) # Fire
                        break
            
            if not hit and BORDER_W < p['x'] < W-BORDER_W and BORDER_H < p['y'] < H-BORDER_H:
                active_proj.append(p)
        projectiles = active_proj

        # 4. DEBRIS
        active_deb = []
        for d in debris:
            d['x'] += d['vx']
            d['y'] += d['vy']
            d['life'] -= 1
            if d['life'] > 0: active_deb.append(d)
        debris = active_deb

        # 5. RENDER SPRITES
        
        # Projectiles (2x2 pixels)
        for p in projectiles:
            px, py = int(p['x']), int(p['y'])
            if 0 <= px < W-1 and 0 <= py < H-1:
                col = C64[p['color']]
                buffer[py, px] = col
                buffer[py+1, px] = col
                buffer[py, px+1] = col
            
        # Debris (Single pixel)
        for d in debris:
            px, py = int(d['x']), int(d['y'])
            if 0 <= px < W and 0 <= py < H:
                buffer[py, px] = C64[d['color'] if d['life'] > 5 else 11]

        # Tanks (Procedural Sprite)
        for t in tanks:
            if t.alive:
                col = C64[t.color]
                cx, cy = int(t.x), int(t.y)
                # Draw Body (5x5 block)
                for y in range(cy-2, cy+3):
                    for x in range(cx-2, cx+3):
                        if 0 <= x < W and 0 <= y < H:
                           buffer[y, x] = col
                # Draw Turret Line
                tx = cx + np.cos(t.turret_angle) * 8
                ty = cy + np.sin(t.turret_angle) * 8
                draw_line(buffer, cx, cy, tx, ty, t.color)
        
        # 6. TEXT OVERLAY
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        
        ax.imshow(buffer, interpolation='nearest', aspect='auto')
        
        # HUD Text
        alive_count = sum(1 for t in tanks if t.alive)
        hud_col = "#aaaaaa"
        ax.text(W/2, BORDER_H - 5, f"SURVIVORS: {alive_count}", color=hud_col, ha='center',
                fontfamily='monospace', fontweight='bold', fontsize=18)
        
        ax.text(W/2, H - BORDER_H + 15, "THE HARD KILL [MADMAN]", color=hud_col, ha='center',
                fontfamily='monospace', fontweight='bold', fontsize=20)
        
        filename = os.path.join(out_dir, f"madman_{i:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES} | Active: {alive_count}")

if __name__ == "__main__":
    generate_madman()
