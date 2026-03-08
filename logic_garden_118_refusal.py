"""
SOVEREIGN CODE: logic_garden_118_refusal.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 118 (Walk Right, Stop, Turn, Walk Left)
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
FPS = 20
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_118_refusal"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 
    'GREY': '#777777', 'LIGHTGREY': '#BBBBBB'
}

def draw_boy(ax, x, y, scale, phase, facing='right'):
    # Boy Palette
    SHIRT = C64['CYAN']
    SHORTS = C64['RED']
    SKIN = C64['LIGHTRED']
    SHOES = C64['WHITE']
    HAIR = C64['BROWN']
    
    w = 24 * scale
    
    # Idle dampener
    if phase == 0:
        bob = math.sin(x * 0.1) * 2 # Breathing while idle
        leg_swing = 0
        arm_swing = 0
    else:
        bob = abs(math.sin(phase * 2 * math.pi)) * 5 * scale
        leg_swing = math.sin(phase * 2 * math.pi)
        arm_swing = -leg_swing

    cx = x
    d = 1 if facing == 'right' else -1
    
    # --- LIMBS ---
    # Far Leg
    fl_angle = -leg_swing * 0.5
    fl_x = cx - (d * math.sin(fl_angle) * 15 * scale)
    fl_y = y
    
    ax.plot([cx, fl_x], [y+20*scale + bob, fl_y], color=SKIN, linewidth=8*scale, zorder=1)
    ax.add_patch(Rectangle((fl_x - (10*scale if d==-1 else 5*scale), fl_y), 15*scale, 6*scale, color=SHOES, zorder=1))

    # Far Arm
    fa_angle = -arm_swing * 0.6
    fa_x = cx - (d * math.sin(fa_angle) * 15 * scale)
    fa_y = y + 30*scale
    ax.plot([cx, fa_x], [y+45*scale+bob, fa_y+bob], color=SKIN, linewidth=6*scale, zorder=0)

    # --- BODY ---
    ax.add_patch(Rectangle((cx - w/2, y + 25*scale + bob), w, 25*scale, color=SHIRT, zorder=2))
    ax.add_patch(Rectangle((cx - w/2, y + 15*scale + bob), w, 10*scale, color=SHORTS, zorder=2))
    
    # Head
    head_size = 18 * scale
    ax.add_patch(Circle((cx, y + 55*scale + bob), head_size/2, color=SKIN, zorder=3))
    
    # Hair
    ax.add_patch(Wedge((cx, y + 58*scale + bob), head_size/2 + 2*scale, 0, 180, color=HAIR, zorder=4))

    # --- NEAR SIDE ---
    nl_angle = leg_swing * 0.5
    nl_x = cx - (d * math.sin(nl_angle) * 15 * scale)
    nl_y = y
    
    ax.plot([cx, nl_x], [y+20*scale + bob, nl_y], color=SKIN, linewidth=8*scale, zorder=3)
    ax.add_patch(Rectangle((nl_x - (10*scale if d==-1 else 5*scale), nl_y), 15*scale, 6*scale, color=SHOES, zorder=3))

    # Near Arm
    na_angle = arm_swing * 0.6
    na_x = cx - (d * math.sin(na_angle) * 15 * scale)
    na_y = y + 30*scale
    ax.plot([cx, na_x], [y+45*scale+bob, na_y+bob], color=SKIN, linewidth=6*scale, zorder=4)


def run():
    print(f"LOGIC GARDEN 118: REFUSAL ({TOTAL_FRAMES} frames)")
    scale = 4.0
    
    sx, sy, sw, sh = 50, 600, 980, 720
    
    frames_in = 100
    frames_wait = 50 # Longer pause for rejection
    frames_out = 100
    
    start_x_left = sx - 100
    center_x = sx + sw/2
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # Background
        ax.set_facecolor(C64['BLACK'])
        ax.add_patch(Rectangle((sx, sy), sw, sh, color=C64['BLACK']))
        ax.axhline(sy + 200, color=C64['WHITE'], linewidth=4)
        
        boy_x = 0
        facing = 'right'
        phase = 0
        caption = ""
        
        if f < frames_in:
            # Walk IN (Rights)
            progress = f / frames_in
            # Ease out
            p_eased = 1 - (1 - progress)**2
            boy_x = start_x_left + (p_eased * (center_x - start_x_left))
            facing = 'right'
            phase = f / 15.0
            
        elif f < frames_in + frames_wait:
            # Idle
            boy_x = center_x
            facing = 'right'
            phase = 0
            if f > frames_in + 20: caption = "..."
            
        else:
            # Walk OUT (Lefts) - REFUSAL
            t = (f - (frames_in + frames_wait)) / frames_out
            p_eased = t * t # Accelerate out
            if p_eased > 1.0: p_eased = 1.0
            
            boy_x = center_x - (p_eased * (center_x - start_x_left))
            facing = 'left'
            phase = f / 15.0
            caption = "LOGIC GARDEN 118"

        draw_boy(ax, boy_x, sy + 210, scale, phase, facing)
        
        if caption:
            ax.text(540, 1500, caption, color=C64['WHITE'], ha='center',
                    fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
