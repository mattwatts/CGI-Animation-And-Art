"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v14.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Reaction-Diffusion (Turing Patterns)
STYLE:  "The Living Skin" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

# --- 1. THE NURSERY PALETTE ---
# Gradient: Yellow (Base) -> Red (Growth) -> Blue (Structure)
COLORS = ["#FFD700", "#FFFFFF", "#FF4500", "#0080FF"]
# Mapping: Low B (Background) -> High B (Pattern)
CMAP = LinearSegmentedColormap.from_list("ZebraWash", ["#FFD700", "#FFFFFF", "#FF4500", "#000514"], N=256)
# Note: Reversed palette relative to usual heatmaps looks organic. 
# Background = Yellow/White. Spots = Red/Black/Blue.

# --- 2. CONFIGURATION ---
WIDTH = 192   # 16:9 Aspect (Low resolution for diffusion speed)
HEIGHT = 108
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
STEPS_PER_FRAME = 20 # Speed up simulation

# Gray-Scott Parameters (Coral / Maze)
Du, Dv = 0.16, 0.08
f, k = 0.060, 0.062  # "The Soliton / Fingerprint" regime

class PetriDish:
    def __init__(self):
        # Initialize Chemicals
        # U = 1.0 (Food)
        # V = 0.0 (Killer)
        self.U = np.ones((HEIGHT, WIDTH))
        self.V = np.zeros((HEIGHT, WIDTH))
        
        # Seed the chaos (A small square of V in the center)
        # Or random noise? 
        # Random noise allows "Emergence" from everywhere.
        h, w = HEIGHT, WIDTH
        
        # Central square seed
        r = 10
        self.V[h//2-r:h//2+r, w//2-r:w//2+r] = 0.25
        
        # Add slight noise to break symmetry
        noise = np.random.rand(HEIGHT, WIDTH) * 0.05
        self.U += noise
        self.V += noise * 0.5

    def laplacian(self, M):
        # Finite difference convolution (3x3 Laplacian)
        # Weights:
        # 0.05  0.20  0.05
        # 0.20 -1.00  0.20
        # 0.05  0.20  0.05
        # We can implement this fast using roll (Periodic Boundary)
        
        top     = np.roll(M, -1, axis=0)
        bottom  = np.roll(M, 1, axis=0)
        left    = np.roll(M, -1, axis=1)
        right   = np.roll(M, 1, axis=1)
        
        # Diagonals slightly simpler or omitted for speed? 
        # Standard 5-point stencil (0, 1, 0...) is faster but 9-point is isotropic.
        # Let's use simple 5-point stencil for "Blocky" look (Toy physics).
        # Center -4, Neighbors +1
        
        lap = (top + bottom + left + right - 4*M)
        return lap

    def update(self):
        # Run multiple sub-steps
        for _ in range(STEPS_PER_FRAME):
            Lu = self.laplacian(self.U)
            Lv = self.laplacian(self.V)
            
            # Reaction
            # U + 2V -> 3V  (Reaction rate uv^2)
            uvv = self.U * self.V * self.V
            
            # Diffusion + Reaction + Feed/Kill
            # du/dt = Du*LapU - uvv + f*(1-u)
            # dv/dt = Dv*LapV + uvv - (f+k)*v
            
            self.U += (Du * Lu - uvv + f * (1 - self.U))
            self.V += (Dv * Lv + uvv - (f + k) * self.V)
            
            # Clip
            self.U = np.clip(self.U, 0, 1)
            self.V = np.clip(self.V, 0, 1)

    def render(self, frame_idx):
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # 2. Draw The Chemical V (The Pattern)
        # We use imshow with interpolation to smooth the grid
        ax.imshow(self.V, cmap=CMAP, interpolation='bicubic', vmin=0, vmax=0.4)
        
        # 3. Add Title? No, "Zero Noise".
        
        # Save
        out_dir = "logic_garden_zebra_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"zebra_{frame_idx:04d}.png")
        plt.savefig(filename)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Growing the Zebra Coat...")
    dish = PetriDish()
    
    for i in range(TOTAL_FRAMES):
        dish.update()
        dish.render(i)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
