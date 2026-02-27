"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v11.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Voronoi Tessellation (Space Partitioning)
STYLE:  "The Stained Glass" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import Voronoi
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"       # Void (The mortar)
PALETTE = ["#FFD700", "#FF4500", "#0080FF"] # Yellow, Red, Blue

# --- 2. CONFIGURATION ---
NUM_SEEDS = 25
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
WIDTH, HEIGHT = 16.0, 9.0
SPEED = 0.08

class VoronoiGarden:
    def __init__(self):
        # Initialize Random Seeds inside the box
        self.pos = np.random.rand(NUM_SEEDS, 2) * [WIDTH, HEIGHT]
        # Random Velocity
        self.vel = (np.random.rand(NUM_SEEDS, 2) - 0.5) * SPEED
        # Assign colors
        self.colors = [PALETTE[i % 3] for i in range(NUM_SEEDS)]

    def update(self):
        # Update Position
        self.pos += self.vel
        
        # BOUNCE off walls (Keep them contained)
        for i in range(NUM_SEEDS):
            # X Bounce
            if self.pos[i, 0] <= 0:
                self.pos[i, 0] = 0
                self.vel[i, 0] *= -1
            elif self.pos[i, 0] >= WIDTH:
                self.pos[i, 0] = WIDTH
                self.vel[i, 0] *= -1
                
            # Y Bounce
            if self.pos[i, 1] <= 0:
                self.pos[i, 1] = 0
                self.vel[i, 1] *= -1
            elif self.pos[i, 1] >= HEIGHT:
                self.pos[i, 1] = HEIGHT
                self.vel[i, 1] *= -1

    def render(self, frame_idx):
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        # 2. Handle "Infinite" Regions via Ghost Points
        # To get clean edges at the screen border, we reflect points across the boundaries
        # This creates a "Surrounding Army" that forces the inner cells to close nicely.
        
        points_center = self.pos
        points_left   = np.copy(points_center); points_left[:,0]   -= WIDTH
        points_right  = np.copy(points_center); points_right[:,0]  += WIDTH
        points_up     = np.copy(points_center); points_up[:,1]     += HEIGHT
        points_down   = np.copy(points_center); points_down[:,1]   -= HEIGHT
        
        # Combine all points (Center + 4 Neighbors is usually enough for a simple rectangle)
        all_points = np.vstack([
            points_center, points_left, points_right, points_up, points_down
        ])
        
        # 3. Compute Voronoi
        vor = Voronoi(all_points)
        
        # 4. Draw Regions (Only for the original seeds: indices 0 to NUM_SEEDS-1)
        for i in range(NUM_SEEDS):
            idx = i # The index of the point in all_points matches the region index usually
            region_idx = vor.point_region[i]
            region = vor.regions[region_idx]
            
            # Check if region is valid (no -1, which means infinite)
            # Since we added ghost points, all center regions MUST be finite.
            if -1 not in region and len(region) > 0:
                polygon = [vor.vertices[i] for i in region]
                
                # Draw Polygon
                # Setup aesthetic: Color fill, Thick White Edge (The Fence)
                poly = Polygon(polygon, facecolor=self.colors[i], 
                             edgecolor=BG_COLOR, linewidth=10) # Thick mortar lines
                ax.add_patch(poly)
                
        # 5. Draw the Seeds?
        # Let's keep it abstract. No dots. Just the "Stained Glass".
        # Actually, adding a tiny white dot in the center helps show the "Source".
        ax.scatter(self.pos[:,0], self.pos[:,1], color=BG_COLOR, s=20, zorder=10)

        # Scale
        ax.set_xlim(0, WIDTH)
        ax.set_ylim(0, HEIGHT)
        ax.set_aspect('equal')
        
        # Save
        out_dir = "logic_garden_voronoi_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"voronoi_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Building the Invisible Fences...")
    garden = VoronoiGarden()
    
    for i in range(TOTAL_FRAMES):
        garden.render(i)
        garden.update()
        
        if i % 50 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
