"""
SOVEREIGN CODE: logic_garden_106_star_wars_v3.py
FORMAT: YouTube Shorts (1080x1920)
SCENE: Star Wars (Phased Engagement: Track -> Kill)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import matplotlib.patheffects as pe
import os
import math
import random

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_106_star_wars_v3"
os.makedirs(OUT_DIR, exist_ok=True)

# RESOLUTION
RES_W = 1080
RES_H = 1920

# PALETTE
C_BG      = '#050510'     # Deep Space
C_EARTH   = '#001133'     # Atmosphere
C_GRID    = '#112233'     # Tracking Grid
C_ICBM    = '#FF3333'     # Boost Phase
C_WARHEAD = '#FF0000'     # RVs
C_DECOY   = '#AA4444'     # Fake Targets
C_SAT     = '#00FFFF'     # SDI Assets
C_TRACK   = '#004444'     # Targeting Computer (Dark Cyan)
C_LASER   = '#00FFFF'     # Kill Shot (Bright Cyan)
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
        angle = math.radians(90 + random.uniform(-15, 15))
        speed = random.uniform(5, 7) # Slower rise to allow buildup
        self.vel = np.array([math.cos(angle)*speed, math.sin(angle)*speed], dtype=float)
        self.state = "BOOST" 
        self.warheads = [] 
        
    def update(self):
        if self.state == "BOOST":
            self.pos += self.vel
            self.vel[1] -= 0.01 
            
            # Separation Logic (Triggered by height)
            # Make sure they get high enough to be seen
            if self.pos[1] > -300 and random.random() < 0.05:
                self.state = "MIRV"
                self.spawn_mirvs()
                
        elif self.state == "MIRV":
            active_rvs = []
            for rv in self.warheads:
                if rv['active']:
                    rv['pos'] += rv['vel']
                    # Drag/Gravity
                    rv['vel'][1] -= 0.01
                    active_rvs.append(rv)
            self.warheads = active_rvs
            
            if not self.warheads:
                self.state = "DEAD"

    def spawn_mirvs(self):
        # Create THREAT CLOUD
        count = random.randint(6, 10)
        for i in range(count):
            spread = np.array([random.uniform(-1.5, 1.5), random.uniform(-0.5, 0.5)])
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
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([random.uniform(-0.5, 0.5), 0.0], dtype=float)
        self.cooldown = 0
        self.hit_pos = None     # Laser (Firing)
        self.track_pos = None   # Tracker (Surveillance)
        
    def update(self, targets, weapons_free):
        self.pos += self.vel
        # Wrap orbit
        if self.pos[0] > 600: self.pos[0] = -600
        if self.pos[0] < -600: self.pos[0] = 600
        
        self.hit_pos = None
        self.track_pos = None
        self.cooldown -= 1
        explosion_point = None
        
        # FIND TARGETS
        best_target = None
        min_dist = 2000
        
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
        
        # LOGIC
        if best_target and min_dist < 1800:
            if not weapons_free:
                # TRACKING MODE (Phase 1/2)
                # Just draw line, do not kill
                self.track_pos = best_target['pos'].copy()
            
            elif weapons_free and self.cooldown <= 0:
                # ENGAGEMENT MODE (Phase 3)
                self.hit_pos = best_target['pos'].copy()
                explosion_point = best_target['pos'].copy()
                self.cooldown = 8 # Rate of Fire
                
                # Kill
                if best_target['type'] == 'MISSILE':
                    best_target['obj'].state = "DEAD"
                elif best_target['type'] == 'RV':
                    best_target['obj']['active'] = False
                    
        return explosion_point

def run():
    print(f"LOGIC GARDEN 106: STAR WARS V3 ({TOTAL_FRAMES} frames)")
    
    missiles = []
    satellites = []
    
    # 5 Satellites High Orbit
    for i in range(5):
        x = -500 + (i * 250)
        y = 700 + (i%2 * 100)
        satellites.append(Satellite(i, x, y))
        
    explosions = []
    
    # TIMELINE PHASES
    # 0-300: LAUNCH & SEPARATION (Weapons Hold)
    # 300-600: INTERCEPTION (Weapons Free)
    WEAPONS_FREE_FRAME = 300
    
    for f in range(TOTAL_FRAMES):
        
        # --- SPAWN ---
        # Heavy saturation in the first half
        if f < WEAPONS_FREE_FRAME and f % 25 == 0:
            start_x = random.uniform(-500, 500)
            missiles.append(Missile(len(missiles), start_x))
            
        # --- UPDATE ---
        weapons_free = (f >= WEAPONS_FREE_FRAME)
        
        # Missiles
        active_m = []
        for m in missiles:
            m.update()
            if m.state != "DEAD" and m.pos[1] > -1200:
                active_m.append(m)
        missiles = active_m
        
        # Satellites
        for s in satellites:
            hit = s.update(missiles, weapons_free)
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
        ax.fill_between([-600, 600], -960, -800, color='#004488', alpha=0.1, zorder=1)
        
        # 2. GRID / ORBITS
        ax.axhline(600, color=C_GRID, linestyle='--', linewidth=1)
        ax.axhline(800, color=C_GRID, linestyle='--', linewidth=1)

        # 3. MISSILES (The Threat)
        for m in missiles:
            if m.state == "BOOST":
                # Bus
                ax.scatter(m.pos[0], m.pos[1], c=C_ICBM, s=80, marker='^', zorder=5)
                # Trail
                ax.plot([m.pos[0], m.pos[0] - m.vel[0]*6], 
                        [m.pos[1], m.pos[1] - m.vel[1]*6], color=C_ICBM, linewidth=3, alpha=0.5)
            
            elif m.state == "MIRV":
                # Cloud
                for rv in m.warheads:
                    col = C_WARHEAD if rv['type'] == 'REAL' else C_DECOY
                    sz = 40 if rv['type'] == 'REAL' else 20
                    ax.scatter(rv['pos'][0], rv['pos'][1], c=col, s=sz, marker='v', zorder=5)

        # 4. SATELLITES (The Assets)
        for s in satellites:
            # Body
            ax.scatter(s.pos[0], s.pos[1], c=C_SAT, s=180, marker='D', zorder=10, edgecolors='white', linewidth=2)
            
            # TRACKING BEAM (Surveillance)
            if s.track_pos is not None:
                # Thin Dotted Line
                ax.plot([s.pos[0], s.track_pos[0]], [s.pos[1], s.track_pos[1]], 
                        color=C_TRACK, linewidth=1, linestyle=':', alpha=0.8, zorder=8)
                # Target HUD box?
                
            # LASER BEAM (Kill)
            if s.hit_pos is not None:
                ax.plot([s.pos[0], s.hit_pos[0]], [s.pos[1], s.hit_pos[1]], 
                        color=C_LASER, linewidth=6, alpha=0.9, zorder=9)
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
        
        # Header
        ax.text(0, 880, "STRATEGIC DEFENSE INITIATIVE", color=C_SAT, ha='center',
                fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)
        
        # Status Messages
        if not weapons_free:
            # SURVEILLANCE
            ax.text(0, 830, "SYSTEM: TRACKING", color=C_TRACK, ha='center',
                   fontsize=25, fontname='monospace', path_effects=stroke)
            
            if f < 100:
                ax.text(0, -700, "LAUNCH DETECTED", color=C_ICBM, ha='center',
                        fontsize=35, fontname='monospace', weight='bold', path_effects=stroke)
            elif f < 300:
                # Show threat count
                 ax.text(0, -700, "THREAT: CLOUD SATURATION", color=C_DECOY, ha='center',
                        fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)
                 
        else:
            # ENGAGEMENT
            ax.text(0, 830, "SYSTEM: WEAPONS FREE", color=C_LASER, ha='center',
                   fontsize=35, fontname='monospace', weight='bold', path_effects=stroke) # Highlighted
            
            ax.text(0, -700, "INTERCEPT IN PROGRESS", color=C_EXP, ha='center',
                    fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
