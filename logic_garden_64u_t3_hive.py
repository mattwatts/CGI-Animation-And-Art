"""
SOVEREIGN CODE: logic_garden_64u_t3_hive.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: T3 Hive Mind (Focus Fire vs Skirmish)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import math
import random

# C64 PALETTE
COLORS = {
    0:  [0, 0, 0],       # Black
    1:  [255, 255, 255], # White
    2:  [136, 0, 0],     # Red
    3:  [170, 255, 238], # Cyan (Hive)
    4:  [204, 68, 204],  # Purple
    5:  [0, 204, 85],    # Green
    6:  [0, 0, 170],     # Blue
    7:  [238, 238, 119], # Yellow
    8:  [221, 136, 85],  # Orange
    9:  [102, 68, 0],    # Brown
    10: [255, 119, 119], # Light Red (Human)
    11: [51, 51, 51],    # Dark Grey
    12: [119, 119, 119], # Grey (Floor)
    13: [170, 255, 102], # Light Green
    14: [0, 136, 255],   # Light Blue
    15: [187, 187, 187]  # Light Grey
}

# CONFIG
FPS = 15
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64u_t3"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 110, 196
GRID = np.zeros((H, W, 3), dtype=np.uint8)

class Unit:
    def __init__(self, x, y, team):
        self.x = float(x)
        self.y = float(y)
        self.team = team # "CYAN" or "RED"
        self.alive = True
        self.hp = 100
        self.dance_phase = 0
        
def draw_rect(canvas, x, y, w, h, c_id):
    x, y, w, h = int(x), int(y), int(w), int(h)
    x1 = max(0, x); y1 = max(0, y)
    x2 = min(W, x+w); y2 = min(H, y+h)
    if x1 < x2 and y1 < y2:
        canvas[y1:y2, x1:x2] = COLORS[c_id]

def draw_line(canvas, x0, y0, x1, y1, c_id):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    # Bresenham simplified for array
    steps = max(abs(x1-x0), abs(y1-y0))
    if steps == 0: return
    for i in range(steps+1):
        x = int(x0 + (x1-x0)*i/steps)
        y = int(y0 + (y1-y0)*i/steps)
        if 0 <= x < W and 0 <= y < H:
            canvas[y, x] = COLORS[c_id]

def run():
    print("LOGIC GARDEN 64u: TERMINATOR HIVE")
    
    # SETUP TEAMS
    cyan_team = [Unit(10 + i*20, 150, "CYAN") for i in range(5)]
    red_team = [Unit(10 + i*20, 30, "RED") for i in range(5)]
    
    explosions = []
    
    for f in range(TOTAL_FRAMES):
        # CLEAR BG (Dark Grid)
        GRID[:, :] = COLORS[0]
        for y in range(0, H, 20): draw_rect(GRID, 0, y, W, 1, 11)
        for x in range(0, W, 20): draw_rect(GRID, x, 0, 1, H, 11)
        
        # LOGIC CYCLE
        # 1. HIVE MIND (Cyan)
        # Find target: Lowest HP Red Unit that is alive
        target_red = None
        
        # Sort red team by dist or simple index? 
        # Hive Logic: Kill one by one. Index 0 priority.
        active_reds = [r for r in red_team if r.alive]
        if active_reds:
            target_red = active_reds[0] # FOCUS FIRE on the first one
            
        # 2. SKIRMISH MIND (Red)
        # Each red targets random Cyan or closest
        
        # UPDATE & RENDER UNITS
        active_cyans = [c for c in cyan_team if c.alive]
        
        # CYAN LOGIC
        for c in cyan_team:
            if not c.alive: continue
            
            # Draw T-1 Robot
            cx, cy = int(c.x), int(c.y)
            draw_rect(GRID, cx-3, cy, 6, 6, 3) # Body Cyan
            draw_rect(GRID, cx-4, cy+4, 2, 4, 14) # Left Tread
            draw_rect(GRID, cx+2, cy+4, 2, 4, 14) # Right Tread
            
            if not active_reds:
                # VICTORY DANCE (Bobbing)
                c.dance_phase += 0.5
                c.y = 150 + math.sin(c.dance_phase + c.x)*2
                # Arms up?
                draw_rect(GRID, cx-5, cy-2, 2, 4, 3)
                draw_rect(GRID, cx+3, cy-2, 2, 4, 3)
                continue

            # SHOOTING (Focus Fire)
            if f % 5 == 0 and target_red:
                # Draw Beam
                draw_line(GRID, cx, cy, target_red.x, target_red.y, 3) # Cyan Beam
                target_red.hp -= 5 # High damage concentration

        # RED LOGIC
        for r in red_team:
            if not r.alive: continue
            
            # Wiggle (Organic Panic)
            r.x += math.sin(f*0.5 + r.y)*0.5
            
            rx, ry = int(r.x), int(r.y)
            draw_rect(GRID, rx-3, ry, 6, 6, 2) # Body Red
            draw_rect(GRID, rx-1, ry-3, 2, 3, 8) # Head
            
            # Skirmish Fire (Random Target)
            if f % 10 == 0 and active_cyans:
                target_c = random.choice(active_cyans)
                draw_line(GRID, rx, ry, target_c.x, target_c.y, 10) # Weak red shot
                target_c.hp -= 2 # Low damage dispersed
                
            # Death Check
            if r.hp <= 0:
                r.alive = False
                explosions.append({'x': r.x, 'y': r.y, 'f': 0})
        
        # EXPLOSIONS
        for ex in explosions:
            ex['f'] += 1
            rad = ex['f'] * 2
            if rad < 15:
                # Ring
                for y in range(H):
                    for x in range(W):
                        d = math.sqrt((x-ex['x'])**2 + (y-ex['y'])**2)
                        if abs(d - rad) < 2:
                             draw_rect(GRID, x, y, 1, 1, 7) # Fire ring
        
        # HUD TEXT
        if not active_reds:
            # VICTORY
            if (f // 5) % 2 == 0:
                draw_rect(GRID, 30, 90, 50, 10, 3) # Flash winning
        else:
            # LOGIC VISUALIZATION
            # Connect all Cyans to Hive Center
            if active_cyans:
                center_x = sum(c.x for c in active_cyans) / len(active_cyans)
                center_y = sum(c.y for c in active_cyans) / len(active_cyans)
                # Draw Node
                draw_rect(GRID, int(center_x)-2, int(center_y)-2, 4, 4, 1)
                # Lines to units
                for c in active_cyans:
                    draw_line(GRID, int(center_x), int(center_y), c.x, c.y, 11)

        # RENDER FRAME
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
