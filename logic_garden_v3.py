"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v3.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Galton Board (Normal Distribution / The Bell Curve)
STYLE:  "Digital Rain" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"      # Canvas
PEG_COLOR = "#0080FF"     # Azure Blue (The Constant)
BALL_A_COLOR = "#FFD700"  # Cyber Yellow (Entropy A)
BALL_B_COLOR = "#FF4500"  # Safety Red (Entropy B)

# --- 2. PHYSICS ENGINE (Simple Kinematics) ---
# We simulate hundreds of particles falling through a peg gride

class GaltonSim:
    def __init__(self, n_balls=300):
        self.balls = [] # List of [x, y, vx, vy, color_index]
        self.pegs = []  # List of (x, y)
        self.bins = []  # To stack balls at bottom
        self.n_balls_total = n_balls
        self.balls_spawned = 0
        self.spawn_rate = 2 # Balls per frame
        
        # Setup Pegs (Triangle)
        rows = 12
        spacing = 0.6
        start_y = 6.0
        
        for r in range(rows):
            cols = r + 1
            y = start_y - r * spacing * 1.5
            x_start = - (r * spacing) / 2
            for c in range(cols):
                x = x_start + c * spacing
                self.pegs.append((x, y))
                
        # Floor (The Bins)
        self.floor_y = -5.0
        self.bin_width = spacing
        
    def update(self):
        # 1. Spawn
        if self.balls_spawned < self.n_balls_total:
            for _ in range(self.spawn_rate):
                # Jitter start x slightly to ensure randomness
                sx = np.random.uniform(-0.05, 0.05)
                sy = 7.0
                vx = 0
                vy = 0
                c = 0 if np.random.random() > 0.5 else 1
                self.balls.append([sx, sy, vx, vy, c])
                self.balls_spawned += 1

        # 2. Move & Collide
        active_balls = []
        dt = 0.05
        gravity = -9.8
        damping = 0.5
        
        for b in self.balls:
            x, y, vx, vy, c = b
            
            # Integrate Gravity
            vy += gravity * dt
            x += vx * dt
            y += vy * dt
            
            # Check Peg Collisions
            hit = False
            for px, py in self.pegs:
                dx = x - px
                dy = y - py
                dist = np.sqrt(dx*dx + dy*dy)
                
                # Peg Radius 0.1, Ball Radius 0.1
                if dist < 0.2:
                    # Bounce!
                    # Normalize normal vector
                    nx, ny = dx/dist, dy/dist
                    
                    # Reflect velocity with randomness (The Chaos)
                    # "Left or Right?"
                    noise = np.random.uniform(-0.5, 0.5) 
                    
                    vx = nx * 2.0 + noise # Push sideways
                    vy = abs(vy) * 0.5 * ny # Dampen y
                    hit = True
                    
                    # Push out to prevent sticking
                    overlap = 0.21 - dist
                    x += nx * overlap
                    y += ny * overlap
            
            # Floor Collision (Stacking)
            if y < self.floor_y:
                # Freeze ball
                self.bins.append((x, self.floor_y, c)) 
                # (In a real physics engine we'd stack them properly, 
                # here we'll visually simplify by letting them disappear 
                # into a "Histogram Count" or just pile up simply)
                # Let's simple pile: 
                # Find which bin index
                # Visual hack: Just freeze it where it lands
                active_balls.append([x, y, 0, 0, c, True]) # True = Frozen
            else:
                active_balls.append([x, y, vx, vy, c, False])
        
        # Filter frozen balls to separate list to save calc? 
        # For simplicity, we keep them but stop updating logic
        self.balls = []
        for b in active_balls:
            if b[5]: # Frozen
                # Simple logic to stop them falling through floor
                # Just keep them in list
                self.balls.append(b[:5])
            else:
                self.balls.append(b[:5])

    def render(self, frame_id):
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        # Draw Pegs
        for px, py in self.pegs:
            # Pegs are squares or circles? Let's do Circles for "Soft Toy" look
            circle = Circle((px, py), 0.1, color=PEG_COLOR, zorder=5)
            ax.add_patch(circle)
            
        # Draw Balls
        for x, y, vx, vy, c in self.balls:
            color = BALL_A_COLOR if c == 0 else BALL_B_COLOR
            circle = Circle((x, y), 0.1, color=color, zorder=10)
            ax.add_patch(circle)
            
        # Draw Floor/Bin Dividers (Optional structure)
        ax.axhline(y=-5.1, color=PEG_COLOR, linewidth=5)
        
        # Scale
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 8)
        ax.set_aspect('equal')
        
        out_dir = "logic_garden_galton_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"galton_{frame_id:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    sim = GaltonSim(n_balls=400)
    FRAMES = 450
    
    print("[NURSERY] Dropping the Probability Rain...")
    
    for i in range(FRAMES):
        sim.update()
        sim.render(i)
        
        if i % 20 == 0:
            print(f"Frame {i}/{FRAMES}")
