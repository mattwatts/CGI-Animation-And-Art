"""
SOVEREIGN CODE: logic_garden_112_companions.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 112 (Boy + Dog)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
import matplotlib.patheffects as pe
import os
import math

# CONFIG
FPS = 15
DURATION = 12
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_112_companions"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_dog(ax, x, y, scale, phase):
    # Dog (Smaller, Leading slightly?)
    FUR = C64['YELLOW']
    
    # Body
    ax.add_patch(Rectangle((x, y), 50*scale, 25*scale, color=FUR))
    
    # Tail (Happy Wag)
    wag = math.sin(phase * 4 * math.pi) * 15
    ax.plot([x, x-15*scale], [y+20*scale, y+35*scale+wag], color=FUR, linewidth=4*scale)
    
    # Head
    head_x = x + 40*scale
    head_y = y + 25*scale
    ax.add_patch(Circle((head_x, head_y), 15*scale, color=FUR))
    ax.add_patch(Rectangle((head_x+5*scale, head_y-5*scale), 12*scale, 10*scale, color=FUR)) # Snout
    
    # Legs (Cycle)
    leg_len = 20*scale
    for i, offset in enumerate([0, 0.5]): # Back, Front
        leg_x = x + (10*scale if i==0 else 40*scale)
        angle = math.sin((phase + i*0.5) * 2 * math.pi) * 0.5
        
        lx_end = leg_x + math.sin(angle)*10*scale
        ly_end = y - leg_len + math.cos(angle)*2*scale
        
        # Draw 2 legs per spot (near/far)
        ax.plot([leg_x, lx_end], [y, ly_end], color=C64['ORANGE'], linewidth=6*scale, zorder=1) # Far
        ax.plot([leg_x, lx_end - 5*scale], [y, ly_end + 2*scale], color=FUR, linewidth=6*scale, zorder=3) # Near

def draw_boy(ax, x, y, scale, phase):
    # Boy (Taller)
    SHIRT = C64['CYAN']
    PANTS = C64['BLUE']
    SKIN = C64['LIGHTRED']
    
    body_w = 20*scale
    body_h = 40*scale
    
    # Legs (Bipedal)
    leg_len = 35*scale
    
    # Far Leg
    angle_r = math.sin(phase * 2 * math.pi) * 0.8
    lx_r = x + body_w/2 + math.sin(angle_r)*20*scale
    ly_r = y - leg_len + math.cos(angle_r)*5*scale
    ax.plot([x+body_w/2, lx_r], [y, ly_r], color=C64['PURPLE'], linewidth=8*scale) # Darker jeans leg
    
    # Body
    ax.add_patch(Rectangle((x, y), body_w, body_h, color=SHIRT))
    
    # Head
    ax.add_patch(Circle((x+body_w/2, y+body_h+12*scale), 12*scale, color=SKIN))
    
    # Near Leg
    angle_l = math.sin((phase + 0.5) * 2 * math.pi) * 0.8
    lx_l = x + body_w/2 + math.sin(angle_l)*20*scale
    ly_l = y - leg_len + math.cos(angle_l)*5*scale
    ax.plot([x+body_w/2, lx_l], [y, ly_l], color=PANTS, linewidth=8*scale)
    
    # Arms (Opposite to legs)
    # Swinging
    arm_angle = -angle_l # Opposite to near leg
    hand_x = x + body_w/2 + math.sin(arm_angle)*15*scale
    hand_y = y + body_h - 25*scale
    ax.plot([x+body_w/2, hand_x], [y+body_h-5*scale, hand_y], color=SHIRT, linewidth=6*scale)
    ax.add_patch(Circle((hand_x, hand_y), 4*scale, color=SKIN))

def run():
    print(f"LOGIC GARDEN 112: COMPANIONS ({TOTAL_FRAMES} frames)")
    
    scale = 3.0
    
    # Screen Setup
    sx, sy, sw, sh = 50, 600, 980, 720
    
    for f in range(TOTAL_FRAMES):
        
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # Void
        ax.set_facecolor(C64['BLACK'])
        ax.add_patch(Rectangle((sx, sy), sw, sh, color=C64['BLACK']))
        
        # Ground Line
        floor_y = sy + 250
        ax.axhline(floor_y, color=C64['WHITE'], linewidth=4)
        
        # Movement
        # Start far left, end far right
        total_dist = sw + 500
        start_x = sx - 300
        progress = f / TOTAL_FRAMES
        
        # Position
        group_x = start_x + (progress * total_dist)
        
        # Walk Cycle
        cycle = (f % 20) / 20.0
        
        # DRAW
        # Boy follows Dog slightly? Or side by side.
        # Let's put Dog slightly ahead visually
        draw_boy(ax, group_x, floor_y + 35, scale, cycle)
        draw_dog(ax, group_x + 80*scale, floor_y + 20, scale, cycle) # Dog ahead
        
        # UI
        ui_col = C64['GREY']
        if 0.45 < progress < 0.55: ui_col = C64['CYAN']
        
        ax.text(540, 1500, "LOGIC GARDEN 112", color=ui_col, ha='center',
                fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
