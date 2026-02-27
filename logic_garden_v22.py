"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v22.py
MODE:   Nursery (Bauhaus Palette)
TARGET: RTG (Seebeck Effect / Nuclear Battery)
STYLE:  "The Silent Fire" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"        # Void
CORE_COLOR = "#FF4500"      # Safety Red (Pu-238)
FIN_COLOR = "#0080FF"       # Azure Blue (Space Radiator)
COUPLE_COLOR = "#333333"    # Thermocouple Metal
ELEC_COLOR = "#FFD700"      # Cyber Yellow (The Flow)

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class RTG_Sim:
    def __init__(self):
        # Physics State
        self.num_fins = 8
        self.electrons = [] # List of angles/radius coords
        
        # Initialize electrons in the circuit
        # They flow radially outward through the couple, then circular?
        # Let's visualize them appearing at the Hot junction and flowing to Cold
        
        for i in range(100):
            # Random placements along the "Couples"
            angle_idx = np.random.randint(0, self.num_fins)
            base_angle = (2 * np.pi / self.num_fins) * angle_idx
            dist = 1.5 + np.random.rand() * 2.0
            self.electrons.append({
                'angle_base': base_angle,
                'dist': dist,
                'speed': 0.05 + (np.random.rand() * 0.02)
            })

    def update(self):
        # Move electrons outward (Heat -> Electricity flow direction visual)
        for e in self.electrons:
            e['dist'] += e['speed']
            
            # Loop?
            # If they hit the fin (Cold sink), they vanish/recycle
            # Visual metaphor: Heat Energy extracted.
            if e['dist'] > 3.5:
                e['dist'] = 1.6 # Respawn at hot junction

    def render(self, frame_idx, ax):
        # 1. Draw Fins (Cold Sink)
        # Radial rectangles
        fin_w = 0.6
        fin_h = 2.0
        
        for i in range(self.num_fins):
            angle = (2 * np.pi / self.num_fins) * i
            ox, oy = 2.0 * np.cos(angle), 2.0 * np.sin(angle)
            
            # We need to rotate the rectangle patches
            # Matplotlib rotation is degrees
            deg = np.degrees(angle)
            
            # Fin (Blue)
            # Distance 2.5 to 4.5
            # Draw using Polygon for easy rotation logic
            
            # Local coords of a fin
            pts = np.array([
                [2.0, -0.3], [4.5, -0.6], # Flared fin
                [4.5, 0.6], [2.0, 0.3]
            ])
            
            # Rotation matrix
            c, s = np.cos(angle), np.sin(angle)
            R = np.array([[c, -s], [s, c]])
            
            rotated_pts = np.dot(pts, R.T)
            
            ax.add_patch(plt.Polygon(rotated_pts, facecolor=FIN_COLOR, zorder=1))
            
            # Thermocouple (Bridge)
            # Distance 1.5 to 2.0
            c_pts = np.array([
                [1.5, -0.15], [2.0, -0.15],
                [2.0, 0.15], [1.5, 0.15]
            ])
            rot_c_pts = np.dot(c_pts, R.T)
            ax.add_patch(plt.Polygon(rot_c_pts, facecolor=COUPLE_COLOR, zorder=2))

        # 2. Draw Electrons (The Current)
        # Yellow dots moving along the bridges
        for e in self.electrons:
            # Polar to Cartesian
            angle = e['angle_base']
            r = e['dist']
            
            # Add slight jitter/wave to look energized
            jitter = np.sin(frame_idx * 0.5 + r*10) * 0.05
            angle += jitter
            
            ex = r * np.cos(angle)
            ey = r * np.sin(angle)
            
            # Draw
            ax.add_patch(Circle((ex, ey), 0.08, color=ELEC_COLOR, zorder=5))

        # 3. Draw The Core (Hot Source)
        # Pulsing Red
        pulse = 1.5 + np.sin(frame_idx * 0.1) * 0.05
        ax.add_patch(Circle((0, 0), pulse, facecolor=CORE_COLOR, zorder=10))
        # Hot Center
        ax.add_patch(Circle((0, 0), pulse * 0.7, facecolor="#FF6633", zorder=11))
        
        # 4. Draw Radiation Ripples? (Optional)
        # Just simple heat
        
        # Scale
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_aspect('equal')
        
        # Save
        out_dir = "logic_garden_rtg_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"rtg_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Lighting the Silent Fire...")
    
    sim = RTG_Sim()
    
    for i in range(TOTAL_FRAMES):
        sim.update()
        
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.render(i, ax)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
