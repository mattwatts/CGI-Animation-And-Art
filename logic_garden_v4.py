"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v4.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Conway's Game of Life (Emergence)
STYLE:  "The Living City" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"       # The Void
GRID_COLOR = "#F0F0F0"     # Soft Guide Lines (Very subtle)
NEWBORN_COLOR = "#FFD700"  # Cyber Yellow (Birth)
SURVIVOR_COLOR = "#0080FF" # Azure Blue (Structure)

# --- 2. THE SIMULATION ---
ROWS, COLS = 30, 50 

def init_grid(seed_type='soup'):
    # Fix seed for deterministic chaos
    np.random.seed(42) 
    
    # 20% Life Density
    grid = np.zeros((ROWS, COLS), dtype=int)
    grid = np.random.choice([0, 1], size=(ROWS, COLS), p=[0.8, 0.2])
    
    ages = np.zeros((ROWS, COLS), dtype=int)
    return grid, ages

def update_grid(grid, ages):
    new_grid = np.zeros((ROWS, COLS), dtype=int)
    new_ages = np.zeros((ROWS, COLS), dtype=int)
    
    # Iterate with wrap-around (Toroidal) for infinite feel
    for r in range(ROWS):
        for c in range(COLS):
            # Calculate neighbors efficiently
            r_min, r_max = max(0, r-1), min(ROWS, r+2)
            c_min, c_max = max(0, c-1), min(COLS, c+2)
            
            subgrid = grid[r_min:r_max, c_min:c_max]
            neighbors = np.sum(subgrid) - grid[r, c]
            
            # THE RULES
            if grid[r, c] == 1:
                # ALIVE
                if neighbors < 2 or neighbors > 3:
                    # DIE (Lonely or Crowded)
                    new_grid[r, c] = 0
                    new_ages[r, c] = 0
                else:
                    # SURVIVE
                    new_grid[r, c] = 1
                    new_ages[r, c] = ages[r, c] + 1
            else:
                # DEAD
                if neighbors == 3:
                    # BIRTH
                    new_grid[r, c] = 1
                    new_ages[r, c] = 0 # Newborn
                    
    return new_grid, new_ages

def render_life_frame(grid, ages, frame_id):
    # 1. Canvas
    fig = plt.figure(figsize=(16, 9), dpi=100)
    
    # Full bleed canvas
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(BG_COLOR)
    
    # 2. Draw Grid (Optional structure)
    for x in range(COLS + 1):
        ax.axvline(x, color=GRID_COLOR, linewidth=1)
    for y in range(ROWS + 1):
        ax.axhline(y, color=GRID_COLOR, linewidth=1)
        
    # 3. Draw Cells
    # We iterate and draw simple squares
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r, c] == 1:
                age = ages[r, c]
                
                # Logic Switch: Color based on Age
                if age == 0:
                    color = NEWBORN_COLOR # Just born!
                else:
                    color = SURVIVOR_COLOR # Established
                
                # Toy Block Aesthetic
                # y is inverted in matrix vs plot usually, so we flip r
                # (0,0) index is top-left in matrix, bottom-left in plot
                # Let's map r=0 to y=ROWS-1 (Top)
                
                # Valid Rectangle Call
                rect = Rectangle((c + 0.1, ROWS - r - 1 + 0.1), 0.8, 0.8, 
                                 facecolor=color, edgecolor=None)
                ax.add_patch(rect)
                
    # Scale
    ax.set_xlim(0, COLS)
    ax.set_ylim(0, ROWS)
    ax.set_aspect('equal')
    
    # Save
    out_dir = "logic_garden_life_frames"
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"life_{frame_id:04d}.png")
    plt.savefig(filename, facecolor=BG_COLOR)
    plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    FRAMES = 400
    print("[NURSERY] Initializing The Living Grid...")
    
    grid, ages = init_grid(seed_type='soup')
    
    for i in range(FRAMES):
        render_life_frame(grid, ages, i)
        grid, ages = update_grid(grid, ages)
        
        if i % 20 == 0:  # Status report every 20 frames
             print(f"Frame {i}/{FRAMES}")
