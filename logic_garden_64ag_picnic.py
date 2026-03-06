"""
SOVEREIGN CODE: logic_garden_64ag_picnic.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 64AG (Picnic)
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
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64ag_picnic"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE (Pepto)
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_kid(ax, x, y, scale, color, state, bite_count):
    # State: IDLE, EAT, CHEW
    
    # Sitting Body (Torso)
    ax.add_patch(Rectangle((x, y+10*scale), 12*scale, 16*scale, color=color))
    
    # Legs (Crossed)
    ax.plot([x+2*scale, x+15*scale], [y+10*scale, y], color='blue', linewidth=4*scale) # Jeans
    ax.plot([x+10*scale, x-2*scale], [y+10*scale, y], color='blue', linewidth=4*scale)
    
    # Head
    head_y = y + 26*scale
    ax.add_patch(Circle((x+6*scale, head_y), 6*scale, color=C64['LIGHTRED']))
    
    # Mouth (Chew animation)
    mouth_y = head_y - 2*scale
    if state == "CHEW":
        ax.add_patch(Circle((x+7*scale, mouth_y), 1.5*scale, color=C64['BLACK']))
    else:
        ax.plot([x+6*scale, x+8*scale], [mouth_y, mouth_y], color=C64['BLACK'], linewidth=1*scale)

    # Arm Logic
    shoulder_x = x + 10*scale
    shoulder_y = y + 22*scale
    
    hand_x = x + 15*scale
    hand_y = y + 12*scale # Lap
    
    if state == "EAT" or state == "CHEW":
        # Hand to mouth
        hand_x = x + 10*scale
        hand_y = head_y - 4*scale
        
    ax.plot([shoulder_x, hand_x], [shoulder_y, hand_y], color=color, linewidth=3*scale)
    
    # Hand
    ax.add_patch(Circle((hand_x, hand_y), 2.5*scale, color=C64['LIGHTRED']))
    
    # Sandwich (Triangle)
    # Shrink based on bites
    sw_size = 6*scale - (bite_count * 1.0*scale)
    if sw_size < 0: sw_size = 0
    
    if sw_size > 0:
        # Draw attached to hand
        # Simple yellow wedge
        p = Polygon([
            (hand_x, hand_y),
            (hand_x + sw_size, hand_y + sw_size),
            (hand_x, hand_y + sw_size*1.5)
        ], closed=True, color=C64['YELLOW'])
        ax.add_patch(p)

def run():
    print(f"LOGIC GARDEN 64AG: PICNIC ({TOTAL_FRAMES} frames)")
    
    # State
    kid1_bites = 0
    kid2_bites = 0
    
    # Timeline
    # Kid 1 eats: 0-30
    # Kid 2 eats: 30-60
    
    scale = 6.0
    k1_x = 250
    k1_y = 700
    k2_x = 750
    k2_y = 700
    
    for f in range(TOTAL_FRAMES):
        
        cycle = f % 60
        
        k1_state = "IDLE"
        k2_state = "IDLE"
        
        # LOGIC
        if cycle < 15:
            k1_state = "EAT" # Lift
        elif cycle < 30:
            k1_state = "CHEW"
            if cycle == 15: kid1_bites += 0.2 # Increment bite logic
        elif cycle < 45:
            k2_state = "EAT"
        elif cycle < 60:
            k2_state = "CHEW"
            if cycle == 45: kid2_bites += 0.2
            
        # Reset sandwiches if gone
        if kid1_bites > 5: kid1_bites = 0
        if kid2_bites > 5: kid2_bites = 0

        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # 1. BORDER
        ax.set_facecolor(C64['LIGHTBLUE'])
        
        # 2. CRT
        screen_x = 50
        screen_y = 600
        screen_w = 980
        screen_h = 720
        
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, screen_h, color=C64['LIGHTBLUE'], zorder=0))
        
        # Ground
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, 300, color=C64['GREEN'], zorder=1))
        
        # Blanket (Checkered)
        bx = 150 + screen_x
        by = screen_y + 20
        bw = 650
        bh = 200
        ax.add_patch(Rectangle((bx, by), bw, bh, color=C64['WHITE'], zorder=2))
        # Checks
        grid_sz = 50
        for gx in range(0, int(bw), grid_sz):
            for gy in range(0, int(bh), grid_sz):
                if (gx//grid_sz + gy//grid_sz) % 2 == 0:
                    ax.add_patch(Rectangle((bx+gx, by+gy), grid_sz, grid_sz, color=C64['RED'], zorder=3))

        # 3. KIDS
        draw_kid(ax, k1_x, k1_y, scale, C64['CYAN'], k1_state, kid1_bites)
        draw_kid(ax, k2_x, k2_y, scale, C64['PURPLE'], k2_state, kid2_bites)

        # 4. SCANLINES
        for y in range(screen_y, screen_y + screen_h, 4):
            ax.axhline(y, color='black', alpha=0.1, linewidth=1)

        # 5. UI
        stroke = [pe.withStroke(linewidth=0, foreground="black")]
        
        ax.text(540, 1600, "LOGIC GARDEN 64AG", color=C64['WHITE'], ha='center',
                fontsize=40, fontname='monospace', weight='bold', path_effects=[pe.withStroke(linewidth=4, foreground=C64['BLUE'])])

        ax.text(540, 1500, "LUNCH BREAK", color=C64['YELLOW'], ha='center',
                fontsize=30, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
