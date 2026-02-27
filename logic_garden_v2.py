"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v2.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Recursive Fractal Tree ("The Infinite Tree")
STYLE:  "Organic Logic" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"     # Canvas
TRUNK_COLOR = "#0080FF"  # Azure Blue (Structure)
LEAF_A_COLOR = "#FFD700" # Cyber Yellow (Left Child)
LEAF_B_COLOR = "#FF4500" # Safety Red (Right Child)

# --- 2. THE ALGORITHM: RECURSION ---
def get_tree_segments(x, y, angle, length, depth, max_depth, sway_angle, segments, leaves):
    """
    Recursive function to calculate tree geometry.
    """
    if depth == 0:
        # We are at the tip - add a leaf!
        # Alternating colors based on parentage
        color = LEAF_A_COLOR if len(leaves) % 2 == 0 else LEAF_B_COLOR
        leaves.append((x, y, color))
        return

    # Calculate end point of this branch
    x_end = x + length * np.cos(angle)
    y_end = y + length * np.sin(angle)
    
    # Store this branch segment
    # Width gets thinner as we go up
    width = 2.0 * (depth / max_depth) ** 1.5 * 18.0 
    segments.append([(x, y), (x_end, y_end), width])
    
    # Parameters for children
    new_length = length * 0.75
    
    # The "Wind" affects the angles dynamically
    # Depth multiplier ensures the top sways more than the bottom
    wind_effect = sway_angle * (1 + (max_depth - depth) * 0.1)
    
    # Recursive Calls (The Magic)
    # Left Branch
    get_tree_segments(x_end, y_end, angle + 0.4 + wind_effect, new_length, depth - 1, max_depth, sway_angle, segments, leaves)
    # Right Branch
    get_tree_segments(x_end, y_end, angle - 0.4 + wind_effect, new_length, depth - 1, max_depth, sway_angle, segments, leaves)

def render_tree_frame(frame_id, t_val):
    """
    Renders one frame of the breathing tree.
    """
    # 1. Canvas
    fig = plt.figure(figsize=(16, 9), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(BG_COLOR)
    
    # 2. Calculate Physics (The Wind)
    # Simple harmonic motion
    sway = 0.15 * np.sin(t_val) 
    
    # 3. Build The Tree Structure
    segments_data = [] # List of [start, end, width]
    leaves_data = []   # List of (x, y, color)
    
    # Start recursion from bottom center
    # Root: (0, -4), Angle: pi/2 (Up), Length: 2.5, Depth: 9
    get_tree_segments(0, -4.5, np.pi/2, 2.2, 9, 9, sway, segments_data, leaves_data)
    
    # 4. Draw Branches (Vector Lines)
    # Split data for plotting
    lines = [s[:2] for s in segments_data]
    widths = [s[2] for s in segments_data]
    
    # Draw logic lines
    lc = LineCollection(lines, linewidths=widths, color=TRUNK_COLOR, capstyle='round')
    ax.add_collection(lc)
    
    # 5. Draw Leaves (The Fruit)
    # Only draw leaves at the tips
    for lx, ly, lcolor in leaves_data:
        # Randomize leaf size slightly for organic feel
        # Using deterministic hash of coordinates so it doesn't flicker
        seed = (lx * 100 + ly * 100) % 1
        r = 0.08 + 0.04 * seed
        
        leaf = Circle((lx, ly), r, color=lcolor, zorder=10)
        ax.add_patch(leaf)
        
    # Scale
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    
    # Output
    out_dir = "logic_garden_tree_frames"
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"tree_{frame_id:04d}.png")
    plt.savefig(filename, facecolor=BG_COLOR)
    plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    FRAMES = 300
    print("[NURSERY] Planting the Infinite Tree...")
    
    for i in range(FRAMES):
        # Time variable for wind cycle (0 to 2pi * 2)
        t = (i / FRAMES) * 2 * np.pi * 2 
        
        render_tree_frame(i, t)
        
        if i % 10 == 0:
            print(f"Frame {i}/{FRAMES}")
