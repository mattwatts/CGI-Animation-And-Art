"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v27.py
MODE:   Nursery (Titanium Palette)
TARGET: SR-71 J58 Engine (Turboramjet / Variable Geometry Inlet)
STYLE:  "The Fire Eater" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Wedge, Arrow
import os

# --- 1. THE TITANIUM PALETTE ---
BG_COLOR = "#101010"        # Titanium Skin (Dark)
SPIKE_COLOR = "#00FF00"     # Technical Green (Moving Part)
AIR_COLD = "#0088FF"        # Subsonic Air
AIR_COMP = "#FF8800"        # Hot Air
SHOCK_COLOR = "#FF0000"     # The Shockwave
BYPASS_GOLD = "#FFD700"     # Bypass Flow

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class J58_Sim:
    def __init__(self):
        # State: Mach Number (1.0 to 3.2)
        self.mach = 1.0
        self.spike_retraction = 0.0 # 0 to 1.0 (26 inches)
        
        # Air particles
        self.particles = []
        for i in range(50):
            self.particles.append({
                'x': np.random.uniform(-4, 0),
                'y': np.random.uniform(-0.8, 0.8),
                'mode': 'intake' # intake, core, bypass, exhaust
            })

    def update(self, frame_idx):
        # 1. Accelerate
        progress = frame_idx / TOTAL_FRAMES
        self.mach = 1.0 + (progress * 2.2) # Max 3.2
        
        # 2. Logic: The Spike Logic
        # Spike starts moving at Mach 1.6
        if self.mach > 1.6:
            # Scale retraction to max at Mach 3.2
            self.spike_retraction = (self.mach - 1.6) / 1.6
            if self.spike_retraction > 1.0: self.spike_retraction = 1.0
        else:
            self.spike_retraction = 0.0

        # 3. Particle Flow
        # Speed increases with Mach
        flow_speed = 0.1 * self.mach
        
        for p in self.particles:
            p['x'] += flow_speed
            
            # Reset
            if p['x'] > 6:
                p['x'] = -4
                p['y'] = np.random.uniform(-0.8, 0.8)
                p['mode'] = 'intake'
                
            # Mode Switching (The "Trick")
            # If past the spike (x > 0)
            if p['x'] > 0 and p['x'] < 4:
                # BYPASS LOGIC
                # At Mach 3, most air bypasses the core (4th stage bleed)
                # Visual: Push particles to the edges (Bypass ducts)
                
                bypass_strength = 0.0
                if self.mach > 2.0:
                    bypass_strength = (self.mach - 2.0) / 1.2
                
                # If random chance < bypass_strength, go to bypass
                # Deterministic visual:
                if abs(p['y']) > 0.3: # Outer streams
                     # Push outward to duct
                     if p['y'] > 0: p['y'] = 0.7 # Top duct
                     else: p['y'] = -0.7 # Bottom duct
                     p['mode'] = 'bypass'
                else:
                    # Core stream
                    p['mode'] = 'core'
                    # If high mach, reduce core flow visual?
                    pass

    def render(self, frame_idx, ax):
        # --- A. DRAW THE ENGINE STRUCTURE ---
        
        # 1. Cowling (Outer Shell) - Static
        # Top Lip
        ax.add_patch(Rectangle((-1, 0.8), 6, 0.2, color="#444444"))
        # Bottom Lip
        ax.add_patch(Rectangle((-1, -1.0), 6, 0.2, color="#444444"))
        
        # Inlet Lip Sharpness
        # Draw triangles at x=-1
        ax.add_patch(Polygon([[-1, 0.8], [-1.2, 1.0], [-1, 1.0]], color="#444444"))
        ax.add_patch(Polygon([[-1, -0.8], [-1.2, -1.0], [-1, -1.0]], color="#444444"))
        
        # 2. The Core (Turbojet) - Static Block in center
        # Compressor / Turbine
        ax.add_patch(Rectangle((1.5, -0.4), 2.5, 0.8, color="#222222", zorder=5))
        
        # 3. The Spike (Moving)
        # Point starts at -0.5 (Extended) moves to 0.5 (Retracted)
        spike_x = -1.5 + (self.spike_retraction * 1.0)
        
        # Spike Geometry (Cone)
        # Using a Polygon to look like a cone/centerbody
        spike_pts = [
            [spike_x, 0], # Tip
            [spike_x + 3.0, 0.6], # Base Top
            [spike_x + 3.0, -0.6] # Base Bottom
        ]
        ax.add_patch(Polygon(spike_pts, color=SPIKE_COLOR, zorder=6))
        
        # --- B. DRAW THE PHYSICS ---
        
        # 4. The Shockwave (Red Line)
        # Angle gets steeper as Mach increases (Mach Angle)
        # sin(mu) = 1/M
        mu = np.arcsin(1.0 / self.mach)
        
        # Originates from Spike Tip
        lx = 5.0 * np.cos(mu)
        ly = 5.0 * np.sin(mu)
        
        # Top Shock
        ax.plot([spike_x, spike_x - lx], [0, ly], color=SHOCK_COLOR, linewidth=2, linestyle="--")
        # Bottom Shock
        ax.plot([spike_x, spike_x - lx], [0, -ly], color=SHOCK_COLOR, linewidth=2, linestyle="--")
        
        # Captured Shock (The "Trap")
        # At high mach, a normal shock sits inside the throat
        if self.mach > 2.0:
            throat_x = 0.5
            ax.plot([throat_x, throat_x], [-0.8, 0.8], color=SHOCK_COLOR, linewidth=3, alpha=0.7)
        
        # 5. The Air Flow
        for p in self.particles:
            c = AIR_COLD
            ms = 2 # size
            
            if p['x'] > spike_x:
                # Compressed air
                c = AIR_COMP
                
            if p['mode'] == 'bypass':
                c = BYPASS_GOLD
                
            if p['x'] > 4.0:
                # Afterburner!
                c = "#FFFFFF"
                ms = 4 + np.random.rand() * 2 # Expanding gas
                
            ax.add_patch(plt.Circle((p['x'], p['y']), radius=0.03 * ms, color=c, alpha=0.8, zorder=4))
        
        # 6. Afterburner Flame (Procedural)
        if frame_idx > 0:
            # Flame length proportional to Mach
            flame_len = self.mach * 1.5
            
            # Simple triangle pulse
            pulse = np.random.rand() * 0.5
            flame_poly = [
                [4.0, 0.4], [4.0 + flame_len + pulse, 0], [4.0, -0.4]
            ]
            ax.add_patch(Polygon(flame_poly, color="#FFFFFF", alpha=0.2, zorder=3))
            
            # Shock Diamonds (The coolest part)
            if self.mach > 2.0:
                 for d in range(1, 4):
                     dx = 4.0 + (d * 1.0)
                     ax.add_patch(plt.Circle((dx, 0), radius=0.2, color="#FF00FF", alpha=0.4, zorder=3))

        # --- C. HUD ---
        ax.text(-4.5, 1.2, f"MACH {self.mach:.2f}", color=SPIKE_COLOR, fontsize=15, fontfamily='monospace', fontweight='bold')
        
        state = "TURBOJET"
        if self.mach > 2.5: state = "RAMJET BIAS"
        ax.text(3.5, 1.2, state, color=BYPASS_GOLD, fontsize=10, fontfamily='monospace')

        # Scale
        ax.set_xlim(-5, 8)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.set_axis_off()
        
        # Save
        out_dir = "logic_garden_sr71_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"sr71_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Advancing the Throttle...")
    
    sim = J58_Sim()
    
    for i in range(TOTAL_FRAMES):
        sim.update(i)
        
        # Canvas
        fig = plt.figure(figsize=(16, 6), dpi=100) # Wide aspect for the Engine
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.render(i, ax)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
