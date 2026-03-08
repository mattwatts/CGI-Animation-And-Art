"""
SOVEREIGN CODE: logic_garden_115_return_companions.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 115 (Boy + Dog, Right to Left)
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
OUT_DIR = "frames_115_return_companions"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_dog_left(ax, x, y, scale, phase):
    # Dog Moving Left
    FUR = C64['YELLOW']
    SHADOW = C64['ORANGE']
    
    # Body (Anchored Right, extends Left)
    body_w = 50*scale
    ax.add_patch(Rectangle((x - body_w, y), body_w, 25*scale, color=FUR))
    
    # Tail (At Right end, Wagging)
    tail_x = x
    wag = math.sin(phase * 4 * math.pi) * 15
    ax.plot([tail_x, tail_x+15*scale], [y+20*scale, y+35*scale+wag], color=FUR, linewidth=4*scale)
    
    # Head (At Left end)
    head_x = x - (40*scale)
    head_y = y + 25*scale
    ax.add_patch(Circle((head_x, head_y), 15*scale, color=FUR))
    # Snout (Left)
    ax.add_patch(Rectangle((head_x-17*scale, head_y-5*scale), 12*scale, 10*scale, color=FUR))
    
    # Legs
    leg_len = 20*scale
    for i, offset in enumerate([0, 0.5]): # Back(Right), Front(Left)
        # Leg Anchor X
        leg_anchor_x = x - (10*scale if i==0 else 40*scale)
        
        angle = math.sin((phase + i*0.5) * 2 * math.pi) * 0.5
        
        lx_end = leg_anchor_x + math.sin(angle)*10*scale
        ly_end = y - leg_len + math.cos(angle)*2*scale
        
        # Far Leg
        ax.plot([leg_anchor_x, lx_end], [y, ly_end], color=SHADOW, linewidth=6*scale, zorder=1)
        # Near Leg
        ax.plot([leg_anchor_x, lx_end - 5*scale], [y, ly_end + 2*scale], color=FUR, linewidth=6*scale, zorder=3)

def draw_boy_left(ax, x, y, scale, phase):
    # Boy Moving Left
    SHIRT = C64['CYAN']
    PANTS = C64['BLUE']
    SKIN = C64['LIGHTRED']
    
    body_w = 20*scale
    body_h = 40*scale
    
    # Center X of body
    cx = x - body_w/2
    
    leg_len = 35*scale
    
    # Far Leg (Right side of sprite, but 'Far' regarding Z-depth)
    angle_r = math.sin(phase * 2 * math.pi) * 0.8
    lx_r = cx + math.sin(angle_r)*20*scale
    ly_r = y - leg_len + math.cos(angle_r)*5*scale
    ax.plot([cx, lx_r], [y, ly_r], color=C64['PURPLE'], linewidth=8*scale)
    
    # Body
    ax.add_patch(Rectangle((x - body_w, y), body_w, body_h, color=SHIRT))
    
    # Head
    ax.add_patch(Circle((cx, y+body_h+12*scale), 12*scale, color=SKIN))
    
    # Near Leg
    angle_l = math.sin((phase + 0.5) * 2 * math.pi) * 0.8
    lx_l = cx + math.sin(angle_l)*20*scale
    ly_l = y - leg_len + math.cos(angle_l)*5*scale
    ax.plot([cx, lx_l], [y, ly_l], color=PANTS, linewidth=8*scale)
    
    # Arms (Left swinging)
    arm_angle = -angle_l
    hand_x = cx + math.sin(arm_angle)*15*scale
    hand_y = y + body_h - 25*scale
    ax.plot([cx, hand_x], [y+body_h-5*scale, hand_y], color=SHIRT, linewidth=6*scale)
    ax.add_patch(Circle((hand_x, hand_y), 4*scale, color=SKIN))

def run():
    print(f"LOGIC GARDEN 115: HOMEWARD BOUND ({TOTAL_FRAMES} frames)")
    scale = 3.0
    
    # Screen
    sx, sy, sw, sh = 50, 600, 980, 720
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # Void
        ax.set_facecolor(C64['BLACK'])
        ax.add_patch(Rectangle((sx, sy), sw, sh, color=C64['BLACK']))
        
        # Floor
        floor_y = sy + 250
        ax.axhline(floor_y, color=C64['WHITE'], linewidth=4)
        
        # Movement: Right to Left
        start_x = sx + sw + 300
        end_x = sx - 300
        total_dist = abs(start_x - end_x)
        
        progress = f / TOTAL_FRAMES
        
        boy_x = start_x - (progress * total_dist)
        # Dog is AHEAD (to the Left), so Dog X < Boy X
        dog_x = boy_x - (80 * scale)
        
        cycle = (f % 20) / 20.0
        
        # Draw Dog first (Ahead)
        draw_dog_left(ax, dog_x, floor_y + 20, scale, cycle)
        # Draw Boy (Behind)
        draw_boy_left(ax, boy_x, floor_y + 35, scale, cycle)
        
        # UI
        mid_screen = sx + sw/2
        dist = abs(boy_x - mid_screen)
        if dist < 250:
            ax.text(540, 1500, "LOGIC GARDEN 115", color=C64['CYAN'], ha='center',
                    fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
