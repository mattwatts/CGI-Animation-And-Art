"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v47.py
MODE:   Nursery (Kinetic Palette)
TARGET: Disney Bomb (Rocket Assisted Kinetic Penetrator)
STYLE:  "The Concrete Breaker" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import os

# --- 1. THE KINETIC PALETTE ---
BG_COLOR = "#051020"        # Night Sky
BUNKER_GREY = "#505050"     # Reinforced Concrete
BOMB_BODY = "#004000"       # Olive Drab
THRUST_CORE = "#FFFF00"     # Yellow
THRUST_OUTER = "#FF0000"    # Red
SHOCKWAVE = "#FFFFFF"       # Mach Cone

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class BombSim:
    def __init__(self):
        self.y = 10.0      # Drop height (km scale visual)
        self.v = 0.0       # Velocity
        self.fuel = 100    # Rocket burn time frames
        self.ignited = False
        self.impact = False
        self.timer = 0
        
        self.bunker_y = -5.0
        self.impact_depth = 0.0
        
    def update(self, frame_idx):
        self.timer += 1
        
        # 1. DROP PHASE
        if not self.ignited and not self.impact:
            # Gravity drag
            self.v += 0.005 # G
            self.y -= self.v
            
            # Ignite at specific altitude (y=2.0)
            if self.y < 2.0:
                self.ignited = True
                
        # 2. ROCKET ASSIST PHASE
        elif self.ignited and not self.impact:
            if self.fuel > 0:
                self.v += 0.02 # ROCKET ASSIST (4x Gravity)
                self.fuel -= 1
            else:
                self.v += 0.005 # Just gravity again
            
            self.y -= self.v
            
            # Hit Bunker
            if self.y < self.bunker_y:
                self.y = self.bunker_y
                self.impact = True
                self.impact_timer = 0
        
        # 3. PENETRATION PHASE
        elif self.impact:
            self.impact_timer += 1
            # Burrowing logic
            if self.v > 0:
                self.impact_depth += self.v * 0.5
                self.v *= 0.8 # Friction stop
                if self.v < 0.001: self.v = 0

    def render(self, frame_idx, ax):
        # Camera tracking? No, fixed wide shot to see acceleration
        ax.set_xlim(-5, 5)
        ax.set_ylim(-8, 12)
        
        # 1. The Bunker (U-Boat Pen)
        bunker_h = 3.0
        ax.add_patch(Rectangle((-8, self.bunker_y - bunker_h), 16, bunker_h, color=BUNKER_GREY))
        # Roof reinforcement pattern
        for i in range(-5, 6):
            ax.plot([i, i], [self.bunker_y, self.bunker_y-3], color="black", alpha=0.3)
            
        # 2. The Bomb
        # Draw vertically
        bx = 0
        by = self.y - self.impact_depth
        
        # Body
        b_w = 0.3
        b_h = 1.2
        poly = [
            [bx-b_w, by+b_h], [bx+b_w, by+b_h], # Tail
            [bx+b_w, by], [bx, by-0.5], [bx-b_w, by] # Nose cone
        ]
        ax.add_patch(Polygon(poly, color=BOMB_BODY))
        
        # Fins (Disney had ring tail)
        ax.add_patch(Rectangle((bx-0.4, by+b_h-0.2), 0.8, 0.1, color="black"))

        # 3. The Rocket Plume
        if self.ignited and self.fuel > 0 and not self.impact:
            # Flicker
            flame_len = np.random.uniform(1.5, 2.5)
            flame_w = np.random.uniform(0.2, 0.4)
            
            # Core
            ax.add_patch(Polygon([
                [bx-0.1, by+b_h], [bx+0.1, by+b_h],
                [bx, by+b_h+flame_len*0.8]
            ], color=THRUST_CORE))
            # Outer
            ax.add_patch(Polygon([
                [bx-0.2, by+b_h], [bx+0.2, by+b_h],
                [bx, by+b_h+flame_len]
            ], color=THRUST_OUTER, alpha=0.6))
            
            # Mach Cone (Shockwave) if fast enough
            if self.v > 0.1:
                # White cone
                angle = 0.3 # narrow
                cone = [
                    [bx, by-0.5], 
                    [bx-2, by+3],
                    [bx+2, by+3]
                ]
                ax.add_patch(Polygon(cone, color=SHOCKWAVE, alpha=0.1))

        # 4. Spalling / Impact
        if self.impact:
            # Dust
            cloud_r = min(3.0, self.impact_timer * 0.2)
            ax.add_patch(Circle((0, self.bunker_y), cloud_r, color="#606060", alpha=0.5))
            # Crater lip
            ax.plot([-1, 1], [self.bunker_y+0.1, self.bunker_y+0.1], color="black", linewidth=2)

        # 5. HUD - Velocity
        # Speedometer bar
        bar_h = self.v * 20.0
        ax.add_patch(Rectangle((-4, -7), 1, bar_h, color=THRUST_OUTER))
        ax.text(-4, -7.5, f"V: {self.v*1000:.0f} MPH", color="white", fontfamily='monospace')
        
        status = "PHASE 1: FREEFALL"
        col = "white"
        if self.ignited: 
            status = "PHASE 2: ROCKET ASSIST (BURN)"
            col = THRUST_OUTER
        if self.impact:
            status = "PHASE 3: KINETIC PENETRATION"
            col = "white"
            
        ax.text(0, 10, status, color=col, ha='center', fontfamily='monospace',
                bbox=dict(facecolor='black', edgecolor=col))

        ax.set_axis_off()
        
        out_dir = "logic_garden_disney_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"disney_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Dropping 4500lb Rocket Bomb...")
    
    sim = BombSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 16), dpi=100) # Tall aspect ratio
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
