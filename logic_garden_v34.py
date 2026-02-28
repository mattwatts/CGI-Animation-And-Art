"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v34.py
MODE:   Nursery (High Energy Physics Palette)
TARGET: Large Hadron Collider (Beam Crossing & Decay Tracks)
STYLE:  "The God Machine" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge
import os

# --- 1. THE PHYSICS PALETTE ---
BG_COLOR = "#080810"        # Tunnel Dark
MAGNET_BLUE = "#0047AB"     # Cryogenic Liquid Helium
BEAM_PIPE = "#404040"       # Steel Vacuum Pipe
BEAM_1 = "#FFD700"          # Proton A (Gold)
BEAM_2 = "#00FFFF"          # Proton B (Cyan)
COLLISION_FLASH = "#FFFFFF" # Pure Energy
TRACK_MUON = "#39FF14"      # Neon Green (Long tracks)
TRACK_ELECTRON = "#FF0040"  # Red (Short curved)
TRACK_HADRON = "#1E90FF"    # Blue (Jets)

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
RING_RADIUS = 3.5

class ParticleTrack:
    def __init__(self, x, y, p_type):
        self.x = x
        self.y = y
        self.type = p_type
        self.life = 1.0
        
        # Random initial velocity vector (Explosion)
        angle = np.random.uniform(0, 2*np.pi)
        speed = np.random.uniform(0.2, 0.8)
        
        self.vx = np.cos(angle) * speed
        self.vy = np.sin(angle) * speed
        
        # Curvature (Magnetic Field B=4 Tesla)
        # q/m ratio affects curvature.
        if p_type == 'muon':
            self.curve = np.random.uniform(-0.02, 0.02) # Stiff track
            self.decay = 0.02 # Lasts long
        elif p_type == 'electron':
            self.curve = np.random.uniform(-0.15, 0.15) # Spirals
            self.decay = 0.05 # Stops fast
        else: # Hadron
            self.curve = np.random.uniform(-0.05, 0.05)
            self.decay = 0.04
            
        self.trail = [] # History for drawing lines

    def update(self):
        # Move
        self.x += self.vx
        self.y += self.vy
        
        # Apply Magnetic Force (Turn velocity vector)
        # Rotate [vx, vy] by curve angle
        c, s = np.cos(self.curve), np.sin(self.curve)
        nvx = self.vx * c - self.vy * s
        nvy = self.vx * s + self.vy * c
        self.vx, self.vy = nvx, nvy
        
        # Store trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10: self.trail.pop(0)
        
        # Die
        self.life -= self.decay

