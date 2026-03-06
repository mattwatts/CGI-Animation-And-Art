"""
SOVEREIGN CODE: logic_garden_64z_ludicrous.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation via Python
SCENE: Spaceballs (Ludicrous Speed -> Plaid)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patheffects as pe
import os
import math
import random

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64z_ludicrous"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE (Pepto)
C64_COLORS = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

PLAID_PALETTE = [C64_COLORS['PURPLE'], C64_COLORS['RED'], C64_COLORS['ORANGE'], C64_COLORS['GREEN'], C64_COLORS['BLUE']]

class Star:
    def __init__(self):
        self.reset()
        self.y = random.uniform(0, 1920) # Start anywhere
        
    def reset(self):
        self.x = random.uniform(0, 1080)
        self.y = 1920
        self.z = random.uniform(1, 3) # Depth/Speed factor
        self.color = C64_COLORS['WHITE']
        
    def update(self, speed_factor, stretch_factor):
        speed = 20 * self.z * speed_factor
        self.y -= speed
        
        length = 10 * stretch_factor
        
        return self.x, self.y, length

def run():
    print(f"LOGIC GARDEN 64z: LUDICROUS SPEED ({TOTAL_FRAMES} frames)")
    
    stars = [Star() for _ in range(200)]
    
    # PLAID GRID SETUP
    # We simulate a tunnel of moving rectangles
    grid_rows = 20
    grid_cols = 10
    
    for f in range(TOTAL_FRAMES):
        
        # --- TIMELINE ---
        # 0-150: LIGHT SPEED (Speed 1.0)
        # 150-300: RIDICULOUS SPEED (Speed 5.0, Stretch 20)
        # 300-450: LUDICROUS SPEED (Speed 20.0, Stretch 200)
        # 450-600: PLAID (Grid Effect)
        
        mode = "LIGHT"
        speed = 1.0
        stretch = 1.0
        border_col = C64_COLORS['BLACK']
        
        if f > 150:
            mode = "RIDICULOUS"
            speed = 5.0
            stretch = 5.0
            # Alarm Flash
            if (f // 5) % 2 == 0: border_col = C64_COLORS['RED']
            
        if f > 300:
            mode = "LUDICROUS"
            speed = 30.0
            stretch = 50.0
            if (f // 2) % 2 == 0: border_col = C64_COLORS['WHITE'] # Strobe
            
        if f > 450:
            mode = "PLAID"
        
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        if mode == "PLAID":
            ax.set_facecolor(C64_COLORS['BLACK'])
            # Draw The Plaid Tunnel
            # Center is roughly (540, 960)
            cx, cy = 540, 960
            
            # Draw concentric rectangles moving OUT
            # Speed of tunnel
            tunnel_t = (f - 450) * 0.2
            
            for i in range(20):
                # Distance from center (exponential for perspective)
                z = (i + (tunnel_t % 1.0)) 
                scale = math.pow(1.3, z) * 50
                
                w = scale
                h = scale * 1.5
                
                # Interchanging colors
                col_idx = int(z + f*0.1) % len(PLAID_PALETTE)
                col = PLAID_PALETTE[col_idx]
                
                # Draw thick bands
                lw = scale * 0.2
                rect = Rectangle((cx - w/2, cy - h/2), w, h, 
                               edgecolor=col, facecolor='none', linewidth=lw)
                ax.add_patch(rect)
                
                # Add cross-hatch
                if i % 2 == 0:
                    ax.axhline(cy + h/2, color=col, linewidth=2, alpha=0.5)
                    ax.axvline(cx + w/2, color=col, linewidth=2, alpha=0.5)

        else:
            # STARFIELD MODE
            ax.set_facecolor(C64_COLORS['BLACK'])
            
            # Border Flash logic (Draw large rect behind)
            if border_col != C64_COLORS['BLACK']:
                 # Create a border effect by drawing a slightly smaller black rect
                 # Actually, just fill BG with Border Color and draw black inner
                 ax.set_facecolor(border_col)
                 inner = Rectangle((50, 50), 980, 1820, facecolor='black')
                 ax.add_patch(inner)

            for s in stars:
                sx, sy, slen = s.update(speed, stretch)
                
                # C64 Pixel Art Star: Just a line
                ax.plot([sx, sx], [sy, sy + slen], color='white', linewidth=3)
                
                if s.y < -500: s.reset()

        # UI TEXT (C64 Style)
        stroke = [pe.withStroke(linewidth=0, foreground="black")] # No smooth stroke, retro style
        
        txt = "LIGHT SPEED"
        col = C64_COLORS['LIGHTBLUE']
        
        if mode == "RIDICULOUS":
            txt = "RIDICULOUS SPEED"
            col = C64_COLORS['YELLOW']
        elif mode == "LUDICROUS":
            txt = "LUDICROUS SPEED"
            col = C64_COLORS['RED']
        elif mode == "PLAID":
            txt = "THEY'VE GONE TO PLAID!"
            col = C64_COLORS['WHITE']

        # Draw Text with a "Blocky" feel (using Monospace)
        # Shadow
        ax.text(540+5, 1600-5, txt, color=C64_COLORS['DARKGREY'], ha='center',
                fontsize=40, fontname='monospace', weight='bold')
        # Main
        ax.text(540, 1600, txt, color=col, ha='center',
                fontsize=40, fontname='monospace', weight='bold')

        # FOOTER
        ax.text(540, 200, "C64 VIC-II EMULATION", color=C64_COLORS['LIGHTGREY'], ha='center',
                fontsize=20, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
