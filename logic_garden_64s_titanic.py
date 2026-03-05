"""
SOVEREIGN CODE: logic_garden_64s_titanic.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: Titanic (King of the World)
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
    3:  [170, 255, 238], # Cyan (Sky)
    4:  [204, 68, 204],  # Purple
    5:  [0, 204, 85],    # Green
    6:  [0, 0, 170],     # Blue (Ocean)
    7:  [238, 238, 119], # Yellow
    8:  [221, 136, 85],  # Orange
    9:  [102, 68, 0],    # Brown (Hair)
    10: [255, 119, 119], # Light Red
    11: [51, 51, 51],    # Dark Grey
    12: [119, 119, 119], # Grey (Dolphins)
    13: [170, 255, 102], # Light Green
    14: [0, 136, 255],   # Light Blue
    15: [187, 187, 187]  # Light Grey
}

# CONFIG
FPS = 15
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64s_titanic"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 110, 196 
GRID = np.zeros((H, W, 3), dtype=np.uint8)

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
        if 0 <= x0 < W and 0 <= y0 < H:
            canvas[y0, x0] = COLORS[c_id]
        if x0 == x1 and y0 == y1: break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def run():
    print("LOGIC GARDEN 64s: KING OF THE WORLD")
    
    # WATER TEXTURE (Scrolling)
    water_offset = 0
    dolphins = []
    
    for f in range(TOTAL_FRAMES):
        # 1. SKY (Cyan Gradient)
        for y in range(80):
            c = 14 # Light Blue
            if y < 40: c = 3 # Cyan
            if y < 10: c = 6 # Deep Blue fade
            draw_rect(GRID, 0, y, W, 1, c)
            
        # 2. OCEAN (Deep Blue #6)
        draw_rect(GRID, 0, 80, W, H-80, 6)
        
        # WAKE EFFECT (Speed)
        water_offset += 4
        # Random white foam specs moving DOWN and OUT from center
        # Center of bow is roughly X=55
        
        # Bow Wave Left
        for y in range(80, H, 2):
            # Parabolic wake
            dist_y = (y - 80)
            wake_x_l = 55 - (dist_y * 0.5) - 10
            wake_x_r = 55 + (dist_y * 0.5) + 10
            
            # Draw foam lines
            noise = random.randint(-5, 5)
            draw_rect(GRID, wake_x_l + noise, y, 4, 1, 1) # White
            draw_rect(GRID, wake_x_r + noise, y, 4, 1, 1) # White
            
            # Fill between wake and ship with "Clipped" water? No.
            
        # 3. THE SHIP (Bow)
        # Black Hull coming from bottom center up to vanish point
        # Vanishing Point roughly (55, 80)
        
        # Railing Height
        rail_y = 100
        
        # Draw Hull (Black Triangle)
        # Scanline poly fill
        for y in range(rail_y, H):
            width = (y - rail_y) * 0.8 + 10
            start_x = 55 - width/2
            draw_rect(GRID, start_x, y, width, 1, 0) # Black Hull
            
            # Railing (White)
            if y == rail_y:
                draw_rect(GRID, start_x, y-2, width, 2, 1) # Top Rail
            
            # Deck (Brown #9)
            if y > rail_y and y < rail_y + 30:
                 # Perspective deck
                 draw_rect(GRID, start_x+2, y, width-4, 1, 9)

        # 4. JACK DAWSON
        jx, jy = 55, rail_y - 2
        
        # Legs (Black Trousers)
        draw_rect(GRID, jx-2, jy-10, 4, 10, 0)
        
        # Torso (White Shirt/Suspenders?) -> Grey/White #1
        draw_rect(GRID, jx-3, jy-22, 6, 12, 1)
        # Suspenders (Brown pixels)
        draw_rect(GRID, jx-2, jy-22, 1, 12, 9)
        draw_rect(GRID, jx+1, jy-22, 1, 12, 9)
        
        # Head (Flesh #8)
        draw_rect(GRID, jx-2, jy-28, 4, 6, 8)
        # Hair (Brown #9 Floppy)
        draw_rect(GRID, jx-3, jy-29, 6, 3, 9)
        draw_rect(GRID, jx+3, jy-28, 1, 2, 9) # Wind sweep
        
        # ARMS (The Pose)
        # 0-60: Climbing up?
        # 60+: Extended
        
        if f > 60:
            # Extended "King" Pose
            # Left Arm
            draw_line(GRID, jx-3, jy-20, jx-15, jy-22, 1) # Shirt
            draw_rect(GRID, jx-17, jy-23, 2, 2, 8) # Hand
            
            # Right Arm
            draw_line(GRID, jx+3, jy-20, jx+15, jy-22, 1)
            draw_rect(GRID, jx+15, jy-23, 2, 2, 8)
        else:
            # Holding Rail
            draw_line(GRID, jx-3, jy-20, jx-6, jy-5, 1)
            draw_line(GRID, jx+3, jy-20, jx+6, jy-5, 1)

        # 5. DOLPHINS (Jumping in wake)
        if f % 30 == 0:
            dolphins.append({'x': 55 + random.choice([-20, 20]), 'y': 150, 'frame': 0, 'dir': random.choice([-1, 1])})
            
        for d in dolphins:
            d['frame'] += 1
            # Parabolic jump
            t = d['frame'] / 10.0
            dy = -1 * t * (2 - t) * 40 # Up and down
            rx = d['x'] + (t * 10 * d['dir'])
            ry = d['y'] + dy
            
            # Draw Dolphin (Grey #12)
            if t < 2:
                # Arced body
                draw_rect(GRID, rx, ry, 6, 3, 12)
                draw_rect(GRID, rx+2, ry-2, 2, 2, 12) # dorsal
            
        dolphins = [d for d in dolphins if d['frame'] < 25]
        
        # 6. TEXT
        if f > 80:
             # Subtitle
             # "I'M KING OF THE WORLD!"
             pass

        # RENDER
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
