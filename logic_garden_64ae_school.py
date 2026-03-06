"""
SOVEREIGN CODE: logic_garden_64ae_school.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 64AE (Schoolhouse)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Wedge
import matplotlib.patheffects as pe
import os
import math

# CONFIG
FPS = 15
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64ae_school"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE (Pepto)
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_school(ax, x, y, scale):
    # Main Building (Red Brick)
    width = 160 * scale
    height = 100 * scale
    ax.add_patch(Rectangle((x, y), width, height, color=C64['RED']))
    
    # Roof (Dark Grey Triangle)
    roof_h = 60 * scale
    roof_poly = Polygon([
        (x - 10*scale, y + height),
        (x + width/2, y + height + roof_h),
        (x + width + 10*scale, y + height)
    ], closed=True, color=C64['DARKGREY'])
    ax.add_patch(roof_poly)
    
    # Door (Black Void)
    door_w = 30 * scale
    door_h = 50 * scale
    door_x = x + width/2 - door_w/2
    ax.add_patch(Rectangle((door_x, y), door_w, door_h, color=C64['BLACK']))
    
    # Windows (Blue with White Frame)
    win_w = 30 * scale
    win_h = 30 * scale
    win_y = y + 40 * scale
    
    # Left Window
    ax.add_patch(Rectangle((x + 20*scale, win_y), win_w, win_h, color=C64['LIGHTBLUE']))
    ax.add_patch(Rectangle((x + 20*scale, win_y), win_w, win_h, fill=False, edgecolor='white', linewidth=2*scale))
    
    # Right Window
    ax.add_patch(Rectangle((x + width - 20*scale - win_w, win_y), win_w, win_h, color=C64['LIGHTBLUE']))
    ax.add_patch(Rectangle((x + width - 20*scale - win_w, win_y), win_w, win_h, fill=False, edgecolor='white', linewidth=2*scale))
    
    # Bell Tower
    bell_w = 30 * scale
    bell_h = 30 * scale
    bell_x = x + width/2 - bell_w/2
    bell_y = y + height + roof_h - 10*scale
    ax.add_patch(Rectangle((bell_x, bell_y), bell_w, bell_h, color=C64['WHITE']))
    # Bell
    ax.add_patch(Circle((bell_x + bell_w/2, bell_y + bell_h/2), 8*scale, color=C64['YELLOW']))
    
    return door_x + door_w/2 # Return door center X

def draw_kid(ax, x, y, scale, tick):
    # Scale offset for sprite size
    
    # Legs (Walk Cycle)
    leg_len = 15 * scale
    stride = math.sin(tick * 0.8) * 10 * scale
    
    # Left Leg
    ax.plot([x, x - stride], [y + 15*scale, y], color=C64['BLUE'], linewidth=4*scale)
    # Right Leg
    ax.plot([x, x + stride], [y + 15*scale, y], color=C64['BLUE'], linewidth=4*scale)
    
    # Body
    ax.add_patch(Rectangle((x - 6*scale, y + 15*scale), 12*scale, 18*scale, color=C64['CYAN']))
    
    # Backpack (Yellow)
    ax.add_patch(Rectangle((x - 10*scale, y + 20*scale), 6*scale, 12*scale, color=C64['YELLOW']))
    
    # Head
    head_y = y + 33 * scale
    ax.add_patch(Circle((x, head_y), 7*scale, color=C64['LIGHTRED']))
    
    # Arm (Swing)
    arm_swing = -stride
    ax.plot([x, x + arm_swing], [y + 28*scale, y + 15*scale], color=C64['CYAN'], linewidth=3*scale)

def run():
    print(f"LOGIC GARDEN 64AE: SCHOOL ({TOTAL_FRAMES} frames)")
    
    school_x = 400
    school_y = 650
    scale = 3.0
    
    kid_x = -100 # Start offscreen
    kid_y = school_y
    state = "WALK"
    
    for f in range(TOTAL_FRAMES):
        
        # --- LOGIC ---
        door_center_x = 400 + (160*scale)/2 # Approx
        
        if state == "WALK":
            kid_x += 5
            if kid_x >= door_center_x:
                kid_x = door_center_x
                state = "ENTER"
                enter_timer = 0
                
        elif state == "ENTER":
            # Fade out / Shrink into door
            enter_timer += 1
            # Simple visual trick: Just stop drawing kid after a few frames
        
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # 1. BORDER
        ax.set_facecolor(C64['LIGHTBLUE'])
        
        # 2. VIRTUAL CRT
        screen_x = 50
        screen_y = 600
        screen_w = 980
        screen_h = 720
        
        # Sky
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, screen_h, color=C64['LIGHTBLUE'], zorder=0))
        # Ground
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, 100, color=C64['GREEN'], zorder=1))
        
        # 3. SCHOOL
        draw_school(ax, school_x, school_y, scale)
        
        # 4. KID
        if state == "WALK":
            draw_kid(ax, kid_x, kid_y + 10, scale, f) # +10 to align with ground
        elif state == "ENTER":
            if enter_timer < 10:
                # Disappear into door (Draw opaque rect partly over kid?)
                # Or just draw kid inside the black rect zone with alpha?
                # Let's just draw him entering
                draw_kid(ax, kid_x, kid_y + 10, scale, f)
            else:
                pass # Gone inside
                
        # 5. SCANLINES
        for y in range(screen_y, screen_y + screen_h, 4):
            ax.axhline(y, color='black', alpha=0.1, linewidth=1)

        # 6. UI
        stroke = [pe.withStroke(linewidth=0, foreground="black")]
        
        ax.text(540, 1600, "LOGIC GARDEN 64AE", color=C64['RED'], ha='center',
                fontsize=40, fontname='monospace', weight='bold')
        
        ax.text(540, 1500, "SCHOOL DAYS", color=C64['YELLOW'], ha='center',
                fontsize=30, fontname='monospace', weight='bold', path_effects=[pe.withStroke(linewidth=4, foreground=C64['BLACK'])])

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
