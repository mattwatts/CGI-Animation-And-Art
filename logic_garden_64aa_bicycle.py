"""
SOVEREIGN CODE: logic_garden_64a_bicycle_v2.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 64A (Syntax Patched)
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
FPS = 15 # Low FPS for Retro Feel
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64a_bicycle_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE (Pepto)
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_pixel_sprite(ax, x, y, scale, wobble_y):
    # Draw simple blocks
    
    # 1. Wheels (Rotating spokes via simple color flip?)
    # Rear Wheel
    wheel_r = 10 * scale
    ax.add_patch(Circle((x - 20*scale, y), wheel_r, color=C64['BLACK']))
    ax.add_patch(Circle((x - 20*scale, y), wheel_r-3*scale, color=C64['GREY']))
    
    # Front Wheel
    ax.add_patch(Circle((x + 20*scale, y), wheel_r, color=C64['BLACK']))
    ax.add_patch(Circle((x + 20*scale, y), wheel_r-3*scale, color=C64['GREY']))

    # 2. Frame (Triangles)
    frame_col = C64['RED']
    # Top bar
    ax.plot([x-15*scale, x+10*scale], [y+10*scale, y+8*scale], color=frame_col, linewidth=5*scale)
    # Seat post
    ax.plot([x-10*scale, x], [y, y+15*scale], color=frame_col, linewidth=5*scale)
    # Handlebars
    ax.plot([x+10*scale, x+8*scale], [y+8*scale, y+20*scale], color=C64['LIGHTGREY'], linewidth=4*scale)
    
    # 3. The Kid
    body_y = y + 15*scale + wobble_y
    
    # Legs (Animation logic based on wobble)
    # Left Leg (Down)
    if wobble_y > 0:
        ax.plot([x, x-5*scale], [body_y, y-5*scale], color=C64['BLUE'], linewidth=6*scale) # Leg
    else:
        ax.plot([x, x+5*scale], [body_y, y+5*scale], color=C64['BLUE'], linewidth=6*scale) # Leg Up
        
    # Torso
    ax.add_patch(Rectangle((x - 8*scale, body_y), 16*scale, 20*scale, color=C64['CYAN']))
    
    # Head
    head_y = body_y + 22*scale
    ax.add_patch(Circle((x, head_y), 12*scale, color=C64['LIGHTRED'])) # Face
    # Helmet (Wedge now defined)
    ax.add_patch(Wedge((x, head_y+5*scale), 14*scale, 0, 180, color=C64['YELLOW'])) 
    
    # Arms
    ax.plot([x, x+12*scale], [body_y+15*scale, y+20*scale], color=C64['CYAN'], linewidth=5*scale)


def run():
    print(f"LOGIC GARDEN 64A: BICYCLE V2 ({TOTAL_FRAMES} frames)")
    
    # SCROLL ASSETS
    trees = [(random.uniform(0, 2000), random.choice([1, 1.2])) for _ in range(10)]
    
    for f in range(TOTAL_FRAMES):
        
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # 1. C64 BORDER
        ax.set_facecolor(C64['LIGHTBLUE'])
        
        # 2. VIRTUAL SCREEN AREA (roughly square in center)
        screen_x = 50
        screen_y = 600
        screen_w = 980
        screen_h = 720 # 4:3 Aspect roughly
        
        # Clip area
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, screen_h, color=C64['LIGHTBLUE'], zorder=0))
        
        # 3. BACKGROUND SCROLL
        scroll_speed = 15.0
        offset = (f * scroll_speed) % 2000
        
        # Sky
        ax.add_patch(Rectangle((screen_x, screen_y + 300), screen_w, 420, color=C64['BLUE'], zorder=1))
        # Grass
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, 300, color=C64['LIGHTGREEN'], zorder=1))
        # Sidewalk
        ax.add_patch(Rectangle((screen_x, screen_y + 50), screen_w, 100, color=C64['GREY'], zorder=2))
        
        # Trees/Houses
        for i, (tx, scale) in enumerate(trees):
            # Calc screen pos
            pos = (tx - offset) 
            if pos < -300: pos += 2000
            
            if -200 < pos < 1200:
                # Draw Tree
                # Trunk
                ax.add_patch(Rectangle((screen_x + pos, screen_y + 150), 40*scale, 100*scale, color=C64['BROWN'], zorder=1))
                # Leaves
                ax.add_patch(Circle((screen_x + pos + 20*scale, screen_y + 250 + (30*scale)), 80*scale, color=C64['GREEN'], zorder=1))

        # 4. THE KID (SPRITE 0)
        kid_x = screen_x + screen_w / 2
        kid_y = screen_y + 140
        
        # Bobbing animation
        bob = math.sin(f * 0.8) * 10
        
        draw_pixel_sprite(ax, kid_x, kid_y, 4.0, bob)
        
        # 5. SCANLINES
        for y in range(screen_y, screen_y + screen_h, 4):
            ax.axhline(y, color='black', alpha=0.1, linewidth=1)

        # 6. UI
        ax.text(540, 1600, "LOGIC GARDEN 64A", color=C64['BLUE'], ha='center',
                fontsize=40, fontname='monospace', weight='bold')
        ax.text(540, 1550, "READY.", color=C64['BLUE'], ha='center',
                fontsize=30, fontname='monospace')
        
        if f > 20:
             ax.text(540, 1500, "RUN", color=C64['BLUE'], ha='center',
                fontsize=30, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
