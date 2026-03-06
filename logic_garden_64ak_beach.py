"""
SOVEREIGN CODE: logic_garden_64ak_beach.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 64AK (Beach Loop)
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
DURATION = 20 # 2 cycles of 10s?
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64ak_beach"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE (Pepto)
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_waves(ax, screen_rect, t):
    sx, sy, sw, sh = screen_rect
    
    # Horizon Y
    horizon_y = sy + sh * 0.6
    shore_y = sy + 100
    
    # Draw Water Base
    ax.add_patch(Rectangle((sx, shore_y), sw, horizon_y - shore_y, color=C64['BLUE']))
    
    # Draw Waves (Lines shifting down)
    # Perspective: Gap increases as y decreases (closer)
    # Actually, simpler: Linear movement with Z depth scaling
    
    num_waves = 8
    cycle_len = 100 # Frames for a wave to travel full distance?
    
    # We create a looping phase for waves
    phase = (t % cycle_len) / cycle_len
    
    for i in range(num_waves):
        # Normalized position (0=Horizon, 1=Shore)
        # We stagger them
        wave_norm = (phase + i/num_waves) % 1.0
        
        # Apply perspective transform (exponential)
        # y = horizon - (dist * scale)? 
        # Easier: Lerp from Horizon to Shore
        # Non-linear to simulate depth
        
        visual_y = horizon_y - (wave_norm**2) * (horizon_y - shore_y)
        
        # Width/Scale of wave line
        thickness = 1 + (wave_norm * 10)
        alpha = 0.5 + (wave_norm * 0.5)
        
        # Foam Color logic (White crest, then fade)
        col = C64['WHITE']
        if wave_norm > 0.9: # Breaking on shore
            col = C64['CYAN'] # Fade
            
        # Draw Wave Line
        ax.plot([sx, sx+sw], [visual_y, visual_y], color=col, linewidth=thickness, alpha=alpha)


def draw_boy_sitting(ax, x, y, scale, tick):
    # Back view
    
    # Body (Red Shirt)
    # Rounded rect
    ax.add_patch(Rectangle((x - 10*scale, y), 20*scale, 18*scale, color=C64['RED']))
    
    # Legs (Shorts/Legs extended?) 
    # Sitting cross-legged or knees up? 
    # Let's do sitting looking out, knees up.
    # Legs (Skin)
    ax.add_patch(Circle((x - 8*scale, y), 6*scale, color=C64['ORANGE'])) # Left Knee
    ax.add_patch(Circle((x + 8*scale, y), 6*scale, color=C64['ORANGE'])) # Right Knee
    
    # Arms (Bracing behind or on knees?)
    # On knees
    ax.plot([x - 10*scale, x - 8*scale], [y + 12*scale, y + 2*scale], color=C64['ORANGE'], linewidth=3*scale)
    ax.plot([x + 10*scale, x + 8*scale], [y + 12*scale, y + 2*scale], color=C64['ORANGE'], linewidth=3*scale)
    
    # Head (Brown Hair) - Slight bob
    bob = math.sin(tick * 0.05) * 2
    head_y = y + 20*scale + bob
    
    ax.add_patch(Circle((x, head_y), 7*scale, color=C64['ORANGE'])) # Neck/Face
    ax.add_patch(Circle((x, head_y + 2*scale), 8*scale, color=C64['BROWN'])) # Hair


def run():
    print(f"LOGIC GARDEN 64AK: THE TIDE ({TOTAL_FRAMES} frames)")
    
    scale = 6.0
    
    # Loop
    # 20 seconds loop
    
    for f in range(TOTAL_FRAMES):
        
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # 1. BORDER
        ax.set_facecolor(C64['LIGHTBLUE'])
        
        # 2. CRT AREA
        screen_x = 50
        screen_y = 600
        screen_w = 980
        screen_h = 720
        
        # Mask
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, screen_h, color=C64['LIGHTBLUE'], zorder=0))
        
        # 3. BACKGROUND LAYERS
        sx, sy, sw, sh = screen_x, screen_y, screen_w, screen_h
        
        # Sky
        horizon_y = sy + sh * 0.6
        ax.add_patch(Rectangle((sx, horizon_y), sw, sh*0.4, color=C64['CYAN'], zorder=1))
        
        # Sun (Setting/Low)
        ax.add_patch(Circle((sx + sw*0.8, horizon_y + 80), 50, color=C64['YELLOW'], zorder=2))
        
        # Waves logic
        draw_waves(ax, (sx, sy, sw, sh), f)
        
        # Sand (Bottom)
        shore_y = sy + 100 # Overlap drawing
        ax.add_patch(Rectangle((sx, sy), sw, 150, color=C64['YELLOW'], zorder=5))
        
        # Wet Sand (Darker Yellow/Brown band where waves hit)
        # Oscillates with tide
        tide_h = math.sin(f * 0.05) * 20
        ax.add_patch(Rectangle((sx, sy + 140 + tide_h), sw, 20, color=C64['BROWN'], alpha=0.5, zorder=5))
        
        # 4. BOY SPRITE
        boy_x = sx + sw/2
        boy_y = sy + 80 # Sitting on sand
        
        draw_boy_sitting(ax, boy_x, boy_y, scale, f)
        
        # Scanlines
        for y in range(screen_y, screen_y + screen_h, 4):
            ax.axhline(y, color='black', alpha=0.1, linewidth=1, zorder=10)

        # UI
        stroke = [pe.withStroke(linewidth=0, foreground="black")]
        
        ax.text(540, 1600, "LOGIC GARDEN 64AK", color=C64['BLUE'], ha='center',
                fontsize=40, fontname='monospace', weight='bold', path_effects=[pe.withStroke(linewidth=4, foreground=C64['WHITE'])])
        
        ax.text(540, 1500, "HIGH TIDE", color=C64['WHITE'], ha='center',
                fontsize=30, fontname='monospace', weight='bold', path_effects=[pe.withStroke(linewidth=4, foreground=C64['BLUE'])])

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
