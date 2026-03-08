"""
SOVEREIGN CODE: logic_garden_114_return.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 114 (Dog Return - Right to Left)
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
DURATION = 10
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_114_return"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_dog_left(ax, x, y, scale, phase):
    """
    Draws a dog facing LEFT.
    All X-offsets are inverted relative to the Right-facing version.
    """
    # Colors
    FUR = C64['YELLOW']
    EAR = C64['BROWN']
    NOSE = C64['BLACK']
    COLLAR = C64['RED']
    SHADOW = C64['ORANGE'] # For far legs
    
    # Body Geometry (Anchored at X, extends Left)
    # Let X be the "Front Shoulder".
    
    # Body: X is shoulder. Body extends RIGHT in coordinate space if facing LEFT?
    # Let's treat X,Y as the center of the shoulder.
    
    # If walking LEFT: Head is at X-offset, Tail is at X+offset.
    
    # Body Rect
    # (x, y) is Top-Left of rect usually. 
    # Let's centre it slightly.
    body_w = 60 * scale
    ax.add_patch(Rectangle((x, y), body_w, 30*scale, color=FUR))
    
    # Tail (Wagging at Right end of body)
    # Tail base at x + body_w
    wag = math.sin(phase * 4 * math.pi) * 20
    tail_base_x = x + body_w
    tail_base_y = y + 25*scale
    # Tail points Right/Up
    ax.plot([tail_base_x, tail_base_x + 20*scale], [tail_base_y, tail_base_y + 10*scale + wag], 
            color=FUR, linewidth=5*scale)
            
    # Head (At Left end of body)
    # Head base at x
    head_x = x
    head_y = y + 20*scale
    # Bob
    bob = math.sin(phase * 4 * math.pi) * 2
    
    # Cranium
    ax.add_patch(Circle((head_x, head_y + bob), 18*scale, color=FUR))
    
    # Ear
    ax.add_patch(Ellipse((head_x - 5*scale, head_y + bob + 5*scale), 12*scale, 20*scale, color=EAR))
    
    # Snout (Pointing Left)
    ax.add_patch(Rectangle((head_x - 25*scale, head_y + bob - 5*scale), 15*scale, 12*scale, color=FUR))
    ax.add_patch(Circle((head_x - 25*scale, head_y + bob + 5*scale), 3*scale, color=NOSE))
    
    # Collar
    ax.add_patch(Rectangle((x - 5*scale, y + 15*scale), 5*scale, 15*scale, color=COLLAR))
    
    # LEGS
    leg_w = 8 * scale
    leg_h = 25 * scale
    
    def draw_leg(lx, ly, l_phase, color):
        # Pendulum
        angle = math.sin((phase + l_phase) * 2 * math.pi)
        
        # Knee 
        kx = lx + (math.sin(angle) * 10 * scale)
        ky = ly - leg_h
        
        # Lift
        lift = max(0, -math.sin(angle + math.pi/2)) * 10 * scale
        
        ax.plot([lx, kx], [ly, ky+lift], color=color, linewidth=leg_w)
        # Paw (Points Left)
        ax.plot([kx, kx-5*scale], [ky+lift, ky+lift], color=color, linewidth=leg_w)

    # Back Legs (Shadow/Far) - Offset visually
    # Rear Leg (Right side of body)
    draw_leg(x + 50*scale, y, 0.5, SHADOW) 
    # Front Leg (Left side of body)
    draw_leg(x + 5*scale, y, 0.0, SHADOW)
    
    # Near Legs (Fur Color)
    draw_leg(x + 50*scale, y, 0.0, FUR) # Rear Right
    draw_leg(x + 5*scale, y, 0.5, FUR) # Front Right

def run():
    print(f"LOGIC GARDEN 114: THE RETURN ({TOTAL_FRAMES} frames)")
    scale = 3.5
    
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
        
        # Physics
        floor_y = sy + 250
        ax.axhline(floor_y, color=C64['WHITE'], linewidth=4)
        
        # Movement: Right to Left
        # Start: Screen Width + Buffer
        # End: Screen Left - Buffer
        
        total_dist = sw + 500
        start_x = sx + sw + 100
        end_x = sx - 400
        
        progress = f / TOTAL_FRAMES
        # Lerp
        dog_x = start_x + (progress * (end_x - start_x))
        dogs_y = floor_y + 30
        
        # Cycle
        cycle = (f % 20) / 20.0
        
        draw_dog_left(ax, dog_x, dogs_y, scale, cycle)
        
        # Text
        # Only show text when dog is near center
        mid_screen = sx + sw/2
        dist_from_center = abs(dog_x - mid_screen)
        
        if dist_from_center < 300:
            ax.text(540, 1500, "LOGIC GARDEN 114", color=C64['YELLOW'], ha='center',
                    fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
