"""
SOVEREIGN CODE: logic_garden_111_dog.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 111 (Dog Walk)
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
DURATION = 10
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_111_dog"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_dog(ax, x, y, scale, phase):
    """
    Draws a dog at x,y with a walk cycle 'phase' (0.0 to 1.0).
    """
    # Colors
    FUR = C64['YELLOW'] # Golden Retriever
    EAR = C64['BROWN']
    NOSE = C64['BLACK']
    COLLAR = C64['RED']
    
    # Body Geometry (Oval-ish rect)
    ax.add_patch(Rectangle((x, y), 60*scale, 30*scale, color=FUR))
    
    # Tail (Wagging)
    # Sine wave wag
    tail_wag = math.sin(phase * 4 * math.pi) * 20
    tail_base_x = x
    tail_base_y = y + 25*scale
    ax.plot([tail_base_x, tail_base_x - 20*scale], [tail_base_y, tail_base_y + 10*scale + tail_wag], 
            color=FUR, linewidth=5*scale)
            
    # Head 
    head_x = x + 50*scale
    head_y = y + 20*scale
    # Head Bob (Vertical)
    bob = math.sin(phase * 4 * math.pi) * 2
    
    ax.add_patch(Circle((head_x, head_y + bob), 18*scale, color=FUR))
    
    # Earl (Floppy)
    ax.add_patch(Ellipse((head_x + 5*scale, head_y + bob + 5*scale), 12*scale, 20*scale, color=EAR))
    
    # Snout
    ax.add_patch(Rectangle((head_x + 10*scale, head_y + bob - 5*scale), 15*scale, 12*scale, color=FUR))
    ax.add_patch(Circle((head_x + 25*scale, head_y + bob + 5*scale), 3*scale, color=NOSE)) # Nose tip
    
    # Collar
    ax.add_patch(Rectangle((x + 50*scale, y + 15*scale), 5*scale, 15*scale, color=COLLAR))
    
    # LEGS (The hard part)
    # 4 Legs. 
    # Phase offset: Front Right (0), Back Left (0.25), Front Left (0.5), Back Right (0.75)
    
    leg_w = 8 * scale
    leg_h = 25 * scale
    
    def draw_leg(lx, ly, l_phase, color):
        # A simple pendulum swing
        angle = math.sin((phase + l_phase) * 2 * math.pi)
        
        # Knee position
        kx = lx + (math.sin(angle) * 10 * scale)
        ky = ly - leg_h
        
        # Foot lift
        lift = max(0, -math.sin(angle + math.pi/2)) * 10 * scale
        
        ax.plot([lx, kx], [ly, ky+lift], color=color, linewidth=leg_w)
        # Paw
        ax.plot([kx, kx+5*scale], [ky+lift, ky+lift], color=color, linewidth=leg_w)

    # Back Legs (Darker/Behind)
    draw_leg(x + 10*scale, y, 0.5, C64['ORANGE'])     # Back Left
    draw_leg(x + 55*scale, y, 0.0, C64['ORANGE'])     # Front Left (Actually Far side)
    
    # Body obscures far legs (redraw body bottom edge?) 
    # Let's just layer them first.
    
    # Front Legs (Lighter/Front)
    draw_leg(x + 10*scale, y, 0.0, FUR)     # Back Right
    draw_leg(x + 55*scale, y, 0.5, FUR)     # Front Right

from matplotlib.patches import Ellipse

def run():
    print(f"LOGIC GARDEN 111: THE GOOD BOY ({TOTAL_FRAMES} frames)")
    
    scale = 3.0
    
    # Virtual Screen
    sx, sy, sw, sh = 50, 600, 980, 720
    
    for f in range(TOTAL_FRAMES):
        
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # Background
        ax.set_facecolor(C64['BLACK'])
        
        # C64 Screen Mask
        ax.add_patch(Rectangle((sx, sy), sw, sh, color=C64['BLACK']))
        
        # Floor (White Line)
        floor_y = sy + 250
        ax.axhline(floor_y, color=C64['WHITE'], linewidth=4)
        
        # Dog Movement
        # Start off screen left -> End off screen right
        total_dist = sw + 400
        start_x = sx - 200
        
        progress = f / TOTAL_FRAMES
        dog_x = start_x + (progress * total_dist)
        dog_y = floor_y + 30 # Pivot point
        
        # Walk Cycle Phase (Frequency)
        cycle_freq = 20 # Frames per step cycle
        phase = (f % cycle_freq) / cycle_freq
        
        draw_dog(ax, dog_x, dog_y, scale, phase)
        
        # Text
        text_col = C64['GREY']
        if 0.4 < progress < 0.6: # Center screen
            text_col = C64['WHITE'] # Pop
            
        ax.text(540, 1500, "LOGIC GARDEN 111", color=text_col, ha='center',
                fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
