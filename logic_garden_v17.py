"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v17.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Quantum Mechanics (Hydrogen 1s Orbital)
STYLE:  "The Lonely Cloud" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"        # Void
NUCLEUS_COLOR = "#FF4500"   # Safety Red (Proton)
ELECTRON_COLOR = "#0080FF"  # Azure Blue (Probability)
GRID_COLOR = "#F0F0F0"      # Metric

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
SAMPLES_PER_FRAME = 50      # Speed of accumulation
MAX_POINTS = 50000          # Memory limit

# Physics: Hydrogen 1s
# Probability P(r) ~ r^2 * exp(-2r/a0) in 3D sphere.
# BUT we are projecting to 2D screen. 
# Visual approximation: 2D Gaussian/Exponential drop-off looks correct for "The Cloud".
# Let's use strict Exponential decay for the radial distance in 2D to mimic the 1s look.
# Distance r = sqrt(x^2 + y^2)
# Prob ~ exp(-r)

class QuantumCloud:
    def __init__(self):
        self.history_x = []
        self.history_y = []
        
    def generate_samples(self, n):
        # Rejection Sampling for P(r) = exp(-abs(r))
        new_x = []
        new_y = []
        
        count = 0
        while count < n:
            # Random point in box [-5, 5]
            x = (np.random.rand() - 0.5) * 10
            y = (np.random.rand() - 0.5) * 10
            r = np.sqrt(x*x + y*y)
            
            # Acceptance prob
            # Using simple exponential decay for visual 1s orbital
            prob = np.exp(-1.5 * r) 
            
            if np.random.rand() < prob:
                new_x.append(x)
                new_y.append(y)
                count += 1
                
        self.history_x.extend(new_x)
        self.history_y.extend(new_y)
        
        # Limit history
        if len(self.history_x) > MAX_POINTS:
            self.history_x = self.history_x[-MAX_POINTS:]
            self.history_y = self.history_y[-MAX_POINTS:]

    def render(self, frame_idx, ax):
        # 1. Draw Grid (Subtle)
        ax.axhline(0, color=GRID_COLOR, linewidth=1)
        ax.axvline(0, color=GRID_COLOR, linewidth=1)
        
        circle1 = plt.Circle((0,0), 1.0, color=GRID_COLOR, fill=False)
        circle2 = plt.Circle((0,0), 2.0, color=GRID_COLOR, fill=False)
        ax.add_patch(circle1)
        ax.add_patch(circle2)
        
        # 2. Draw The Cloud (Electrons)
        # Use scatter with transparency to show density buildup
        ax.scatter(self.history_x, self.history_y, 
                  s=15, # Dot size
                  color=ELECTRON_COLOR, 
                  alpha=0.6, # Transparency to build up darkness
                  edgecolors='none') 
        
        # 3. Draw The Nucleus (Proton)
        # Big solid dot on top
        ax.scatter([0], [0], s=300, color=NUCLEUS_COLOR, zorder=10, edgecolors='white', linewidth=2)
        
        # 4. Draw Current Hit? (The "Pop")
        # Visual flair: Highlight the most recent points to show activity
        if len(self.history_x) > 0:
            recent_x = self.history_x[-10:]
            recent_y = self.history_y[-10:]
            ax.scatter(recent_x, recent_y, s=40, color="#FFD700", alpha=1.0, zorder=5) # Yellow Spark

        # Scale
        limit = 3.5
        # Correct aspect ratio for 16:9
        # set xlim to fit width, ylim to fit height
        # If we want circle to be circular, aspect='equal' handles it.
        ax.set_xlim(-limit * (16/9), limit * (16/9))
        ax.set_ylim(-limit, limit)
        ax.set_aspect('equal')
        
        # Save
        out_dir = "logic_garden_quantum_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"quantum_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Observing the Ghost...")
    
    cloud = QuantumCloud()
    
    # Pre-warm? No, let kids see it build up from nothing.
    
    for i in range(TOTAL_FRAMES):
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        # 2. Physics Step
        cloud.generate_samples(SAMPLES_PER_FRAME)
        
        # 3. Render
        cloud.render(i, ax)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES} | Samples: {len(cloud.history_x)}")
