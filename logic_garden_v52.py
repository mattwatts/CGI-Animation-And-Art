"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v52_fixed.py
MODE:   Nursery (Entropy Palette)
TARGET: Heat Death (Alpha Channel Correction)
STYLE:  "The Long Fade" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import os

# --- 1. THE ENTROPY PALETTE ---
BG_VOID = "#000000"         # Maximum Entropy
ST_GOLD = "#FFD700"         # Main Sequence
ST_RED = "#8B0000"          # Red Dwarf / Dying
REM_WHITE = "#A0A0A0"       # White Dwarf
BH_BLACK = "#101010"        # Black Hole
HAWKING_FLASH = "#00FFFF"   # Evaporation

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = 'star' # star, remnant, bh, dead
        self.fuel = np.random.uniform(0.5, 1.0)
        self.mass = np.random.uniform(0.1, 5.0)
        self.life_timer = 0
        self.flash_timer = 0
        self.born_year = 10.0

class UniverseSim:
    def __init__(self):
        self.stars = []
        self.time_log = 10.0 # Start at 10^10 years
        self.expansion = 1.0
        
        # Init Galaxy Cluster (500 stars)
        for i in range(500):
            # Spiral distribution
            theta = np.random.uniform(0, 4*np.pi)
            r = theta * 0.5 + np.random.normal(0, 0.2)
            x = r * np.cos(theta) * 0.5 + np.random.normal(0, 0.5)
            y = r * np.sin(theta) * 0.5 + np.random.normal(0, 0.5)
            self.stars.append(Star(x, y))
            
    def update(self, frame_idx):
        # Time accelerates logarithmically
        # 10^10 -> 10^100 over 40 seconds
        time_step = (100.0 - 10.0) / TOTAL_FRAMES
        self.time_log += time_step
        
        # Expansion
        self.expansion *= 1.002
        
        current_year_exp = self.time_log
        
        for s in self.stars:
            # Move
            s.x *= 1.002
            s.y *= 1.002
            
            # --- EVOLUTION LOGIC ---
            
            # 1. Star Death
            if s.type == 'star':
                if current_year_exp > 13 + s.fuel: 
                    if s.mass > 3.0:
                        s.type = 'bh'
                    else:
                        s.type = 'remnant'
                        
            # 2. Remnant Cooling (White Dwarf -> Black Dwarf)
            if s.type == 'remnant':
                # Cools down by 10^20
                if current_year_exp > 22:
                    s.type = 'dead_remnant' 
            
            # 3. Black Hole Evaporation
            if s.type == 'bh':
                # Bigger stars = longer lived, but we speed it up for visual
                # Start evaporating around 10^35 - 10^60 range
                decay_start = 35.0 + s.mass * 8.0
                
                if current_year_exp > decay_start:
                    if s.flash_timer == 0:
                        s.flash_timer = 15 # visible flash 0.5s
                    else:
                        s.flash_timer -= 1
                        if s.flash_timer <= 1:
                            s.type = 'evaporated'

    def render(self, frame_idx, ax):
        # Dynamic Camera
        # Expands with universe but slightly slower to simulate drift
        current_limit = 10 * (1 + frame_idx * 0.0025)
        ax.set_xlim(-current_limit, current_limit)
        ax.set_ylim(-current_limit, current_limit)
        
        px_st, py_st = [], []
        px_rem, py_rem = [], []
        px_bh, py_bh = [], []
        px_flash, py_flash = [], []
        
        # Sort for rendering
        for s in self.stars:
            if abs(s.x) > current_limit * 1.2: continue # Optimization
            
            if s.type == 'star':
                px_st.append(s.x); py_st.append(s.y)
            elif s.type == 'remnant':
                px_rem.append(s.x); py_rem.append(s.y)
            elif s.type == 'bh':
                px_bh.append(s.x); py_bh.append(s.y)
                # Check flash
                if s.flash_timer > 0:
                    px_flash.append(s.x); py_flash.append(s.y)

        # 1. Active Stars
        if px_st: 
            # Dimming curve clamped 0-1
            # Fades out by 10^15
            raw_alpha = 1.0 - (self.time_log - 10)/5.0
            alpha = np.clip(raw_alpha, 0.2, 1.0)
            
            # Shift color to Red as time goes on
            color = ST_GOLD if self.time_log < 12.5 else ST_RED
            ax.scatter(px_st, py_st, c=color, s=20, alpha=alpha, edgecolors='none', zorder=10)
            
        # 2. Remnants
        if px_rem:
            # Cooling curve
            # Starts bright at 14, fades by 22
            fade_progress = (self.time_log - 13.0) / 9.0 
            # Inverse
            raw_alpha = 1.0 - fade_progress
            rem_alpha = np.clip(raw_alpha, 0.0, 1.0)
            
            if rem_alpha > 0.01:
                ax.scatter(px_rem, py_rem, c=REM_WHITE, s=5, alpha=rem_alpha, zorder=5)
            
        # 3. Black Holes
        if px_bh:
            ax.scatter(px_bh, py_bh, c="#151515", s=15, edgecolors="#252525", linewidth=0.5, zorder=4)
            
        # 4. Hawking Flashes
        if px_flash:
            # Bright cyan burst
            ax.scatter(px_flash, py_flash, c=HAWKING_FLASH, s=60, marker='+', zorder=20)
            ax.scatter(px_flash, py_flash, c="white", s=25, zorder=21)

        # HUD
        era = "ERA: STELLAR (LIGHT)"
        col = ST_GOLD
        
        if self.time_log > 14:
            era = "ERA: DEGENERATE (REMNANTS)"
            col = ST_RED
        if self.time_log > 22:
             era = "ERA: BLACK HOLE (DARK)"
             col = "#505050"
        if self.time_log > 90:
             era = "ERA: DARK (MAX ENTROPY)"
             col = "#202020"
             
        # Log Year Counter
        year_str = f"YEAR: 10^{int(self.time_log)}"
        
        limit_h = current_limit
        ax.text(0, -limit_h*0.8, era, color=col, ha='center', fontfamily='monospace', fontsize=14, fontweight='bold')
        ax.text(0, -limit_h*0.9, year_str, color="white", ha='center', fontfamily='monospace', fontsize=10)

        # Entropy Meter
        entropy = np.clip((self.time_log - 10) / 90.0, 0.0, 1.0)
        
        # Frame
        bar_w = limit_h * 1.5
        ax.add_patch(Rectangle((-bar_w/2, limit_h*0.9), bar_w, limit_h*0.05, 
                              facecolor="#101010", edgecolor="#303030"))
        # Fill
        ax.add_patch(Rectangle((-bar_w/2, limit_h*0.9), bar_w * entropy, limit_h*0.05, 
                              color=col))
        
        ax.text(0, limit_h*0.85, "ENTROPY", color="white", ha='center', fontsize=6)

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        # Ensure dir exists
        out_dir = "logic_garden_hd_fixed_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"hd_fixed_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Simulating Entropy Increase (Fixed)...")
    
    sim = UniverseSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_VOID)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
