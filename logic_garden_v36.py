"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v36_fixed.py
MODE:   Nursery (Deep Space Palette)
TARGET: Wormhole (Einstein-Rosen Bridge Embedding Diagram)
STYLE:  "The Folded Path" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# --- 1. THE DEEP SPACE PALETTE ---
BG_COLOR = "#000000"        # Infinite Void
GRID_UPPER = "#00FFFF"      # Cyan (Our Universe)
GRID_LOWER = "#FF00FF"      # Magenta (The Upside Down)
THROAT_GLOW = "#FFFFFF"     # Singularity Ring
TRAVELER_COL = "#FFD700"    # Gold
STARS = "#202020"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class WormholeSim:
    def __init__(self):
        self.throat_radius = 0.05 # Starts closed (Singularity)
        self.rotation = 0.0
        
        # Grid Resolution
        self.u = np.linspace(-2.5, 2.5, 40) # Height (z-axis in embedding)
        self.v = np.linspace(0, 2*np.pi, 60) # Angle
        self.U, self.V = np.meshgrid(self.u, self.v)
        
        # Traveler Logic
        self.traveler_pos = -2.5 # Z position
        
    def update(self, frame_idx):
        # 1. Opening Animation
        # Frames 0-90: Open the throat
        if frame_idx < 90:
            target_b = 0.8
            # Smoothstep
            p = frame_idx / 90.0
            p = p*p * (3 - 2*p)
            self.throat_radius = 0.05 + p * (target_b - 0.05)
        
        # 2. Camera Rotation
        self.rotation += 0.5
        
        # 3. Traveler Physics
        # Only travel once open
        if frame_idx > 60:
            self.traveler_pos += 0.04
            if self.traveler_pos > 2.5: self.traveler_pos = -2.5 # Loop

    def render(self, frame_idx, ax):
        ax.set_axis_off()
        ax.set_facecolor(BG_COLOR)
        
        # 1. Physics Math (Morris-Thorne Embedding)
        b = self.throat_radius
        
        # Parametric Equations
        # r depends on u (height)
        R = np.sqrt(self.U**2 + b**2)
        
        X = R * np.cos(self.V)
        Y = R * np.sin(self.V)
        Z = self.U
        
        # 2. Surface Coloring
        # Create color map based on Z height (Upper vs Lower universe)
        colors = np.zeros(Z.shape + (4,))
        
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                z_val = Z[i,j]
                if z_val > 0.1:
                    colors[i,j] = matplotlib.colors.to_rgba(GRID_UPPER, alpha=0.3)
                elif z_val < -0.1:
                    colors[i,j] = matplotlib.colors.to_rgba(GRID_LOWER, alpha=0.3)
                else:
                    # The Throat (White)
                    colors[i,j] = matplotlib.colors.to_rgba(THROAT_GLOW, alpha=0.8)
                    
        # 3. Draw The Surface (FIXED ARGUMENTS)
        # shade=False ensures colors are used directly without light source calculation
        # Removed edgecolors from call to prevent TypeError
        surf = ax.plot_surface(X, Y, Z, facecolors=colors, rstride=2, cstride=2, 
                       linewidth=0.5, shade=False)
        
        # Set edges explicitly after creation
        surf.set_edgecolor("#404040")
        
        # 4. The Throat Ring (Highlight)
        # Circle at Z=0, Radius = b
        theta = np.linspace(0, 2*np.pi, 100)
        rx = b * np.cos(theta)
        ry = b * np.sin(theta)
        rz = np.zeros_like(theta)
        ax.plot(rx, ry, rz, color=THROAT_GLOW, linewidth=3, zorder=10)
        
        # 5. The Traveler (Particle)
        # Moves along a geodesic (constant theta)
        t_z = self.traveler_pos
        t_r = np.sqrt(t_z**2 + b**2)
        t_theta = 0 # Fixed angle path
        
        px = t_r * np.cos(t_theta)
        py = t_r * np.sin(t_theta)
        pz = t_z
        
        # Scatter is 2D in some versions, but 3D scatter exists in Axes3D
        ax.scatter([px], [py], [pz], c=TRAVELER_COL, s=200, edgecolors='white', zorder=20)
        
        # Trail
        trail_z = np.linspace(t_z - 1.0, t_z, 10)
        trail_r = np.sqrt(trail_z**2 + b**2)
        tx = trail_r * np.cos(t_theta)
        ty = trail_r * np.sin(t_theta)
        tz = trail_z
        ax.plot(tx, ty, tz, color=TRAVELER_COL, linewidth=2)

        # 6. Camera & Settings
        ax.view_init(elev=20, azim=self.rotation)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_zlim(-3, 3)
        
        # Remove panes/grid
        # Note: In newer matplotlib, set_axis_off() handles most of this
        try:
            ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        except:
            pass # Safety for aggressive updates
            
        ax.grid(False)
        
        # 7. HUD (Overlay text)
        status = "STATUS: STABLE"
        if self.throat_radius < 0.2: status = "STATUS: FORMING SINGULARITY"
        
        # Use simple text placement in 3D scene space or relative axis coords
        ax.text2D(0.05, 0.95, f"METRIC: SCHWARZSCHILD\nTHROAT RADIUS: {b:.2f}\n{status}", 
                 transform=ax.transAxes, color=GRID_UPPER, fontfamily='monospace',
                 bbox=dict(facecolor='black', edgecolor=GRID_UPPER, alpha=0.5))
        
        out_dir = "logic_garden_wormhole_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"wormhole_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Folding Space-Time (Fixed)...")
    
    sim = WormholeSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(16, 9), dpi=100)
        # Create 3D axis
        ax = fig.add_subplot(111, projection='3d')
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
