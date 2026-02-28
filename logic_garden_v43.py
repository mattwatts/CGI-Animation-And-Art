"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v43.py
MODE:   Nursery (High Energy Spectrum)
TARGET: Gamma-Ray Burst (Relativistic Jet Dynamics)
STYLE:  "The Cosmic Sniper" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle
import os

# --- 1. THE HIGH ENERGY PALETTE ---
BG_COLOR = "#000005"
WR_STAR = "#4040FF"         # Hot massive star
JET_CORE = "#FFFFFF"        # Pure Energy
JET_GAMMA = "#8F00FF"       # Gamma Rays
JET_XRAY = "#00FFFF"        # Afterglow 1
JET_RADIO = "#FF0000"       # Afterglow 2
ACCRETION = "#FFD700"       # Disk

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class GRBSim:
    def __init__(self):
        self.phase = 'collapse' # collapse, drill, breakout, afterglow
        self.star_r = 4.0
        self.jet_len = 0.0
        self.jet_width = 0.5
        self.flash_alpha = 0.0
        self.timer = 0
        
        # Color shift for afterglow
        self.jet_color = JET_GAMMA
        
        # Particles
        self.particles = []

    def update(self, frame_idx):
        self.timer += 1
        
        # PHASE 1: COLLAPSE
        if self.phase == 'collapse':
            # Star shrinks slightly then rapid implosion
            if self.timer < 60:
                self.star_r = 4.0 + 0.1 * np.sin(frame_idx)
            elif self.timer < 90:
                self.star_r *= 0.9 # Implode
            else:
                self.phase = 'drill'
                self.star_r = 2.0 # Compact envelop
                self.timer = 0

        # PHASE 2: DRILL (Jet inside star)
        elif self.phase == 'drill':
            # Jet grows locally
            self.jet_len += 0.05
            
            # Cocoon shockwave logic (star bulges at poles)
            # Visualized by jet rendering
            
            if self.jet_len > self.star_r:
                self.phase = 'breakout'
                self.timer = 0
                self.flash_alpha = 1.0

        # PHASE 3: BREAKOUT (The Flash)
        elif self.phase == 'breakout':
            self.jet_len = 20.0 # Infinite
            self.flash_alpha *= 0.9 # Fade out white screen
            
            if self.flash_alpha < 0.1:
                self.phase = 'afterglow'
                self.timer = 0

        # PHASE 4: AFTERGLOW (Spectrum Shift)
        elif self.phase == 'afterglow':
            # Jet widens
            self.jet_width += 0.01
            # Jet fades
            
            # Color Shift Logic (Manual lerp simulation)
            if self.timer < 100:
                self.jet_color = JET_GAMMA
            elif self.timer < 200:
                self.jet_color = JET_XRAY
            else:
                self.jet_color = JET_RADIO

        # PARTICLE EMISSION (The Jet Stream)
        if self.phase in ['drill', 'breakout', 'afterglow']:
            # Emit relativistic particles along Y axis
            count = 10 if self.phase == 'breakout' else 2
            for _ in range(count):
                # Narrow beam theta = 1/Gamma
                theta = np.random.normal(0, 0.05) # Very narrow
                speed = np.random.uniform(0.5, 1.0)
                
                # Up Jet
                self.particles.append({
                    'x': 0, 'y': 0,
                    'vx': np.sin(theta)*speed, 'vy': np.cos(theta)*speed,
                    'life': 1.0, 'col': self.jet_color
                })
                # Down Jet
                self.particles.append({
                    'x': 0, 'y': 0,
                    'vx': np.sin(theta)*speed, 'vy': -np.cos(theta)*speed,
                    'life': 1.0, 'col': self.jet_color
                })

        # Update particles
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 0.02
        self.particles = [p for p in self.particles if p['life'] > 0]

    def render(self, frame_idx, ax):
        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)
        
        # 1. The Jet (Polygon)
        if self.jet_len > 0:
            # Draw two triangles
            w = self.jet_width
            l = self.jet_len
            
            # Up
            jet_poly_u = [[0,0], [-w, l], [w, l]]
            ax.add_patch(Polygon(jet_poly_u, color=self.jet_color, alpha=0.6, zorder=5))
            # Core
            ax.add_patch(Polygon([[0,0], [-w*0.3, l], [w*0.3, l]], color=JET_CORE, alpha=0.8, zorder=6))

            # Down
            jet_poly_d = [[0,0], [-w, -l], [w, -l]]
            ax.add_patch(Polygon(jet_poly_d, color=self.jet_color, alpha=0.6, zorder=5))
            ax.add_patch(Polygon([[0,0], [-w*0.3, -l], [w*0.3, -l]], color=JET_CORE, alpha=0.8, zorder=6))

        # 2. The Star (Wolf-Rayet Envelop)
        if self.phase != 'afterglow':
            # Pulsing envelope
            ax.add_patch(Circle((0,0), self.star_r, color=WR_STAR, alpha=0.8, zorder=4))
            # Core collapse indicator
            if self.phase == 'collapse':
                ax.add_patch(Circle((0,0), self.star_r*0.3, color="black", zorder=5))

        # 3. The Black Hole (Engine)
        if self.phase in ['drill', 'breakout', 'afterglow']:
            ax.add_patch(Circle((0,0), 0.5, color="black", zorder=10))
            # Accretion Disk (Edge on)
            ax.add_patch(Rectangle((-1.0, -0.1), 2.0, 0.2, color=ACCRETION, zorder=11))

        # 4. Particles
        for p in self.particles:
            ax.add_patch(Circle((p['x'], p['y']), 0.1, color=p['col'], alpha=p['life'], zorder=7))

        # 5. The Flash (Screen Wipe)
        if self.flash_alpha > 0.01:
            ax.add_patch(Rectangle((-10,-10), 20, 20, color="white", alpha=self.flash_alpha, zorder=20))

        # 6. HUD
        status = "PHASE 1: STELLAR COLLAPSE"
        col = WR_STAR
        if self.phase == 'drill': 
            status = "PHASE 2: JET DRILLING"
            col = JET_GAMMA
        if self.phase == 'breakout':
            status = "PHASE 3: GAMMA BREAKOUT"
            col = "black" if self.flash_alpha > 0.5 else JET_GAMMA
        if self.phase == 'afterglow':
            status = "PHASE 4: SYNCHROTRON AFTERGLOW"
            col = self.jet_color

        ax.text(0, -7, status, color=col, ha='center', fontfamily='monospace', fontsize=14,
                bbox=dict(facecolor='black', edgecolor=col, alpha=0.7))

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_grb_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"grb_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Focusing Relativistic Beam...")
    
    sim = GRBSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
