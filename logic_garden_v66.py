"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v66_full.py
MODE:   Nursery (Cosmic Palette)
TARGET: Solar System (Maximized Fill Factor)
STYLE:  "The Great Waltz" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# --- 1. THE COSMIC PALETTE ---
BG_VOID = "#050510"
SUN_GOLD = "#FDB813"
TRAIL_WHITE = "#FFFFFF"

# Planet Colors
C_MERCURY = "#A5A5A5"
C_VENUS = "#E3BB76"
C_EARTH = "#2255FF"
C_MARS = "#FF4500"
C_JUPITER = "#D9A066"
C_SATURN = "#C5AB6E"
C_URANUS = "#ACE5EE"
C_NEPTUNE = "#4169E1"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class SolarSystemSim:
    def __init__(self):
        # We scale distances non-linearly using a Power Law
        # r_vis = r^0.55 (Slightly compressed to let inner planets breathe)
        # Scale Factor needed to fit Neptune (30 AU) into our Limit (10.0)
        # 30^0.55 = 6.49. We multiply by 1.5 -> ~9.7
        
        self.scale_factor = 1.0
        
        self.raw_planets = [
            # Name, R (AU), Color, Size (Relative)
            ("Mercury", 0.4, C_MERCURY, 0.4),
            ("Venus", 0.7, C_VENUS, 0.9),
            ("Earth", 1.0, C_EARTH, 1.0),
            ("Mars", 1.5, C_MARS, 0.5),
            ("Jupiter", 5.2, C_JUPITER, 4.0),   # Boosted size for visibility
            ("Saturn", 9.5, C_SATURN, 3.5),
            ("Uranus", 19.2, C_URANUS, 2.5),
            ("Neptune", 30.0, C_NEPTUNE, 2.5),
        ]
        
        self.planets = []
        for name, r, col, sz in self.raw_planets:
            # 1. VISUAL RADIUS (The Geometry)
            # Power law compression
            r_vis = 1.8 * (r ** 0.55)
            
            # 2. ORBITAL SPEED (The Physics)
            # Kepler: v ~ 1 / sqrt(r)
            # w = v/r = 1 / r^1.5
            # We speed up the simulation so Neptune completes ~0.5 orbits in 40s
            w = 8.0 / (r ** 1.5)
            
            self.planets.append({
                "name": name,
                "r": r_vis,
                "w": w,
                "color": col,
                "size": sz * 200, # Large scatter size for Full Frame
                "theta": np.random.uniform(0, 2*np.pi),
                "history": []
            })
            
    def update(self, frame_idx):
        dt = 0.05
        
        for p in self.planets:
            # Update Angle
            p["theta"] += p["w"] * dt
            
            # Calculate Cartesian
            x = p["r"] * np.cos(p["theta"])
            y = p["r"] * np.sin(p["theta"])
            z = 0 
            
            # Store History
            p["history"].append((x, y, z))
            
            # Trail Length logic
            # Fast inner planets need shorter history to not look like solid rings?
            # Or long history to make rings? Let's make complete rings.
            # 300 frames is enough for a nice arc
            if len(p["history"]) > 300:
                p["history"].pop(0)

    def render(self, frame_idx, fig):
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor(BG_VOID)
        
        # CAMERA: GOD'S EYE (Top Down)
        # Elev=90 puts Y axis up, X axis right. Z axis towards eye.
        # This maximizes frame fill for circular orbits.
        ax.view_init(elev=90, azim=-90) # Azim -90 orients axes conventionally
        
        # LIMITS: TIGHT FIT
        # Neptune is at approx r=1.8 * 30^0.55 = 11.6
        # We set limits to 12.0
        limit = 12.0
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-1, 1)
        ax.set_axis_off()
        
        # 1. DRAW SUN (Center Anchor)
        ax.scatter([0], [0], [0], color=SUN_GOLD, s=2500, alpha=0.2)
        ax.scatter([0], [0], [0], color=SUN_GOLD, s=800, alpha=1.0)
        
        # 2. DRAW PLANETS
        for p in self.planets:
            x = p["r"] * np.cos(p["theta"])
            y = p["r"] * np.sin(p["theta"])
            
            # Draw Orbital Track (Faint Ring)
            # Pure circle for context
            theta_ring = np.linspace(0, 2*np.pi, 100)
            rx = p["r"] * np.cos(theta_ring)
            ry = p["r"] * np.sin(theta_ring)
            ax.plot(rx, ry, np.zeros_like(rx), color=p["color"], alpha=0.15, linewidth=0.8, linestyle="--")
            
            # Draw Active Trail (Bright Arc)
            if len(p["history"]) > 1:
                hx, hy, hz = zip(*p["history"])
                ax.plot(hx, hy, hz, color=p["color"], linewidth=2.0, alpha=0.6)
            
            # Draw Body
            ax.scatter([x], [y], [0], color=p["color"], s=p["size"], alpha=1.0, edgecolors='white', linewidths=0.5, zorder=10)
            
            # SATURN RINGS
            if p["name"] == "Saturn":
                # Visually represents rings as a disk around the point
                # Since top down, it's just a bigger circle
                ax.scatter([x], [y], [0], color="#C5AB6E", s=p["size"]*2.5, alpha=0.4, marker='o', zorder=9)

        # 3. HUD
        fig.text(0.5, 0.95, "LOGIC GARDEN 66: THE GREAT WALTZ", color="white", ha='center', fontsize=16, fontweight='bold', fontfamily='monospace')
        fig.text(0.5, 0.02, "FULL FRAME ORBITAL RESONANCE", color=SUN_GOLD, ha='center', fontsize=10, fontfamily='monospace', alpha=0.6)
        
        # Save
        out_dir = "logic_garden_full_solar_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"solar_full_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID, bbox_inches='tight', pad_inches=0)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Maximizing the Frame...")
    
    sim = SolarSystemSim()
    
    for i in range(TOTAL_FRAMES):
        # Use Square Figure
        fig = plt.figure(figsize=(10, 10), dpi=100)
        
        sim.update(i)
        sim.render(i, fig)
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
