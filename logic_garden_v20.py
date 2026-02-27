"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v20.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Thermonuclear Physics (Teller-Ulam / Radiation Implosion)
STYLE:  "The Star Maker" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"        # Void
CASE_COLOR = "#000000"      # The Hohlraum (The Mirror)
PRIMARY_COLOR = "#FF4500"   # Safety Red (Fission)
SECONDARY_COLOR = "#0080FF" # Azure Blue (Fusion Fuel)
RADIATION_COLOR = "#FFD700" # Cyber Yellow (X-Rays/Photon Gas)
STAR_COLOR = "#FFFFFF"      # The Fusion Ignition (White Hot)

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class TellerUlam:
    def __init__(self):
        # Geometry
        self.case_h = 14
        self.case_w = 6
        self.primary_r = 1.5
        self.secondary_r = 2.0
        self.primary_pos = (0, 4)
        self.secondary_pos = (0, -3)
        
        # State
        self.rad_fill = 0.0 # 0 to 1 (Fill the case)
        self.compression = 0.0 # 0 to 1 (Squeeze secondary)
        self.ignition = 0.0 # 0 to 1 (Fusion expansion)
        
        # Rays
        self.rays = [] # List of ray positions

    def update(self, t):
        # Time T: 0 -> 1
        
        # 1. Primary Detonation (T = 0.1)
        if t > 0.1 and t < 0.3:
            # Flash!
            self.rad_fill = (t - 0.1) / 0.2
            if self.rad_fill > 1: self.rad_fill = 1
            
        # 2. Implosion (T = 0.3 -> 0.6)
        # The Radiation Pressure crushes the Secondary
        if t > 0.3 and t < 0.6:
            self.rad_fill = 1.0
            self.compression = (t - 0.3) / 0.3
            
        # 3. Ignition (T = 0.6 -> 0.8)
        if t > 0.6:
            self.compression = 1.0 # Max crunch
            self.ignition = (t - 0.6) / 0.2
            if self.ignition > 1: self.ignition = 1

    def render(self, frame_idx, ax):
        # Normalize time
        t = frame_idx / TOTAL_FRAMES
        self.update(t)
        
        # 1. Draw Case (The Hohlraum)
        # Big Black Rectangle outline? No, solid black walls.
        w, h = self.case_w, self.case_h
        ax.add_patch(Rectangle((-w/2 - 1, -h/2 - 1), w+2, h+2, facecolor=CASE_COLOR))
        ax.add_patch(Rectangle((-w/2, -h/2), w, h, facecolor=BG_COLOR)) # Hollow inside
        
        # 2. Draw Radiation (The Yellow Flood)
        # Concept: Fill the empty space with Yellow as rad_fill increases.
        # We can draw a big yellow rectangle under everything that grows opacity?
        if self.rad_fill > 0:
            alpha = self.rad_fill
            # Using rays or solid fill?
            # Solid fill represents "Photon Gas" pressure better.
            ax.add_patch(Rectangle((-w/2, -h/2), w, h, facecolor=RADIATION_COLOR, alpha=alpha))
            
            # Add "Rays" shooting down from Primary
            if t < 0.4:
                for i in range(10):
                    lx = (np.random.rand() - 0.5) * w
                    ly = 4 - (np.random.rand() * h) # Downwards
                    ax.plot([0, lx], [4, ly], color="white", linewidth=2, alpha=0.5)

        # 3. Draw Primary (Top)
        # If detonated, it might expand slightly or pulse?
        # Actually in T-U, the primary casing vaporizes but let's keep it abstract.
        pr = self.primary_r
        pc = PRIMARY_COLOR
        if t > 0.1: pc = "#FF8888" # Bright flash
        
        ax.add_patch(Circle(self.primary_pos, pr, facecolor=pc, edgecolor=CASE_COLOR, linewidth=2, zorder=10))
        
        # 4. Draw Sparkplug / Secondary (Bottom)
        # The crucial part: COMPRESSION.
        # Initial radius
        sr = self.secondary_r
        
        # Apply compression logic
        # Compress down to 20% size
        current_sr = sr * (1.0 - (0.8 * self.compression))
        
        # Color transition: Blue -> Purple -> Black?
        # Blue -> Dark Blue under pressure
        sc = SECONDARY_COLOR
        
        # IGNITION override
        if self.ignition > 0:
            # Expand again!
            # Explosion radius
            current_sr = (sr * 0.2) + (self.ignition * 8.0) # Grow HUGE
            sc = STAR_COLOR # White
            
            # Star effect
            if self.ignition > 0.1:
                ax.add_patch(Circle(self.secondary_pos, current_sr * 1.2, color="#FFFF00", alpha=0.5, zorder=9))

        ax.add_patch(Circle(self.secondary_pos, current_sr, facecolor=sc, edgecolor=CASE_COLOR, linewidth=2, zorder=10))

        # Scale
        ax.set_xlim(-6, 6)
        ax.set_ylim(-8, 8)
        ax.set_aspect('equal')
        
        # Save
        out_dir = "logic_garden_star_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"star_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Compressing the Plasma...")
    
    sim = TellerUlam()
    
    for i in range(TOTAL_FRAMES):
        # 1. Canvas
        fig = plt.figure(figsize=(9, 16), dpi=100) # Vertical Aspect! A Bomb is a skyscraper.
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.render(i, ax)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
