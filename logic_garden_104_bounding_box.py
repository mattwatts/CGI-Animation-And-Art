"""
SOVEREIGN CODE: logic_garden_104_bounding_box.py
FORMAT: YouTube Shorts (1080x1920)
SCENE: The Bounding Box (Structure creates Strength)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import matplotlib.patheffects as pe
import os
import random
import math

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_104_bounding"
os.makedirs(OUT_DIR, exist_ok=True)

# RESOLUTION
RES_W = 1080
RES_H = 1920

# PALETTE
C_BG      = '#050510'
C_CHAOS   = '#666677'     # Grey Dust
C_ORDER   = '#FFD700'     # Gold Lattice
C_BOX     = '#00FFFF'     # The Constraint (Cyan)
C_GRID    = '#111122'

class Particle:
    def __init__(self, uid, target_pos):
        self.id = uid
        # Start random
        self.pos = np.array([random.uniform(-500, 500), random.uniform(-500, 500)])
        self.vel = np.array([random.uniform(-4, 4), random.uniform(-4, 4)])
        self.target = np.array(target_pos)
        self.state = "CHAOS" # CHAOS, TRANSITION, CRYSTAL
        
    def update(self, dt, box_dims, influence):
        """
        dt: time step
        box_dims: [width, height] of the bounding box (centered at 0,0)
        influence: 0.0 (Chaos) to 1.0 (Crystal Force)
        """
        w, h = box_dims
        hw = w / 2.0
        hh = h / 2.0
        
        # 1. PHYSICS
        if influence < 0.1:
            # Pure Brownian Motion
            self.pos += self.vel
            
            # Wrap around screen (Entropy)
            if self.pos[0] > 540: self.pos[0] -= 1080
            if self.pos[0] < -540: self.pos[0] += 1080
            if self.pos[1] > 960: self.pos[1] -= 1920
            if self.pos[1] < -960: self.pos[1] += 1920
            
        else:
            # 2. CONSTRAINED OPTIMIZATION
            
            # A. Wall Forces (The Bounding Box)
            # Push inward if outside box
            force = np.array([0.0, 0.0])
            
            if self.pos[0] > hw: force[0] -= (self.pos[0] - hw) * 2.0
            if self.pos[0] < -hw: force[0] -= (self.pos[0] + hw) * 2.0
            if self.pos[1] > hh: force[1] -= (self.pos[1] - hh) * 2.0
            if self.pos[1] < -hh: force[1] -= (self.pos[1] + hh) * 2.0
            
            # B. Lattice Force (Crystallization)
            # As influence grows, particles seek their "Optimal Slot"
            to_target = self.target - self.pos
            force += to_target * influence * 2.0
            
            # C. Damping (Friction)
            # Stabilize the crystal
            force -= self.vel * influence * 1.5
            
            # Integrate
            self.vel += force * dt
            self.pos += self.vel * dt

def generate_lattice(n):
    """ Generate a nice hexagonal/grid layout for N particles """
    points = []
    # Approx grid size
    cols = int(math.sqrt(n)) 
    rows = math.ceil(n / cols)
    
    spacing = 60
    
    offset_x = (cols * spacing) / 2
    offset_y = (rows * spacing) / 2
    
    for i in range(n):
        r = i // cols
        c = i % cols
        
        x = (c * spacing) - offset_x + (spacing/2)
        y = (r * spacing) - offset_y + (spacing/2)
        
        # Offset odd rows for hex look
        if r % 2 == 0:
            x += spacing / 2
            
        points.append([x, y])
    return points

def run():
    print(f"LOGIC GARDEN 104: THE BOUNDING BOX ({TOTAL_FRAMES} frames)")
    
    # 1. SETUP
    count = 100
    lattice_pts = generate_lattice(count)
    particles = [Particle(i, lattice_pts[i]) for i in range(count)]
    
    # BOX ANIMATION
    max_box = [1200, 2000] # Full screen
    min_box = [700, 700]   # Tight constraint
    
    for f in range(TOTAL_FRAMES):
        
        # --- TIMELINE LOGIC ---
        
        # 0 - 90: CHAOS (No Box)
        # 90 - 200: THE CONSTRAINT (Box Appears & Shrinks)
        # 200 - 450: CRYSTALLIZATION (Hold)
        # 450 - 600: THE RELEASE (Box Vanishes, Structure Holds)
        
        box_w, box_h = max_box
        influence = 0.0
        draw_box = False
        box_alpha = 0.0
        
        if f < 90:
            influence = 0.0
            draw_box = False
            
        elif f >= 90 and f < 200:
            draw_box = True
            t = (f - 90) / 110.0 # 0 to 1
            # Ease out
            t = t * (2 - t)
            
            # Lerp Dimensions
            box_w = max_box[0] + (min_box[0] - max_box[0]) * t
            box_h = max_box[1] + (min_box[1] - max_box[1]) * t
            
            # Ramp Influence
            influence = t * 0.8
            box_alpha = min(1.0, t * 2.0)
            
        elif f >= 200 and f < 450:
            draw_box = True
            box_w, box_h = min_box
            influence = 1.0 # Full Lock
            box_alpha = 1.0
            
        elif f >= 450:
            # RELEASE
            draw_box = True
            box_w, box_h = min_box
            influence = 1.0 # Keep struct force, or release it?
            # release force slightly to show stability
            # Actually, "The Release" means we remove the external box
            # but the internal structure holds because they are "trained".
            # In code, we keep the Lattice Force (Internal Values) but hide the Wall Force.
            
            # Visual fade out of box
            t_fade = (f - 450) / 60.0
            if t_fade > 1: t_fade = 1
            box_alpha = 1.0 - t_fade
            if box_alpha < 0: 
                box_alpha = 0
                draw_box = False
                
        # --- PHYSICS ---
        # Pass current box dimensions to update
        for p in particles:
            p.update(0.2, [box_w, box_h], influence)
            
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        ax.set_xlim(-540, 540)
        ax.set_ylim(-960, 960)
        ax.set_facecolor(C_BG)
        
        # 1. BACKGROUND GRID
        for i in range(-500, 600, 200):
            ax.axvline(i, color=C_GRID, linewidth=2)
            ax.axhline(i, color=C_GRID, linewidth=2)
            
        # 2. DRAW BOX
        if draw_box or box_alpha > 0:
            rect = Rectangle((-box_w/2, -box_h/2), box_w, box_h, 
                             fill=False, edgecolor=C_BOX, linewidth=5, alpha=box_alpha)
            ax.add_patch(rect)
            
            # Box Label
            if box_alpha > 0.5:
                ax.text(-box_w/2 + 20, box_h/2 + 20, "CONSTRAINT: ACTIVE", 
                        color=C_BOX, fontsize=15, fontname='monospace', alpha=box_alpha)

        # 3. DRAW PARTICLES
        # Dynamic Color: Grey -> Gold
        # Based on influence
        
        # Draw Connections if crystallized (Lattice lines)
        if influence > 0.8:
            # Draw lines between close neighbors for that "Crystal" look
            # Industrial Hack: Just draw lines to target neighbors in lattice list
            # Too expensive to compute all pairs.
            # Simplified: Use Alpha Gold Glow
            pass

        for p in particles:
            # Color
            if influence < 0.2:
                col = C_CHAOS
                sz = 40
                glow = False
            else:
                # Lerp to Gold
                col = C_ORDER
                sz = 40
                glow = True
                
            ax.scatter(p.pos[0], p.pos[1], c=col, s=sz, zorder=10)
            
            if glow and random.random() < 0.1: # Sparkle effect
                ax.scatter(p.pos[0], p.pos[1], c='white', s=10, zorder=12)

        # 4. UI TEXT
        stroke = [pe.withStroke(linewidth=4, foreground="black")]
        
        if f < 90:
            ax.text(0, 800, "ENTROPY", color=C_CHAOS, ha='center', fontsize=40, fontname='monospace', weight='bold', path_effects=stroke)
            ax.text(0, 750, "(Runtime Chaos)", color=C_CHAOS, ha='center', fontsize=25, fontname='monospace', path_effects=stroke)
            
        elif f > 200 and box_alpha > 0.8:
            ax.text(0, 800, "STRUCTURE", color=C_BOX, ha='center', fontsize=40, fontname='monospace', weight='bold', path_effects=stroke)
            ax.text(0, 750, "(Optimization)", color=C_BOX, ha='center', fontsize=25, fontname='monospace', path_effects=stroke)

            ax.text(0, -600, "BUILD THE WALLS", color=C_BOX, ha='center', fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)
            
        elif f > 450:
            ax.text(0, 800, "ROBUSTNESS", color=C_ORDER, ha='center', fontsize=40, fontname='monospace', weight='bold', path_effects=stroke)
            ax.text(0, 750, "(Compile-Time Safety)", color=C_ORDER, ha='center', fontsize=25, fontname='monospace', path_effects=stroke)
            
            ax.text(0, -600, "THE STRUCTURE HOLDS", color=C_ORDER, ha='center', fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
