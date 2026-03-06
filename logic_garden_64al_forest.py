"""
SOVEREIGN CODE: logic_garden_64al_forest.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 64AL (Eucalypt Forest)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Wedge
import matplotlib.patheffects as pe
import os
import math
import random

# CONFIG
FPS = 15
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64al_forest"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE (Pepto)
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_eucalypt(ax, x, width, height, tick):
    # Trunk (Ghost Gum style - White/Light Grey with Brown patches)
    ax.add_patch(Rectangle((x, 0), width, height, color=C64['LIGHTGREY']))
    
    # Bark patches (Peeling)
    random.seed(x) # Consistent scarring
    for i in range(10):
        py = random.uniform(50, height-50)
        ph = random.uniform(20, 100)
        # Scar
        ax.add_patch(Rectangle((x + random.uniform(0, width-20), py), random.uniform(10, 30), ph, color=C64['GREY']))
        # Strip hanging off?
        if random.random() > 0.5:
            ax.plot([x+width, x+width+10], [py, py-50], color=C64['GREY'], linewidth=2)

    # Canopy (High up)
    # Eucalypt leaves hang down
    foliage_y = height * 0.6
    
    wind = math.sin(tick * 0.05 + x) * 10
    
    # Leaf Clusters
    for i in range(20):
        lx = x + random.uniform(-100, width+100)
        ly = random.uniform(foliage_y, height)
        
        # Sway
        swayed_lx = lx + wind * (ly/height) # More sway higher up? Or lower hanging tips?
        # Hanging tips sway more
        
        # Draw vertically hanging leaf cluster
        ax.plot([lx, swayed_lx], [ly, ly-60], color=C64['GREEN'], linewidth=3, alpha=0.8)
        ax.plot([lx, swayed_lx+5], [ly, ly-50], color=C64['LIGHTGREEN'], linewidth=2, alpha=0.6)

def draw_boy_standing(ax, x, y, scale):
    # Small, insignificant against the trees
    # Red shirt for contrast
    
    # Body
    ax.add_patch(Rectangle((x-5*scale, y), 10*scale, 15*scale, color=C64['RED']))
    # Legs (Jeans)
    ax.add_patch(Rectangle((x-5*scale, y-12*scale), 4*scale, 12*scale, color=C64['BLUE']))
    ax.add_patch(Rectangle((x+1*scale, y-12*scale), 4*scale, 12*scale, color=C64['BLUE']))
    
    # Head
    head_y = y + 15*scale
    ax.add_patch(Circle((x, head_y), 5*scale, color=C64['LIGHTRED']))
    
    # Minimalist face (looking up)
    # Just a pixel for eye
    ax.add_patch(Rectangle((x+2*scale, head_y+1*scale), 1*scale, 1*scale, color=C64['BLACK']))

def run():
    print(f"LOGIC GARDEN 64AL: FOREST ({TOTAL_FRAMES} frames)")
    
    # SCENE SETUP
    trees = [
        {'x': 100, 'w': 80, 'h': 1200},
        {'x': 800, 'w': 120, 'h': 1200},
        {'x': -50, 'w': 60, 'h': 1200}, # Far left
        {'x': 450, 'w': 40, 'h': 900}   # Background tree (Darker?)
    ]
    
    scale = 4.0
    
    for f in range(TOTAL_FRAMES):
        
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # 1. BACKGROUND (Deep Forest Shadow)
        ax.set_facecolor(C64['BLACK'])
        # Virtual Screen
        screen_x, screen_y, screen_w, screen_h = 50, 600, 980, 720
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, screen_h, color=C64['BLACK'], zorder=0))
        
        # Ground (Forest Floor - Brown/Green mix)
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, 150, color=C64['BROWN'], zorder=1))
        
        # 2. TREES
        # Sort by depth roughly? 
        # Draw background tree first
        
        # Tree 3 (Midground)
        t = trees[3]
        # Darker tint? Simulate by using darker palette
        # Just standard
        draw_eucalypt(ax, screen_x + t['x'], t['w']*scale, screen_h + 400, f)
        
        # Tree 0, 1, 2 (Foreground)
        for i in [0, 1, 2]:
            t = trees[i]
            draw_eucalypt(ax, screen_x + t['x'], t['w']*scale, screen_h + 500, f)

        # 3. BOY SPRITE
        # In front of Tree 0, 3 but behind 1?
        # Let's put him central
        boy_x = screen_x + 350
        boy_y = screen_y + 100 # Ground level
        
        draw_boy_standing(ax, boy_x, boy_y, scale)
        
        # 4. LIGHTING (Dappled Light Effect)
        # Overlay patches of alpha white/yellow to simulate sun breaking through canopy
        # These shift slightly
        light_shift = math.sin(f * 0.02) * 50
        for i in range(5):
            lx = screen_x + 200 + (i*200) + light_shift
            ly = screen_y + 100
            ax.add_patch(Circle((lx, ly), 80, color=C64['YELLOW'], alpha=0.1, zorder=10))

        # 5. SCANLINES
        for y in range(screen_y, screen_y + screen_h, 4):
            ax.axhline(y, color='black', alpha=0.1, linewidth=1, zorder=20)

        # UI
        stroke = [pe.withStroke(linewidth=0, foreground="black")]
        ax.text(540, 1600, "LOGIC GARDEN 64AL", color=C64['GREEN'], ha='center',
                fontsize=40, fontname='monospace', weight='bold', path_effects=[pe.withStroke(linewidth=4, foreground=C64['WHITE'])])
        ax.text(540, 1500, "OLD GROWTH", color=C64['LIGHTGREEN'], ha='center',
                fontsize=30, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
