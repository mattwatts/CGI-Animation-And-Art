"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v26.py
MODE:   Nursery (Plasma Palette)
TARGET: Nuclear Fusion (Tokamak / Lorentz Force)
STYLE:  "The Magnetic Bottle" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
import os

# --- 1. THE PLASMA PALETTE ---
BG_COLOR = "#000000"        # Reactor Chamber
WALL_COLOR = "#333333"      # The Physical Wall (Danger Zone)
FIELD_COLOR = "#222222"     # Magnetic Lines (Subtle)
D_COLOR = "#FF4500"         # Deuterium (Red)
T_COLOR = "#0080FF"         # Tritium (Blue)
FUSION_COLOR = "#FFFFFF"    # Helium/Neutron (White Hot)
GLOW_COLOR = "#FFD700"      # Energy Halo

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class TokamakSim:
    def __init__(self):
        self.num_particles = 40
        self.r_min = 2.0
        self.r_max = 3.5
        
        # Initialize Particles
        # State: [angle, radius, type(0=D, 1=T), wobble_phase]
        self.particles = []
        for i in range(self.num_particles):
            t = i % 2 # Alternating types
            angle = np.random.rand() * 2 * np.pi
            r = self.r_min + np.random.rand() * (self.r_max - self.r_min)
            wobble = np.random.rand() * 2 * np.pi
            speed = 0.05 + np.random.rand() * 0.03 # Fast!
            self.particles.append({
                'theta': angle, 
                'r': r, 
                'type': t, 
                'wobble': wobble,
                'speed': speed,
                'alive': True
            })
            
        self.flares = [] # Fusion events

    def update(self):
        # 1. Move Particles
        for p in self.particles:
            if not p['alive']: continue
            
            # Orbital motion (The Toroidal flow)
            p['theta'] += p['speed']
            
            # Thermal Jitter (The Gyromotion / Instability)
            p['wobble'] += 0.5
            p['r'] += np.sin(p['wobble']) * 0.02
            
            # MAGNETIC CONFINEMENT (The "Bottle")
            # If particle drifts too far out or in, Force acts strongly
            if p['r'] < self.r_min:
                p['r'] += 0.05 # Push out
            if p['r'] > self.r_max:
                p['r'] -= 0.05 # Push in

        # 2. Check Fusibility (Collisions)
        # Brute force check O(N^2) is fine for N=40
        for i, p1 in enumerate(self.particles):
            if not p1['alive']: continue
            
            for j, p2 in enumerate(self.particles):
                if i >= j or not p2['alive']: continue
                
                # Must be opposites (Red + Blue)
                if p1['type'] == p2['type']: continue
                
                # Check dist (Polar conversion approx)
                # Just check angle diff and r diff
                angle_diff = abs(p1['theta'] - p2['theta']) % (2*np.pi)
                if angle_diff > np.pi: angle_diff = 2*np.pi - angle_diff
                
                # Arc length distance approx r * theta
                dist_arc = p1['r'] * angle_diff
                dist_r = abs(p1['r'] - p2['r'])
                
                if dist_arc < 0.2 and dist_r < 0.2:
                    # FUSION EVENT
                    self.trigger_fusion(p1, p2)
                    break # One event per particle per frame

        # 3. Update Flares
        for f in self.flares:
            f['age'] += 1

    def trigger_fusion(self, p1, p2):
        # Calc midpoint position for visual
        mid_theta = (p1['theta'] + p2['theta']) / 2
        mid_r = (p1['r'] + p2['r']) / 2
        
        # Kill parents? Or scatter them?
        # In this game, they merge then respawn elsewhere to keep flux constant
        # Respawn logic
        p1['theta'] = np.random.rand() * 2 * np.pi
        p1['r'] = self.r_min + 0.2
        p2['theta'] = np.random.rand() * 2 * np.pi
        p2['r'] = self.r_max - 0.2
        
        self.flares.append({
            'theta': mid_theta, 'r': mid_r, 'age': 0, 'max_age': 15
        })

    def render(self, frame_idx, ax):
        # 1. The Machine (Tokamak Walls)
        # Inner Wall
        ax.add_patch(Circle((0,0), self.r_min - 0.1, facecolor=BG_COLOR, edgecolor=WALL_COLOR, linewidth=3))
        # Outer Wall
        ax.add_patch(Wedge((0,0), self.r_max + 0.1, 0, 360, width=0.1, facecolor=WALL_COLOR))
        
        # Magnetic Field Lines (Dashed Circles)
        for r_line in np.linspace(self.r_min, self.r_max, 4):
            ax.add_patch(Circle((0,0), r_line, color=FIELD_COLOR, fill=False, linestyle="--", linewidth=1))

        # 2. The Plasma (Particles)
        for p in self.particles:
            if not p['alive']: continue
            
            x = p['r'] * np.cos(p['theta'])
            y = p['r'] * np.sin(p['theta'])
            
            c = D_COLOR if p['type'] == 0 else T_COLOR
            
            # Draw tail?
            # Visual speed blur
            tail_x = p['r'] * np.cos(p['theta'] - 0.1)
            tail_y = p['r'] * np.sin(p['theta'] - 0.1)
            ax.plot([tail_x, x], [tail_y, y], color=c, alpha=0.5, linewidth=2)
            
            ax.add_patch(Circle((x, y), 0.08, color=c, zorder=10))

        # 3. Fusion Flares
        for f in self.flares:
            if f['age'] < f['max_age']:
                x = f['r'] * np.cos(f['theta'])
                y = f['r'] * np.sin(f['theta'])
                
                # Expand
                prog = f['age'] / f['max_age']
                size = 0.5 * (1.0 - prog)
                
                # Core
                ax.add_patch(Circle((x, y), size, color=FUSION_COLOR, zorder=20))
                # Halo
                ax.add_patch(Circle((x, y), size * 2.5, color=GLOW_COLOR, alpha=0.5 * (1-prog), zorder=19))

        # Scale
        limit = 4.5
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_aspect('equal')
        
        # Save
        out_dir = "logic_garden_fusion_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"fusion_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Confining the Plasma...")
    
    sim = TokamakSim()
    
    for i in range(TOTAL_FRAMES):
        sim.update()
        
        # Canvas
        fig = plt.figure(figsize=(10, 10), dpi=100) # Square visual for Tokamak
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.render(i, ax)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
