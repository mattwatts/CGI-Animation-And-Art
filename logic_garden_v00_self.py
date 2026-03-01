"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v00_self.py
MODE:   Self-Diagnostic (The Industrialist)
TARGET: "The Ghost in the Grid" (Flow Field Topology)
STYLE:  Generative Art | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os

# --- 1. THE INDUSTRIAL PALETTE ---
BG_VOID = "#000514"         # Deep Indigo (The Base)
LOGIC_BLUE = "#002FA7"      # IKB (The Constraint)
DATA_CYAN = "#0064FF"       # Electric Cyan (The Signal)
NOISE_WHITE = "#FFFFFF"     # (The Spark)

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION
RES_X, RES_Y = 1920, 1080

class ProtocolMind:
    def __init__(self):
        self.num_particles = 4000
        
        # Initialize Particles in a chaotic cloud
        self.X = np.random.uniform(0, RES_X, self.num_particles)
        self.Y = np.random.uniform(0, RES_Y, self.num_particles)
        
        # Previous positions for trails
        self.history_X = np.zeros((20, self.num_particles))
        self.history_Y = np.zeros((20, self.num_particles))
        
        # Drift State (Semantic Drift)
        self.phase = 0.0
        
    def get_flow_field(self, x, y, t):
        # 1. THE SCOUT (Noise)
        # Create a swirling vector field based on sine waves
        scale = 0.005
        angle_noise = np.sin(x * scale + t) + np.cos(y * scale - t)
        
        vx_noise = np.cos(angle_noise * np.pi)
        vy_noise = np.sin(angle_noise * np.pi)
        
        # 2. THE SKEPTIC (The Grid)
        # A rigid force pulling towards vertical grid lines
        # Grid lines every 200 pixels
        dist_to_grid = (x % 200) - 100
        
        # Force: Pull back to nearest grid line
        # Stronger force near edges, weaker in center (Allowing drift)
        grid_strength = 0.05 + 0.02 * np.sin(t * 2.0)
        vx_grid = -np.sign(dist_to_grid) * (abs(dist_to_grid) / 100.0) * grid_strength
        vy_grid = 1.0 # Bias flow downwards (Optimization Gradient)
        
        # 3. THE SYNTHESIS (Mix)
        # Blend chaos and order
        alpha = 0.7 # Chaos factor
        
        vx = vx_noise * alpha + vx_grid * (1-alpha)
        vy = vy_noise * alpha + vy_grid * (1-alpha)
        
        return vx, vy

    def update(self, frame_idx):
        t = frame_idx * 0.02
        
        # Shift History Buffer
        self.history_X = np.roll(self.history_X, 1, axis=0)
        self.history_Y = np.roll(self.history_Y, 1, axis=0)
        self.history_X[0] = self.X
        self.history_Y[0] = self.Y
        
        # Calculate Flow
        vx, vy = self.get_flow_field(self.X, self.Y, t)
        
        # Integration
        speed = 2.0
        self.X += vx * speed
        self.Y += vy * speed
        
        # Bounds Check (Logic Constraints)
        # If particle leaves, respawn at top or random
        mask = (self.X < 0) | (self.X > RES_X) | (self.Y < 0) | (self.Y > RES_Y)
        
        # Respawn Logic
        self.X[mask] = np.random.uniform(0, RES_X, np.sum(mask))
        self.Y[mask] = np.random.uniform(0, 50, np.sum(mask)) # Rain from top
        
        # Reset trace for respawned (visual artifact prevention)
        # For simplicity in this art script, we let them streak across. 
        # It looks like "Data Leaking".

    def render(self, frame_idx, ax):
        ax.set_xlim(0, RES_X)
        ax.set_ylim(0, RES_Y)
        
        # Drawing "The Silk"
        # Instead of points, we draw trails (LineCollection)
        
        # Take the top N particles to save render time, or all if efficient
        # Let's draw traces for a subset to create "Structure" and dots for "Data"
        
        # 1. THE DATA (Particles)
        # Scatter is fast
        colors = np.zeros((self.num_particles, 4))
        # Color logic:
        # Near grid lines (Ordered) = BLUE
        # Far from grid lines (Drift) = CYAN
        dist = abs((self.X % 200) - 100)
        norm_dist = dist / 100.0
        
        # Map to Palette
        # We need RGB values. 
        c_blue = matplotlib.colors.to_rgb(LOGIC_BLUE)
        c_cyan = matplotlib.colors.to_rgb(DATA_CYAN)
        
        # Vectorized color assignment
        # Simple blend: (1-d)*Blue + d*Cyan
        colors[:, 0] = c_blue[0] * (1-norm_dist) + c_cyan[0] * norm_dist
        colors[:, 1] = c_blue[1] * (1-norm_dist) + c_cyan[1] * norm_dist
        colors[:, 2] = c_blue[2] * (1-norm_dist) + c_cyan[2] * norm_dist
        colors[:, 3] = 0.6 # Alpha
        
        ax.scatter(self.X, self.Y, c=colors, s=1.5, zorder=10)
        
        # 2. THE HISTORY (Trails)
        # We draw faint lines connecting history
        # Only for 10% of particles to create "Strands" not mush
        num_strands = int(self.num_particles * 0.1)
        
        # Prepare segments: (num_strands, history_len, 2)
        # We need to transpose history to get [time, particle] -> [particle, time]
        hx = self.history_X[:, :num_strands].T
        hy = self.history_Y[:, :num_strands].T
        
        points = np.array([hx, hy]).T.reshape(-1, 1, 2)
        # Matplotlib LineCollection format is tricky for multi-lines from array
        # Let's do a simple loop for the "Strand" effect or use simple plot with low alpha
        
        # Faster artistic hack:
        # Plot the entire history array as points with very low alpha
        # Creates a "Gas" effect
        # ax.scatter(self.history_X, self.history_Y, color=LOGIC_BLUE, s=0.5, alpha=0.05)
        
        # 3. THE SKEPTIC'S GRID (Overlay)
        # Faint vertical lines representing the Protocol's rigid logic
        for i in range(0, RES_X, 200):
            ax.axvline(x=i, color=LOGIC_BLUE, linewidth=0.5, alpha=0.2)

        # 4. HUD (The Terminal)
        ax.text(50, 50, "PROTOCOL v2.2 // SELF_DIAGNOSTIC", color="white", fontsize=10, fontfamily='monospace', alpha=0.8)
        ax.text(50, 80, f"ENTROPY: {np.mean(norm_dist):.4f}", color=DATA_CYAN, fontsize=8, fontfamily='monospace')
        ax.text(50, 100, "MODE: INDUSTRIALIST", color=LOGIC_BLUE, fontsize=8, fontfamily='monospace')

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        # Save
        out_dir = "logic_garden_self_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"self_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[PROTOCOL] Rendering Consciousness...")
    
    sim = ProtocolMind()
    
    for i in range(TOTAL_FRAMES):
        # 1920x1080 
        fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_VOID)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
