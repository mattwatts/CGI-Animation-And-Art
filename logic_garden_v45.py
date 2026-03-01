"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v45.py
MODE:   Nursery (Quantum Interference Palette)
TARGET: Multi-Body Hawking Radiation & Superposition
STYLE:  "The Interference of Being" | High Complexity | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os

# --- 1. THE INTERFERENCE PALETTE ---
BG_COLOR = "#050015"        # Deep Indigo Void
BH_COLOR = "#000000"        # Black Hole
HORIZON_COLOR = "#FFFFFF"   # Event Horizon
WAVE_COLOR = "#00FFFF"      # Hawking Radiation (Cyan)
INTERFERENCE_COL = "#FFD700"# The "Us" (Gold)

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class Wave:
    def __init__(self, x, y, r, intensity):
        self.x = x
        self.y = y
        self.r = r
        self.intensity = intensity

class BlackHole:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.phase = np.random.uniform(0, np.pi*2)
        self.freq = 0.5 + np.random.rand() * 0.5
        
    def emit(self, timer):
        # Pulse radiation based on mass (smaller = faster evaporation)
        rate = 20.0 / self.mass
        if timer % int(rate) == 0:
            return True
        return False

class UniverseSim:
    def __init__(self):
        self.holes = []
        self.waves = []
        self.sparks = [] # Interference points
        
        # Spawn Black Holes in a random cloud
        for _ in range(7):
            bx = np.random.uniform(-7, 7)
            by = np.random.uniform(-7, 7)
            mass = np.random.uniform(1.0, 3.0)
            self.holes.append(BlackHole(bx, by, mass))
            
        self.timer = 0
            
    def get_intersections(self, w1, w2):
        # Calculate intersection points of two circles
        d2 = (w1.x - w2.x)**2 + (w1.y - w2.y)**2
        d = np.sqrt(d2)
        
        # Check concentric or too far
        if d > w1.r + w2.r or d < abs(w1.r - w2.r) or d == 0:
            return []
            
        # Circle intersection math
        a = (w1.r**2 - w2.r**2 + d2) / (2*d)
        h = np.sqrt(max(0, w1.r**2 - a**2))
        
        x2 = w1.x + a * (w2.x - w1.x) / d
        y2 = w1.y + a * (w2.y - w1.y) / d
        
        x3_1 = x2 + h * (w2.y - w1.y) / d
        y3_1 = y2 - h * (w2.x - w1.x) / d
        
        x3_2 = x2 - h * (w2.y - w1.y) / d
        y3_2 = y2 + h * (w2.x - w1.x) / d
        
        return [(x3_1, y3_1), (x3_2, y3_2)]

    def update(self, frame_idx):
        self.timer += 1
        self.sparks = []
        
        # 1. BH Emission
        for bh in self.holes:
            if bh.emit(self.timer):
                # Spawn Wave
                # Radius starts at Event Horizon (approx mass/2)
                self.waves.append(Wave(bh.x, bh.y, bh.mass * 0.2, 1.0))
                
        # 2. Wave Propagation
        c = 0.15 # Speed of light
        for w in self.waves:
            w.r += c
            w.intensity *= 0.985 # Dissipation over volume
            
        # Remove dead waves
        self.waves = [w for w in self.waves if w.intensity > 0.05]
        
        # 3. Calculate Interference (The "Us" Logic)
        # Check intersections between all active waves
        # Only check waves that are reasonably strong
        
        # To save O(N^2), only check a subset or optimize?
        # N is small (< 50 usually), so O(N^2) is fine for "Sovereign Code"
        
        for i in range(len(self.waves)):
            for j in range(i + 1, len(self.waves)):
                w1 = self.waves[i]
                w2 = self.waves[j]
                
                # Proximity check
                dist = np.sqrt((w1.x-w2.x)**2 + (w1.y-w2.y)**2)
                if dist < (w1.r + w2.r):
                    pts = self.get_intersections(w1, w2)
                    for px, py in pts:
                        # Only keep points inside screen
                        if -9 < px < 9 and -9 < py < 9:
                            # Intensity is product of both parents
                            power = (w1.intensity + w2.intensity)
                            self.sparks.append({'x': px, 'y': py, 'power': power})
                            
    def render(self, frame_idx, ax):
        ax.set_xlim(-9, 9)
        ax.set_ylim(-9, 9)
        
        # 1. Background Waves (The Ripples)
        for w in self.waves:
            # Alpha based on intensity
            alpha = max(0.0, min(1.0, w.intensity * 0.5))
            circle = Circle((w.x, w.y), w.r, color=WAVE_COLOR, fill=False, linewidth=1.5, alpha=alpha)
            ax.add_patch(circle)
            
        # 2. Black Holes (The Source)
        for bh in self.holes:
            # Horizon
            ax.add_patch(Circle((bh.x, bh.y), bh.mass*0.2 + 0.05, color=HORIZON_COLOR, zorder=5))
            # Hole
            ax.add_patch(Circle((bh.x, bh.y), bh.mass*0.2, color=BH_COLOR, zorder=6))

        # 3. The Interference Pattern (The "Us")
        # Render sparks where waves overlap
        sx = [s['x'] for s in self.sparks]
        sy = [s['y'] for s in self.sparks]
        sp = [s['power'] * 20 for s in self.sparks] # Size
        sa = [min(1.0, s['power']*0.8) for s in self.sparks] # Alpha
        
        if sx:
            # We must set alpha per point, scatter takes single alpha or array
            # We use RGBA array for colors to handle alphas
            
            # Map intensity to Gold Alpha
            # Base Gold: 255, 215, 0 (#FFD700)
            colors = np.zeros((len(sx), 4))
            colors[:, 0] = 1.0 # R
            colors[:, 1] = 0.84 # G
            colors[:, 2] = 0.0 # B
            colors[:, 3] = sa # A
            
            ax.scatter(sx, sy, s=sp, c=colors, marker='o', zorder=10, edgecolors='none')
            
            # Add a super-bright white core to strong interference for "glint"
            filters = [i for i, power in enumerate(sp) if power > 1.5]
            if filters:
                 high_x = [sx[i] for i in filters]
                 high_y = [sy[i] for i in filters]
                 ax.scatter(high_x, high_y, s=5, c='white', zorder=11)

        # 4. HUD
        active_waves = len(self.waves)
        complexity = len(self.sparks)
        
        ax.text(0, -8, f"QUANTUM PACKETS: {active_waves}", color=WAVE_COLOR, ha='center', fontfamily='monospace', fontsize=10)
        ax.text(0, -8.5, f"COMPLEXITY NODES (US): {complexity}", color=INTERFERENCE_COL, ha='center', fontfamily='monospace', fontsize=12, fontweight='bold')

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_interference_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"inter_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Calculating Wave Function Collapse...")
    
    sim = UniverseSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(12, 12), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
