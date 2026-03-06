"""
SOVEREIGN CODE: logic_garden_106_star_wars_v2.py
FORMAT: YouTube Shorts (1080x1920)
SCENE: Star Wars (Syntax Patched)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patheffects as pe
import os
import math
import random

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_106_star_wars_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# RESOLUTION
RES_W = 1080
RES_H = 1920

# PALETTE
C_BG      = '#050510'     # Deep Space
C_EARTH   = '#001133'     # Atmosphere
C_GRID    = '#111122'     # Orbital Mechanics
C_ICBM    = '#FF3333'     # Boost Phase
C_WARHEAD = '#FF0000'     # RVs
C_DECOY   = '#AA4444'     # Fake Targets
C_SAT     = '#00FFFF'     # SDI Assets
C_LASER   = '#00FFFF'     # Directed Energy
C_EXP     = '#FFD700'     # Plasma

class Explosion:
    def __init__(self, pos):
        self.pos = np.array(pos, dtype=float)
        self.age = 0
        self.max_age = 15
        self.active = True
        
    def update(self):
        self.age += 1
        if self.age > self.max_age:
            self.active = False

class Missile:
    def __init__(self, uid, start_x):
        self.id = uid
        self.pos = np.array([start_x, -950.0], dtype=float) 
        # Aim roughly up but spread out
        angle = math.radians(90 + random.uniform(-20, 20))
        speed = random.uniform(8, 10)
        self.vel = np.array([math.cos(angle)*speed, math.sin(angle)*speed], dtype=float)
        self.state = "BOOST" # BOOST, MIRV, DEAD
        self.warheads = [] 
        
    def update(self):
        if self.state == "BOOST":
            self.pos += self.vel
            self.vel[1] -= 0.02 # Gravity
            
            # Separation Logic
            if self.pos[1] > -200 and random.random() < 0.1:
                self.state = "MIRV"
                self.spawn_mirvs()
                
        elif self.state == "MIRV":
            active_rvs = []
            for rv in self.warheads:
                if rv['active']:
                    rv['pos'] += rv['vel']
                    rv['vel'][1] -= 0.02
                    active_rvs.append(rv)
            self.warheads = active_rvs
            
            if not self.warheads:
                self.state = "DEAD"

    def spawn_mirvs(self):
        count = random.randint(5, 8)
        for i in range(count):
            spread = np.array([random.uniform(-1, 1), random.uniform(-0.5, 0.5)])
            rv_vel = self.vel + spread
            self.warheads.append({
                'pos': self.pos.copy(),
                'vel': rv_vel,
                'active': True,
                'type': 'REAL' if i < 3 else 'DECOY'
            })

class Satellite:
    def __init__(self, uid, x, y):
        self.id = uid
        # Fix: Ensure float dtype to allow velocity (float) addition
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([random.uniform(-1, 1), 0.0], dtype=float)
        self.cooldown = 0
        self.hit_pos = None # Store hit for rendering line
        
    def update(self, targets):
        self.pos += self.vel
        
        # Wrap orbit
        if self.pos[0] > 600: self.pos[0] = -600
        if self.pos[0] < -600: self.pos[0] = 600
        
        self.hit_pos = None
        self.cooldown -= 1
        explosion_point = None
        
        if self.cooldown <= 0:
            # Find closest target below
            best_target = None
            min_dist = 2000
            
            # Identify all valid targets
            potential_targets = []
            for m in targets:
                if m.state == "BOOST":
                    potential_targets.append({'obj': m, 'type': 'MISSILE', 'pos': m.pos})
                elif m.state == "MIRV":
                    for rv in m.warheads:
                        if rv['active']:
                            potential_targets.append({'obj': rv, 'type': 'RV', 'pos': rv['pos']})

            for t in potential_targets:
                if t['pos'][1] < self.pos[1]: # Look down
                    d = np.linalg.norm(t['pos'] - self.pos)
                    if d < min_dist:
                        min_dist = d
                        best_target = t
            
            # Engage
            if best_target and min_dist < 1500:
                self.hit_pos = best_target['pos'].copy()
                explosion_point = best_target['pos'].copy()
                self.cooldown = 10 # Fire Rate
                
                # Destroy Target
                if best_target['type'] == 'MISSILE':
                    best_target['obj'].state = "DEAD"
                elif best_target['type'] == 'RV':
                    best_target['obj']['active'] = False
                    
        return explosion_point

def run():
    print(f"LOGIC GARDEN 106: STAR WARS V2 ({TOTAL_FRAMES} frames)")
    
    missiles = []
    satellites = []
    
    # Create Constellation
    for i in range(5):
        x = -400 + (i * 200)
        y = 600 + (i%2 * 100)
        satellites.append(Satellite(i, x, y))
        
    explosions = []
    
    for f in range(TOTAL_FRAMES):
        
        # --- SPAWN ---
        if f % 40 == 0 and f < 300:
            # Random launch site
            start_x = random.uniform(-400, 400)
            missiles.append(Missile(len(missiles), start_x))
            
        # --- UPDATE ---
        
        # Missiles
        active_m = []
        for m in missiles:
            m.update()
            if m.state != "DEAD" and m.pos[1] > -1100:
                active_m.append(m)
        missiles = active_m
        
        # Satellites
        for s in satellites:
            hit = s.update(missiles)
            if hit is not None:
                explosions.append(Explosion(hit))
                
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
        
        # 1. EARTH
        earth = Circle((0, -3200), 2300, color=C_EARTH, alpha=0.9, zorder=0)
        ax.add_patch(earth)
        # Horizon Glow
        ax.fill_between([-600, 600], -960, -800, color='#004488', alpha=0.1, zorder=1)
        
        # 2. GRID
        ax.axhline(600, color=C_GRID, linestyle='--', linewidth=1)

        # 3. MISSILES
        for m in missiles:
            if m.state == "BOOST":
                ax.scatter(m.pos[0], m.pos[1], c=C_ICBM, s=80, marker='^', zorder=5)
                # Trail
                ax.plot([m.pos[0], m.pos[0] - m.vel[0]*4], 
                        [m.pos[1], m.pos[1] - m.vel[1]*4], color=C_ICBM, linewidth=3, alpha=0.5)
            
            elif m.state == "MIRV":
                for rv in m.warheads:
                    col = C_WARHEAD if rv['type'] == 'REAL' else C_DECOY
                    sz = 40 if rv['type'] == 'REAL' else 20
                    ax.scatter(rv['pos'][0], rv['pos'][1], c=col, s=sz, marker='v', zorder=5)

        # 4. SATELLITES & LASERS
        for s in satellites:
            # Icon
            ax.scatter(s.pos[0], s.pos[1], c=C_SAT, s=180, marker='D', zorder=10, edgecolors='white', linewidth=2)
            
            # Beam
            if s.hit_pos is not None:
                ax.plot([s.pos[0], s.hit_pos[0]], [s.pos[1], s.hit_pos[1]], 
                        color=C_LASER, linewidth=6, alpha=0.8, zorder=9)
                # Source Flash
                ax.scatter(s.pos[0], s.pos[1], c='white', s=300, alpha=0.9, zorder=12)

        # 5. EXPLOSIONS
        for ex in explosions:
            r = ex.age * 6
            alpha = 1.0 - (ex.age / ex.max_age)
            if alpha < 0: alpha = 0
            
            c = Circle((ex.pos[0], ex.pos[1]), r, color=C_EXP, alpha=alpha*0.6, zorder=15)
            ax.add_patch(c)
            ax.scatter(ex.pos[0], ex.pos[1], c='white', s=80*alpha, zorder=16)

        # 6. UI
        stroke = [pe.withStroke(linewidth=4, foreground="black")]
        
        if f > 10:
             ax.text(0, 850, "STRATEGIC DEFENSE INITIATIVE", color=C_SAT, ha='center',
                fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)
             
        if f > 50 and f < 150:
             ax.text(0, -850, "THREAT: BALISTIC SATURATION", color=C_ICBM, ha='center',
                fontsize=25, fontname='monospace', weight='bold', path_effects=stroke)
             
        if f > 200:
             ax.text(0, -850, "INTERCEPT CONFIRMED", color=C_EXP, ha='center',
                fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
