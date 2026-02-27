"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v13.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Merge Sort (Divide & Conquer)
STYLE:  "The Rainbow Bridge" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

# --- 1. THE NURSERY PALETTE (Gradient) ---
BG_COLOR = "#FFFFFF"
# Gradient: Yellow -> Red -> Blue
COLORS = ["#FFD700", "#FF4500", "#0080FF"]
N_BINS = 100  # Resolution of gradient
CMAP = LinearSegmentedColormap.from_list("BauhausBridges", COLORS, N=N_BINS)

# --- 2. CONFIGURATION ---
NUM_BARS = 64  # Power of 2 makes Merge Sort look nice
FPS = 30
BAR_WIDTH = 0.8

# Global generator registry
history = []

class Sorter:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        
    def merge_sort(self, arr, left, right):
        if left >= right:
            return

        mid = (left + right) // 2
        
        # Visualize: Highlight the split?
        # yield arr.copy() 
        
        yield from self.merge_sort(arr, left, mid)
        yield from self.merge_sort(arr, mid + 1, right)
        yield from self.merge(arr, left, mid, right)

    def merge(self, arr, left, mid, right):
        # Create temp arrays
        L = arr[left:mid + 1].copy()
        R = arr[mid + 1:right + 1].copy()

        i = 0
        j = 0
        k = left

        # Merge Phase
        while i < len(L) and j < len(R):
            # Record state before change
            yield arr.copy(), [k] # Check index k
            
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            
        while i < len(L):
            yield arr.copy(), [k]
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            yield arr.copy(), [k]
            arr[k] = R[j]
            j += 1
            k += 1
            
        # Final yield for this section
        yield arr.copy(), range(left, right+1)

def render_frame(data, active_indices, frame_idx):
    # 1. Canvas
    fig = plt.figure(figsize=(16, 9), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(BG_COLOR)
    
    # 2. Draw Bars
    x = np.arange(len(data))
    heights = data
    
    # Color mapping based on VALUE (Height), not position
    # This ensures the "Rainbow" travels with the bar.
    colors = [CMAP(h) for h in heights]
    
    # Highlight active?
    # Make active bars slightly brighter or draw a marker?
    # Let's keep it simple "Toy" style. The motion is enough.
    
    bars = ax.bar(x, heights, color=colors, width=BAR_WIDTH, align='center')
    
    # 3. Add "Active Limit" markers?
    # No, keep it clean.
        
    # Scale
    ax.set_xlim(-1, len(data))
    ax.set_ylim(0, 1.05)
    
    # Save
    out_dir = "logic_garden_sort_frames"
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"sort_{frame_idx:04d}.png")
    plt.savefig(filename, facecolor=BG_COLOR)
    plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Sorting the Rainbow...")
    
    # 1. Init Data
    # Sorted then Shuffled
    data = np.linspace(0.05, 1.0, NUM_BARS)
    np.random.seed(42)
    np.random.shuffle(data)
    
    # 2. Init Solver
    sorter = Sorter(data)
    algo = sorter.merge_sort(data, 0, len(data)-1)
    
    # 3. Render Loop
    frame_idx = 0
    
    # Hold initial state
    print("Capturing Chaos...")
    for _ in range(30):
        render_frame(data, [], frame_idx)
        frame_idx += 1
        
    # Step through algo
    print("Running Algorithm...")
    for state in algo:
        arr_snapshot, active = state
        
        # Render Comparison
        render_frame(arr_snapshot, active, frame_idx)
        frame_idx += 1
        
        # Add a duplicate frame to slow down visually fast operations?
        # Merge sort is fast. Let's strictly 1:1 map.
    
    # Hold Final State (The Harmony)
    print("Restoring Order...")
    for _ in range(60):
        render_frame(data, [], frame_idx)
        frame_idx += 1
        
    print(f"Total Frames: {frame_idx}")
