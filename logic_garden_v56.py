"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v56_fixed.py
MODE:   Nursery (Arctic Palette)
TARGET: Fata Morgana (Import Patch)
STYLE:  "The Silent Castle" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Arc, Circle
import os

# --- 1. THE ARCTIC PALETTE ---
SEA_INDIGO = "#001040"      # The Water
AIR_COLD = "#B0E0E6"        # Powder Blue (Dense)
AIR_WARM = "#FFFAFA"        # Snow (Light)
RAY_YELLOW = "#FFFF00"      # The Path
SHIP_BLACK = "#000000"      # The Object
GHOST_CYAN = "#E0FFFF"      # The Mirage
GHOST_EDGE = "#408080"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class MirageSim:
    def __init__(self):
        # Geometry
        self.horizon_y = 0.0
        self.obs_x = 8.0
        self.obj_x = -8.0
        
        # Ray trace points
        self.ray_path = []
        self.ray_progress = 0.0
        self.virtual_path = [] # The dotted line overlap
        
        # Ghost State
        self.ghost_opacity = 0.0
        self.ghost_stretch = 1.0
        
    def _get_curve_point(self, t):
        # Quadratic Bezier over the "hump" of the earth
        # P0 = Object (-8, -1)
        # P1 = Apex (0, 3) -> High due to refraction arc
        # P2 = Observer (8, 1)
        
        p0 = np.array([self.obj_x, -1.0])
        p1 = np.array([0.0, 4.0]) # The warp point
        p2 = np.array([self.obs_x, 1.0])
        
        # B(t) = (1-t)^2 P0 + 2(1-t)t P1 + t^2 P2
        point = ((1-t)**2 * p0) + (2*(1-t)*t * p1) + (t**2 * p2)
        return point

    def update(self, frame_idx):
        # 1. SETUP (0-5s)
        
        # 2. THE RAY (5-20s)
        if frame_idx > 150 and frame_idx < 600:
            prog = (frame_idx - 150) / 450.0
            self.ray_progress = prog
            pt = self._get_curve_point(prog)
            self.ray_path.append(pt)
            
        # 3. THE PROJECTION (20-30s)
        if frame_idx > 600 and frame_idx < 900:
            prog = (frame_idx - 600) / 300.0
            # Clamp progress
            self.ghost_opacity = min(1.0, prog)
            
        # 4. THE STRETCH (30-40s)
        if frame_idx > 900:
            self.ghost_stretch = 1.5 + 0.5 * np.sin((frame_idx - 900) * 0.1)
            self.ghost_opacity = 1.0

    def render(self, frame_idx, ax):
        ax.set_xlim(-10, 10)
        ax.set_ylim(-5, 10)
        
        # 1. ATMOSPHERE (Gradient)
        steps = 50
        for i in range(steps):
            y = -2 + (12.0/steps)*i
            r = i / steps
            
            # Interpolate Blue to White
            cr = 0.69 + (1.0 - 0.69)*r
            cg = 0.87 + (0.98 - 0.87)*r
            cb = 0.90 + (0.98 - 0.90)*r
            col = (cr, cg, cb)
            
            # Use facecolor to avoid warning
            ax.add_patch(Rectangle((-12, y), 24, 12.0/steps + 0.1, facecolor=col, edgecolor='none', zorder=0))

        # 2. EARTH / SEA
        earth_r = 30.0
        earth_x = np.linspace(-12, 12, 100)
        # Curve downwards
        earth_y = -np.sqrt(earth_r**2 - earth_x**2) + (earth_r - 2.5)
        
        sea_poly = list(zip(earth_x, earth_y))
        sea_poly.append((12, -10))
        sea_poly.append((-12, -10))
        ax.add_patch(Polygon(sea_poly, color=SEA_INDIGO, zorder=5))

        # 3. REAL OBJECT (The Ship)
        sx, sy = self.obj_x, -1.8 # Lower physics
        
        # Ship Silhouette
        ship_poly = [
            [sx-1, sy], [sx+1, sy], [sx+0.8, sy-0.5], [sx-0.8, sy-0.5]
        ]
        mast_poly = [[sx, sy], [sx, sy+1.5]]
        flag_poly = [[sx, sy+1.4], [sx+0.4, sy+1.3], [sx, sy+1.2]]
        
        ax.add_patch(Polygon(ship_poly, color=SHIP_BLACK, zorder=4))
        ax.plot([p[0] for p in mast_poly], [p[1] for p in mast_poly], color=SHIP_BLACK, linewidth=2, zorder=4)
        ax.add_patch(Polygon(flag_poly, color=SHIP_BLACK, zorder=4))
        ax.text(sx, sy-1.5, "REALITY", ha='center', fontsize=8, color=SHIP_BLACK)

        # 4. OBSERVER
        ox, oy = self.obs_x, 1.0
        ax.add_patch(Circle((ox, oy), 0.2, color="black", zorder=6))
        ax.add_patch(Circle((ox, oy), 0.05, color="white", zorder=7))

        # 5. THE RAY
        if len(self.ray_path) > 1:
            # Need to unzip list of arrays properly
            rx = [p[0] for p in self.ray_path]
            ry = [p[1] for p in self.ray_path]
            ax.plot(rx, ry, color=RAY_YELLOW, linewidth=2, alpha=0.8, zorder=10)

        # 6. THE MIRAGE
        if self.ghost_opacity > 0:
            gx, gy = -8.0, 5.0 # Projected position
            stretch = self.ghost_stretch
            
            # Ghost Hull
            g_poly = [
                # Inverted/Distorted top
                [gx-1, gy], [gx+1, gy], 
                [gx+0.8, gy + 0.5*stretch], [gx-0.8, gy + 0.5*stretch]
            ]
            
            # Ghost Stack
            for stack in range(3):
                offset = stack * (1.0 * stretch)
                alpha = np.clip(self.ghost_opacity - (stack*0.2), 0, 1) * 0.6
                
                # Use standard plot for lines
                ax.add_patch(Rectangle((gx-0.8, gy+offset), 1.6, 0.8*stretch, facecolor=GHOST_CYAN, alpha=alpha, zorder=3))
                ax.plot([gx, gx], [gy+offset, gy+offset+1.5*stretch], color=GHOST_EDGE, alpha=alpha, linewidth=1, zorder=3)

            # Dotted Line of Sight
            ax.plot([ox, gx], [oy, gy], color=RAY_YELLOW, linestyle="--", alpha=self.ghost_opacity*0.5, zorder=9)
            
            if self.ghost_opacity > 0.8:
                ax.text(gx, gy+4, "FATA MORGANA", ha='center', fontsize=10, color=GHOST_EDGE, fontweight='bold', alpha=self.ghost_opacity)

        # HUD
        if frame_idx < 150:
            lbl = "PHASE 1: TEMPERATURE INVERSION"
            col = AIR_COLD
        elif frame_idx < 600:
            lbl = "PHASE 2: THE BENT PATH (SNELL'S LAW)"
            col = RAY_YELLOW
        else:
            lbl = "PHASE 3: THE SUPERIOR MIRAGE"
            col = GHOST_CYAN
            
        ax.text(0, 9, lbl, color=col, ha='center', fontfamily='monospace', fontsize=14, fontweight='bold',
                bbox=dict(facecolor='black', edgecolor=col))
        
        ax.text(0, 7, "WARM AIR (LOW n)", ha='center', color="#808080", fontsize=8, alpha=0.5)
        ax.text(0, -1, "COLD AIR (HIGH n)", ha='center', color="#204060", fontsize=8, alpha=0.5)


        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_mirage_fixed_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"mirage_fixed_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor="white")
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Simulating Atmospheric Refraction (Fixed)...")
    
    sim = MirageSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 8), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor("white")
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
