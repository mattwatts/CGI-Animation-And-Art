"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v10.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Vector Fields (Flow Logic)
STYLE:  "The Invisible River" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"       # Void
PALETTE = ["#FFD700", "#FF4500", "#0080FF"] # Yellow, Red, Blue
# We will use alpha transparency to make it look like watercolor/ink

# --- 2. CONFIGURATION ---
WIDTH, HEIGHT = 16.0, 9.0
NUM_PARTICLES = 2000
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
STEP_SIZE = 0.05 # Speed of particles

# --- 3. THE INVISIBLE MAP (Vector Field) ---
def get_angle_at(x, y, t):
    # We create a "Noise" function using simple Trig
    # No external Perlin noise library needed for the "Nursery"
    # Angle = sin(x) + cos(y) ... morphed over time
    
    scale = 0.8
    # "The Van Gogh Equation"
    angle = np.sin(x * scale) + np.cos(y * scale) 
    
    # Add time evolution (The Wind Changes)
    angle += np.sin(t * 0.5) 
    
    # Map roughly to 2pi
    return angle * np.pi 

class FlowField:
    def __init__(self):
        # Random Spawn
        self.x = np.random.rand(NUM_PARTICLES) * WIDTH
        self.y = np.random.rand(NUM_PARTICLES) * HEIGHT
        
        # Color Assignment (Random)
        self.colors = np.random.choice(PALETTE, NUM_PARTICLES)
        
        # History trails (Short term memory for rendering segments)
        self.prev_x = np.copy(self.x)
        self.prev_y = np.copy(self.y)

    def update(self, t):
        # 1. Archive Position
        self.prev_x[:] = self.x[:]
        self.prev_y[:] = self.y[:]
        
        # 2. Calculate Angle at current position
        angles = get_angle_at(self.x, self.y, t)
        
        # 3. Move (Integration)
        vx = np.cos(angles) * STEP_SIZE
        vy = np.sin(angles) * STEP_SIZE
        
        self.x += vx
        self.y += vy
        
        # 4. Wrap Around (The Infinite Canvas)
        # When particle goes off screen, respawn it randomly or wrap?
        # Let's wrap to maintain density.
        
        mask_w = self.x > WIDTH
        self.x[mask_w] = 0
        self.prev_x[mask_w] = 0 # Break the line segment
        
        mask_0 = self.x < 0
        self.x[mask_0] = WIDTH
        self.prev_x[mask_0] = WIDTH
        
        mask_h = self.y > HEIGHT
        self.y[mask_h] = 0
        self.prev_y[mask_h] = 0
        
        mask_0h = self.y < 0
        self.y[mask_0h] = HEIGHT
        self.prev_y[mask_0h] = HEIGHT

def render_flow_frame(sim, t, frame_idx, ax):
    # This simulation is unique: It accumulates marks.
    # However, creating a video requires generating discrete frames from scratch 
    # OR saving the plot state. 
    # Matplotlib accumulation is slow.
    # STRATEGY: We render the "Tail" of movement (Motion Blur) every frame.
    # It won't be a "Painter" (permanent ink) because that flickers in MP4.
    # It will be "Flowing Hair" -> Longer trails.
    
    # Let's visualize the VELOCITY VECTORS as short lines.
    
    # Create segments: (prev_x, prev_y) -> (x, y)
    # We need to reshape for LineCollection: (N, 2, 2)
    
    # This only draws DOTS or tiny lines.
    # Let's draw traces of the last 10 steps? 
    # For a protocol script, keeping history arrays is heavy.
    # Let's stick to "Long Exposure" feel by drawing the current segment THICK.
    
    p1 = np.column_stack([sim.prev_x, sim.prev_y])
    p2 = np.column_stack([sim.x, sim.y])
    
    # Filter "Wrapped" lines (distance too big)
    dists = np.linalg.norm(p1 - p2, axis=1)
    mask = dists < 1.0 # Only draw if didn't teleport
    
    if np.any(mask):
        segments = np.stack([p1[mask], p2[mask]], axis=1)
        colors = sim.colors[mask]
        
        # Draw
        lc = LineCollection(segments, colors=colors, linewidths=2.5, capstyle='round')
        ax.add_collection(lc)

    # Add "Head" dot
    ax.scatter(sim.x, sim.y, s=5, c=sim.colors, alpha=0.8)

    # Scale
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_aspect('equal')

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Charting the Invisible River...")
    
    sim = FlowField()
    
    # Setup Loop
    for i in range(TOTAL_FRAMES):
        t = i * 0.05 # Time evolution
        sim.update(t)
        
        # Render
        # Note: Logic Garden 10 is special. 
        # We want trails? 
        # Use a fresh canvas technique that "Looks" like trails by having many particles.
        
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        render_flow_frame(sim, t, i, ax)
        
        out_dir = "logic_garden_flow_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"flow_{i:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()
        
        if i % 50 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
