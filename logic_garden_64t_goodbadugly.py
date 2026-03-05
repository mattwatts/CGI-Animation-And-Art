"""
SOVEREIGN CODE: logic_garden_64t_goodbadugly.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: The Good, The Bad, and The Ugly (Sad Hill Standoff)
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
    7:  [238, 238, 119], # Yellow (Sand)
    8:  [221, 136, 85],  # Orange (Skin/Clay)
    9:  [102, 68, 0],    # Brown (Wood/Poncho)
    10: [255, 119, 119], # Light Red (Sunburn)
    11: [51, 51, 51],    # Dark Grey
    12: [119, 119, 119], # Grey (Stone)
    13: [170, 255, 102], # Light Green
    14: [0, 136, 255],   # Light Blue (Sky)
    15: [187, 187, 187]  # Light Grey
}

# CONFIG
FPS = 15
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64t_goodbadugly"
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

def draw_wide_shot(canvas, f):
    # Sad Hill Arena (Top Down / Isometric)
    # Ground: Yellow #7 / Orange #8 Dither
    for y in range(H):
        draw_rect(canvas, 0, y, W, 1, 7 if y % 2 == 0 else 8)
        
    # The Circle (Stone center)
    cx, cy = W//2, H//2
    r = 30
    # Draw Stone Circle logic
    for y in range(cy-r, cy+r):
        for x in range(cx-r, cx+r):
            if (x-cx)**2 + (y-cy)**2 < r**2:
                if (x-cx)**2 + (y-cy)**2 > (r-5)**2:
                    draw_rect(canvas, x, y, 1, 1, 12) # Grey Ring
                else:
                    draw_rect(canvas, x, y, 1, 1, 7) # Sand center
                    
    # THE TRIANGLE
    # Blondie (Good): Bottom Center
    bx, by = cx, cy + 25
    draw_rect(canvas, bx-2, by-5, 4, 10, 9) # Green/Brown Poncho
    draw_rect(canvas, bx-2, by-7, 4, 2, 8) # Head
    
    # Angel Eyes (Bad): Top Right
    ax, ay = cx + 22, cy - 15
    draw_rect(canvas, ax-2, ay-5, 4, 10, 0) # Black Suit
    draw_rect(canvas, ax-2, ay-7, 4, 2, 0) # Hat
    
    # Tuco (Ugly): Top Left
    tx, ty = cx - 22, cy - 15
    draw_rect(canvas, tx-2, ty-5, 4, 10, 12) # Grey Rags
    draw_rect(canvas, tx-2, ty-7, 4, 2, 8) # Head

def draw_eyes(canvas, character, twitch):
    # SERGIO LEONE ZOOM
    # Full screen face slice
    
    # Skin Base
    draw_rect(canvas, 0, 0, W, H, 8) # Orange Skin
    
    # Texture (Sweat/Grime)
    for _ in range(100):
        rx, ry = random.randint(0, W), random.randint(0, H)
        draw_rect(canvas, rx, ry, 1, 1, 10 if character=="GOOD" else 9)
        
    # EYES
    eye_y = H//2
    eye_sep = 30
    eye_w = 20
    eye_h = 10
    
    # Left Eye
    lx = W//2 - eye_sep//2 - eye_w
    draw_rect(canvas, lx, eye_y, eye_w, eye_h, 1) # White
    # Pupil
    offset = twitch if random.random() > 0.5 else 0
    draw_rect(canvas, lx + eye_w//2 - 2 + offset, eye_y+2, 4, 6, 0 if character=="BAD" else 6)
    
    # Right Eye
    rx = W//2 + eye_sep//2
    draw_rect(canvas, rx, eye_y, eye_w, eye_h, 1)
    draw_rect(canvas, rx + eye_w//2 - 2 + offset, eye_y+2, 4, 6, 0 if character=="BAD" else 6)
    
    # Hat Brim / Hair
    if character == "GOOD":
        draw_rect(canvas, 0, 0, W, 60, 9) # Brown Hat
    elif character == "BAD":
        draw_rect(canvas, 0, 0, W, 70, 0) # Black Hat
    elif character == "UGLY":
        draw_rect(canvas, 0, 0, W, 40, 0) # Messy Hair

def run():
    print("LOGIC GARDEN 64t: THE ECSTASY OF GOLD")
    
    # EDITING RHYTHM (Accelerating)
    cuts = [0, 60, 100, 130, 150, 160, 165, 170, 175, 180]
    # Phases roughly correspond to cuts
    
    char_cycle = ["GOOD", "BAD", "UGLY"]
    
    for f in range(TOTAL_FRAMES):
        
        # Determine Phase based on cuts
        phase = "WIDE"
        current_cut_idx = 0
        for i, cut in enumerate(cuts):
            if f >= cut:
                current_cut_idx = i
                
        # Logic: 
        # Even indices = Wide Shot
        # Odd indices = Close Up
        
        if f > 180:
            phase = "DRAW"
        elif current_cut_idx % 2 == 0:
            phase = "WIDE"
        else:
            phase = "CLOSEUP"
            
        # RENDER PHASE
        if phase == "WIDE":
            draw_wide_shot(GRID, f)
            
        elif phase == "CLOSEUP":
            # Which character? Rotate based on cut index
            char_idx = current_cut_idx % 3
            char = char_cycle[char_idx]
            
            # Draw Face
            twitch = int(math.sin(f * 0.5) * 3)
            draw_eyes(GRID, char, twitch)
            
        elif phase == "DRAW":
            # THE SHOT
            if f < 185:
                # Flash
                GRID[:, :] = COLORS[1] # White
            else:
                # Aftermath (Wide)
                draw_wide_shot(GRID, f)
                # Angel Eyes (Top Right) Falls
                cx, cy = W//2, H//2
                ax, ay = cx + 22, cy - 15
                # Erase standing
                draw_rect(GRID, ax-5, ay-10, 10, 20, 7) # Erase with ground color
                # Draw Dead (Lying horizontal)
                draw_rect(GRID, ax-5, ay, 12, 4, 0) 
                
                # Blondie Gun Smoke
                bx, by = cx, cy + 25
                draw_rect(GRID, bx, by-5, 2, 2, 1) # Smoke puff

        # RENDER
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
