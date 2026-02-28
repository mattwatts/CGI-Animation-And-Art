"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v44_fixed.py
MODE:   Nursery (High Gravity Palette)
TARGET: Tidal Disruption Event (TDE) / Spaghettification
STYLE:  "The Unravelling" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import os

# --- 1. THE HIGH GRAVITY PALETTE ---
BG_COLOR = "#050010"        # Deep Gravity Well
BH_COLOR = "#000000"        # Event Horizon
BH_GLOW = "#4B0082"         # Indigo Lensing

STAR_CORE = "#FFFFFF"       # Dense Core
STAR_NOSE = "#FF0055"       # The "Victim" (Front)
STAR_TAIL = "#0088FF"       # The "Survivor" (Back)
ACCRETION = "#FFFF00"       # Shock Heat

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40               # 40 Seconds (Slow Motion)
TOTAL_FRAMES = FPS * DURATION

class Debris:
    def __init__(self, x, y, vx, vy, color_type):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.active = True
        self.color_type = color_type # 'core', 'nose', 'tail'
        self.hist_x = []
        self.hist_y = []

class TDESim:
    def __init__(self):
        # Physics Constants
        self.G = 1.0
        self.M_BH = 800.0 
        
        # Star Initial State (Closer start, slower approach for detail)
        self.star_x = -5.0
        self.star_y = 5.0
        
        # Velocity tuning: Aim for a Parabolic trajectory that grazes the Event Horizon
        # This maximizes the stretching time
        self.star_vx = 0.5
        self.star_vy = -0.3
        self.star_r = 0.4
        
        self.particles = []
        self.accretion_glow = 0.0
        
        # Initialize 2000 Particles (High Density Fluid)
        for i in range(2000):
            # create a solid sphere distribution relative to star center
            # Rejection sampling for uniform circle
            while True:
                dx = np.random.uniform(-1, 1)
                dy = np.random.uniform(-1, 1)
                if dx*dx + dy*dy <= 1.0:
                    break
            
            # Position
            px = self.star_x + dx * self.star_r
            py = self.star_y + dy * self.star_r
            
            # Color Coding based on position relative to BH
            # To show the gradient, we color based on initial distance to BH
            # Nose = Red, Tail = Blue
            
            # Rotate vectors to match approach angle roughly (-45 deg)
            # Project d onto velocity vector
            proj = dx * 1.0 + dy * -1.0
            
            if proj > 0.3: col = STAR_NOSE    # Leading edge
            elif proj < -0.3: col = STAR_TAIL # Trailing edge
            else: col = STAR_CORE             # Core
            
            self.particles.append(Debris(px, py, self.star_vx, self.star_vy, col))

    def update(self, frame_idx):
        tidal_radius = 3.0
        dt = 0.02 # Slow time step for precision
        
        center_x = 0
        center_y = 0
        
        for p in self.particles:
            if not p.active: continue
            
            dx = center_x - p.x
            dy = center_y - p.y
            dist_sq = dx*dx + dy*dy
            dist = np.sqrt(dist_sq)
            
            # NEWTONIAN GRAVITY (with softening)
            # F = G * M / r^2
            force = (self.G * self.M_BH) / (dist_sq + 0.1)
            
            ax = (dx / dist) * force
            ay = (dy / dist) * force
            
            p.vx += ax * dt
            p.vy += ay * dt
            
            p.x += p.vx * dt
            p.y += p.vy * dt
            
            # Event Horizon Consumption
            if dist < 0.3:
                p.active = False
                self.accretion_glow = min(1.0, self.accretion_glow + 0.01)

    def render(self, frame_idx, ax):
        # Camera that zooms slightly or tracks?
        # Let's keep a wide Fixed View to see the scale of stretching
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        
        # 1. Black Hole
        # Glow
        glow_size = 0.8 + self.accretion_glow * 0.5
        ax.add_patch(Circle((0,0), glow_size, color=BH_GLOW, alpha=0.3, zorder=5))
        if self.accretion_glow > 0.1:
             ax.add_patch(Circle((0,0), 0.6, color=ACCRETION, alpha=self.accretion_glow, zorder=6))
             
        # Event Horizon
        ax.add_patch(Circle((0,0), 0.3, color=BH_COLOR, zorder=10))
        
        # 2. Tidal Radius (Roche Limit)
        ax.add_patch(Circle((0,0), 2.5, color="white", fill=False, linestyle='--', alpha=0.1))

        # 3. Particles (Batch render for speed)
        px_nose, py_nose = [], []
        px_core, py_core = [], []
        px_tail, py_tail = [], []
        
        for p in self.particles:
            if not p.active: continue
            if p.color_type == STAR_NOSE:
                px_nose.append(p.x); py_nose.append(p.y)
            elif p.color_type == STAR_TAIL:
                px_tail.append(p.x); py_tail.append(p.y)
            else:
                px_core.append(p.x); py_core.append(p.y)
                
        # Draw Tails (Blue) - They lag behind
        if px_tail: ax.scatter(px_tail, py_tail, color=STAR_TAIL, s=10, alpha=0.6, edgecolors='none', zorder=7)
        # Draw Nose (Red) - They fall in first
        if px_nose: ax.scatter(px_nose, py_nose, color=STAR_NOSE, s=10, alpha=0.8, edgecolors='none', zorder=8)
        # Draw Core (White)
        if px_core: ax.scatter(px_core, py_core, color=STAR_CORE, s=12, alpha=1.0, edgecolors='none', zorder=9)

        # 4. HUD
        # Phase Detection based on geometry
        # Find average distance
        avg_dist = 0
        active_count = 0
        if self.particles:
             avg_dist = np.mean([np.sqrt(p.x**2 + p.y**2) for p in self.particles if p.active])
        
        if frame_idx < 300:
            phase = "PHASE 1: THE APPROACH (GRAVITY GRADIENT DETECTED)"
            col = "white"
        elif frame_idx < 800:
            phase = "PHASE 2: SPAGHETTIFICATION (STRETCHING)"
            col = STAR_NOSE
        else:
            phase = "PHASE 3: ACCRETION & UNBINDING"
            col = ACCRETION
            
        ax.text(0, -5, phase, color=col, ha='center', fontfamily='monospace', fontsize=12,
               bbox=dict(facecolor='black', edgecolor=col, alpha=0.8))

        # Legend
        ax.text(-5, 5, "NOSE (FAST)", color=STAR_NOSE, fontsize=8, fontweight='bold')
        ax.text(-5, 4.7, "TAIL (SLOW)", color=STAR_TAIL, fontsize=8, fontweight='bold')
        ax.text(0, 2.6, "ROCHE LIMIT", color="white", fontsize=6, ha='center', alpha=0.5)

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_tde_slow_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"tde_slow_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Simulating {TOTAL_FRAMES} frames of Spaghettification...")
    
    sim = TDESim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(12, 12), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
