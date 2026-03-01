"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v49_final.py
MODE:   Nursery (Civil Defense Palette)
TARGET: Ad Hoc Shelter (Blast Physic)
STYLE:  "The Geometry of Survival" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle
import os

# --- 1. THE DEFENSE PALETTE ---
BG_COLOR = "#101010"        # Concrete
BLAST_INCIDENT = "#FF0000"  # Incoming (Fatal)
BLAST_REFLECT = "#FF8C00"   # Bouncing (High Pressure)
BLAST_DIFFRACT = "#00BFFF"  # Curling (Low Pressure)
SHELTER_COL = "#8B4513"     # Oak
HUMAN_COL = "#39FF14"       # Survivor

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class Particle:
    def __init__(self, x, y, vx, vy, type_tag):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.type = type_tag # 0=Incident, 1=Reflected, 2=Diffracted
        self.active = True

class BlastSim:
    def __init__(self):
        self.particles = []
        
        # Room: -10 to 10
        # Table Center
        self.tx = -2.0
        self.tw = 6.0
        self.th = 4.0
        self.leg_w = 0.5
        self.top_h = 0.5
        
        self.human_pos = (self.tx + self.tw/2, 0)
        
    def update(self, frame_idx):
        # 1. EMITTER (Stop halfway to show clearing)
        if frame_idx < 800:
            for _ in range(20):
                # Wall of particles at x=-10
                y = np.random.uniform(0, 10)
                # Speed tuned to cross room in ~200 frames (6s)
                # Distance 20 units. Speed 0.1
                s = 0.1 + np.random.normal(0, 0.01)
                self.particles.append(Particle(-10, y, s, 0, 0))

        # 2. PHYSICS
        tx1 = self.tx
        tx2 = self.tx + self.tw
        ty_btm = self.th - self.top_h
        ty_top = self.th
        
        for p in self.particles:
            if not p.active: continue
            
            p.x += p.vx
            p.y += p.vy
            
            # --- COLLISION: FRONT LEG ---
            # Box: tx1 to tx1+leg_w, 0 to ty_btm
            if (p.x > tx1 and p.x < tx1+self.leg_w) and (p.y < ty_btm):
                if p.vx > 0: # Hit front
                    p.x = tx1 - 0.1
                    p.vx *= -0.5 # Bounce back
                    p.vy += np.random.uniform(-0.1, 0.1) # Scatter
                    p.type = 1 # Reflected
            
            # --- COLLISION: TABLE EDGES ---
            # Front Edge of Top
            if (p.x > tx1 and p.x < tx1+0.2) and (p.y > ty_btm and p.y < ty_top):
                if p.vx > 0:
                    p.x = tx1 - 0.1
                    p.vx *= -0.5
                    p.vy += 0.1
                    p.type = 1

            # --- DIFFRACTION (THE CURL) ---
            # If particle clears the top and passes the back edge
            # Gravity/Suction pulls it down into the wake
            if p.x > tx2 and p.y > 0:
                # Stronger pull closer to table
                if p.y < 6.0:
                    p.vy -= 0.005
                    p.vx *= 0.99
                    p.type = 2 # Diffracted

            # --- FLOORS/CEILINGS ---
            if p.y < 0:
                p.y = 0
                p.vy *= -0.5
                p.vx *= 0.9 # Ground friction
            
            if p.y > 10:
                p.y = 10
                p.vy *= -0.5

        # Cleanup
        self.particles = [p for p in self.particles if p.x < 12 and p.x > -12]

    def render(self, frame_idx, ax):
        ax.set_xlim(-10, 10)
        ax.set_ylim(0, 10)
        
        # 1. SHELTER
        # Top
        ax.add_patch(Rectangle((self.tx, self.th - self.top_h), self.tw, self.top_h, color=SHELTER_COL, zorder=20))
        # Front Leg
        ax.add_patch(Rectangle((self.tx, 0), self.leg_w, self.th, color=SHELTER_COL, zorder=20))
        # Back Leg
        ax.add_patch(Rectangle((self.tx + self.tw - self.leg_w, 0), self.leg_w, self.th, color=SHELTER_COL, zorder=20))

        # 2. PARTICLES
        px0, py0 = [], [] # Incident
        px1, py1 = [], [] # Reflected
        px2, py2 = [], [] # Diffracted
        
        for p in self.particles:
            if p.type == 0:
                px0.append(p.x); py0.append(p.y)
            elif p.type == 1:
                px1.append(p.x); py1.append(p.y)
            else:
                px2.append(p.x); py2.append(p.y)
        
        if px0: ax.scatter(px0, py0, c=BLAST_INCIDENT, s=5, alpha=0.5, zorder=10)
        if px1: ax.scatter(px1, py1, c=BLAST_REFLECT, s=5, alpha=0.6, zorder=11)
        if px2: ax.scatter(px2, py2, c=BLAST_DIFFRACT, s=5, alpha=0.4, zorder=5) # Behind table

        # 3. SAFETY SHADOW
        # Visual Triangle
        poly = [
            [self.tx + self.leg_w, 0],
            [self.tx + self.leg_w, self.th - self.top_h],
            [self.tx + self.tw + 3.0, 0]
        ]
        ax.add_patch(Polygon(poly, color=BLAST_DIFFRACT, alpha=0.1, zorder=2))

        # 4. SURVIVOR
        hx, hy = self.human_pos
        ax.add_patch(Circle((hx, 0.6), 0.4, color=HUMAN_COL, zorder=5))
        ax.add_patch(Rectangle((hx-0.3, 0), 0.6, 0.6, color=HUMAN_COL, zorder=5))

        # 5. HUD PHASE
        if frame_idx < 150:
            p = "PHASE 1: INCIDENT SHOCK (APPROACH)"
            c = BLAST_INCIDENT
        elif frame_idx < 450:
            p = "PHASE 2: REFLECTION (DOUBLE PRESSURE)"
            c = BLAST_REFLECT
        elif frame_idx < 900:
            p = "PHASE 3: DIFFRACTION (THE CURL)"
            c = BLAST_DIFFRACT
        else:
            p = "PHASE 4: THE WAKE (SURVIVAL)"
            c = HUMAN_COL
            
        ax.text(0, 9, p, color=c, ha='center', fontfamily='monospace', fontsize=14, fontweight='bold',
                bbox=dict(facecolor='black', edgecolor=c))

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_shelter_final_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"shelter_final_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Simulating {TOTAL_FRAMES} frames (Corrected Timeline)...")
    
    sim = BlastSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 5), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
