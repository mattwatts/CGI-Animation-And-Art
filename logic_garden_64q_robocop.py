"""
SOVEREIGN CODE: logic_garden_64q_robocop.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: RoboCop (ED-209 Demo)
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
OUT_DIR = "frames_64q_robocop"
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

def draw_ed209(canvas, x, y, frame):
    # The Beast. Top heavy.
    # Breathing animation: Top part bobs.
    bob = int(math.sin(frame * 0.2) * 2)
    
    # LEGS (Static)
    draw_rect(canvas, x-10, y+20, 6, 20, 11) # L Leg
    draw_rect(canvas, x+14, y+20, 6, 20, 11) # R Leg
    draw_rect(canvas, x-12, y+38, 10, 4, 0) # L Foot
    draw_rect(canvas, x+12, y+38, 10, 4, 0) # R Foot
    
    # TORSO (Bobs)
    ty = y + bob
    # Main Dome
    draw_rect(canvas, x-20, ty-10, 50, 25, 11) # Body Dark Grey
    draw_rect(canvas, x-18, ty-8, 46, 10, 0) # Visor Black
    
    # Grill/Vent
    for i in range(0, 10, 2):
        draw_rect(canvas, x-10, ty+5+i, 30, 1, 0)
        
    # ARMS (Gun Pods)
    # Left Arm
    draw_rect(canvas, x-28, ty, 8, 15, 11)
    draw_rect(canvas, x-28, ty+15, 8, 8, 0) # Gatling
    # Right Arm
    draw_rect(canvas, x+30, ty, 8, 15, 11)
    draw_rect(canvas, x+30, ty+15, 8, 8, 0) # Gatling

def draw_kinney(canvas, x, y, pose):
    # Generic Corporate Victim
    if pose == "DEAD":
        # Pile of pixels
        draw_rect(canvas, x, y+20, 20, 5, 6) # Suit
        draw_rect(canvas, x+5, y+22, 5, 2, 2) # Blood
        return

    # Suit Blue #6
    draw_rect(canvas, x, y, 10, 20, 6)
    # Legs
    draw_rect(canvas, x, y+20, 4, 10, 0)
    draw_rect(canvas, x+6, y+20, 4, 10, 0)
    # Head
    draw_rect(canvas, x+2, y-6, 6, 6, 8) # Skin
    
    # Arms
    if pose == "PANIC":
        # Waving
        draw_rect(canvas, x-4, y-5, 4, 15, 6)
        draw_rect(canvas, x+10, y-5, 4, 15, 6)
        # Gun (Tiny grey pixel)
        draw_rect(canvas, x+12, y-8, 4, 2, 12)
    elif pose == "POINTING":
        draw_rect(canvas, x+10, y+5, 8, 3, 6)
        draw_rect(canvas, x+18, y+4, 4, 2, 12) # Gun

def run():
    print("LOGIC GARDEN 64q: 20 SECONDS TO COMPLY")
    
    for f in range(TOTAL_FRAMES):
        # BACKGROUND: OCP Boardroom
        # Wall
        draw_rect(GRID, 0, 0, W, H, 15) # Light Grey
        # Carpet
        draw_rect(GRID, 0, 130, W, H-130, 12) # Mid Grey
        # Table Edge
        draw_rect(GRID, 0, 120, W, 10, 1) # White table
        
        # LOGIC STATES
        # 0-60: "Please put down your weapon." (Standout)
        # 60-200: "20 Seconds to comply." (Countdown)
        # 200-240: "Authorized to use physical force." (Growl)
        # 240+: CHAOS.
        
        mode = "NORMAL"
        if 60 < f < 200: mode = "COUNTDOWN"
        if 200 < f < 240: mode = "LOCKED"
        if f > 240: mode = "FIRE"
        
        # CAMERA SWITCH (POV vs WIDE)
        # Every 40 frames we toggle
        is_pov = False
        if mode == "COUNTDOWN" and (f // 40) % 2 == 0:
            is_pov = True
        if mode == "LOCKED": is_pov = True
        
        if is_pov:
            # ED-209 HUD
            # Scanlines
            draw_rect(GRID, 0, 0, W, H, 0) # Black BG
            for y in range(0, H, 2):
                draw_rect(GRID, 0, y, W, 1, 0)
                # Green Grid
                if y % 20 == 0: draw_rect(GRID, 0, y, W, 1, 5)
            for x in range(0, W, 20):
                draw_rect(GRID, x, 0, 1, H, 5)
                
            # Kinney in Thermals? (Red Sprite)
            draw_rect(GRID, 50, 100, 15, 30, 2) # Red Blob
            
            # HUD TEXT
            if mode == "COUNTDOWN":
                sec = 20 - int((f-60)/7)
                if f % 10 < 5: 
                    # Simulating Text Flash
                    pass
                    
            if mode == "LOCKED":
                draw_rect(GRID, 40, 90, 35, 50, 2) # Locking Box
                # "LOCK" TEXT simulation
                draw_rect(GRID, 45, 80, 25, 5, 2)

        elif mode == "FIRE":
            # CHAOS
            # Flash Background randomly
            bg = random.choice([0, 1, 15])
            GRID[:, :] = COLORS[bg]
            
            # Draw ED-209 Firing
            draw_ed209(GRID, 20, 80, f)
            # Muzzle Flash
            if f % 2 == 0:
                draw_rect(GRID, 50, 95, 20, 20, 7) # Yellow Flash
                draw_rect(GRID, 55, 100, 10, 10, 1) # White core
            
            # Draw Kinney Dying
            kinney_x = 80
            if f < 260:
                draw_kinney(GRID, kinney_x, 100 + (random.randint(-2,2)), "PANIC")
            else:
                 # Falling
                 draw_kinney(GRID, kinney_x, 140, "DEAD")
                 
        else:
            # NORMAL VIEW
            # ED-209 Left, Kinney Right
            draw_ed209(GRID, 20, 80, f)
            draw_kinney(GRID, 80, 100, "POINTING" if f < 60 else "PANIC")
            
        # HUD OVERLAYS (Text)
        if mode == "COUNTDOWN" and not is_pov:
            # Drawing the number
            sec = int(20 - (f-60)/6)
            if sec < 0: sec = 0
            
            # Bar Chart for Voice Stress
            # Bottom Center
            amp = (f % 10) * 3
            draw_rect(GRID, 45, 180, 20, 10, 0) # Box
            draw_rect(GRID, 47, 185, amp, 2, 5) # Green line
            
            # Subtitle
            if f > 60:
                 # "20 SECONDS"
                 pass

        # RENDER
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
