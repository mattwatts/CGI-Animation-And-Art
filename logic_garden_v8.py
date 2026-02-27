"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v8.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Boids (Flocking Simulation)
STYLE:  "The School of Fish" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"       # Void
BOID_COLORS = ["#FFD700", "#FF4500", "#0080FF"] # Yellow, Red, Blue

# --- 2. CONFIGURATION ---
NUM_BOIDS = 60
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
WIDTH, HEIGHT = 16.0, 9.0  # Aspect Ratio 16:9

# Physics Constants
SPEED_LIMIT = 0.15
PERCEPTION_RADIUS = 2.0
SEPARATION_DIST = 0.5
COHESION_FORCE = 0.005
ALIGNMENT_FORCE = 0.02
SEPARATION_FORCE = 0.03

class BoidFlock:
    def __init__(self, n):
        self.n = n
        # Random Positions
        self.pos = np.random.rand(n, 2) * [WIDTH, HEIGHT]
        # Random Velocities
        self.vel = (np.random.rand(n, 2) - 0.5) * SPEED_LIMIT
        # Assign fixed colors
        self.colors = [BOID_COLORS[i % 3] for i in range(n)]
        
    def update(self):
        # Apply Rules for each boid
        # (Naive O(n^2) implementation is fine for n=50)
        
        new_vel = np.copy(self.vel)
        
        for i in range(self.n):
            p = self.pos[i]
            v = self.vel[i]
            
            # Find Neighbors
            # Calculate distances (handling wrap-around is tricky, let's stick to Euclidean for simplicity
            # OR implement wrap-distance logic for perfect toroid)
            # For nursery, simple Euclidean is okay, but edges might look weird.
            # Let's do simple distance.
            
            diff = self.pos - p
            dist = np.linalg.norm(diff, axis=1)
            
            # Mask for neighbors (excluding self)
            mask = (dist > 0) & (dist < PERCEPTION_RADIUS)
            
            if np.any(mask):
                # 1. Cohesion (Steer to center of mass)
                center_mass = np.mean(self.pos[mask], axis=0)
                new_vel[i] += (center_mass - p) * COHESION_FORCE
                
                # 2. Alignment (Match velocity)
                avg_vel = np.mean(self.vel[mask], axis=0)
                new_vel[i] += (avg_vel - v) * ALIGNMENT_FORCE
                
                # 3. Separation (Avoid crowding)
                # Filter for very close neighbors
                close_mask = (dist > 0) & (dist < SEPARATION_DIST)
                if np.any(close_mask):
                    # Move away from them
                    move_away = p - self.pos[close_mask]
                    # Weight by distance? 
                    new_vel[i] += np.sum(move_away, axis=0) * SEPARATION_FORCE

        # Update Velocities
        self.vel = new_vel
        
        # Limit Speed
        speed = np.linalg.norm(self.vel, axis=1)
        # Avoid divide by zero
        speed = np.maximum(speed, 0.001) 
        over_speed = speed > SPEED_LIMIT
        
        # Normalize and scale cap
        self.vel[over_speed] = (self.vel[over_speed] / speed[over_speed][:,None]) * SPEED_LIMIT
        
        # Update Position
        self.pos += self.vel
        
        # Wrap Around (Toroidal World)
        self.pos[:, 0] = self.pos[:, 0] % WIDTH
        self.pos[:, 1] = self.pos[:, 1] % HEIGHT

    def render(self, frame_idx):
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        # 2. Draw Boids
        # Boid shape: Triangle pointing in velocity direction
        boid_size = 0.3
        
        for i in range(self.n):
            p = self.pos[i]
            v = self.vel[i]
            c = self.colors[i]
            
            # Calculate angle
            angle = np.arctan2(v[1], v[0])
            
            # Rotate triangle vertices
            # Sharp nose, wide tail
            # Tip at (0,0) -> Rotated -> Translated to P
            # Vertices relative to center: (size, 0), (-size, -size/2), (-size, size/2)
            
            tip = p + np.array([np.cos(angle), np.sin(angle)]) * boid_size
            left = p + np.array([np.cos(angle + 2.5), np.sin(angle + 2.5)]) * boid_size * 0.8
            right = p + np.array([np.cos(angle - 2.5), np.sin(angle - 2.5)]) * boid_size * 0.8
            
            poly = Polygon([tip, left, right], facecolor=c, edgecolor=None)
            ax.add_patch(poly)
            
            # Handle Wrap-around render? 
            # (If a boid is half-off screen, draw a ghost on the other side? 
            # Too complex for quick script. Let them pop.)

        # Scale
        ax.set_xlim(0, WIDTH)
        ax.set_ylim(0, HEIGHT)
        ax.set_aspect('equal')
        
        # Save
        out_dir = "logic_garden_boids_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"boid_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Releasing the Swarm...")
    flock = BoidFlock(NUM_BOIDS)
    
    for i in range(TOTAL_FRAMES):
        flock.render(i)
        flock.update()
        
        if i % 50 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
