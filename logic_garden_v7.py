"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v7.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Phyllotaxis (The Golden Ratio)
STYLE:  "The Perfect Packer" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"       # Void
SEED_COLORS = ["#FFD700", "#FF4500", "#0080FF"] # Yellow, Red, Blue

# --- 2. CONFIGURATION ---
MAX_SEEDS = 600
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
GOLDEN_ANGLE = 137.507764  # The Magic Number (Degrees)
SCALE_C = 0.4              # Spread factor

def render_flower_frame(frame_idx):
    # 1. Canvas
    fig = plt.figure(figsize=(16, 9), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(BG_COLOR)
    
    # 2. Logic: How many seeds exist right now?
    # Ramps up linearly
    # We want to fill the screen by the end
    progress = frame_idx / TOTAL_FRAMES
    current_seed_count = int(progress * MAX_SEEDS) + 1
    
    # 3. Calculate Positions (Vectorized)
    indices = np.arange(current_seed_count)
    
    # Angle theta = n * Golden Angle (in radians)
    thetas = indices * (GOLDEN_ANGLE * np.pi / 180.0)
    
    # Radius r = c * sqrt(n)
    radii = SCALE_C * np.sqrt(indices)
    
    # Polar to Cartesian
    x = radii * np.cos(thetas)
    y = radii * np.sin(thetas)
    
    # 4. Coloring Logic
    # We assign colors based on index modulo 3
    # This might show specific spiral arms depending on Fibonacci numbers
    colors = [SEED_COLORS[i % 3] for i in indices]
    
    # 5. Draw
    # We draw them as scatter points? Or Circles for "Toy" look?
    # Scatter is faster but Circles look nicer. 
    # Let's use Scatter for speed, but size them nicely.
    
    # Size grows slightly as they move out? 
    # In real sunflowers, outer seeds are older/larger. 
    # Let's make size proportional to sqrt(index) slightly or constant.
    # Constant size "Toy Pegs" looks cleaner for Bauhaus.
    sizes = 400 * np.ones_like(indices) # Area in points^2
    
    # To handle overlapping or "growth pop", maybe animate size of the NEWEST/LAST seed?
    # The last 5 seeds are "popping in"
    if len(sizes) > 0:
        sizes[-1] = sizes[-1] * (frame_idx % 5 + 1) / 5.0 # Pop effect? No, keep it clean.
        
        # Better: Scale the whole flower so the camera stays centered but "zooms out" 
        # as new seeds appear? 
        # No, let the flower fill the frame.
    
    ax.scatter(x, y, s=sizes, c=colors, alpha=1.0, edgecolors='none')
    
    # 6. Scale
    # Fix the scale to the FINAL size so we see it filling up
    # Max radius will be c * sqrt(MAX_SEEDS)
    max_r = SCALE_C * np.sqrt(MAX_SEEDS) * 1.2 # padding
    limit = 10.0 # Standard logic garden unit
    
    # Use dynamic limit? No, fixed limits reinforces "Space Filling"
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit * (9/16), limit * (9/16)) # Aspect ratio match
    ax.set_aspect('equal')
    
    # 7. Output
    out_dir = "logic_garden_flower_frames"
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"flower_{frame_idx:04d}.png")
    plt.savefig(filename, facecolor=BG_COLOR)
    plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Planting the Golden Seeds...")
    for i in range(TOTAL_FRAMES):
        render_flower_frame(i)
        if i % 50 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
