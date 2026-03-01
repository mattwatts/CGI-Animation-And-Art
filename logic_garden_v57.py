"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v57_fixed.py
MODE:   Nursery (Aurora Palette)
TARGET: Aurora Australis (Import Patch)
STYLE:  "The Magnetic Loom" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba
import os

# --- 1. THE TASMAN PALETTE ---
BG_VOID = "#000510"         # Night Sky
PLASMA_GOLD = "#FFD700"     # Solar Wind
FIELD_CYAN = "#008B8B"      # Magnetic Lines
OXY_RED = "#DC143C"         # High Alt
OXY_GREEN = "#39FF14"       # Mid Alt
NITRO_PURP = "#9400D3"      # Low Alt
EARTH_SILHOUETTE = "#000000"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class SolarParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = np.random.uniform(0.05, 0.1) # Moving Right
        self.vy = np.random.uniform(-0.02, 0.02)
        self.captured = False
        self.t_capture = 0

class AuroraCurtain:
    def __init__(self, x_base):
        self.x_base = x_base
        self.phase_offset = np.random.uniform(0, 2*np.pi)
        self.intensity = 0.0
        
    def get_shape(self, t):
        # Generate the wavy line of the curtain
        ys = np.linspace(1, 9, 50) # Altitude 1 to 9 (Reduced resolution for speed)
        
        # Wavy x based on Y and Time
        # The higher up, the more it waves
        wave = np.sin(ys * 0.8 + t + self.phase_offset) * 0.5 + \
               np.sin(ys * 2.0 - t * 0.5) * 0.2
               
        xs = self.x_base + wave
        return xs, ys

class AuroraSim:
    def __init__(self):
        self.particles = []
        self.curtains = []
        
        # Create 5 "Sheets" of aurora
        for i in range(5):
            self.curtains.append(AuroraCurtain(-3.0 + i * 1.5))
            
        self.solar_wind_intensity = 0.0
        self.mag_field_visible = 0.0
        
    def update(self, frame_idx):
        t = frame_idx * 0.05
        
        # SEQUENCE
        
        # 1. SOLAR WIND (0-10s)
        if frame_idx < 300:
            self.solar_wind_intensity = min(1.0, frame_idx / 100.0)
            # Spawn linear particles
            if np.random.random() < 0.3:
                self.particles.append(SolarParticle(-9, np.random.uniform(5, 10)))
        
        # 2. CAPTURE (10-20s)
        elif frame_idx < 600:
            self.mag_field_visible = min(1.0, (frame_idx - 300) / 100.0)
            # Spawn particles that curve down
            if np.random.random() < 0.4:
                p = SolarParticle(-9, np.random.uniform(6, 9))
                # Just marking them for logic, visual velocity handled in render
                self.particles.append(p)
                
        # 3. IGNITION (20s+)
        else:
            # Power up curtains
            for c in self.curtains:
                target = 0.8 + 0.2 * np.sin(t * 0.5 + c.phase_offset)
                c.intensity = c.intensity * 0.95 + target * 0.05
                
        # Update Particles
        # We need a new list to avoid modifying while iterating
        active_particles = []
        for p in self.particles:
            if not p.captured:
                p.x += p.vx
                p.y += p.vy
                
                # Capture Logic (Simulated)
                # If they hit the "Magnetic Funnel" region (x > -4), they start spiraling down
                if frame_idx > 300 and p.x > -4 and p.x < 4 and not p.captured:
                    p.captured = True
                    p.vx = 0 
            else:
                # Spiral Down
                p.t_capture += 0.1
                p.x += np.sin(p.t_capture * 5) * 0.05 # Wiggle
                p.y -= 0.15 # Fall
                
                # Burn up
                if p.y < 2.0:
                    continue # Remove
            
            # Bounds check
            if p.x < 10 and p.y > 0:
                active_particles.append(p)
                
        self.particles = active_particles

    def render(self, frame_idx, ax):
        ax.set_xlim(-8, 8)
        ax.set_ylim(0, 10)
        
        t = frame_idx * 0.05
        
        # 1. FIELD LINES (The Funnel)
        if self.mag_field_visible > 0:
            alpha = self.mag_field_visible * 0.3
            for x_start in [-4, -2, 0, 2, 4]:
                ys = np.linspace(1, 10, 50)
                # Field spreads out as it goes up
                xs = x_start * (ys * 0.1 + 0.5) 
                ax.plot(xs, ys, color=FIELD_CYAN, alpha=alpha, linestyle="--", linewidth=1)

        # 2. AURORA CURTAINS
        # Draw vertically colored segments
        for c in self.curtains:
            if c.intensity > 0.01:
                xs, ys = c.get_shape(t)
                
                points = np.array([xs, ys]).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)
                
                # Build Gradient Colors
                colors = []
                for y in ys[:-1]:
                    a = np.clip(c.intensity, 0, 1) * 0.6
                    
                    if y > 6.0: # High (Red)
                        col = to_rgba(OXY_RED, alpha=a)
                    elif y > 2.0: # Mid (Green)
                        col = to_rgba(OXY_GREEN, alpha=a)
                    else: # Low (Purple)
                        col = to_rgba(NITRO_PURP, alpha=a)
                    colors.append(col)
                
                # LineCollection allows gradient line
                lc = LineCollection(segments, colors=colors, linewidth=15, capstyle='round')
                ax.add_collection(lc)

        # 3. SOLAR PARTICLES
        px_sol = [p.x for p in self.particles if not p.captured]
        py_sol = [p.y for p in self.particles if not p.captured]
        
        px_cap = [p.x for p in self.particles if p.captured]
        py_cap = [p.y for p in self.particles if p.captured]
        
        if px_sol:
            ax.scatter(px_sol, py_sol, c=PLASMA_GOLD, s=10, alpha=0.8, zorder=10)
            
        if px_cap:
            ax.scatter(px_cap, py_cap, c="white", s=5, alpha=0.6, zorder=10)

        # 4. SILHOUETTE (Earth Surface)
        # Using Polygon now correctly imported
        poly_pts = [
            [-8, 0], [-6, 1.0], [-4, 0.5], [-2, 1.5], 
            [0, 0.8], [2, 2.0], [4, 0.5], [6, 1.2], [8, 0], [8, -1], [-8, -1]
        ]
        ax.add_patch(Polygon(poly_pts, color="black", zorder=20))

        # HUD
        if frame_idx < 300:
            lbl = "PHASE 1: SOLAR WIND (PLASMA)"
            col = PLASMA_GOLD
        elif frame_idx < 600:
            lbl = "PHASE 2: THE MAGNETIC FUNNEL"
            col = FIELD_CYAN
        else:
            lbl = "PHASE 3: IONIZATION (THE GLOW)"
            col = OXY_GREEN
            
        ax.text(0, 9.2, lbl, color=col, ha='center', fontfamily='monospace', fontsize=14, fontweight='bold',
                bbox=dict(facecolor='black', edgecolor=col))
        
        # Color Key
        if frame_idx > 600:
            ax.text(-7, 8, "OXYGEN (RED)", color=OXY_RED, fontsize=8, fontweight='bold')
            ax.text(-7, 5, "OXYGEN (GREEN)", color=OXY_GREEN, fontsize=8, fontweight='bold')
            ax.text(-7, 1.5, "NITROGEN (PURPLE)", color=NITRO_PURP, fontsize=8, fontweight='bold')

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_aurora_fixed_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"aurora_fixed_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Energizing the Magnetosphere (Fixed)...")
    
    sim = AuroraSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 8), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_VOID)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
