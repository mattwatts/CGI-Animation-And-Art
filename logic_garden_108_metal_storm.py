"""
SOVEREIGN CODE: logic_garden_108_metal_storm.py
FORMAT: YouTube Shorts (1080x1920)
SCENE: Metal Storm (CIWS Lead Computing)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge
import matplotlib.patheffects as pe
import os
import math
import random

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_108_metal_storm"
os.makedirs(OUT_DIR, exist_ok=True)

# RESOLUTION
RES_W = 1080
RES_H = 1920

# PALETTE
C_BG      = '#050510'     # Deep Ocean/Night
C_TURRET  = '#DDDDDD'     # Phalanx White
C_BARREL  = '#444444'     # Gun Metal
C_MISSILE = '#FF3333'     # Threat Red
C_TRAIL   = '#AA2222'     # Missile Vapor
C_TRACER  = '#FFCC00'     # Tungsten Rounds (Gold/Orange)
C_CORE    = '#FFFFFF'     # Tracer Core
C_LEAD    = '#00FFFF'     # The Computed Solution (Cyan)
C_KILLBOX = '#00FFFF'     # The Wireframe Cage
C_HUD     = '#00FF00'     # Radar Green

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: return v
    return v / norm

class Threat:
    def __init__(self, uid, start_x):
        self.id = uid
        self.pos = np.array([start_x, 1100.0], dtype=float)
        
        # Target aims roughly at the ship (bottom center)
        # Add random jinking
        target_x = random.uniform(-200, 200)
        target_y = -900.0
        
        direction = np.array([target_x, target_y]) - self.pos
        self.vel = normalize(direction) * random.uniform(15, 20) # FAST
        
        self.alive = True
        self.history = []

    def update(self):
        if self.alive:
            self.pos += self.vel
            self.history.append(self.pos.copy())
            if len(self.history) > 8: self.history.pop(0)

class Projectile:
    def __init__(self, pos, vel):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.active = True
        self.age = 0
        
    def update(self):
        self.pos += self.vel
        self.age += 1
        if self.age > 40: self.active = False # Range limit

class Explosion:
    def __init__(self, pos):
        self.pos = pos
        self.age = 0
        self.max_age = 10
        self.active = True
    
    def update(self):
        self.age += 1
        if self.age > self.max_age: self.active = False

class CIWS:
    def __init__(self):
        self.pos = np.array([0.0, -800.0], dtype=float)
        self.angle = math.radians(90) # Pointing up
        self.ammo_speed = 60.0 # Very Fast
        self.fire_rate_counter = 0
        self.target_lead_pos = None # For visualization
        self.is_firing = False
        
    def get_lead_point(self, target):
        # Iterative approximation for Lead Computing
        # 1. Estimate time to hit current position
        dist = np.linalg.norm(target.pos - self.pos)
        t = dist / self.ammo_speed
        
        # 2. Predict future position
        future_pos = target.pos + (target.vel * t)
        
        # 3. Refine (Re-calculate time to future pos)
        dist_2 = np.linalg.norm(future_pos - self.pos)
        t_2 = dist_2 / self.ammo_speed
        final_pos = target.pos + (target.vel * t_2)
        
        return final_pos

    def update(self, threats, bullets):
        # 1. Acquire Target
        nearest = None
        min_dist = 2000
        
        valid_threats = [t for t in threats if t.alive and t.pos[1] > -800]
        
        for t in valid_threats:
            d = np.linalg.norm(t.pos - self.pos)
            if d < min_dist:
                min_dist = d
                nearest = t
        
        self.is_firing = False
        self.target_lead_pos = None
        
        if nearest:
            # Calculate Lead
            lead_point = self.get_lead_point(nearest)
            self.target_lead_pos = lead_point
            
            # Aim
            dx = lead_point[0] - self.pos[0]
            dy = lead_point[1] - self.pos[1]
            target_angle = math.atan2(dy, dx)
            
            # Slew Turret (Instant for this visual, or smooth?)
            # Let's make it snappy but mechanical
            self.angle = target_angle
            
            # Fire logic (Range check)
            if min_dist < 1600:
                self.is_firing = True
                # METAL STORM: Fire multiple rounds per frame
                for _ in range(3):
                    # Spread
                    spread = random.uniform(-0.02, 0.02)
                    fire_angle = self.angle + spread
                    vel = np.array([math.cos(fire_angle), math.sin(fire_angle)]) * self.ammo_speed
                    
                    # Offset muzzle
                    p = Projectile(self.pos + vel*0.5, vel)
                    bullets.append(p)
                    
def run():
    print(f"LOGIC GARDEN 108: METAL STORM ({TOTAL_FRAMES} frames)")
    
    ciws = CIWS()
    threats = []
    bullets = []
    explosions = []
    kill_boxes = [] # List of {pos, age} to draw the wireframe hits
    
    # TIMELINE
    # Waves of attacks
    
    for f in range(TOTAL_FRAMES):
        
        # --- SPAWN THREATS ---
        if f % 40 == 0 and f < 450:
            # Spawn logic
            x = random.choice([-500, -300, 0, 300, 500])
            # Add noise
            x += random.uniform(-50, 50)
            threats.append(Threat(len(threats), x))
            
        # --- UPDATE ---
        
        # CIWS
        ciws.update(threats, bullets)
        
        # Bullets
        active_bullets = []
        for b in bullets:
            b.update()
            if b.active: active_bullets.append(b)
        bullets = active_bullets
        
        # Threats & Collision
        # Brute force check (N*M) - OK for < 100 objs
        for t in threats:
            t.update()
            if t.alive:
                # Hitbox check
                hit = False
                for b in bullets:
                    if b.active:
                        dist = np.linalg.norm(b.pos - t.pos)
                        if dist < 40: # Hit radius
                            hit = True
                            b.active = False # Bullet spent
                            # Don't break, maybe multiple hits needed? 
                            # Let's say 1 hit kill for visual pop
                            break
                if hit:
                    t.alive = False
                    explosions.append(Explosion(t.pos))
                    kill_boxes.append({'pos': t.pos.copy(), 'age': 0})
        
        # Explosions
        active_ex = []
        for ex in explosions:
            ex.update()
            if ex.active: active_ex.append(ex)
        explosions = active_ex
        
        # Kill Boxes
        active_kb = []
        for kb in kill_boxes:
            kb['age'] += 1
            if kb['age'] < 5: active_kb.append(kb)
        kill_boxes = active_kb

        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        ax.set_xlim(-540, 540)
        ax.set_ylim(-960, 960)
        ax.set_facecolor(C_BG)
        
        # 1. GRID / HUD
        # Radar circles
        for r in [400, 800, 1200]:
            c = Circle((0, -800), r, fill=False, edgecolor=C_HUD, alpha=0.1, linewidth=2, linestyle='--')
            ax.add_patch(c)
            
        # 2. DRAW LEAD COMPUTING VISUALS
        if ciws.target_lead_pos is not None:
            # A. The Ghost Target (Where missile will be)
            ax.scatter(ciws.target_lead_pos[0], ciws.target_lead_pos[1], 
                       s=150, facecolors='none', edgecolors=C_LEAD, linewidth=2, linestyle='--', alpha=0.8)
            
            # B. The Solution Vector (Gun to Lead)
            ax.plot([ciws.pos[0], ciws.target_lead_pos[0]], 
                    [ciws.pos[1], ciws.target_lead_pos[1]],
                    color=C_LEAD, linewidth=1, linestyle=':', alpha=0.5)

        # 3. THREATS (Missiles)
        for t in threats:
            if t.alive:
                # Trail
                if len(t.history) > 1:
                    hx = [p[0] for p in t.history]
                    hy = [p[1] for p in t.history]
                    ax.plot(hx, hy, color=C_TRAIL, linewidth=4, alpha=0.6)
                
                # Body
                ax.scatter(t.pos[0], t.pos[1], c=C_MISSILE, s=80, marker='v', zorder=5)
                
                # Engine Flare
                ax.scatter(t.pos[0], t.pos[1]+20, c='white', s=30, alpha=0.8)

        # 4. BULLETS (The Stream)
        if len(bullets) > 0:
            # Vectorized draw for speed
            bx = [b.pos[0] for b in bullets]
            by = [b.pos[1] for b in bullets]
            
            # Draw Tracers as lines (using velocity)
            # We iterate to draw lines
            for b in bullets:
                tail = b.pos - (b.vel * 2.0) # Long tracers
                # Tracer Glow
                ax.plot([b.pos[0], tail[0]], [b.pos[1], tail[1]], 
                        color=C_TRACER, linewidth=3, alpha=0.9)
                # Core
                ax.plot([b.pos[0], tail[0]], [b.pos[1], tail[1]], 
                        color=C_CORE, linewidth=1, alpha=1.0)

        # 5. KILL BOXES (The Intercept)
        for kb in kill_boxes:
            # Wireframe box flashing
            sz = 100
            rect = Rectangle((kb['pos'][0]-sz/2, kb['pos'][1]-sz/2), sz, sz,
                             edgecolor=C_KILLBOX, facecolor='none', linewidth=4, zorder=20)
            ax.add_patch(rect)
            
            # Text tag
            ax.text(kb['pos'][0]+60, kb['pos'][1], "INTERCEPT", 
                    color=C_KILLBOX, fontsize=20, fontname='monospace', weight='bold')

        # 6. EXPLOSIONS
        for ex in explosions:
            r = ex.age * 8
            alpha = 1.0 - (ex.age / ex.max_age)
            if alpha < 0: alpha = 0
            
            c = Circle((ex.pos[0], ex.pos[1]), r, color='white', alpha=alpha, zorder=15)
            ax.add_patch(c)
            # Debris
            for i in range(5):
                dx = random.uniform(-50, 50)
                dy = random.uniform(-50, 50)
                ax.scatter(ex.pos[0]+dx, ex.pos[1]+dy, c='orange', s=20*alpha)

        # 7. CIWS TURRET
        # Base
        ax.add_patch(Circle((ciws.pos[0], ciws.pos[1]), 60, color=C_TURRET, zorder=10))
        # Gun Barrel Block (Rect rotated by angle)
        # Setup transformation
        barrel_len = 100
        barrel_w = 40
        rect_b = Rectangle((ciws.pos[0]-barrel_w/2, ciws.pos[1]), barrel_w, barrel_len, color=C_BARREL, zorder=9)
        
        t = matplotlib.transforms.Affine2D().rotate_around(ciws.pos[0], ciws.pos[1], ciws.angle - math.pi/2) + ax.transData
        rect_b.set_transform(t)
        ax.add_patch(rect_b)
        
        # Muzzle Flash
        if ciws.is_firing:
            mx = ciws.pos[0] + math.cos(ciws.angle)*110
            my = ciws.pos[1] + math.sin(ciws.angle)*110
            # Jagged flash
            flash_sz = random.uniform(80, 120)
            c_flash = Circle((mx, my), flash_sz, color='white', alpha=0.8, zorder=11)
            ax.add_patch(c_flash)


        # 8. UI
        stroke = [pe.withStroke(linewidth=4, foreground="black")]
        
        ax.text(0, 880, "METAL STORM (CIWS)", color=C_TURRET, ha='center',
                fontsize=35, fontname='monospace', weight='bold', path_effects=stroke)
        
        if ciws.is_firing:
             ax.text(0, -900, "ENGAGING THREAT", color=C_TRACER, ha='center',
                    fontsize=40, fontname='monospace', weight='bold', path_effects=stroke)
        else:
             ax.text(0, -900, "RADAR SCANNING", color=C_HUD, ha='center',
                    fontsize=25, fontname='monospace', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
