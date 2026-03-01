"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_satori_fixed.py
MODE:   Satori (IKB Palette)
TARGET: Gravitational Lensing / Zen Enso
STYLE:  "The Event Horizon Enso" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os

# --- 1. THE KLEIN PALETTE ---
DEEP_INDIGO = "#000514"     # rgb(0, 5, 20)
IKB_BLUE = "#002FA7"        # rgb(0, 47, 167)
ELEC_CYAN = "#0064FF"       # rgb(0, 100, 255)
SINGULARITY = "#FFFFFF"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION
RES_X, RES_Y = 1920, 1080
ASPECT = RES_X / RES_Y

class SatoriSim:
    def __init__(self):
        # Generate Grid Points (Source Plane)
        # High resolution for smooth curves
        self.grid_res = 100 # Increased for smoother contours
        x = np.linspace(-3.0 * ASPECT, 3.0 * ASPECT, self.grid_res)
        y = np.linspace(-3.0, 3.0, self.grid_res)
        self.X, self.Y = np.meshgrid(x, y)
        
        # Mass Properties
        self.mass = 0.0 # Grows
        self.spin = 0.0 # Frame dragging
        
    def lens_map(self, x, y):
        # Calculate radius from center
        r = np.sqrt(x**2 + y**2)
        
        # Avoid division by zero
        r_safe = np.maximum(r, 0.1)
        
        displacement = self.mass / r_safe
        
        theta = np.arctan2(y, x)
        
        # FRAME DRAGGING (Swirl)
        # Twist theta based on radius
        twist = self.spin / (r_safe**2 + 0.1)
        theta_twisted = theta + twist
        
        # Inverse Mapping: Where did this pixel come from?
        sx = x - displacement * np.cos(theta_twisted)
        sy = y - displacement * np.sin(theta_twisted)
        
        return sx, sy

    def update(self, frame_idx):
        # 1. Breathe Mass (Expansion/Contraction)
        # 0 -> 20s: Grow Mass
        if frame_idx < 600:
            prog = frame_idx / 600.0
            # Logistic growth
            self.mass = 1.5 * (1 / (1 + np.exp(-10*(prog-0.5))))
        else:
            self.mass = 1.5
            
        # 2. Spin Up (Frame Dragging)
        self.spin = frame_idx * 0.005

    def render(self, frame_idx, ax):
        ax.set_xlim(-3.0 * ASPECT, 3.0 * ASPECT)
        ax.set_ylim(-3.0, 3.0)
        
        # Calculate distorted grid coordinates
        LX, LY = self.lens_map(self.X, self.Y)
        
        # --- DRAWING THE GRID ---
        # Draw contour lines of the source coordinates
        levels = 40
        
        # Vertical Lines (Blue)
        ax.contour(self.X, self.Y, LX, levels=levels, colors=IKB_BLUE, linewidths=0.8, alpha=0.6)
        
        # Horizontal Lines (Blue)
        ax.contour(self.X, self.Y, LY, levels=levels, colors=IKB_BLUE, linewidths=0.8, alpha=0.6)
        
        # --- THE EVENT HORIZON ENSO ---
        # The region where light cannot escape (or loops)
        # R_E ~ sqrt(mass) roughly in these units
        r_E = np.sqrt(max(0, self.mass))
        
        if r_E > 0.1:
            # The Black Hole
            circle = plt.Circle((0, 0), r_E, color="black", zorder=5)
            ax.add_patch(circle)
            
            # The Photon Ring (Cyan)
            ring = plt.Circle((0, 0), r_E * 1.05, fill=False, edgecolor=ELEC_CYAN, linewidth=2, zorder=6)
            ax.add_patch(ring)
            
            # The Singularity (Center Point)
            ax.scatter([0], [0], c=SINGULARITY, s=15, zorder=10)

        # HUD
        # Removed letter_spacing parameter
        ax.text(0, -2.5, "S A T O R I", color=ELEC_CYAN, ha='center', fontfamily='monospace', fontsize=20, alpha=0.9, fontweight='bold')
        
        # Zen Maths
        if self.mass > 0.1:
            ax.text(0, 2.5, "R_uv = R_g - (1/2)g_uv R", color=IKB_BLUE, ha='center', fontsize=10, alpha=0.5, fontfamily='monospace')

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        # Save
        out_dir = "logic_garden_satori_fixed_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"satori_fixed_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=DEEP_INDIGO)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[ZEN] Contemplating the Void (Fixed)...")
    
    sim = SatoriSim()
    
    for i in range(TOTAL_FRAMES):
        # 1920x1080 setup
        fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(DEEP_INDIGO)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
