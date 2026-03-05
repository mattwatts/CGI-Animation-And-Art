"""
SOVEREIGN CODE: logic_garden_64l.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation (Python Implementation)
SCENE: Gene Kelly / Singin' in the Rain
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import math

# C64 PALETTE (The Holy 16)
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
FPS = 15 # Authentic Retro Framerate
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64l_rain"
os.makedirs(OUT_DIR, exist_ok=True)

# LOW RES CANVAS (Multicolor Mode)
W, H = 110, 196 
GRID = np.zeros((H, W, 3), dtype=np.uint8)

# BRESENHAM LINE ALGORITHM (Integer Math)
def draw_line(canvas, x0, y0, x1, y1, color_id):
    c = COLORS[color_id]
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    while True:
        if 0 <= x0 < W and 0 <= y0 < H:
            canvas[y0, x0] = c
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_rect(canvas, x, y, w, h, color_id):
    c = COLORS[color_id]
    x, y, w, h = int(x), int(y), int(w), int(h)
    canvas[y:y+h, x:x+w] = c

def run():
    print("LOGIC GARDEN 64l: SINGIN IN THE RAIN")
    
    # RAIN SYSTEM
    drops = []
    for _ in range(50):
        drops.append([np.random.randint(0, W), np.random.randint(0, H)])
        
    for f in range(TOTAL_FRAMES):
        # 1. CLEAR SCREEN (Dark Blue #6)
        # Using numpy assignment is fast
        GRID[:, :] = COLORS[6]
        
        # 2. DRAW SIDEWALK (Grey #12)
        draw_rect(GRID, 0, H-20, W, 20, 12)
        # Puddle (Blue #14)
        draw_rect(GRID, W//2 - 20, H-15, 40, 5, 14)
        
        # 3. DRAW LAMP POST (Black #0 / Light Grey #15)
        pole_x = W // 2 + 10
        # Base
        draw_rect(GRID, pole_x-2, H-20, 4, 20, 11) # Dark Grey base
        # Pole
        draw_rect(GRID, pole_x-1, 40, 2, H-60, 0) # Black stick
        # Lamp Head
        draw_rect(GRID, pole_x-5, 30, 10, 10, 0)
        # THE GLOW (Yellow #7)
        # Dither pattern?
        draw_rect(GRID, pole_x-3, 32, 6, 6, 7)
        # Light Shafts (Dithered Yellow pixels)
        if f % 2 == 0:
            draw_line(GRID, pole_x, 40, pole_x-10, 60, 7)
            draw_line(GRID, pole_x, 40, pole_x+10, 60, 7)
            
        # 4. GENE KELLY (Stick Figure Logic)
        # Time driver
        t = f * 0.2
        swing = math.sin(t) # -1 to 1
        
        # Anchor Point (Hand holding pole)
        hand_x, hand_y = pole_x - 1, 90
        
        # Shoulder Position (Movies in circle around hand)
        # Radius of arm = 12
        arm_len = 12
        shoulder_angle = math.pi + swing * 0.5 # Oscillates around left side
        
        shoulder_x = hand_x + arm_len * math.cos(shoulder_angle)
        shoulder_y = hand_y + arm_len * math.sin(shoulder_angle)
        
        # Head
        head_x = shoulder_x
        head_y = shoulder_y - 8
        
        # Torso (Down from shoulder)
        hip_x = shoulder_x + swing * 5 # Hips drag behind slightly
        hip_y = shoulder_y + 20
        
        # Legs
        leg_l_x = hip_x - 5 + math.cos(t*2)*3
        leg_l_y = hip_y + 15
        
        leg_r_x = hip_x + 5 - math.cos(t*2)*3
        leg_r_y = hip_y + 15
        
        # Other Arm (Holding Umbrella)
        arm_r_x = shoulder_x - 10
        arm_r_y = shoulder_y + 5 + math.sin(t*3)*2
        
        # DRAW ZERO LAYER (Umbrella Back)
        # Black #0
        draw_line(GRID, arm_r_x, arm_r_y, arm_r_x-10, arm_r_y-10, 0) # Handle
        # Top
        dx = 12
        draw_line(GRID, arm_r_x-10-dx, arm_r_y-10+5, arm_r_x-10, arm_r_y-10-5, 0)
        draw_line(GRID, arm_r_x-10+dx, arm_r_y-10+5, arm_r_x-10, arm_r_y-10-5, 0)
        draw_line(GRID, arm_r_x-10-dx, arm_r_y-10+5, arm_r_x-10+dx, arm_r_y-10+5, 0)

        # DRAW BODY (Grey Suit #15)
        # Head
        draw_rect(GRID, head_x-3, head_y-3, 6, 6, 15)
        # Hat (Black)
        draw_rect(GRID, head_x-4, head_y-4, 8, 2, 0)
        
        # Spine
        draw_line(GRID, shoulder_x, shoulder_y, hip_x, hip_y, 15)
        # Arm L (To Pole)
        draw_line(GRID, shoulder_x, shoulder_y, hand_x, hand_y, 15)
        # Arm R (To Umbrella)
        draw_line(GRID, shoulder_x, shoulder_y, arm_r_x, arm_r_y, 15)
        # Legs
        draw_line(GRID, hip_x, hip_y, leg_l_x, leg_l_y, 15)
        draw_line(GRID, hip_x, hip_y, leg_r_x, leg_r_y, 15)
        
        # 5. RAIN (Cyan #3)
        # Draw ON TOP of everything
        # Speed = 3px / frame
        for drop in drops:
            # Erase old? No, we clear screen every frame.
            # Update pos
            drop[0] += 1 # Wind right
            drop[1] += 4 # Gravity down
            
            # Wrap
            if drop[1] > H: 
                drop[1] = 0
                drop[0] = np.random.randint(0, W)
            if drop[0] > W:
                drop[0] = 0
            
            # Draw Line (Streak)
            draw_line(GRID, drop[0], drop[1], drop[0]-1, drop[1]-3, 3)

        # RENDER TO FIGURE
        # We save the raw pixel array logic
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        # Crucial: No interpolation to preserve "Pixel Perfect" C64 look
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
