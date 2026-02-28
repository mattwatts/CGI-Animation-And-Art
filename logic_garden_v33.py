"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v33.py
MODE:   Nursery (Cosmic Noir Palette)
TARGET: Hawking Radiation (Quantum Fluctuations / Evaporation)
STYLE:  "The Quantum Thief" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os

# --- 1. THE COSMIC PALETTE ---
BG_COLOR = "#050510"        # Deep Indigo Void
EVENT_HORIZON = "#000000"   # Vantablack
PHOTON_SPHERE = "#002FA7"   # International Klein Blue
PARTICLE_REAL = "#00FFFF"   # Electric Cyan (Escaping)
PARTICLE_ANTI = "#FF0040"   # Ruby Red (Falling)
ENTANGLEMENT = "#404040"    # Grey Bond

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class QuantumPair:
    def __init__(self, r_spawn):
        # Spawn at random angle near horizon
        theta = np.random.uniform(0, 2*np.pi)
        
        # Position 1 (Matter)
        self.x1 = r_spawn * np.cos(theta)
        self.y1 = r_spawn * np.sin(theta)
        
        # Position 2 (Anti-Matter) - tiny offset
        offset = 0.2
        self.x2 = self.x1 + np.random.uniform(-offset, offset)
        self.y2 = self.y1 + np.random.uniform(-offset, offset)
        
        # Velocities (Brownian Motion initially)
        self.vx1 = np.random.uniform(-0.1, 0.1)
        self.vy1 = np.random.uniform(-0.1, 0.1)
        self.vx2 = -self.vx1 # Newton's law checks out
        self.vy2 = -self.vy1
        
        self.state = 'fluctuating' # fluctuating, separated, annihilated
        self.life = 1.0 # Frames to live before annihilation

