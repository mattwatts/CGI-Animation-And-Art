"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v51.py
MODE:   Nursery (Cosmology Palette)
TARGET: The Big Bang (Metric Expansion)
STYLE:  "The Inflation" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os

# --- 1. THE COSMIC PALETTE ---
BG_VOID = "#000000"         # Nothing
PL_WHITE = "#FFFFFF"        # Singularity
INF_VIOLET = "#8A2BE2"      # Inflation
PL_ORANGE = "#FF4500"       # Plasma (Opaque)
CMB_BLUE = "#000020"        # Background Radiation
ST_GOLD = "#FFD700"         # First Stars

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class Matter:
    def __init__(self, r, theta):
        self.r0 = r      # Co-moving coordinate
        self.theta = theta
        self.r_current = 0
        self.x = 0
        self.y = 0
        self.active = True
        self.is_star = False
        
        # Quantum Fluctuation (Seed)
        # Some areas are slightly denser
        self.density_bias = np.random.uniform(0.8, 1.2)

class UniverseSim:
    def __init__(self):
        self.scale_factor = 0.001
        self.temperature = 1000000 # Kelvin-ish scale
        self.particles = []
        
        # Initialize Uniform Universe (Seeds)
        # 1000 Particles
        for i in range(1000):
            # Uniform distribution in circle
            r = np.sqrt(np.random.uniform(0, 1)) * 5.0
            theta = np.random.uniform(0, 2*np.pi)
            self.particles.append(Matter(r, theta))
            
    def get_color(self, temp):
        # Temperature to Hex approx
        if temp > 10000: return PL_WHITE
        if temp > 5000: return INF_VIOLET
        if temp > 3000: return PL_ORANGE
        if temp > 500: return "#402020" # Dark Ages cooling
        return "#101030" # Cold gas

    def update(self, frame_idx):
        # 1. EXPANSION LOGIC (Cosmic Scale Factor a(t))
        if frame_idx < 100: # Singularity/Inflation
            # Exponential Burst
            self.scale_factor *= 1.05
        elif frame_idx < 400: # Radiation Dominated (Decelerating)
            self.scale_factor += 0.01
        elif frame_idx < 800: # Matter Dominated
            self.scale_factor += 0.005
        else: # Dark Energy (Accelerating)
            self.scale_factor *= 1.002
            
        # 2. COOLING LOGIC
        # T ~ 1/a
        self.temperature = 10000 / (self.scale_factor * 10 + 0.1)
        
        # 3. STRUCTURE FORMATION (Gravity)
        # Once cool enough, particles clump based on initial density bias
        gravity_on = (frame_idx > 600)
        
        # Update Particles
        center_clump_factor = 0.0
        
        for p in self.particles:
            # Expansion
            p.r_current = p.r0 * self.scale_factor
            
            # Position
            p.x = p.r_current * np.cos(p.theta)
            p.y = p.r_current * np.sin(p.theta)
            
            # Gravity (Simple Clustering approximation)
            if gravity_on:
                # Move slightly towards neighbors or denser seeds
                # We simulate this by perturbing r0 based on density bias
                # High density bias pulls in (shrinks r0 relative to expansion)
                if p.density_bias > 1.0:
                    p.r0 *= 0.999 # Clump
                    # Chance to ignite star
                    target_density = 0.5 # Visual density threshold
                    if frame_idx > 900 and not p.is_star:
                         if np.random.random() < 0.01:
                             p.is_star = True
                else:
                    p.r0 *= 1.001 # Void expands

    def render(self, frame_idx, ax):
        # Dynamic Camera Limit (Zoom out as universe grows)
        limit = max(10, self.scale_factor * 6.0)
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        # Background Color (CMB Evolution)
        # Starts White -> Orange -> Black/Blue
        bg = BG_VOID
        if self.temperature > 4000: bg = PL_WHITE
        elif self.temperature > 3000: bg = PL_ORANGE
        elif self.temperature > 1000: # Recombination transparency
            # Interpolate Orange to Black? 
            # Hard color step for Recombination event
            pass 
            
        # For simplicity in Matplotlib without complex blending, keep black BG
        # and use a large patch for the "Fog"
        
        track_color = self.get_color(self.temperature)
        
        # 1. The Fog (Background Plasma)
        if self.temperature > 1000:
            # Draw big circle filling universe
            fog_r = limit * 1.5
            alpha = min(1.0, self.temperature / 3000.0)
            ax.add_patch(Circle((0,0), fog_r, color=track_color, alpha=alpha, zorder=0))

        # 2. The Matter
        px = [p.x for p in self.particles]
        py = [p.y for p in self.particles]
        sizes = [15 * self.scale_factor for p in self.particles] # Matter spreads out visually
        
        # Star Logic
        stars_x = [p.x for p in self.particles if p.is_star]
        stars_y = [p.y for p in self.particles if p.is_star]
        
        # Render Gas/Matter
        if self.temperature < 3000: # Transparent universe
             ax.scatter(px, py, c="#404040", s=5, alpha=0.5, zorder=5)
             
        # Render Stars (Dawn)
        if stars_x:
            ax.scatter(stars_x, stars_y, c=ST_GOLD, s=20, marker='*', zorder=10)
            # Twinkle
            if frame_idx % 2 == 0:
                ax.scatter(stars_x, stars_y, c="white", s=5, zorder=11)

        # 3. HUD
        # Time Epoch
        epoch = "T ~ 0"
        if frame_idx < 50: epoch = "EPOCH: SINGULARITY (PLANCK)"
        elif frame_idx < 150: epoch = "EPOCH: INFLATION (EXPONENTIAL)"
        elif frame_idx < 400: epoch = "EPOCH: PLASMA SOUP (OPAQUE)"
        elif frame_idx < 600: epoch = "EPOCH: RECOMBINATION (CLEARING)"
        elif frame_idx < 900: epoch = "EPOCH: DARK AGES (GRAVITY)"
        else: epoch = "EPOCH: COSMIC DAWN (STARS)"
        
        temp_disp = f"TEMP: {int(self.temperature)} K"
        
        ax.text(0, limit*0.8, epoch, color="white", ha='center', fontfamily='monospace', fontsize=12,
               bbox=dict(facecolor='black', edgecolor='white'))
        ax.text(0, limit*0.7, temp_disp, color="white", ha='center', fontsize=8)

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_bb_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"bb_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Initiating Big Bang...")
    
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
