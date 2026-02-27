"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v18.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Nuclear Transmutation (U-238 -> Pu-239)
STYLE:  "The Alchemist" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"        # Void
PROTON_COLOR = "#FF4500"    # Safety Red (Identity)
NEUTRON_COLOR = "#0080FF"   # Azure Blue (Ballast)
BETA_COLOR = "#FFD700"      # Cyber Yellow (The Spark/Electron)
TEXT_COLOR = "#000000"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

# Physics Model (Toy)
# We don't need 238 circles. It's too messy visually.
# Let's use a "Symbolic Nucleus" of ~50 visible balls.
# But keeping the Ratio roughly right visually.

class NucleusSim:
    def __init__(self):
        self.particles = [] # List of dicts: {'x', 'y', 'type', 'id'}
        self.stage = "U-238" # U-238, U-239, Np-239, Pu-239
        self.proton_count = 92
        self.neutron_count = 146
        
        # Build symbolic cluster
        # Pack circles in a spiral or random packing
        # Let's use concentric circles for stability
        
        num_viz = 100 # Visual representation
        for i in range(num_viz):
            # Spiral
            r = 0.5 * np.sqrt(i)
            theta = 2.4 * i # Golden angle approx
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            
            # Type distribution
            # 92/238 approx 40% Protons
            is_proton = np.random.rand() < 0.38
            if i == 0: is_proton = False # Reserve center for "The Change" to be visible?
            # Actually, let's target specific indices for transmutation later.
            
            p_type = 'proton' if is_proton else 'neutron'
            color = PROTON_COLOR if is_proton else NEUTRON_COLOR
            
            self.particles.append({
                'x': x, 'y': y, 
                'type': p_type, 
                'color': color,
                'target': False # Is this the one that changes?
            })
            
        # Select targets for decay (Two neutrons near the outside or center?)
        # Let's pick two Neutrons to be our "Actors"
        neutrons = [p for p in self.particles if p['type'] == 'neutron']
        self.target1 = neutrons[-1] # Outer one
        self.target2 = neutrons[-5] # Another outer one
        
        self.target1['target'] = True
        self.target2['target'] = True
        
        # Incoming Neutron
        self.incoming = {'x': -10, 'y': -5, 'type': 'neutron', 'color': NEUTRON_COLOR}
        
        # Beta Particles (Sparks)
        self.betas = []

    def render(self, frame_idx, ax):
        # 1. State Logic (Hardcoded Timeline for Animation)
        # 0-100: Neutron Approaches
        # 100-150: Absorption (U-238 -> U-239)
        # 150-250: Wait... Shake...
        # 250: Decay 1 (U-239 -> Np-239)
        # 250-350: Wait...
        # 350: Decay 2 (Np-239 -> Pu-239)
        # 350-End: Glory
        
        t = frame_idx
        
        # --- PHASE 1: APPROACH ---
        if t < 100:
            # Lerp incoming neutron to a gap
            # Let's aim for (2, 2) roughly
            target_pos = np.array([2.5, 2.0])
            start_pos = np.array([-8.0, 5.0])
            progress = t / 100.0
            curr = start_pos + (target_pos - start_pos) * progress
            self.incoming['x'] = curr[0]
            self.incoming['y'] = curr[1]
            
            self.label = "Uranium-238"
            self.sub = "92 Protons"

        # --- PHASE 2: ABSORPTION ---
        elif t >= 100 and t < 220:
            # Grid lock
            self.incoming['x'] = 2.5
            self.incoming['y'] = 2.0
            
            self.stage = "U-239"
            self.label = "Uranium-239"
            self.sub = "Unstable..."
            
            # Shake effect (The fever)
            shake = np.sin(t * 0.5) * 0.05
            for p in self.particles:
                p['x'] += shake * (np.random.rand()-0.5)
                p['y'] += shake * (np.random.rand()-0.5)

        # --- PHASE 3: DECAY 1 ---
        elif t >= 220 and t < 380:
            if t == 220:
                # TRANSFORMATION
                self.target1['type'] = 'proton'
                self.target1['color'] = PROTON_COLOR # Turns RED
                
                # Emit Electron
                self.betas.append({
                    'x': self.target1['x'], 
                    'y': self.target1['y'], 
                    'vx': 0.2, 'vy': 0.2 # Fly away
                })
            
            self.label = "Neptunium-239"
            self.sub = "93 Protons"
            
            # Move beta
            if self.betas:
                self.betas[0]['x'] += self.betas[0]['vx']
                self.betas[0]['y'] += self.betas[0]['vy']

        # --- PHASE 4: DECAY 2 ---
        elif t >= 380:
            if t == 380:
                # TRANSFORMATION 2
                self.target2['type'] = 'proton'
                self.target2['color'] = PROTON_COLOR # Turns RED
                
                # Emit Electron 2
                self.betas.append({
                    'x': self.target2['x'], 
                    'y': self.target2['y'], 
                    'vx': -0.2, 'vy': 0.1 # Fly away different direction
                })
            
            self.label = "Plutonium-239"
            self.sub = "94 Protons (The King)"
            
            # Move betas
            for b in self.betas:
                b['x'] += b['vx']
                b['y'] += b['vy']

        # 2. Draw Nucleus
        for p in self.particles:
            c = Circle((p['x'], p['y']), 0.45, 
                       facecolor=p['color'], edgecolor='black', linewidth=1)
            ax.add_patch(c)
            
        # 3. Draw Incoming (if visible)
        if t < 100:
            c = Circle((self.incoming['x'], self.incoming['y']), 0.45, 
                       facecolor=self.incoming['color'], edgecolor='black', linewidth=1)
            ax.add_patch(c)
        elif t >= 100:
            # Drawn as part of nucleus now? 
            # Or just statically drawn where it landed
            c = Circle((self.incoming['x'], self.incoming['y']), 0.45, 
                       facecolor=NEUTRON_COLOR, edgecolor='black', linewidth=1)
            ax.add_patch(c)

        # 4. Draw Betas (Sparks)
        for b in self.betas:
            # Draw as Star or small yellow dot
            c = Circle((b['x'], b['y']), 0.2, facecolor=BETA_COLOR, zorder=10)
            ax.add_patch(c)
            # Speed lines?
            
        # 5. Typography
        ax.text(0, -6, self.label, ha='center', fontsize=28, fontweight='bold', fontfamily='sans-serif')
        ax.text(0, -7.5, self.sub, ha='center', fontsize=18, color="#555555", fontfamily='sans-serif')

        # Scale
        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)
        ax.set_aspect('equal')
        
        # Save
        out_dir = "logic_garden_alchemy_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"alchemy_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Performing Alchemy...")
    
    sim = NucleusSim()
    
    for i in range(TOTAL_FRAMES):
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.render(i, ax)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
