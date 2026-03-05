"""
SOVEREIGN CODE: logic_garden_64m_oz_fixed.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: Wizard of Oz (Sepia -> Technicolor)
FIX: Indentation Error resolved.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import math

# C64 PALETTE
COLORS = {
    0:  [0, 0, 0],       # Black
    1:  [255, 255, 255], # White
    2:  [136, 0, 0],     # Red
    3:  [170, 255, 238], # Cyan (Sky)
    4:  [204, 68, 204],  # Purple
    5:  [0, 204, 85],    # Green (Grass)
    6:  [0, 0, 170],     # Blue
    7:  [238, 238, 119], # Yellow (The Road)
    8:  [221, 136, 85],  # Orange
    9:  [102, 68, 0],    # Brown (Sepia)
    10: [255, 119, 119], # Light Red
    11: [51, 51, 51],    # Dark Grey (Sepia shadow)
    12: [119, 119, 119], # Grey (Sepia mid)
    13: [170, 255, 102], # Light Green
    14: [0, 136, 255],   # Light Blue
    15: [187, 187, 187]  # Light Grey 
}

# CONFIG
FPS = 15
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64m_oz"
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

def run():
    print("LOGIC GARDEN 64m: SOMEWHERE OVER THE RAINBOW (FIXED)")
    
    # 1. PRE-RENDER OZ (Background Buffer)
    OZ_LAYER = np.zeros((H, W, 3), dtype=np.uint8)
    
    # Sky
    OZ_LAYER[:, :] = COLORS[3] # Cyan
    
    # Hills
    for x in range(W):
        hill_h = 80 + 10 * math.sin(x * 0.05)
        OZ_LAYER[int(H-hill_h):H, x] = COLORS[5] # Green
        
    # Yellow Brick Road
    for y in range(H//2, H):
        progress = (y - H//2) / (H/2)
        road_w = 2 + progress * 60
        road_x = W//2 + 30 * math.sin(progress * 2) 
        
        start_x = int(road_x - road_w/2)
        end_x = int(road_x + road_w/2)
        
        start_x = max(0, start_x)
        end_x = min(W, end_x)
        OZ_LAYER[y, start_x:end_x] = COLORS[7] # Yellow
        
        if y % 4 == 0:
            OZ_LAYER[y, start_x:end_x] = COLORS[8] # Orange texture

    # Poppies
    np.random.seed(42)
    for _ in range(200):
        rx = np.random.randint(0, W)
        ry = np.random.randint(H//2, H)
        if np.all(OZ_LAYER[ry, rx] == COLORS[5]):
            OZ_LAYER[ry, rx] = COLORS[2] # Red
            
    # Emerald City
    cx, cy = W//2 + 10, H//2 - 20
    draw_rect(OZ_LAYER, cx-5, cy, 10, 30, 13) # Light Green
    draw_rect(OZ_LAYER, cx-15, cy+20, 10, 20, 13)
    draw_rect(OZ_LAYER, cx+5, cy+20, 10, 20, 13)

    # 2. ANIMATION LOOP
    for f in range(TOTAL_FRAMES):
        # A. Copy Oz Background
        GRID[:] = OZ_LAYER[:]
        
        # B. Calculate Door State
        # 0-30 frames: Closed
        # 30-90 frames: Opening
        open_factor = 0.0
        if f > 30:
            open_factor = (f - 30) / 60.0
            if open_factor > 1.0: open_factor = 1.0
            # Easing
            open_factor = open_factor * open_factor * (3 - 2 * open_factor)
            
        # C. Draw The House (Masking Oz)
        hole_x = 25
        hole_w = 60
        hole_y = 40
        hole_h = 120
        
        # HOUSE WALLS (Sepia #11 and #9)
        draw_rect(GRID, 0, 0, W, hole_y, 11) # Top
        draw_rect(GRID, 0, hole_y + hole_h, W, H - (hole_y + hole_h), 9) # Floor
        draw_rect(GRID, 0, hole_y, hole_x, hole_h, 11) # Left Wall
        draw_rect(GRID, hole_x + hole_w, hole_y, W - (hole_x+hole_w), hole_h, 11) # Right Wall
        
        # THE DOOR (Moving Obstruction)
        # It shrinks from Right to Left to simulate opening inward/outward
        current_door_w = hole_w * (1.0 - open_factor)
        
        if current_door_w > 1:
            # Draw door pane
            draw_rect(GRID, hole_x, hole_y, current_door_w, hole_h, 12) # Grey Door
            
            # Details
            if current_door_w > 10:
                # Handle
                draw_rect(GRID, hole_x + current_door_w - 8, hole_y + 60, 4, 2, 0)
            if current_door_w > 20:
                # Panels
                draw_rect(GRID, hole_x + 5, hole_y + 10, current_door_w - 10, 40, 11)
                draw_rect(GRID, hole_x + 5, hole_y + 60, current_door_w - 10, 40, 11)

        # D. DOROTHY
        dx, dy = W//2 - 10, H - 40
        
        # Body (Grey/White Dress)
        draw_rect(GRID, dx, dy-30, 14, 30, 15) # Light Grey
        draw_rect(GRID, dx+2, dy-30, 10, 30, 12) # Checkered Grey
        
        # Head (Brown)
        draw_rect(GRID, dx+2, dy-40, 10, 10, 9)
        
        # Arms (Flesh -> Sepia #8)
        draw_rect(GRID, dx+14, dy-25, 4, 15, 8) 
        
        # Animation: Tiny step forward at end?
        if f > 150:
             # Just a tiny bob
             dx += 1
        
        # RENDER
        fig = plt.figure(figsize=(9, 16), dpi=80)
        # Crucial for pixel look:
        fig.figimage(GRID, resize=True) 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