class LHCSim:
    def __init__(self):
        self.beam_energy = 0.0 # 0 to 13 TeV
        self.bunch_angle_1 = 0.0 # CW
        self.bunch_angle_2 = np.pi # CCW (Start opposite)
        
        self.tracks = []
        self.collision_flash = 0.0
        
    def update(self, frame_idx):
        # 1. Accelerate Beams (Ramp)
        target_energy = 13.0 # TeV
        if self.beam_energy < target_energy:
            self.beam_energy += 0.05
            
        # Speed relates to Energy (Relativistic, but visually just rotate faster)
        # Base speed + Energy boost
        speed = 0.1 + (self.beam_energy / 13.0) * 0.4
        
        self.bunch_angle_1 -= speed # CW
        self.bunch_angle_2 += speed # CCW
        
        # Normalize angles 0-2pi
        self.bunch_angle_1 %= (2*np.pi)
        self.bunch_angle_2 %= (2*np.pi)
        
        # 2. Check Collision at Interaction Points
        # Let's define the interaction point at 90 deg (Top, pi/2)
        # Check proximity to pi/2 for both beams
        
        # Simplified: Just trigger sporadic collisions when energy is high
        # Determine "Collision Phase"
        if self.beam_energy > 5.0:
            # Chance to collide every few frames
            if np.random.rand() < 0.2:
                self.trigger_collision()
                
        # 3. Update Tracks
        for t in self.tracks:
            t.update()
        self.tracks = [t for t in self.tracks if t.life > 0]
        
        # Flash fade
        self.collision_flash *= 0.8
        
    def trigger_collision(self):
        self.collision_flash = 1.0
        
        # Spawn particles at Interaction Point (0, RING_RADIUS)
        # Actually, let's put the detector in the center for better vis, 
        # or keep the ring logic?
        # Let's make the collision happen at the top of the ring (0, 3.5)
        
        cx, cy = 0, RING_RADIUS
        
        # Spawn showers
        count = int(self.beam_energy * 2) # More energy = More debris
        
        for _ in range(count):
            # Pick type
            r = np.random.rand()
            if r < 0.2: p_type = 'muon'
            elif r < 0.5: p_type = 'electron'
            else: p_type = 'hadron'
            
            self.tracks.append(ParticleTrack(cx, cy, p_type))


    def render(self, frame_idx, ax):
        ax.set_xlim(-6, 6)
        ax.set_ylim(-2, 10) # Shift view to focus on top half of ring
        
        # 1. The Tunnel / Pipe
        # Draw the ring
        ring = Circle((0,0), RING_RADIUS, color=BEAM_PIPE, fill=False, linewidth=25)
        ax.add_patch(ring)
        
        # Magnets (Dipoles)
        # Draw segments
        for i in range(12):
            ang = (i / 12) * 2 * np.pi
            # Don't draw over the Interaction Point at top
            if abs(ang - np.pi/2) < 0.3: continue
            
            mx = RING_RADIUS * np.cos(ang)
            my = RING_RADIUS * np.sin(ang)
            
            # Box representation of cryostat
            # Rotation logic?
            # Simple circles for now acting as quadrupole/dipole nodes
            ax.add_patch(Circle((mx, my), 0.6, color=MAGNET_BLUE, zorder=2))
            ax.add_patch(Circle((mx, my), 0.4, color="black", zorder=3)) # Bore
            
        # 2. The Beams (Bunches)
        # Beam 1
        b1x = RING_RADIUS * np.cos(self.bunch_angle_1)
        b1y = RING_RADIUS * np.sin(self.bunch_angle_1)
        ax.add_patch(Circle((b1x, b1y), 0.3, color=BEAM_1, zorder=5))
        # Trail
        for k in range(5):
            lag = (k+1)*0.1
            tx = RING_RADIUS * np.cos(self.bunch_angle_1 + lag)
            ty = RING_RADIUS * np.sin(self.bunch_angle_1 + lag)
            ax.add_patch(Circle((tx, ty), 0.2 - k*0.03, color=BEAM_1, alpha=0.5 - k*0.1))
            
        # Beam 2
        b2x = RING_RADIUS * np.cos(self.bunch_angle_2)
        b2y = RING_RADIUS * np.sin(self.bunch_angle_2)
        ax.add_patch(Circle((b2x, b2y), 0.3, color=BEAM_2, zorder=5))
        # Trail
        for k in range(5):
            lag = (k+1)*0.1
            tx = RING_RADIUS * np.cos(self.bunch_angle_2 - lag)
            ty = RING_RADIUS * np.sin(self.bunch_angle_2 - lag)
            ax.add_patch(Circle((tx, ty), 0.2 - k*0.03, color=BEAM_2, alpha=0.5 - k*0.1))

        # 3. The Particle Shower (Tracks)
        for t in self.tracks:
            # Color based on type
            if t.type == 'muon': c = TRACK_MUON
            elif t.type == 'electron': c = TRACK_ELECTRON
            else: c = TRACK_HADRON
            
            # Draw trail line
            if len(t.trail) > 1:
                pts = np.array(t.trail)
                ax.plot(pts[:,0], pts[:,1], color=c, linewidth=1.5, alpha=t.life)
            
            # Head
            ax.add_patch(Circle((t.x, t.y), 0.05, color="white", alpha=t.life))
            
        # 4. Collision Flash
        if self.collision_flash > 0.05:
            # Interaction Poin is (0, RING_RADIUS)
            ax.add_patch(Circle((0, RING_RADIUS), 1.5 * self.collision_flash, color=COLLISION_FLASH, alpha=self.collision_flash, zorder=20))
            
        # 5. HUD
        energy_disp = f"ENERGY: {self.beam_energy:05.2f} TeV"
        status = "INJECTING"
        if self.beam_energy > 3: status = "RAMPING"
        if self.beam_energy > 12: status = "COLLISIONS STABLE"
        
        info = f"{status}\n{energy_disp}"
        ax.text(0, -1, info, color=BEAM_1, ha='center', fontfamily='monospace', fontsize=12,
                bbox=dict(facecolor='black', edgecolor=BEAM_1))

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_lhc_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"lhc_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Injecting Protons...")
    
    sim = LHCSim()
    
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
