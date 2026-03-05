"""
SOVEREIGN CODE: logic_garden_64p_helmsdeep.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: Battle of Helm's Deep (The Wall Breach)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random
import math

# C64 PALETTE
COLORS = {
    0:  [0, 0, 0],       # Black
    1:  [255, 255, 255], # White
    2:  [136, 0, 0],     # Red
    3:  [170, 255, 238], # Cyan
    4:  [204, 68, 204],  # Purple
    5:  [0, 204, 85],    # Green
    6:  [0, 0, 170],     # Blue
    7:  [238, 238, 119], # Yellow
    8:  [221, 136, 85],  # Orange
    9:  [102, 68, 0],    # Brown
    10: [255, 119, 119], # Light Red
    11: [51, 51, 51],    # Dark Grey
    12: [119, 119, 119], # Grey
    13: [170, 255, 102], # Light Green
    14: [0, 136, 255],   # Light Blue
    15: [187, 187, 187]  # Light Grey
}

# CONFIG
FPS = 15
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64p_helmsdeep"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 110, 196 
GRID = np.zeros((H, W, 3), dtype=np.uint8)

def draw_pixel(canvas, x, y, c_id):
    if 0 <= x < W and 0 <= y < H:
        canvas[int(y), int(x)] = COLORS[c_id]

def draw_rect(canvas, x, y, w, h, c_id):
    x, y, w, h = int(x), int(y), int(w), int(h)
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(W, x+w)
    y2 = min(H, y+h)
    if x1 < x2 and y1 < y2:
        canvas[y1:y2, x1:x2] = COLORS[c_id]

def run():
    print("LOGIC GARDEN 64p: THE HORN OF HELM HAMMERHAND")
    
    # ENTITIES
    # The Wall geometry
    wall_y = 120
    drain_x = 60
    
    # Swarm
    uruks = []
    for _ in range(200):
        uruks.append({
            'x': random.randint(0, W), 
            'y': random.randint(wall_y + 10, H),
            'c': random.choice([0, 11]) # Black/Dark Grey
        })
        
    # Torch Runner
    runner = {'x': 20, 'y': H-10, 'active': False, 'dead': False}
    
    # Arrows
    arrows = []
    
    # Explosion
    explosion_r = 0
    explode_triggered = False
    
    for f in range(TOTAL_FRAMES):
        # 1. BACKGROUND (Night/Rain)
        # Gradient Dark Blue #6 -> Black #0
        for y in range(H):
            c = 0
            if y < 100: c = 6 # Blue Sky
            if y > 50 and y < 100 and (y+f)%2 == 0: c = 11 # Clouds
            draw_rect(GRID, 0, y, W, 1, c)
            
        # RAIN (Cyan Streaks)
        for _ in range(50):
            rx = random.randint(0, W)
            ry = random.randint(0, H)
            draw_rect(GRID, rx, ry, 1, 3, 3) # Cyan rain

        # 2. THE WALL
        if not explode_triggered or explosion_r < 10:
            draw_rect(GRID, 0, wall_y, W, 30, 12) # Grey Wall
            # Keep
            draw_rect(GRID, 0, wall_y-40, 30, 70, 12) 
            # Battlement Details
            for bx in range(0, W, 10):
                draw_rect(GRID, bx, wall_y-2, 5, 2, 0) # Gaps
                
            # THE DRAIN (Weakness)
            draw_rect(GRID, drain_x, wall_y+20, 8, 8, 0) # Black hole
        else:
            # BREACHED WALL
            draw_rect(GRID, 0, wall_y, drain_x-10, 30, 12) # Left chunk
            draw_rect(GRID, drain_x+20, wall_y, W-(drain_x+20), 30, 12) # Right chunk
            # Rubble
            draw_rect(GRID, drain_x-10, wall_y+20, 40, 10, 11)

        # 3. THE HORDE (Uruk-hai)
        # Update positions (Move UP towards wall)
        for u in uruks:
            if u['y'] > wall_y + 30:
                u['y'] -= 0.2
            draw_pixel(GRID, u['x'], u['y'], u['c'])
            # Spears?
            if random.random() > 0.9:
                draw_pixel(GRID, u['x'], u['y']-2, 12) # Steel tip

        # 4. DEFENDERS (Elves)
        # On the wall
        for dx in range(0, W, 5):
            draw_pixel(GRID, dx, wall_y-3, 7) # Yellow/Gold (Elves)
            draw_pixel(GRID, dx, wall_y-4, 13) # Cloaks

        # 5. THE RUNNER
        # Starts at frame 30
        if f > 30 and not explode_triggered:
            runner['active'] = True
            
        if runner['active']:
            # Move towards drain
            dx = drain_x - runner['x']
            dy = (wall_y + 24) - runner['y']
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < 2:
                explode_triggered = True
                runner['active'] = False
            else:
                runner['x'] += (dx/dist) * 1.5
                runner['y'] += (dy/dist) * 1.5
                
            # Draw Runner (Berserker)
            rx, ry = runner['x'], runner['y']
            draw_rect(GRID, rx, ry, 4, 4, 8) # Body
            draw_rect(GRID, rx+1, ry-2, 2, 2, 1) # Helmet
            # THE TORCH (Bright)
            draw_rect(GRID, rx+2, ry-4, 2, 4, 2) # Red Handle
            draw_rect(GRID, rx+1, ry-6, 4, 4, 7) # Yellow Fire
            draw_rect(GRID, rx, ry-7, 6, 2, 8) # Orange glow
            
            # Legolas shoots? (Arrows)
            if f % 10 == 0:
                arrows.append({'x': drain_x, 'y': wall_y, 'vx': -0.5, 'vy': 2})
        
        # 6. ARROWS
        for a in arrows:
            a['x'] += a['vx']
            a['y'] += a['vy']
            draw_pixel(GRID, a['x'], a['y'], 15) # White line
            
        # 7. EXPLOSION
        if explode_triggered:
            explosion_r += 2
            # Draw Circle
            cx, cy = drain_x + 4, wall_y + 24
            
            # Flash Screen White for first 2 frames
            if explosion_r < 6:
                GRID[:, :] = COLORS[1]
            else:
                # Expanding Fireball
                for y in range(H):
                    for x in range(W):
                        d = math.sqrt((x-cx)**2 + (y-cy)**2)
                        if d < explosion_r:
                            # Center White -> Yellow -> Red -> Smoke
                            if d < explosion_r * 0.3: c = 1
                            elif d < explosion_r * 0.6: c = 7
                            elif d < explosion_r * 0.8: c = 8
                            else: c = 2
                            draw_pixel(GRID, x, y, c)
                            
                # Flying Debris (Rocks)
                for _ in range(10):
                    ox = cx + random.randint(-explosion_r, explosion_r)
                    oy = cy + random.randint(-explosion_r, explosion_r)
                    if 0 <= ox < W and 0 <= oy < H:
                         draw_pixel(GRID, ox, oy, 11)

        # RENDER
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
