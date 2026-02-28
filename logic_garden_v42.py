
"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v42_fixed.py
MODE:   Nursery (Magma Palette)
TARGET: Earth-Theia Collision (Moon Formation)
STYLE:  "The Big Splash" | Time-Dilated | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
import os
import shutil

# --- 1. THE MAGMA PALETTE ---
BG_COLOR = "#050505"
GAIA_CORE = "#FF4500"       # Molten Earth
THEIA_CORE = "#8B0000"      # Dark Red Planet
DEBRIS_HOT = "#FFFF00"      # White Hot
DEBRIS_COOL = "#808080"     # Cooling Ash
MOON_BASE = "#D0D0D0"       # The Result
ROCHE_LINE = "#00FFFF"      # The Math Limit

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class Particle:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = 1.0
        self.heat = 1.0 
        self.captured = False

class ImpactSim:
    def __init__(self):
        self.gaia_r = 2.5
        self.gaia_pos = np.array([0.0, 0.0])
        
        # Start Theia much further away for dramatic approach
        self.theia_r = 1.2
        self.theia_pos = np.array([-9.0, 6.0]) 
        self.theia_vel = np.array([0.06, -0.04]) # Slow motion approach
        
        self.particles = []
        
        self.moon_r = 0.05
        self.moon_pos = np.array([5.0, 0.0])
        self.moon_active = False
        
        self.phase = 'approach'
        self.timer = 0
        self.screen_shake = 0.0
        
    def update(self, frame_idx):
        self.timer += 1
        
        # --- PHASE 1: THE APPROACH ---
        if self.phase == 'approach':
            self.theia_pos += self.theia_vel
            
            # Distance check
            dist = np.linalg.norm(self.theia_pos - self.gaia_pos)
            
            # Trigger impact when close
            if dist < (self.gaia_r + self.theia_r) * 0.85:
                self.phase = 'impact'
                self.screen_shake = 2.0
                self.timer = 0 # Reset timer for phase duration

        # --- PHASE 2: THE IMPACT ---
        elif self.phase == 'impact':
            self.screen_shake *= 0.95
            
            # Move Theia INTO Earth (don't stop)
            self.theia_pos += self.theia_vel * 0.5
            
            # Dissolve Theia slowly (takes ~150 frames)
            self.theia_r *= 0.98
            self.gaia_r = min(3.0, self.gaia_r * 1.0005) # Earth swells
            
            # Continuous Debris Spray
            if self.theia_r > 0.1:
                for _ in range(10): # Spray particles
                    angle = np.random.uniform(-np.pi, np.pi)
                    speed = np.random.uniform(0.2, 0.8)
                    
                    # Particles explode from the contact point
                    # Contact point is between Earth and Theia
                    direction = self.theia_pos - self.gaia_pos
                    direction /= np.linalg.norm(direction)
                    contact = self.gaia_pos + direction * self.gaia_r * 0.8
                    
                    vx = np.cos(angle) * speed + self.theia_vel[0]
                    vy = np.sin(angle) * speed + self.theia_vel[1]
                    
                    self.particles.append(Particle(contact[0], contact[1], vx, vy))
            
            if self.theia_r < 0.1:
                self.phase = 'ring'
                self.timer = 0

        # --- PHASE 3: THE RING ---
        elif self.phase == 'ring':
            self.screen_shake = 0.0
            
            # Wait for debris to stabilize before forming moon
            # Particles orbit
            if self.timer > 100:
                self.phase = 'accretion'
                self.moon_active = True
                
                # Place Moon seed in the thickest part of debris
                # Usually lagrange point or just orbit
                self.moon_pos = np.array([3.5, 0.0])
                self.moon_vel = np.array([0.0, 0.18]) # Orbital speed

        # --- PHASE 4: ACCRETION ---
        elif self.phase == 'accretion':
            # Moon Orbit
            r_vec = self.moon_pos - self.gaia_pos
            r_dist = np.linalg.norm(r_vec)
            force_mag = 0.8 / (r_dist**2) # Gravity
            acc = -r_vec / r_dist * force_mag
            self.moon_vel += acc
            self.moon_pos += self.moon_vel
            
            # Grow moon if it sweeps particles (Logic below)

        # --- GLOBAL PARTICLE PHYSICS ---
        for p in self.particles:
            if p.captured: continue
            
            # Gravity from Earth
            dx = p.x - self.gaia_pos[0]
            dy = p.y - self.gaia_pos[1]
            dist = np.sqrt(dx*dx + dy*dy)
            
            # Force
            f = 0.08 / (dist*dist)
            p.vx -= (dx/dist) * f
            p.vy -= (dy/dist) * f
            
            # Drag (Simulate gas cloud friction)
            p.vx *= 0.995
            p.vy *= 0.995
            
            p.x += p.vx
            p.y += p.vy
            
            # Cooling
            p.heat *= 0.992
            
            # Collision Earth
            if dist < self.gaia_r:
                p.captured = True
            
            # Accretion by Moon
            if self.moon_active:
                mdx = p.x - self.moon_pos[0]
                mdy = p.y - self.moon_pos[1]
                mdist = np.sqrt(mdx*mdx + mdy*mdy)
                
                # Hit moon?
                if mdist < self.moon_r + 0.3:
                    p.captured = True
                    self.moon_r += 0.002 # Grow

        self.particles = [p for p in self.particles if not p.captured]

    def render(self, frame_idx, ax):
        # Shake
        sx, sy = 0, 0
        if self.screen_shake > 0:
            sx = np.random.uniform(-0.1, 0.1) * self.screen_shake
            sy = np.random.uniform(-0.1, 0.1) * self.screen_shake
            
        ax.set_xlim(-8+sx, 8+sx)
        ax.set_ylim(-8+sy, 8+sy)
        
        # 1. Roche Limit
        ax.add_patch(Circle((0,0), 3.5, color=ROCHE_LINE, fill=False, linestyle='--', alpha=0.2))
        
        # 2. Particles (Debris first so planet is on top or bottom?)
        # Debris should be behind Moon, in front of Earth?
        x_hot, y_hot = [], []
        x_cool, y_cool = [], []
        for p in self.particles:
            if p.heat > 0.3:
                x_hot.append(p.x)
                y_hot.append(p.y)
            else:
                x_cool.append(p.x)
                y_cool.append(p.y)
        
        if x_cool: ax.scatter(x_cool, y_cool, color=DEBRIS_COOL, s=10, marker='.', zorder=4)
        if x_hot: ax.scatter(x_hot, y_hot, color=DEBRIS_HOT, s=15, marker='.', zorder=5)

        # 3. Earth
        ax.add_patch(Circle(self.gaia_pos, self.gaia_r, color=GAIA_CORE, zorder=6))
        # Atmosphere
        ax.add_patch(Circle(self.gaia_pos, self.gaia_r*1.1, color=GAIA_CORE, alpha=0.2, zorder=6))

        # 4. Theia
        if self.phase in ['approach', 'impact']:
            ax.add_patch(Circle(self.theia_pos, self.theia_r, color=THEIA_CORE, zorder=7))

        # 5. Moon
        if self.moon_active:
            ax.add_patch(Circle(self.moon_pos, self.moon_r, color=MOON_BASE, zorder=10))
            # Text label attached to moon
            ax.text(self.moon_pos[0], self.moon_pos[1]+0.5, "LUNA", color="white", fontsize=8, ha='center')

        # 6. HUD
        if self.phase == 'approach': 
            status = "PHASE 1: THEIA APPROACH"
            col = Theme.WHITE
        elif self.phase == 'impact':
            status = "PHASE 2: LIQUEFACTION"
            col = Theme.RED
        elif self.phase == 'ring':
            status = "PHASE 3: THE RING (ROCHE LIMIT)"
            col = Theme.YELLOW
        else:
            status = "PHASE 4: ACCRETION"
            col = Theme.GREY
            
        ax.text(0, 7, status, color="white", ha='center', fontfamily='monospace', fontsize=14,
               bbox=dict(facecolor='black', edgecolor='white'))
               
        ax.set_aspect('equal')
        ax.set_axis_off()
        
        # Output
        out_dir = "logic_garden_moon_frames_fixed"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"moon_fixed_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# Helper color class
class Theme:
    WHITE = "#FFFFFF"
    RED = "#FF0000"
    YELLOW = "#FFFF00"
    GREY = "#D0D0D0"

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Calculating Orbital Vectors...")
    
    sim = ImpactSim()
    
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
