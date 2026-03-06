"""
SOVEREIGN CODE: logic_garden_108b_lead.py
FORMAT: YouTube Shorts (1080x1920)
SCENE: Logic Garden 108b: Lead Computing (High Fidelity Dynamics)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyArrowPatch
import matplotlib.lines as mlines
import matplotlib.patheffects as pe
import os
import math
import random

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_108b_lead"
os.makedirs(OUT_DIR, exist_ok=True)

# RESOLUTION
RES_W = 1080
RES_H = 1920

# PALETTE
C_BG       = '#080814'    # Dark Navy Void
C_GRID     = '#111122'
C_REAL     = '#FF3333'    # The Physical Target (Red)
C_GHOST    = '#00FFFF'    # The Computed Future (Cyan)
C_VECTOR   = '#008888'    # Prediction Line
C_LOS      = '#333333'    # Line of Sight (Dumb Aim)
C_GUN_LINE = '#FFFF00'    # Where we are actually pointing (Gold)
C_TRACER   = '#FFCC00'    # The Projectiles
C_IMPACT   = '#FFFFFF'    # Kill
C_TEXT     = '#00FFFF'

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: return v
    return v / norm

def get_intercept_time(shooter_pos, bullet_speed, target_pos, target_vel):
    """
    Solves |P_t + V_t * t - P_s| = V_b * t
    Approximation via iteration for stability in sim
    """
    t = 0.0
    for i in range(3): # 3 Iterations is usually enough
        future_pos = target_pos + target_vel * t
        dist = np.linalg.norm(future_pos - shooter_pos)
        t = dist / bullet_speed
    return t

class Threat:
    def __init__(self, uid, side="LEFT"):
        self.id = uid
        self.alive = True
        self.history = []
        
        # Setup Crossing Run
        y_level = random.uniform(200, 800)
        speed = 22.0 # High speed trans-sonic
        
        if side == "LEFT":
            self.pos = np.array([-600.0, y_level], dtype=float)
            self.vel = np.array([speed, random.uniform(-2, 2)], dtype=float)
        else:
            self.pos = np.array([600.0, y_level], dtype=float)
            self.vel = np.array([-speed, random.uniform(-2, 2)], dtype=float)
            
    def update(self):
        if self.alive:
            self.pos += self.vel
            self.history.append(self.pos.copy())
            if len(self.history) > 10: self.history.pop(0)
            
            # Bounds cleanup
            if self.pos[0] < -700 or self.pos[0] > 700:
                self.alive = False

class Bullet:
    def __init__(self, pos, vel):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.active = True
        self.age = 0
        
    def update(self):
        self.pos += self.vel
        self.age += 1
        if self.age > 60: self.active = False

class Explosion:
    def __init__(self, pos):
        self.pos = pos
        self.age = 0
        self.max_age = 15
        self.active = True
    
    def update(self):
        self.age += 1
        if self.age > self.max_age: self.active = False

class CIWS:
    def __init__(self):
        self.pos = np.array([0.0, -800.0], dtype=float)
        self.angle = math.radians(90)
        self.ammo_speed = 50.0 # Faster than target
        self.ghost_pos = None # The computed intercept
        self.is_firing = False
        self.target_locked = False
        
    def update(self, threats, bullets):
        # 1. Select Threat
        target = None
        # Prioritize closest
        min_dist = 3000
        for t in threats:
            if t.alive:
                d = np.linalg.norm(t.pos - self.pos)
                if d < min_dist:
                    min_dist = d
                    target = t
        
        self.ghost_pos = None
        self.is_firing = False
        self.target_locked = False
        
        if target:
            self.target_locked = True
            
            # 2. Compute Lead
            t_intercept = get_intercept_time(self.pos, self.ammo_speed, target.pos, target.vel)
            intercept_point = target.pos + target.vel * t_intercept
            self.ghost_pos = intercept_point
            
            # 3. Aim at Ghost
            aim_vec = intercept_point - self.pos
            target_angle = math.atan2(aim_vec[1], aim_vec[0])
            
            # Smooth tracking? No, "Machine Precision" snaps.
            self.angle = target_angle
            
            # 4. Fire Check
            # Only fire if target is in "Kill Zone" (on screen, visible)
            if -450 < intercept_point[0] < 450 and intercept_point[1] < 900:
                self.is_firing = True
                
                # Burst Fire (3 rounds)
                for _ in range(3):
                    spread = random.uniform(-0.01, 0.01) # Precision fire
                    fire_angle = self.angle + spread
                    vel = np.array([math.cos(fire_angle), math.sin(fire_angle)]) * self.ammo_speed
                    bullets.append(Bullet(self.pos + vel*0.6, vel))

def run():
    print(f"LOGIC GARDEN 108b: LEAD COMPUTING ({TOTAL_FRAMES} frames)")
    
    ciws = CIWS()
    threats = []
    bullets = []
    explosions = []
    
    # TIMELINE
    # 0-150: Single Crossing (Right)
    # 150-300: Single Crossing (Left)
    # 300-600: Dual Crossing (Scissors)
    
    next_spawn = 30
    
    for f in range(TOTAL_FRAMES):
        
        # --- SPAWN LOGIC ---
        if f == next_spawn:
            if f < 200:
                threats.append(Threat(len(threats), "LEFT")) # Low Left
                next_spawn += 180
            elif f < 400:
                threats.append(Threat(len(threats), "RIGHT")) # High Right
                next_spawn += 120
            else:
                # Chaos
                threats.append(Threat(len(threats), random.choice(["LEFT", "RIGHT"])))
                next_spawn += 60

        # --- UPDATE ---
        ciws.update(threats, bullets)
        
        # Projectiles
        active_bullets = []
        for b in bullets:
            b.update()
            if b.active: active_bullets.append(b)
        bullets = active_bullets
        
        # Collisions
        for t in threats:
            if t.alive:
                t.update()
                # Check hit
                for b in bullets:
                    if b.active:
                        d = np.linalg.norm(b.pos - t.pos)
                        if d < 50: # Hit Size
                            b.active = False
                            t.alive = False
                            explosions.append(Explosion(t.pos))
                            # Add "Debris" drifting
                            break
        
        # Explosions
        active_ex = []
        for ex in explosions:
            ex.update()
            if ex.active: active_ex.append(ex)
        explosions = active_ex

        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_xlim(-540, 540)
        ax.set_ylim(-960, 960)
        ax.set_facecolor(C_BG)
        
        # 1. GRID
        for y in range(-800, 1000, 200):
            ax.axhline(y, color=C_GRID, linewidth=1)
        for x in range(-500, 600, 200):
            ax.axvline(x, color=C_GRID, linewidth=1)

        # 2. COMPUTATION LAYER (The Logic)
        if ciws.target_locked:
            # Draw Aim Vector (Gun -> Ghost)
            if ciws.ghost_pos is not None:
                # A. The Ghost (Future Position)
                # Wireframe Triangle
                sz = 80
                ghost_tri = Polygon([
                    ciws.ghost_pos + np.array([0, 40]),
                    ciws.ghost_pos + np.array([-30, -30]),
                    ciws.ghost_pos + np.array([30, -30])
                ], closed=True, fill=False, edgecolor=C_GHOST, linewidth=2, linestyle='--')
                ax.add_patch(ghost_tri)
                
                # B. The Solution Line (Gun -> Ghost)
                ax.plot([ciws.pos[0], ciws.ghost_pos[0]], [ciws.pos[1], ciws.ghost_pos[1]], 
                        color=C_GUN_LINE, linewidth=1, linestyle='-', alpha=0.3)
                
                # Find which target is locked for visual connection
                locked_t = None
                min_d = 9999
                for t in threats:
                    if t.alive:
                        # Heuristic: Closest to aiming logic
                        # Just assume closest threat for viz
                        d = np.linalg.norm(t.pos - ciws.pos)
                        if d < min_d: 
                            min_d = d
                            locked_t = t
                
                if locked_t:
                    # C. The Vector (Target -> Ghost)
                    ax.plot([locked_t.pos[0], ciws.ghost_pos[0]], 
                            [locked_t.pos[1], ciws.ghost_pos[1]], 
                            color=C_VECTOR, linewidth=2, linestyle=':')
                    
                    # D. Current LoS (Gun -> Target) - "Dumb Aim"
                    # Visualize what NOT to do
                    ax.plot([ciws.pos[0], locked_t.pos[0]], [ciws.pos[1], locked_t.pos[1]], 
                            color=C_LOS, linewidth=1, linestyle='--', alpha=0.3)


        # 3. THREATS (The Reality)
        for t in threats:
            if t.alive:
                # Trail
                if len(t.history) > 1:
                    hx, hy = zip(*t.history)
                    ax.plot(hx, hy, color=C_REAL, linewidth=3, alpha=0.5)
                # Body
                ax.scatter(t.pos[0], t.pos[1], c=C_REAL, s=120, marker='v', zorder=10)


        # 4. BULLETS (The Kinetic Solution)
        for b in bullets:
            # Draw elongated
            tail = b.pos - (b.vel * 1.5)
            ax.plot([b.pos[0], tail[0]], [b.pos[1], tail[1]], color=C_TRACER, linewidth=4, alpha=0.9)

        # 5. EXPLOSIONS
        for ex in explosions:
            r = ex.age * 10
            alpha = 1.0 - (ex.age/ex.max_age)
            if alpha > 0:
                # Flash
                ax.add_patch(Circle((ex.pos[0], ex.pos[1]), r, color='white', alpha=alpha, zorder=20))
                # Text
                ax.text(ex.pos[0], ex.pos[1]+50, "INTERCEPT RECONCILED", color=C_GHOST, 
                        ha='center', fontsize=20, fontname='monospace', weight='bold', alpha=alpha)

        # 6. CIWS MODEL
        # Base
        ax.add_patch(Circle((ciws.pos[0], ciws.pos[1]), 50, color='#888888', zorder=5))
        # Turret Head
        head_len = 80
        head_w = 40
        # Rotate rectangle
        rect = Rectangle((ciws.pos[0]-head_w/2, ciws.pos[1]), head_w, head_len, color='#FFFFFF', zorder=6)
        t = matplotlib.transforms.Affine2D().rotate_around(ciws.pos[0], ciws.pos[1], ciws.angle - math.pi/2) + ax.transData
        rect.set_transform(t)
        ax.add_patch(rect)


        # 7. UI / HUD
        stroke = [pe.withStroke(linewidth=4, foreground="black")]
        
        ax.text(0, 880, "LEAD COMPUTING", color=C_GHOST, ha='center',
                fontsize=40, fontname='monospace', weight='bold', path_effects=stroke)
        
        # Legend (Bottom)
        ax.text(-300, -900, "CURRENT POS (REALITY)", color=C_REAL, ha='center', fontsize=20, fontname='monospace', weight='bold')
        ax.text(300, -900, "FUTURE POS (COMPUTED)", color=C_GHOST, ha='center', fontsize=20, fontname='monospace', weight='bold')
        
        # Lead Angle Delta
        if ciws.target_locked:
             ax.text(0, -750, "SOLVING INTERCEPT...", color=C_GUN_LINE, ha='center', 
                     fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
