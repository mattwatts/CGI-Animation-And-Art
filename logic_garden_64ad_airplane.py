"""
SOVEREIGN CODE: logic_garden_64ad_airplane.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 64AD (Airplane)
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
OUT_DIR = "frames_64ad_airplane"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE (Pepto)
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_plane_sprite(ax, x, y, scale, tick):
    # Fuselage (White cigar shape)
    ax.add_patch(Rectangle((x, y), 60*scale, 14*scale, color=C64['WHITE']))
    # Cockpit window (Cyan/Black)
    p = Polygon([
        (x + 40*scale, y + 14*scale),
        (x + 45*scale, y + 20*scale),
        (x + 55*scale, y + 14*scale)
    ], closed=True, color=C64['CYAN'])
    ax.add_patch(p)
    
    # Tail
    p_tail = Polygon([
        (x, y + 14*scale),
        (x, y + 25*scale),
        (x + 10*scale, y + 14*scale)
    ], closed=True, color=C64['RED'])
    ax.add_patch(p_tail)
    
    # Wing (Main) - Trapezoid
    p_wing = Polygon([
        (x + 25*scale, y + 8*scale),
        (x + 45*scale, y + 8*scale),
        (x + 40*scale, y - 5*scale),
        (x + 30*scale, y - 5*scale)
    ], closed=True, color=C64['GREY'])
    ax.add_patch(p_wing)
    # Wing Strut
    ax.plot([x + 35*scale, x + 35*scale], [y, y-5*scale], color=C64['BLACK'], linewidth=1*scale)

    # Trim Line (Red)
    ax.add_patch(Rectangle((x, y+5*scale), 60*scale, 2*scale, color=C64['RED']))
    
    # Engine Cowl
    ax.add_patch(Rectangle((x + 58*scale, y + 2*scale), 4*scale, 10*scale, color=C64['GREY']))
    
    # Propeller (0: Vertical, 1: Horizontal)
    prop_x = x + 62*scale
    prop_y = y + 7*scale
    
    if tick % 2 == 0:
        # Vertical Stick
        ax.plot([prop_x, prop_x], [prop_y - 15*scale, prop_y + 15*scale], color=C64['BLACK'], linewidth=2*scale)
        # Blur disc
        ax.add_patch(Circle((prop_x, prop_y), 12*scale, color=C64['GREY'], alpha=0.3))
    else:
        # Cross / Blur
        ax.add_patch(Circle((prop_x, prop_y), 10*scale, color=C64['BLACK'], alpha=0.5))

    # Wheels
    ax.add_patch(Circle((x + 40*scale, y - 10*scale), 4*scale, color=C64['BLACK']))
    ax.plot([x + 40*scale, x + 40*scale], [y, y - 10*scale], color=C64['GREY'], linewidth=2*scale)


def run():
    print(f"LOGIC GARDEN 64AD: AIRPLANE ({TOTAL_FRAMES} frames)")
    
    # CLOUD ASSETS
    clouds = [] # (x, y, scale, speed, type)
    for i in range(15):
        clouds.append({
            'x': random.uniform(0, 2000),
            'y': random.uniform(50, 400),
            'scale': random.uniform(0.5, 1.5),
            'speed': random.uniform(2, 8)
        })
        
    for f in range(TOTAL_FRAMES):
        
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
        
        # Sky Background
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, screen_h, color=C64['LIGHTBLUE'], zorder=0))
        
        # Sun
        ax.add_patch(Circle((screen_x + 850, screen_y + 600), 60, color=C64['YELLOW'], zorder=1))
        
        # 3. CLOUDS (Parallax)
        for c in clouds:
            # Move
            c['x'] -= c['speed']
            if c['x'] < -200: c['x'] += 1500 # Wrap
            
            # Draw (3 circles)
            cx = screen_x + c['x']
            cy = screen_y + c['y']
            s = c['scale'] * 40
            
            if -300 < cx < 1200:
                ax.add_patch(Circle((cx, cy), s, color=C64['WHITE'], zorder=1))
                ax.add_patch(Circle((cx + s, cy + s*0.5), s*0.8, color=C64['WHITE'], zorder=1))
                ax.add_patch(Circle((cx - s, cy + s*0.5), s*0.8, color=C64['WHITE'], zorder=1))
        
        # 4. AIRPLANE SPRITE
        plane_x = screen_x + 300
        plane_y = screen_y + 300
        
        # Bobbing
        bob = math.sin(f * 0.2) * 15
        
        draw_plane_sprite(ax, plane_x, plane_y + bob, 4.0, f)
        
        # Exhaust trail (Particles)
        if f % 3 == 0:
             # Add simple particles logic? Or just draw static trail for simplicity
             # Simple dots trailing behind
             for i in range(5):
                 tx = plane_x - (i * 60) - (f%20 * 5)
                 ty = plane_y + bob + 5
                 if i > 0:
                    ax.add_patch(Circle((tx, ty), 5 - i, color=C64['WHITE'], alpha=0.5))

        # 5. GROUND (Far below)
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, 50, color=C64['GREEN'], zorder=2))
        
        # 6. SCANLINES
        for y in range(screen_y, screen_y + screen_h, 4):
            ax.axhline(y, color='black', alpha=0.1, linewidth=1)

        # 7. UI
        stroke = [pe.withStroke(linewidth=0, foreground="black")]
        
        ax.text(540, 1600, "LOGIC GARDEN 64AD", color=C64['WHITE'], ha='center',
                fontsize=40, fontname='monospace', weight='bold', path_effects=[pe.withStroke(linewidth=4, foreground=C64['BLUE'])])
        
        ax.text(540, 1500, "TAKE FLIGHT", color=C64['BLUE'], ha='center',
                fontsize=30, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
