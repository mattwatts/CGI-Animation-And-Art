"""
SOVEREIGN CODE: logic_garden_113_walker_v2.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 113 (The Walker)
STATUS: PATCHED (Fixed math.abs attribution error)
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
DURATION = 10
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_113_walker"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_boy(ax, x, y, scale, phase):
    # Boy Archetype
    # Primary Colors for 'Pop'
    SHIRT = C64['CYAN']
    SHORTS = C64['RED']
    SKIN = C64['LIGHTRED'] # Standard C64 Flesh tone
    SHOES = C64['WHITE']
    
    # Dimensions
    w = 24 * scale
    h = 50 * scale
    
    # Head Bob (FIXED: abs is built-in, not math.abs)
    bob = abs(math.sin(phase * 2 * math.pi)) * 5 * scale
    
    # Limb Angles
    leg_swing = math.sin(phase * 2 * math.pi)
    arm_swing = -leg_swing # Counter-balance
    
    # --- FAR SIDE ---
    # Far Leg
    fl_angle = -leg_swing * 0.5
    fl_x = x + w/2 + math.sin(fl_angle) * 15 * scale
    fl_y = y  # Foot Y target
    # Simple line leg
    ax.plot([x+w/2, fl_x], [y+20*scale + bob, fl_y], color=SKIN, linewidth=8*scale, zorder=1)
    # Shoe
    ax.add_patch(Rectangle((fl_x-5*scale, fl_y), 15*scale, 6*scale, color=SHOES, zorder=1))

    # Far Arm
    fa_angle = -arm_swing * 0.6
    fa_x = x + w/2 + math.sin(fa_angle) * 15 * scale
    fa_y = y + 30*scale 
    ax.plot([x+w/2, fa_x], [y+45*scale+bob, fa_y+bob], color=SKIN, linewidth=6*scale, zorder=0)

    # --- BODY ---
    # Torso
    ax.add_patch(Rectangle((x, y + 25*scale + bob), w, 25*scale, color=SHIRT, zorder=2))
    # Shorts
    ax.add_patch(Rectangle((x, y + 15*scale + bob), w, 10*scale, color=SHORTS, zorder=2))
    
    # Head
    head_size = 18 * scale
    ax.add_patch(Circle((x+w/2, y + 55*scale + bob), head_size/2, color=SKIN, zorder=3))
    
    # Hair (Brown cap)
    ax.add_patch(Wedge((x+w/2, y + 58*scale + bob), head_size/2 + 2*scale, 0, 180, color=C64['BROWN'], zorder=4))

    # --- NEAR SIDE ---
    # Near Leg
    nl_angle = leg_swing * 0.5
    nl_x = x + w/2 + math.sin(nl_angle) * 15 * scale
    nl_y = y
    
    ax.plot([x+w/2, nl_x], [y+20*scale + bob, nl_y], color=SKIN, linewidth=8*scale, zorder=3)
    ax.add_patch(Rectangle((nl_x-5*scale, nl_y), 15*scale, 6*scale, color=SHOES, zorder=3))

    # Near Arm
    na_angle = arm_swing * 0.6
    na_x = x + w/2 + math.sin(na_angle) * 15 * scale
    na_y = y + 30*scale
    ax.plot([x+w/2, na_x], [y+45*scale+bob, na_y+bob], color=SKIN, linewidth=6*scale, zorder=4)


def run():
    print(f"LOGIC GARDEN 113: THE WALKER ({TOTAL_FRAMES} frames)")
    scale = 4.0 # Big sprite
    
    # Screen
    sx, sy, sw, sh = 50, 600, 980, 720
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # Background
        ax.set_facecolor(C64['BLACK'])
        ax.add_patch(Rectangle((sx, sy), sw, sh, color=C64['BLACK']))
        
        # Horizon Line
        floor_y = sy + 200
        ax.axhline(floor_y, color=C64['WHITE'], linewidth=4)
        
        # Metrics
        total_dist = sw + 400
        start_x = sx - 200
        
        progress = f / TOTAL_FRAMES
        boy_x = start_x + (progress * total_dist)
        
        # Cycle
        cycle = (f % 15) / 15.0
        
        draw_boy(ax, boy_x, floor_y + 10, scale, cycle)
        
        # Text
        if 0.4 < progress < 0.6:
            ax.text(540, 1500, "LOGIC GARDEN 113", color=C64['WHITE'], ha='center',
                    fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
