"""
SOVEREIGN CODE: logic_garden_64x_metal_storm_v2.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: CIWS Phalanx Defense (Lead Computing) - PATCHED
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import math
import random

COLORS = {
    0:  [0, 0, 0],       # Black
    1:  [255, 255, 255], # White
    2:  [136, 0, 0],     # Red
    3:  [170, 255, 238], # Cyan
    5:  [0, 204, 85],    # Green
    6:  [0, 0, 170],     # Blue (ADDED)
    7:  [238, 238, 119], # Yellow
    11: [51, 51, 51],    # Dark Grey
    12: [119, 119, 119]  # Grey
}

W, H = 110, 196
OUT_DIR = "frames_64x_metal"
os.makedirs(OUT_DIR, exist_ok=True)
GRID = np.zeros((H, W, 3), dtype=np.uint8)

def draw_rect(canvas, x, y, w, h, c):
    x, y, w, h = int(x), int(y), int(w), int(h)
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(W, x+w), min(H, y+h)
    if x1 < x2 and y1 < y2: canvas[y1:y2, x1:x2] = COLORS[c]

def draw_line(canvas, x0, y0, x1, y1, c):
    # Bresenham
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx = abs(x1 - x0); dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        draw_rect(canvas, x0, y0, 1, 1, c)
        if x0 == x1 and y0 == y1: break
        e2 = 2 * err
        if e2 > -dy: err -= dy; x0 += sx
        if e2 < dx: err += dx; y0 += sy

def run():
    print("LOGIC GARDEN 64x: METAL STORM (PATCHED)")
    
    # ENTITIES
    gun_x, gun_y = W/2, H - 20
    missiles = []
    bullets = []
    explosions = []
    
    for f in range(300):
        GRID[:, :] = COLORS[0]
        
        # 0. UI (Radar Horizon)
        draw_line(GRID, 0, H-20, W, H-20, 6) # Sea level (Blue)
        
        # 1. SPAWN MISSILES (Waves)
        if f % 25 == 0:
            mx = random.choice([10, 20, W-20, W-10])
            vx = (W/2 - mx) * 0.05 # Aim at gun
            missiles.append({'x': mx, 'y': 0, 'vx': vx, 'vy': random.uniform(2.5, 3.5), 'active': True})
            
        # 2. GUN LOGIC (Lead Computing)
        target = None
        min_dist = 999
        for m in missiles:
            if not m['active']: continue
            d = math.sqrt((m['x']-gun_x)**2 + (m['y']-gun_y)**2)
            if d < min_dist:
                min_dist = d
                target = m
        
        aim_x, aim_y = gun_x, 0
        firing = False
        
        if target:
            # PREDICITON
            t_impact = min_dist / 9.0 # Bullet speed approx
            pred_x = target['x'] + (target['vx'] * t_impact)
            pred_y = target['y'] + (target['vy'] * t_impact)
            
            # DRAW COMPUTING LINE (Green Logic)
            if f % 2 == 0:
                draw_line(GRID, gun_x, gun_y, pred_x, pred_y, 5) # Green Vector
                draw_rect(GRID, pred_x-2, pred_y-2, 4, 4, 5) # Kill Box
            
            # FIRE!
            firing = True
            angle = math.atan2(pred_y - gun_y, pred_x - gun_x)
            # Add spread
            angle += random.uniform(-0.05, 0.05)
            bx = math.cos(angle) * 9
            by = math.sin(angle) * 9
            bullets.append({'x': gun_x, 'y': gun_y, 'vx': bx, 'vy': by})

        # 3. UPDATE BULLETS
        active_bal = []
        for b in bullets:
            b['x'] += b['vx']
            b['y'] += b['vy']
            draw_rect(GRID, b['x'], b['y'], 2, 2, 1) # White Tracer
            
            hit = False
            for m in missiles:
                if not m['active']: continue
                if abs(m['x'] - b['x']) < 6 and abs(m['y'] - b['y']) < 6:
                    hit = True
                    m['active'] = False
                    explosions.append({'x': m['x'], 'y': m['y'], 'r': 1})
            
            if 0 < b['x'] < W and 0 < b['y'] < H and not hit:
                active_bal.append(b)
        bullets = active_bal

        # 4. UPDATE MISSILES
        active_mis = []
        for m in missiles:
            if not m['active']: continue
            m['x'] += m['vx']
            m['y'] += m['vy']
            
            # Draw Missile (Red)
            draw_rect(GRID, m['x']-2, m['y'], 4, 6, 2)
            draw_rect(GRID, m['x'], m['y']+2, 2, 2, 7) # Thruster (Yellow)
            
            if m['y'] < H: active_mis.append(m)
        missiles = active_mis

        # 5. EXPLOSIONS
        active_ex = []
        for ex in explosions:
            ex['r'] += 3
            draw_rect(GRID, ex['x']-ex['r']/2, ex['y']-ex['r']/2, ex['r'], ex['r'], 7) # Yellow
            draw_rect(GRID, ex['x']-(ex['r']-2)/2, ex['y']-(ex['r']-2)/2, ex['r']-2, ex['r']-2, 2) # Red Center
            if ex['r'] < 15: active_ex.append(ex)
        explosions = active_ex

        # 6. DRAW GUN
        draw_rect(GRID, gun_x-6, gun_y, 12, 10, 3) 
        if firing:
            draw_rect(GRID, gun_x-4, gun_y-8, 8, 8, 1) # Flash

        # RENDER
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
