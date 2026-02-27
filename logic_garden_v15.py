"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v15.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Elastic Collisions (The Pi Machine)
STYLE:  "The Clacking Blocks" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"        # Void
WALL_COLOR = "#000000"      # The Limit
BLOCK_1_COLOR = "#FF4500"   # Safety Red (The Photon / Small Mass)
BLOCK_2_COLOR = "#0080FF"   # Azure Blue (The Hammer / Large Mass)
COUNT_COLOR = "#FFD700"     # Cyber Yellow (The Score)

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
MASS_1 = 1.0       # Small
GRAVITY_FACTOR = 100 # Mass Ratio 100^N. Use 100 for N=1 -> 31 collisions.
MASS_2 = MASS_1 * GRAVITY_FACTOR 

# Initial Conditions
VEL_1 = 0.0
VEL_2 = -1.0 # Moving Left
POS_1 = 2.0
POS_2 = 6.0
WIDTH_1 = 1.0
WIDTH_2 = 2.0 # Visual size only

class PhysicsEngine:
    def __init__(self):
        self.m1 = MASS_1
        self.m2 = MASS_2
        self.x1 = POS_1
        self.x2 = POS_2
        self.v1 = VEL_1
        self.v2 = VEL_2
        self.w1 = WIDTH_1
        self.w2 = WIDTH_2
        self.clacks = 0
        self.time = 0.0

    def step(self, dt):
        # We need continuous collision detection because small block moves FAST.
        # Logic: Calculate Time to Next Event. 
        # Events: 
        # A) Block 1 hits Wall (x=0)
        # B) Block 1 hits Block 2 (x1 + w1 = x2)
        
        remaining_dt = dt
        
        while remaining_dt > 0:
            # Time to Wall? (Only if moving left)
            t_wall = float('inf')
            if self.v1 < 0:
                t_wall = (0 - self.x1) / self.v1
                
            # Time to Hit? (Only if v1 > v2, closing the gap)
            t_hit = float('inf')
            if self.v1 > self.v2:
                # Distance gap
                gap = self.x2 - (self.x1 + self.w1)
                rel_v = self.v1 - self.v2
                t_hit = gap / rel_v
                
            # Find earliest event
            t_event = min(t_wall, t_hit)
            
            if t_event > remaining_dt:
                # No event in this frame step
                self.x1 += self.v1 * remaining_dt
                self.x2 += self.v2 * remaining_dt
                self.time += remaining_dt
                remaining_dt = 0
            else:
                # Advance to event
                # Add slight epsilon to ensure contact
                self.x1 += self.v1 * t_event
                self.x2 += self.v2 * t_event
                self.time += t_event
                remaining_dt -= t_event
                
                # Process Collision
                if t_wall <= t_hit:
                    # Wall Bounce
                    self.v1 *= -1
                    self.clacks += 1
                else:
                    # Block Bounce (Elastic 1D)
                    # New v1 = (v1(m1-m2) + 2m2v2) / (m1+m2)
                    # New v2 = (v2(m2-m1) + 2m1v1) / (m1+m2)
                    
                    u1 = self.v1
                    u2 = self.v2
                    M_sum = self.m1 + self.m2
                    
                    self.v1 = (u1 * (self.m1 - self.m2) + 2 * self.m2 * u2) / M_sum
                    self.v2 = (u2 * (self.m2 - self.m1) + 2 * self.m1 * u1) / M_sum
                    
                    self.clacks += 1

    def render(self, frame_idx, ax):
        # 1. Floor & Wall
        ax.plot([-5, 20], [0, 0], color='black', linewidth=2)
        ax.plot([0, 0], [0, 10], color='black', linewidth=5) # Wall
        
        # 2. Blocks
        rect1 = Rectangle((self.x1, 0), self.w1, self.w1, facecolor=BLOCK_1_COLOR, edgecolor='black')
        rect2 = Rectangle((self.x2, 0), self.w2, self.w2, facecolor=BLOCK_2_COLOR, edgecolor='black')
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        
        # 3. Text Counter
        ax.text(10, 5, f"{self.clacks}", fontsize=80, color=COUNT_COLOR, 
                ha='center', va='center', fontweight='bold', alpha=0.9)

        # Scale
        # Follow the action? Or fixed camera?
        # Fixed camera is better for "Stage" feel.
        ax.set_xlim(-1, 15)
        ax.set_ylim(-1, 8) # 16:9 Aspect roughly
        
        
        # Save
        out_dir = "logic_garden_pi_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"pi_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Calculating Pi with Hammer Blows...")
    
    sim = PhysicsEngine()
    dt = 1.0 / FPS
    
    # Run loop
    for i in range(TOTAL_FRAMES):
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        # 2. Render State
        sim.render(i, ax)
        
        # 3. Advance Physics
        # Sub-step visual dt
        sim.step(dt)
        
        if i % 50 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES} | Clacks: {sim.clacks}")
