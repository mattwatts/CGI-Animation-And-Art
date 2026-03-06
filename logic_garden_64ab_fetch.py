"""
SOVEREIGN CODE: logic_garden_64ab_fetch.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 64AB (Fetch)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge
import matplotlib.patheffects as pe
import os
import math

# CONFIG
FPS = 15
DURATION = 12
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64ab_fetch"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE (Pepto)
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_kid(ax, x, y, scale, arm_angle):
    # simple blocky kid
    # Legs
    ax.add_patch(Rectangle((x, y), 6*scale, 15*scale, color=C64['BLUE']))
    ax.add_patch(Rectangle((x+8*scale, y), 6*scale, 15*scale, color=C64['BLUE']))
    
    # Torso
    ax.add_patch(Rectangle((x, y+15*scale), 14*scale, 18*scale, color=C64['CYAN']))
    
    # Head
    ax.add_patch(Circle((x+7*scale, y+38*scale), 6*scale, color=C64['LIGHTRED']))
    
    # Arm (Rotating based on throw)
    shoulder_x = x + 10*scale
    shoulder_y = y + 28*scale
    
    # Arm length
    arm_len = 12*scale
    hand_x = shoulder_x + math.cos(math.radians(arm_angle)) * arm_len
    hand_y = shoulder_y + math.sin(math.radians(arm_angle)) * arm_len
    
    ax.plot([shoulder_x, hand_x], [shoulder_y, hand_y], color=C64['CYAN'], linewidth=4*scale)
    # Hand
    ax.add_patch(Circle((hand_x, hand_y), 3*scale, color=C64['LIGHTRED']))
    
    return hand_x, hand_y

def draw_dog(ax, x, y, scale, tail_wag):
    # Body
    ax.add_patch(Rectangle((x, y+5*scale), 20*scale, 10*scale, color=C64['BROWN']))
    
    # Legs
    ax.add_patch(Rectangle((x+2*scale, y), 4*scale, 5*scale, color=C64['BROWN']))
    ax.add_patch(Rectangle((x+14*scale, y), 4*scale, 5*scale, color=C64['BROWN']))
    
    # Head
    ax.add_patch(Rectangle((x-5*scale, y+10*scale), 8*scale, 8*scale, color=C64['BROWN']))
    # Ears
    ax.add_patch(Rectangle((x-5*scale, y+16*scale), 3*scale, 4*scale, color=C64['BLACK']))
    
    # Tail (Wag)
    tail_base_x = x + 20*scale
    tail_base_y = y + 12*scale
    tail_tip_x = tail_base_x + 5*scale
    tail_tip_y = tail_base_y + tail_wag
    
    ax.plot([tail_base_x, tail_tip_x], [tail_base_y, tail_tip_y], color=C64['BROWN'], linewidth=3*scale)

def run():
    print(f"LOGIC GARDEN 64AB: FETCH ({TOTAL_FRAMES} frames)")
    
    # BALL PHYSICS
    ball_x = 0
    ball_y = 0
    ball_vx = 0
    ball_vy = 0
    state = "HOLD" # HOLD, THROW, CATCH
    
    throw_timer = 0
    
    for f in range(TOTAL_FRAMES):
        
        # --- LOGIC ---
        scale = 5.0
        kid_x = 200
        kid_y = 650
        dog_x = 800
        dog_y = 650
        
        arm_angle = -45 # Relaxed
        
        # Animation Loop
        cycle = f % 90 # 3 second loop
        
        if cycle < 20:
            state = "HOLD"
            # Wind up
            norm = cycle / 20.0
            arm_angle = -45 + (135 * norm) # Swing back to -45, forward to 90
            
        elif cycle == 20:
            state = "AIR"
            # Release
            # Calculate start pos from hand
            # Recalc hand pos locally
            shoulder_x = kid_x + 10*scale
            shoulder_y = kid_y + 28*scale
            hand_x = shoulder_x + math.cos(math.radians(45)) * 12*scale
            hand_y = shoulder_y + math.sin(math.radians(45)) * 12*scale
            
            ball_x = hand_x
            ball_y = hand_y
            
            # Trajectory to hit Dog X
            dx = dog_x - ball_x
            t = 30.0 # Frames to travel
            ball_vx = dx / t
            # Gravity: y = vy*t - 0.5*g*t^2
            # We want y to end at dog_y + 20
            # dy = vy*t - 0.5*g*t^2
            # vy = (dy + 0.5*g*t^2) / t
            g = 1.5
            dy = (dog_y + 50) - ball_y
            ball_vy = (dy + 0.5 * g * (t**2)) / t
            
        elif cycle > 20 and cycle < 50:
            state = "AIR"
            ball_x += ball_vx
            ball_y += ball_vy
            ball_vy -= 1.5 # Gravity
            arm_angle = 45 # Follow through
            
        else:
            state = "CATCH"
            ball_x = dog_x - 5*scale
            ball_y = dog_y + 15*scale
            arm_angle = -45

        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # Background
        ax.set_facecolor(C64['LIGHTBLUE'])
        
        # Virtual Monitor
        width = 980
        height = 720
        screen_x = 50
        screen_y = 600
        
        # Flash Effect on Catch
        bg_col = C64['BLUE']
        if state == "CATCH" and cycle < 60:
            if f % 4 < 2: bg_col = C64['LIGHTBLUE'] # Flash
            
        ax.add_patch(Rectangle((screen_x, screen_y), width, height, color=bg_col))
        
        # Grass
        ax.add_patch(Rectangle((screen_x, screen_y), width, 100, color=C64['LIGHTGREEN']))
        
        # Sprites
        hand_x, hand_y = draw_kid(ax, kid_x, kid_y, scale, arm_angle)
        
        wag = math.sin(f * 1.5) * 10 * scale
        draw_dog(ax, dog_x, dog_y, scale, wag)
        
        # Ball
        if state == "HOLD":
            ball_x = hand_x
            ball_y = hand_y
            
        ax.add_patch(Circle((ball_x, ball_y), 3*scale, color=C64['RED']))
        
        # Scanlines
        for y in range(screen_y, screen_y + height, 4):
            ax.axhline(y, color='black', alpha=0.1, linewidth=1)

        # UI
        stroke = [pe.withStroke(linewidth=0, foreground="black")]
        
        ax.text(540, 1600, "LOGIC GARDEN 64AB", color=C64['BLUE'], ha='center',
                fontsize=40, fontname='monospace', weight='bold')
        
        if state == "CATCH" and cycle < 80:
             ax.text(540, 1400, "GOOD DOG!", color=C64['YELLOW'], ha='center',
                fontsize=50, fontname='monospace', weight='bold', path_effects=[pe.withStroke(linewidth=4, foreground=C64['BLACK'])])

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
