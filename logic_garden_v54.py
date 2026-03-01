"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v54_fixed.py
MODE:   Nursery (Relativity Palette)
TARGET: Time Dilation (Calibrated Speed)
STYLE:  "The Stretched Second" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import os

# --- 1. THE RELATIVITY PALETTE ---
BG_SPACE = "#050510"        # Vacuum
MIRROR_COL = "#C0C0C0"      # Matter
PHOTON_STATIC = "#00FFFF"   # Cyan (Reference)
PHOTON_MOVING = "#FF00FF"   # Magenta (Dilated)
TRACE_PATH = "#FFFFFF"      # History

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class LightClock:
    def __init__(self, start_x, y_pos, velocity_ratio, label, color):
        self.x = start_x
        self.y = y_pos
        self.v_ratio = velocity_ratio # Fraction of c
        self.color = color
        self.label = label
        
        # Dimensions
        self.mirror_sep = 3.0 # Height
        self.mirror_w = 2.0   # Width
        
        # Physics Constants
        # We need the moving clock to cross ~20 units in 1200 frames
        # v ~ 20/1200 = 0.0166 units/frame
        # If v = 0.866c, then c = v / 0.866 = 0.0192
        self.c = 0.020 
        
        self.vx_clock = self.c * self.v_ratio
        
        # Photon Velocity Components
        # Photon X speed = Clock X speed (Galilean relativity for transverse motion)
        # Photon Y speed = sqrt(c^2 - vx^2)
        # This ensures total speed = c
        self.p_vx = self.vx_clock
        self.p_vy = np.sqrt(self.c**2 - self.p_vx**2)
        
        # Photon Position
        self.px = self.x
        self.py = self.y - self.mirror_sep/2 + 0.1 # Start at bottom
        
        self.ticks = 0
        self.direction = 1 # 1 = Up, -1 = Down
        self.path = [] # Trail
        
    def update(self):
        # Move Clock
        self.x += self.vx_clock
        
        # Move Photon
        self.px += self.p_vx
        self.py += self.p_vy * self.direction
        
        # Record Trail
        self.path.append((self.px, self.py))
        if len(self.path) > 400: self.path.pop(0) # Long tail
        
        # Check Bounces
        top_limit = self.y + self.mirror_sep/2
        btm_limit = self.y - self.mirror_sep/2
        
        # BOUNCE TOP
        if self.direction == 1 and self.py >= top_limit:
            self.py = top_limit
            self.direction = -1
            # Half-tick (Buzz)
            
        # BOUNCE BOTTOM (Full Tick)
        if self.direction == -1 and self.py <= btm_limit:
            self.py = btm_limit
            self.direction = 1
            self.ticks += 1

class RelativitySim:
    def __init__(self):
        # Stationary Clock at Top (-8, 4)
        self.clock_a = LightClock(-8.0, 4.0, 0.0, "STATIONARY (v=0)", PHOTON_STATIC)
        
        # Moving Clock at Bottom (-8, -4)
        # v = 0.866c gives Gamma = 2.0
        self.clock_b = LightClock(-8.0, -4.0, 0.866, "MOVING (v=0.866c)", PHOTON_MOVING)
        
    def update(self, frame_idx):
        self.clock_a.update()
        self.clock_b.update()

    def render(self, frame_idx, ax):
        # Fixed Camera covering the "Race Track"
        # From -12 to +14
        ax.set_xlim(-12, 14)
        ax.set_ylim(-10, 10)
        
        # Grid lines (Static Reference Frame)
        for i in range(-12, 15, 2):
            alpha = 0.2 if i % 4 != 0 else 0.4
            ax.plot([i, i], [-10, 10], color="#202030", linewidth=1, alpha=alpha, zorder=0)

        # Render Clocks
        for clk in [self.clock_a, self.clock_b]:
            
            # 1. Mirrors
            w = clk.mirror_w
            h = clk.mirror_sep
            # Top Mirror
            ax.add_patch(Rectangle((clk.x - w/2, clk.y + h/2), w, 0.3, color=MIRROR_COL))
            # Bottom Mirror
            ax.add_patch(Rectangle((clk.x - w/2, clk.y - h/2 - 0.3), w, 0.3, color=MIRROR_COL))
            
            # 2. Light Path (Trail)
            if len(clk.path) > 1:
                px, py = zip(*clk.path)
                ax.plot(px, py, color=clk.color, linewidth=1.5, alpha=0.5, linestyle='-')
            
            # 3. Photon
            ax.add_patch(Circle((clk.px, clk.py), 0.2, color=clk.color, zorder=10))
            ax.add_patch(Circle((clk.px, clk.py), 0.5, color=clk.color, alpha=0.3, zorder=9))
            
            # 4. Connecting Line (Clock Frame Vertical)
            # Visualize the "vertical" movement relative to the clock itself
            ax.plot([clk.x, clk.x], [clk.y - h/2, clk.y + h/2], color="white", linestyle=":", alpha=0.1)

            # 5. Tick Counter
            ax.text(clk.x, clk.y, f"{clk.ticks}", color="white", ha='center', va='center',
                    fontsize=24, fontfamily='monospace', fontweight='bold')
            
            # Label
            ax.text(clk.x, clk.y + h/2 + 1.0, clk.label, color=clk.color, ha='center', fontsize=10)

        # HUD
        ax.text(1, 9, "LOGIC GARDEN 54: THE STRETCHED SECOND", color="white", ha='center', fontweight='bold', fontsize=14)
        
        # Calc Gamma Live
        ticks_a = self.clock_a.ticks + (self.clock_a.py - (self.clock_a.y - 1.5))/3.0 # Approximate fractional tick
        # Simple integer ticks calculation for display
        ratio = "Waiting..."
        if self.clock_b.ticks > 0:
            r = self.clock_a.ticks / self.clock_b.ticks
            ratio = f"RATIO: {r:.1f} : 1"
            
        ax.text(1, -9, f"TIME DILATION: 2.0x | {ratio}", color=PHOTON_MOVING, ha='center', fontfamily='monospace')

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_time_fixed_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"time_fixed_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_SPACE)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Simulating Relativistic Mechanic (Slow)...")
    
    sim = RelativitySim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(12, 8), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_SPACE)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