class BlackHoleSim:
    def __init__(self):
        self.radius = 4.0        # Event Horizon Radius
        self.mass = 100.0        # Arbitrary mass unit
        self.pairs = []
        self.radiation_particles = [] # The survivors
        
    def update(self, frame_idx):
        # 1. Spawn Fluctuations
        # Spawn near the horizon (r = 4.0)
        # We spawn between 3.5 and 5.0
        if frame_idx % 2 == 0:
            spawn_r = self.radius + np.random.uniform(-0.5, 1.0)
            self.pairs.append(QuantumPair(spawn_r))
            
        # 2. Update Pairs
        for p in self.pairs:
            if p.state == 'annihilated': continue
            
            # GRAVITY
            # Pulls everything in
            for pid in [1, 2]:
                if pid == 1: x, y, vx, vy = p.x1, p.y1, p.vx1, p.vy1
                else:        x, y, vx, vy = p.x2, p.y2, p.vx2, p.vy2
                
                dist_sq = x*x + y*y
                dist = np.sqrt(dist_sq)
                
                # Gravity Force F = G/r^2
                # But careful not to divide by zero
                force = 0.5 / max(0.1, dist_sq)
                
                # Vector to center
                dx = -x / dist
                dy = -y / dist
                
                # Add Force to Vel
                vx += dx * force
                vy += dy * force
                
                # Quantum Jitter (Heisenberg Uncertainty)
                vx += np.random.uniform(-0.05, 0.05)
                vy += np.random.uniform(-0.05, 0.05)
                
                # Apply
                x += vx
                y += vy
                
                if pid == 1: p.x1, p.y1, p.vx1, p.vy1 = x, y, vx, vy
                else:        p.x2, p.y2, p.vx2, p.vy2 = x, y, vx, vy

            # CHECK SEPARATION (The Hawking Process)
            d1 = np.sqrt(p.x1**2 + p.y1**2)
            d2 = np.sqrt(p.x2**2 + p.y2**2)
            
            bh_r = self.radius
            
            # Condition: One Inside, One Outside
            cond1 = (d1 < bh_r and d2 > bh_r)
            cond2 = (d2 < bh_r and d1 > bh_r)
            
            if (cond1 or cond2) and p.state == 'fluctuating':
                # SEPARATION EVENT!
                p.state = 'separated'
                
                # Identify Survivor vs Victim
                if d1 > bh_r: 
                    survivor = {'x': p.x1, 'y': p.y1, 'vx': p.vx1, 'vy': p.vy1}
                    victim_idx = 2
                else: 
                    survivor = {'x': p.x2, 'y': p.y2, 'vx': p.vx2, 'vy': p.vy2}
                    victim_idx = 1
                    
                # Radiation is born!
                # Boost it OUTWARDS to conserve energy (The "Kick")
                # Normalize velocity outward
                mag = np.sqrt(survivor['x']**2 + survivor['y']**2)
                nx = survivor['x'] / mag
                ny = survivor['y'] / mag
                survivor['vx'] = nx * 0.3 # Escape velocity kick
                survivor['vy'] = ny * 0.3
                survivor['life'] = 1.0 # Alpha
                
                self.radiation_particles.append(survivor)
                
                # Black Hole Shrinks!
                self.radius *= 0.999 # Evaporation
                
            # If both inside -> Doomed (Just vanish)
            if d1 < bh_r and d2 < bh_r:
                p.state = 'annihilated'

            # If both outside and too old -> Annihilate (Vacuum fluctuation returns to nothing)
            # Distance between them
            sep = np.sqrt((p.x1-p.x2)**2 + (p.y1-p.y2)**2)
            if sep > 1.0 and p.state == 'fluctuating':
                p.state = 'annihilated' # Snaps back
            
            # Drift too far without separation
            if d1 > bh_r + 2.0 and p.state == 'fluctuating':
                p.state = 'annihilated'

        # 3. Update Radiation (The Real Particles)
        for r in self.radiation_particles:
            r['x'] += r['vx']
            r['y'] += r['vy']
            # Friction/Fade
            r['life'] -= 0.01

        # Cleanup
        self.pairs = [p for p in self.pairs if p.state != 'annihilated' and p.state != 'separated']
        self.radiation_particles = [r for r in self.radiation_particles if r['life'] > 0]


    def render(self, frame_idx, ax):
        # Zoom camera slightly as hole shrinks
        view = 10.0
        ax.set_xlim(-view, view)
        ax.set_ylim(-view, view)
        
        # 1. The Black Hole (Event Horizon)
        # Glowing Ring (Photon Sphere)
        # Pulsing slightly
        pulse = 1.0 + 0.02 * np.sin(frame_idx * 0.2)
        ax.add_patch(Circle((0,0), self.radius * 1.5, color=PHOTON_SPHERE, alpha=0.1 * pulse))
        ax.add_patch(Circle((0,0), self.radius * 1.2, color=PHOTON_SPHERE, alpha=0.3))
        
        # The Void itself
        ax.add_patch(Circle((0,0), self.radius, color=EVENT_HORIZON, zorder=10))
        
        # 2. The Quantum Foam (Pairs)
        for p in self.pairs:
            # Draw Bond
            ax.plot([p.x1, p.x2], [p.y1, p.y2], color=ENTANGLEMENT, linewidth=0.5, alpha=0.5)
            
            # Draw Particles
            # Faint, ghost-like until they separate
            alpha = 0.4
            c1 = "#FFFFFF"
            c2 = "#FFFFFF"
            
            # Logic: If one is crossing horizon, color code them
            d1 = np.sqrt(p.x1**2 + p.y1**2)
            d2 = np.sqrt(p.x2**2 + p.y2**2)
            
            if d1 < self.radius + 0.5: c1 = PARTICLE_ANTI # Falling
            if d2 < self.radius + 0.5: c2 = PARTICLE_ANTI
            
            ax.add_patch(Circle((p.x1, p.y1), 0.08, color=c1, alpha=alpha, zorder=5))
            ax.add_patch(Circle((p.x2, p.y2), 0.08, color=c2, alpha=alpha, zorder=5))
            
        # 3. The Radiation (Escaped Real Particles)
        for r in self.radiation_particles:
            alpha = max(0, min(1.0, r['life']))
            ax.add_patch(Circle((r['x'], r['y']), 0.15, color=PARTICLE_REAL, alpha=alpha, zorder=20))
            # Trail
            ax.plot([r['x'] - r['vx']*2, r['x']], [r['y'] - r['vy']*2, r['y']], 
                   color=PARTICLE_REAL, linewidth=1, alpha=alpha*0.5)

        # 4. HUD
        mass_energy = int(self.radius * 25)
        info = f"MASS: {mass_energy}%\nSTATUS: EVAPORATING"
        ax.text(0, -9, info, color=PHOTON_SPHERE, ha='center', fontfamily='monospace',
                bbox=dict(facecolor='black', edgecolor=PHOTON_SPHERE, alpha=0.5))

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_hawking_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"hawking_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Collapsing Vacuum State...")
    
    sim = BlackHoleSim()
    
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
