"""
SOVEREIGN CODE: logic_garden_107_hk_swarm_v2.py
FORMAT: YouTube Shorts (1080x1920)
SCENE: HK Swarm (Syntax Patched)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Wedge, Rectangle
import matplotlib.patheffects as pe
import os
import math
import random

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_107_swarm_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# RESOLUTION
RES_W = 1080
RES_H = 1920

# PALETTE
C_BG      = '#050510'     # Deep Space
C_HK      = '#00FFFF'     # Cyan Swarm (Hunter Killers)
C_TRAIL   = '#008888'     # Motion Blur
C_TURRET  = '#FF3333'     # Red Static Threat
C_FLAK    = '#FF6666'     # Anti-Air
C_EXP     = '#FFD700'     # Impact/Victory

def mag(v):
    return np.linalg.norm(v)

def limit(v, max_val):
    m = mag(v)
    if m > max_val:
        return (v / m) * max_val
    return v

def normalize(v):
    m = mag(v)
    if m > 0:
        return v / m
    return v

class Boid:
    def __init__(self, uid):
        self.id = uid
        # Start High
        self.pos = np.array([random.uniform(-500, 500), random.uniform(400, 900)])
        self.vel = np.array([random.uniform(-5, 5), random.uniform(-2, 2)])
        self.acc = np.array([0.0, 0.0])
        self.max_force = 0.5
        self.max_speed = 10.0
        self.history = [] # For trails

    def update(self):
        self.vel += self.acc
        self.vel = limit(self.vel, self.max_speed)
        self.pos += self.vel
        self.acc *= 0 # Reset acc
        
        # History
        self.history.append(self.pos.copy())
        if len(self.history) > 5: self.history.pop(0)

        # Wrap X only (Tube world)
        if self.pos[0] > 600: self.pos[0] = -600
        if self.pos[0] < -600: self.pos[0] = 600
        
        # Hard floor clamp (Ground)
        if self.pos[1] < -1200: self.pos[1] = -1200 # Crash

    def apply_force(self, force):
        self.acc += force

    def flock(self, boids, target=None, state="PATROL"):
        sep = self.separate(boids)
        ali = self.align(boids)
        coh = self.cohesion(boids)
        
        # Weightings Change by State
        if state == "PATROL":
            # Loose, organic
            sep *= 2.5
            ali *= 1.0
            coh *= 1.0
            self.max_speed = 12.0
            
            # Gentle drift force to keep them on screen
            center_push = np.array([0.0, 0.0])
            if self.pos[1] < 400: center_push[1] += 0.05
            if self.pos[1] > 900: center_push[1] -= 0.05
            self.apply_force(center_push)

        elif state == "ATTACK":
            # Tighter, faster, focused
            sep *= 3.0  # Don't crash
            ali *= 2.0  # Move as one
            coh *= 0.5  # Stream out 
            self.max_speed = 25.0 # Dive speed
            
            if target is not None:
                seek = self.seek(target)
                seek *= 3.0 # Strong pull to target
                self.apply_force(seek)
                
                # Sine Wave Evasion Logic
                # If moving down, oscillate X
                if self.vel[1] < 0:
                    evade = np.array([math.sin(self.pos[1] * 0.02) * 2.0, 0])
                    self.apply_force(evade)

        elif state == "PULL_UP":
            sep *= 4.0
            ali *= 2.0
            coh *= 0.0
            self.max_speed = 15.0
            # Seek sky
            sky = np.array([self.pos[0], 1500])
            up = self.seek(sky)
            up *= 4.0
            self.apply_force(up)

        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)

    def seek(self, target):
        desired = target - self.pos
        desired = normalize(desired) * self.max_speed
        steer = desired - self.vel
        return limit(steer, self.max_force)

    def separate(self, boids):
        # Avoid crowding
        desired_separation = 40.0
        steer = np.array([0.0, 0.0])
        count = 0
        for other in boids:
            d = mag(self.pos - other.pos)
            if d > 0 and d < desired_separation:
                diff = self.pos - other.pos
                diff = normalize(diff)
                diff /= d # Weight by distance
                steer += diff
                count += 1
        if count > 0:
            steer /= count
            steer = normalize(steer) * self.max_speed
            steer -= self.vel
            steer = limit(steer, self.max_force)
        return steer

    def align(self, boids):
        # Steer towards average heading of neighbors
        neighbor_dist = 80.0
        sum_vel = np.array([0.0, 0.0])
        count = 0
        for other in boids:
            d = mag(self.pos - other.pos)
            if d > 0 and d < neighbor_dist:
                sum_vel += other.vel
                count += 1
        if count > 0:
            sum_vel /= count
            sum_vel = normalize(sum_vel) * self.max_speed
            steer = sum_vel - self.vel
            return limit(steer, self.max_force)
        return np.array([0.0, 0.0])

    def cohesion(self, boids):
        # Steer towards average position of neighbors
        neighbor_dist = 80.0
        sum_pos = np.array([0.0, 0.0])
        count = 0
        for other in boids:
            d = mag(self.pos - other.pos)
            if d > 0 and d < neighbor_dist:
                sum_pos += other.pos
                count += 1
        if count > 0:
            sum_pos /= count
            return self.seek(sum_pos)
        return np.array([0.0, 0.0])

class Turret:
    def __init__(self, x):
        self.pos = np.array([x, -900.0])
        self.alive = True
        self.recharge = 0
        # Simple hitbox visual size
        self.size = 60 
        
    def fire(self):
        # Simple upward flak
        if self.alive and self.recharge <= 0:
            self.recharge = random.randint(5, 15)
            # Spawn flak
            return True # Signal to spawn
        
        self.recharge -= 1
        return False

def run():
    print(f"LOGIC GARDEN 107: HK SWARM V2 ({TOTAL_FRAMES} frames)")
    
    # 1. SETUP
    flock_size = 60
    boids = [Boid(i) for i in range(flock_size)]
    
    turrets = [Turret(-300), Turret(0), Turret(300)]
    flak = [] # List of {pos, vel, age}
    explosions = [] # {pos, age, size}
    
    # TIMELINE CONSTANTS
    PHASE_PATROL = 0
    PHASE_LOCK   = 240 # 8s
    PHASE_DIVE   = 300 # 10s
    PHASE_IMPACT = 450 # 15s
    PHASE_EVADE  = 500 # 16.5s
    
    current_target_xy = np.array([0.0, -900.0]) # Center Turret

    for f in range(TOTAL_FRAMES):
        
        # --- STATE MACHINE ---
        state = "PATROL"
        target = None
        
        if f >= PHASE_LOCK and f < PHASE_DIVE:
            state = "PATROL" # Visual lock phase
        
        elif f >= PHASE_DIVE and f < PHASE_IMPACT:
            state = "ATTACK"
            target = current_target_xy
            
        elif f >= PHASE_IMPACT and f < PHASE_EVADE:
            state = "ATTACK"
            # Keep hitting
            target = current_target_xy
            
        elif f >= PHASE_EVADE:
            state = "PULL_UP"
            
        # --- PHYSICS ---
        
        # Boids
        for b in boids:
            b.flock(boids, target, state)
            b.update()
            
            # Collision Logic (Boid hits Turret)
            if state == "ATTACK" and b.pos[1] < -800:
                for t in turrets:
                    if t.alive and abs(b.pos[0] - t.pos[0]) < 80:
                        # Impact
                        explosions.append({'pos': t.pos.copy(), 'age': 0, 'size': 200})
                        t.alive = False # Kill turret
        
        # Turrets / Flak
        for t in turrets:
            if t.fire():
                # Spawn flak particle
                # Aim roughly up
                flak_vel = np.array([random.uniform(-2, 2), random.uniform(15, 25)])
                flak.append({'pos': t.pos.copy(), 'vel': flak_vel, 'age': 0})
        
        active_flak = []
        for fk in flak:
            fk['pos'] += fk['vel']
            fk['age'] += 1
            if fk['age'] < 50: 
                active_flak.append(fk)
        flak = active_flak
        
        # Explosions
        for ex in explosions:
            ex['age'] += 1

        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        ax.set_xlim(-540, 540)
        ax.set_ylim(-960, 960)
        ax.set_facecolor(C_BG)
        
        # 1. GROUND / TURRETS
        ax.fill_between([-600, 600], -960, -900, color='#221111')
        
        for t in turrets:
            if t.alive:
                # Dome
                w = Wedge((t.pos[0], t.pos[1]), 60, 0, 180, color=C_TURRET)
                ax.add_patch(w)
                # Barrels
                ax.plot([t.pos[0]-10, t.pos[0]-10], [t.pos[1], t.pos[1]+50], color=C_TURRET, linewidth=4)
                ax.plot([t.pos[0]+10, t.pos[0]+10], [t.pos[1], t.pos[1]+50], color=C_TURRET, linewidth=4)
            else:
                # Wreckage
                ax.scatter(t.pos[0], t.pos[1], color='#443333', s=200, marker='x', linewidth=5)

        # 2. FLAK
        for fk in flak:
            ax.scatter(fk['pos'][0], fk['pos'][1], color=C_FLAK, s=30)
            
        # 3. EXPLOSIONS
        for ex in explosions:
            if ex['age'] < 20:
                sz = ex['size'] * (ex['age']/10.0) if ex['age'] < 10 else ex['size']
                alpha = 1.0 - (ex['age']/20.0)
                if alpha > 0:
                    c = Circle((ex['pos'][0], ex['pos'][1]), sz, color=C_EXP, alpha=alpha)
                    ax.add_patch(c)

        # 4. SWARM (BOIDS)
        for b in boids:
            # Draw Velocity Triangle
            angle = math.atan2(b.vel[1], b.vel[0])
            
            # Simple shape
            tip = b.pos + b.vel * 2.0
            wing_len = 20.0
            
            # Back wings
            p1_a = angle + math.radians(140)
            p2_a = angle - math.radians(140)
            
            p1 = b.pos + np.array([math.cos(p1_a), math.sin(p1_a)]) * wing_len
            p2 = b.pos + np.array([math.cos(p2_a), math.sin(p2_a)]) * wing_len
            
            poly = Polygon([tip, p1, p2], closed=True, color=C_HK)
            ax.add_patch(poly)
            
            # Trail
            if len(b.history) > 1:
                hx = [pt[0] for pt in b.history]
                hy = [pt[1] for pt in b.history]
                ax.plot(hx, hy, color=C_TRAIL, linewidth=2, alpha=0.5)

        # 5. UI
        stroke = [pe.withStroke(linewidth=4, foreground="black")]
        
        ax.text(0, 880, "HK-AERIAL SWARM", color=C_HK, ha='center',
                fontsize=35, fontname='monospace', weight='bold', path_effects=stroke)
        
        # State Text
        if f < PHASE_LOCK:
             ax.text(0, -700, "MODE: AUTONOMOUS PATROL", color=C_TRAIL, ha='center',
                    fontsize=25, fontname='monospace', path_effects=stroke)
        elif f < PHASE_DIVE:
             ax.text(0, -700, "TARGET ACQUIRED", color=C_TURRET, ha='center',
                    fontsize=40, fontname='monospace', weight='bold', path_effects=stroke)
             # Draw Box around Turrets
             rect_w = 800
             rect = Rectangle((-400, -950), 800, 200, edgecolor=C_TURRET, fill=False, linewidth=3, linestyle='--')
             ax.add_patch(rect)
             
        elif f < PHASE_IMPACT:
             ax.text(0, -700, "DIVING... SINE WAVE ENGAGED", color=C_HK, ha='center',
                    fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)
        
        elif f >= PHASE_EVADE:
             ax.text(0, -700, "TARGET NEUTRALIZED. RTB.", color=C_EXP, ha='center',
                    fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
