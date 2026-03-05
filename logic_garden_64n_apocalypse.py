"""
SOVEREIGN CODE: logic_garden_64n_apocalypse_fixed.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: Apocalypse Now (Ride of the Valkyries)
FIX: Resolved UnboundLocalError in Sky Gradient loop.
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
OUT_DIR = "frames_64n_apocalypse"
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

def draw_line(canvas, x0, y0, x1, y1, c_id):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        draw_pixel(canvas, x0, y0, c_id)
        if x0 == x1 and y0 == y1: break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_huey(canvas, x, y, scale, angle, rotor_frame, color_id=0):
    # Pitch simulates hovering
    pitch = int(math.sin(angle) * 3)
    
    # Coordinates
    cabin_w = 12 * scale
    cabin_h = 6 * scale
    
    # 1. BODY (Black Silhouette)
    draw_rect(canvas, x - cabin_w/2, y - cabin_h/2 + pitch, cabin_w, cabin_h, color_id)
    
    # Tail
    tail_len = 12 * scale
    tail_start_x = x - cabin_w/2
    tail_start_y = y + pitch
    tail_end_x = tail_start_x - tail_len
    tail_end_y = tail_start_y - 2*scale
    draw_line(canvas, tail_start_x, tail_start_y, tail_end_x, tail_end_y, color_id)
    
    # Tail Rotor
    draw_line(canvas, tail_end_x, tail_end_y-3*scale, tail_end_x, tail_end_y+3*scale, color_id)
    
    # Skids
    skid_y = y + cabin_h/2 + pitch
    draw_line(canvas, x - 4*scale, skid_y + 1*scale, x + 4*scale, skid_y + 1*scale, color_id)
    draw_line(canvas, x - 2*scale, skid_y, x - 2*scale, skid_y + 1*scale, color_id)
    draw_line(canvas, x + 2*scale, skid_y, x + 2*scale, skid_y + 1*scale, color_id)
    
    # 2. MAIN ROTOR
    mast_top_y = y - cabin_h/2 + pitch - 3*scale
    draw_line(canvas, x, y - cabin_h/2 + pitch, x, mast_top_y, color_id)
    
    blade_len = 18 * scale
    if rotor_frame % 2 == 0:
        # FLAT (Wide)
        draw_line(canvas, x - blade_len, mast_top_y, x + blade_len, mast_top_y, color_id)
        draw_line(canvas, x - blade_len, mast_top_y+1, x + blade_len, mast_top_y+1, color_id)
    else:
        # X (Spin)
        draw_line(canvas, x - 4*scale, mast_top_y - 2, x + 4*scale, mast_top_y + 2, color_id)
        draw_line(canvas, x - 4*scale, mast_top_y + 2, x + 4*scale, mast_top_y - 2, color_id)

def run():
    print("LOGIC GARDEN 64n: RIDE OF THE VALKYRIES (FIXED)")
    
    # SCROLL BUFFER (Jungle Hills)
    jungle_offset = 0
    
    explosions = []
    
    for f in range(TOTAL_FRAMES):
        # 1. SKY GENERATION (GRADIENT + DITHER)
        # We iterate Y, but for dither zones we iterate X
        
        for y in range(H):
            # Base Color Definition
            if y < 40: base_c = 7   # Yellow
            elif y < 80: base_c = 8 # Orange
            elif y < 120: base_c = 2 # Red
            elif y < 150: base_c = 9 # Brown
            else: base_c = 0 # Ground
            
            # Fast Fill Line
            draw_rect(GRID, 0, y, W, 1, base_c)
            
            # DITHER ZONES (The Fix: Explicit X loops)
            # Zone 1: Yellow -> Orange (Rows 35-45)
            if 35 < y < 45:
                for x in range(W):
                    if (x + y) % 2 == 0:
                        draw_pixel(GRID, x, y, 8) # Mix Orange into Yellow
                        
            # Zone 2: Orange -> Red (Rows 75-85)
            if 75 < y < 85:
                for x in range(W):
                    if (x + y) % 2 == 0:
                        draw_pixel(GRID, x, y, 2) # Mix Red into Orange

            # Zone 3: Red -> Brown (Rows 115-125)
            if 115 < y < 125:
                for x in range(W):
                    if (x + y) % 2 == 0:
                        draw_pixel(GRID, x, y, 9) # Mix Brown into Red

        # 2. SUN (The Napalm Orb)
        # Low center sun
        sun_x, sun_y = W//2, 100
        for sy in range(sun_y - 15, sun_y + 15):
            for sx in range(sun_x - 15, sun_x + 15):
                dist = math.sqrt((sx-sun_x)**2 + (sy-sun_y)**2)
                if dist < 15:
                    col = 7 if dist < 8 else 8 # Yellow core, Orange rim
                    draw_pixel(GRID, sx, sy, col)

        # 3. JUNGLE SCROLL (Black Silhouette)
        jungle_offset += 2
        for x in range(W):
            # Sine wave hills
            real_x = x + jungle_offset
            h_val = 30 + 10 * math.sin(real_x * 0.05) + 5 * math.sin(real_x * 0.15)
            jy = int(H - h_val)
            draw_rect(GRID, x, jy, 1, H-jy, 0) # Black

        # 4. HUEYS (The Swarm)
        # Formation Flight
        base_h = 60 + 5 * math.sin(f * 0.1)
        
        # Leader
        draw_huey(GRID, W//2 + 20, base_h, 1.0, f*0.1, f)
        # Wingman L
        draw_huey(GRID, W//2 - 15, base_h - 20, 0.8, (f+3)*0.1, f+1)
        # Wingman R
        draw_huey(GRID, W//2 + 45, base_h - 25, 0.8, (f+5)*0.1, f)
        # Distant
        draw_huey(GRID, 20, base_h - 40, 0.5, 0, f)

        # 5. NAPALM (Explosions)
        if f > 20 and random.random() < 0.1:
            explosions.append({'x': random.randint(0, W), 'y': H-10, 'age': 0})
            
        for ex in explosions:
            ex['age'] += 1
            age = ex['age']
            if age < 12:
                r = age * 1.5
                if age < 4: c_ex = 1 # White flash
                elif age < 8: c_ex = 7 # Yellow fire
                else: c_ex = 2 # Red bloom
                
                # Draw circle
                cx, cy = ex['x'], ex['y'] - (age*2) # Rising
                for ey in range(int(cy-r), int(cy+r)):
                    for exx in range(int(cx-r), int(cx+r)):
                        if (exx-cx)**2 + (ey-cy)**2 < r**2:
                            draw_pixel(GRID, exx, ey, c_ex)
                            
        explosions = [e for e in explosions if e['age'] < 12]

        # RENDER
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
