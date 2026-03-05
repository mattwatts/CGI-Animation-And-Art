"""
SOVEREIGN CODE: logic_garden_64o_dancing.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: Dirty Dancing (The Corner & The Lift)
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
    3:  [170, 255, 238], # Cyan
    4:  [204, 68, 204],  # Purple
    5:  [0, 204, 85],    # Green
    6:  [0, 0, 170],     # Blue
    7:  [238, 238, 119], # Yellow
    8:  [221, 136, 85],  # Orange
    9:  [102, 68, 0],    # Brown
    10: [255, 119, 119], # Light Red (Pink Dress)
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
OUT_DIR = "frames_64o_dancing"
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

def draw_baby(canvas, x, y, pose):
    # Baby Houseman
    # Dress: Pink (#10)
    # Hair: Yellow (#7) Curly
    
    if pose == "SITTING":
        # Huddled in corner
        draw_rect(canvas, x, y, 10, 10, 10) # Dress
        draw_rect(canvas, x+2, y-4, 6, 6, 7) # Head
        draw_rect(canvas, x+1, y+4, 8, 4, 10) # Skirt on chair
    
    elif pose == "STANDING":
        draw_rect(canvas, x, y, 6, 14, 10) # Dress body
        draw_rect(canvas, x-2, y+14, 10, 6, 10) # Skirt flare
        draw_rect(canvas, x, y-5, 6, 5, 7) # Head
        draw_rect(canvas, x-2, y, 2, 8, 8) # Arm L
        draw_rect(canvas, x+6, y, 2, 8, 8) # Arm R
        
    elif pose == "LIFT":
        # Flying horizontalish
        # Body horizontal
        draw_rect(canvas, x-10, y, 20, 6, 10) # Torso
        draw_rect(canvas, x-14, y-2, 6, 6, 7) # Head (Left)
        draw_rect(canvas, x+10, y, 10, 4, 10) # Legs extended
        # Arm out
        draw_rect(canvas, x-5, y-5, 10, 2, 8) 

def draw_johnny(canvas, x, y, pose):
    # Johnny Castle
    # Outfit: Black (#0)
    # Hair: Black/Dark Grey (#11)
    
    if pose == "WALKING":
        draw_rect(canvas, x, y, 8, 16, 0) # Torso
        draw_rect(canvas, x, y-6, 6, 6, 11) # Head
        # Legs (walking cycle simplified)
        draw_rect(canvas, x, y+16, 3, 10, 0)
        draw_rect(canvas, x+5, y+16, 3, 10, 0)
        
    elif pose == "LIFTING":
        draw_rect(canvas, x, y, 8, 16, 0) # Torso
        draw_rect(canvas, x, y-6, 6, 6, 11) # Head
        # Legs braced
        draw_rect(canvas, x-2, y+16, 4, 12, 0)
        draw_rect(canvas, x+6, y+16, 4, 12, 0)
        # Arms UP
        draw_rect(canvas, x-2, y-10, 3, 12, 0)
        draw_rect(canvas, x+7, y-10, 3, 12, 0)

def run():
    print("LOGIC GARDEN 64o: NOBODY PUTS BABY IN A CORNER")
    
    # CHARACTERS
    baby = {'x': 10, 'y': 170, 'pose': 'SITTING'}
    johnny = {'x': 120, 'y': 160, 'pose': 'WALKING'} # Starts off screen
    
    for f in range(TOTAL_FRAMES):
        # 1. BACKGROUND (Kellerman's Party - Dark Grey)
        GRID[:, :] = COLORS[11]
        
        # Floor (Wood - Brown #9 with dither)
        for y in range(180, H):
            for x in range(W):
                c = 9
                if (x+y)%2==0: c = 8 # Dither
                if 0 <= x < W: GRID[y, x] = COLORS[c]
                
        # The Corner (Wall)
        draw_rect(GRID, 0, 0, 5, 180, 12)
        
        # 2. STATES
        # 0-60: The Corner / Johnny Enters
        # 60-120: The Pull / Walk to Center
        # 120-180: The Lift
        # 180+: Freeze
        
        phase = ""
        
        if f < 60:
            phase = "THE CORNER"
            # Johnny walks in from Right
            johnny['x'] -= 2
            if johnny['x'] < 30: johnny['x'] = 30
            
            # Text Bubble logic?
            # Implied.
            
        elif f < 100:
            phase = "THE WALK"
            # Baby stands up
            baby['pose'] = "STANDING"
            # They walk to center (X=55)
            target = 55
            
            johnny['x'] += (target - johnny['x']) * 0.1
            baby['x'] += (target - baby['x']) * 0.1
            
            johnny['y'] = 150
            baby['y'] = 150
            
        elif f < 120:
             phase = "PREPARING"
             # Pause at center
             johnny['pose'] = "LIFTING" # Arms up preparatory
             
             # Baby runs back to run forward?
             # No, simple elevator lift logic for 8-bit
             pass
             
        else:
            phase = "THE LIFT"
            johnny['pose'] = "LIFTING"
            baby['pose'] = "LIFT"
            
            # Baby rises
            target_h = 110 # Johnny's head height -ish
            curr_h = baby['y']
            
            if curr_h > target_h:
                baby['y'] -= 4 # Lift speed
            
            # Johnny Holds
            pass

        # 3. DRAW CHARACTERS
        draw_johnny(GRID, int(johnny['x']), int(johnny['y']), johnny['pose'])
        draw_baby(GRID, int(baby['x']), int(baby['y']), baby['pose'])
        
        # 4. SPOTLIGHT (Final Phase)
        if phase == "THE LIFT":
            # White/Cyan Dither cone
            center_x = 55
            for y in range(0, H):
                radius = (y / H) * 40 + 10
                for x in range(W):
                    dist = abs(x - center_x)
                    if dist < radius:
                        # Dither Mask (Checkboard)
                        if (x+y+f)%2 == 0:
                            # Add brightness (mix White #1)
                            # Current color?
                            # Just draw transparency hack
                            if GRID[y, x, 0] == COLORS[11][0]: # If BG
                                GRID[y, x] = COLORS[6] # Blue/Party tint
                            elif GRID[y, x, 0] == COLORS[0][0]: # Johnny
                                GRID[y, x] = COLORS[11] # Lighten Johnny

        # 5. TEXT OVERLAY
        if f > 30 and f < 90:
            # "NOBODY PUTS BABY..."
            # Scrolling marquee? 
            # Static text
            pass
            
        if f > 130:
            # "TIME OF MY LIFE"
            draw_rect(GRID, 10, 20, 90, 10, 0)
            # Dots for text
            draw_rect(GRID, 12, 22, 2, 6, 1)
            draw_rect(GRID, 16, 22, 2, 6, 1)

        # RENDER
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
