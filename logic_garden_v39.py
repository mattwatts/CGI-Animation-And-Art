"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v39_fixed.py
MODE:   Nursery (Cosmic Forge Palette)
TARGET: Supernova (Core Collapse & Nucleosynthesis)
STYLE:  "The Cosmic Forge" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Rectangle # FIXED: Added Rectangle
import os

# --- 1. THE FORGE PALETTE ---
BG_COLOR = "#050005"        # Deep Space
STAR_CORE = "#FFA500"       # Solar Orange
STAR_OUTER = "#FF4500"      # Red Giant Edge
IRON_HEART = "#505050"      # Dead Iron
SHOCKWAVE = "#9D00FF"       # High Energy UV
NEUTRINO_FLASH = "#FFFFFF"  # Burst
ELEMENT_GOLD = "#FFD700"    # Au
ELEMENT_SILVER = "#C0C0C0"  # Ag
ELEMENT_OXYGEN = "#00FFFF"  # O

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class Particle:
    def __init__(self, x, y, v_mag, color):
        angle = np.random.uniform(0, 2*np.pi)
        self.x = x
        self.y = y
        self.vx = np.cos(angle) * v_mag * np.random.uniform(0.8, 1.2)
        self.vy = np.sin(angle) * v_mag * np.random.uniform(0.8, 1.2)
        self.color = color
        self.life = 1.0
        self.size = np.random.uniform(0.1, 0.4)

class SupernovaSim:
    def __init__(self):
        self.state = 'fusion' # fusion, iron_poison, collapse, bounce, nebula
        self.radius = 3.0
        self.color_core = STAR_CORE
        self.timer = 0
        self.shock_radius = 0.0
        self.particles = []
        
        # Star surface noise
        self.noise_offset = 0.0
        
    def update(self, frame_idx):
        self.timer += 1
        
        # PHASE 1: FUSION (Red Giant)
        if self.state == 'fusion':
            # Breathe
            self.radius = 3.0 + 0.1 * np.sin(frame_idx * 0.2)
            self.color_core = STAR_CORE
            
            # Transition to Iron Core at frame 60
            if frame_idx > 60:
                self.state = 'iron_poison'
        
        # PHASE 2: IRON POISON (Turn Grey)
        elif self.state == 'iron_poison':
            self.color_core = IRON_HEART
            self.radius = 3.0 # Stop breathing
            
            # Brief pause to realize what happened
            if frame_idx > 90:
                self.state = 'collapse'
                
        # PHASE 3: COLLAPSE (Freefall)
        elif self.state == 'collapse':
            # Exponential decay
            self.radius *= 0.6
            
            if self.radius < 0.2:
                self.state = 'bounce'
                self.radius = 0.1
                
        # PHASE 4: BOUNCE (Explosion)
        elif self.state == 'bounce':
            # 1 Frame trigger
            self.shock_radius = 0.2
            self.radius = 0.1
            
            # Spawn Elements
            count = 800
            for i in range(count):
                # Element Distribution
                r = np.random.rand()
                if r < 0.1: c = ELEMENT_GOLD   # 10% Gold
                elif r < 0.3: c = ELEMENT_SILVER # 20% Silver
                elif r < 0.6: c = ELEMENT_OXYGEN # 30% Oxygen
                else: c = SHOCKWAVE            # Remainder Energy
                
                speed = 0.3 if c == SHOCKWAVE else np.random.uniform(0.1, 0.3)
                self.particles.append(Particle(0, 0, speed, c))
            
            self.state = 'nebula'
            
        # PHASE 5: NEBULA (Expansion)
        elif self.state == 'nebula':
            # Expand Shockwave
            self.shock_radius += 0.4
            
            # Move Particles
            for p in self.particles:
                p.x += p.vx
                p.y += p.vy
                
                # Drag (Nebula Friction)
                p.vx *= 0.98
                p.vy *= 0.98
                
                # Fade shockwave particles faster
                if p.color == SHOCKWAVE:
                    p.life -= 0.02
                else:
                    p.life -= 0.005
                    
            self.particles = [p for p in self.particles if p.life > 0]

    def render(self, frame_idx, ax):
        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)
        
        # 1. The Star (Pre-Explosion)
        if self.state in ['fusion', 'iron_poison', 'collapse']:
            # Halo
            if self.state == 'fusion':
                ax.add_patch(Circle((0,0), self.radius*1.2, color=STAR_OUTER, alpha=0.3))
            
            # Core
            ax.add_patch(Circle((0,0), self.radius, color=self.color_core, zorder=10))
            
            # Text
            if self.state == 'fusion':
                lbl = "STATUS: FUSING (H -> He)"
                col = STAR_CORE
            elif self.state == 'iron_poison':
                lbl = "STATUS: IRON POISONING"
                col =IRON_HEART
            else:
                lbl = "STATUS: GRAVITATIONAL COLLAPSE"
                col = "#FF0000"
                
            ax.text(0, -7, lbl, color=col, ha='center', fontfamily='monospace',
                   bbox=dict(facecolor='black', edgecolor=col))
                   
        # 2. The Explosion
        if self.state == 'nebula':
            # The Flash (Neutrinos) uses RECTANGLE (Now Imported)
            flash_alpha = max(0, 1.0 - (self.shock_radius / 10.0))
            if flash_alpha > 0:
                ax.add_patch(Rectangle((-10,-10), 20, 20, color=NEUTRINO_FLASH, alpha=flash_alpha*0.5, zorder=0))
            
            # The Shockwave Ring
            sw = Circle((0,0), self.shock_radius, color=SHOCKWAVE, fill=False, linewidth=5, alpha=flash_alpha, zorder=5)
            ax.add_patch(sw)
            
            # The Heavy Elements (Debris)
            for p in self.particles:
                safe_alpha = max(0.0, min(1.0, p.life))
                ax.add_patch(Circle((p.x, p.y), p.size, color=p.color, alpha=safe_alpha, zorder=6))

            # The Neutron Star (Remnant)
            # A tiny pinprick of pure density left behind
            ax.add_patch(Circle((0,0), 0.1, color="#FFFFFF", zorder=20))
            ax.add_patch(Circle((0,0), 0.2, color="#00FFFF", alpha=0.5, zorder=19)) # Pulsar glow

            # Text
            ax.text(0, -7, "STATUS: NUCLEOSYNTHESIS (GOLD CREATED)", color=ELEMENT_GOLD, ha='center', fontfamily='monospace',
                   bbox=dict(facecolor='black', edgecolor=ELEMENT_GOLD))

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_supernova_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"supernova_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Igniting Star (Import Fixed)...")
    
    sim = SupernovaSim()
    
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
