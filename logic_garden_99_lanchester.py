"""
SOVEREIGN CODE: logic_garden_103_lanchester.py
FORMAT: True HD 1080x1920
SCENE: Lanchester's Square Law (Phalanx vs Boids)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import matplotlib.patheffects as pe
import os
import random
import math

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_103_lanchester"
os.makedirs(OUT_DIR, exist_ok=True)

# WORLD
RES_W = 1080
RES_H = 1920
ASPECT = RES_H / RES_W

# COLORS
C_BG    = '#050510'
C_CYAN  = '#00FFFF'
C_RED   = '#FF0044'
C_LASER_C = '#AAFFFF' # Cyan Laser
C_LASER_R = '#FF8888' # Red Laser
C_CORE  = '#FFFFFF'

class Unit:
    def __init__(self, x, y, team, u_id):
        self.pos = np.array([float(x), float(y)])
        self.vel = np.array([0.0, 0.0])
        self.team = team
        self.id = u_id
        self.active = True
        self.hp = 100.0
        self.max_hp = 100.0
        self.cooldown = 0
        self.target = None # Who am I shooting?
        self.laser_active = 0 # Frame counter for laser draw

    def update(self, dt, allies, enemies, global_target=None):
        if not self.active: return
        
        # --- MOVEMENT LOGIC ---
        if self.team == "CYAN":
            # PHALANX LOGIC: Rigid Formulation
            # Move towards center Y slowly
            target_y = 1000
            
            # Destination is based on ID (Formation slot)
            # Center is 0, offsets: -200, -100, 0, 100, 200
            slot_x = (self.id - 2) * 120 
            
            desired_pos = np.array([slot_x, target_y])
            
            # Steering
            steer = desired_pos - self.pos
            # Dampen
            self.vel = steer * 0.05
            
        elif self.team == "RED":
            # BOIDS LOGIC: Chaotic/Organic
            sep = np.array([0.0, 0.0])
            ali = np.array([0.0, 0.0])
            coh = np.array([0.0, 0.0])
            
            # 1. Separation (Don't crowd)
            for other in allies:
                if other.id != self.id and other.active:
                    dist = np.linalg.norm(self.pos - other.pos)
                    if dist < 150 and dist > 0:
                        push = self.pos - other.pos
                        sep += (push / dist) * 200
            
            # 2. Cohesion (Stay somewhat together)
            center = np.mean([u.pos for u in allies if u.active], axis=0)
            coh = (center - self.pos) * 0.5
            
            # 3. Attraction (Attack Cyan)
            if enemies:
                # Find closest Enemy centroid
                enemy_center = np.mean([u.pos for u in enemies if u.active], axis=0)
                attract = (enemy_center - self.pos) * 1.0
            else:
                attract = np.array([0.0, 0.0])
                
            # Brownian Noise
            noise = np.array([random.uniform(-50, 50), random.uniform(-50, 50)])
            
            # Apply Boids Forces
            total_force = (sep * 1.5) + (coh * 0.1) + (attract * 0.5) + noise
            
            # Integrate
            self.vel += (total_force - self.vel) * 0.1
            
            # Speed Limit
            speed = np.linalg.norm(self.vel)
            if speed > 30:
                self.vel = (self.vel / speed) * 30

        # Update Pos
        self.pos += self.vel
        
        # --- COMBAT LOGIC ---
        self.cooldown -= 1
        if self.laser_active > 0: self.laser_active -= 1
        
        if self.cooldown <= 0 and enemies:
            
            if self.team == "RED":
                # DISTRIBUTED FIRE: Target closest individual
                dists = [(np.linalg.norm(self.pos - e.pos), e) for e in enemies if e.active]
                if dists:
                    dists.sort(key=lambda x: x[0])
                    target_unit = dists[0][1]
                    
                    # Fire!
                    self.target = target_unit
                    self.cooldown = random.randint(20, 40) # Rapid, chaotic fire
                    self.laser_active = 5
                    
                    # Inflict minor damage
                    target_unit.take_damage(5) 

            elif self.team == "CYAN":
                # CONCENTRATED FIRE: Use Shared Register
                if global_target and global_target.active:
                    self.target = global_target
                    self.cooldown = 60 # Slow, synchronized volley
                    self.laser_active = 10 # Long pulse
                    
                    # Inflict MASSIVE damage (Synchronized)
                    # 5 units * 25 dmg = 125 dmg (Instant Kill)
                    global_target.take_damage(25)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.active = False
            self.hp = 0

def run():
    print(f"LOGIC GARDEN 103: LANCHESTER ({TOTAL_FRAMES} frames)")
    
    # 1. SETUP TEAMS
    cyan_team = [Unit((i-2)*100, 300, "CYAN", i) for i in range(5)]
    # Red team scattered at top
    red_team = [Unit(random.randint(-400, 400), random.randint(1400, 1600), "RED", i) for i in range(5)]
    
    explosions = []
    
    for f in range(TOTAL_FRAMES):
        
        # --- LOGIC ---
        
        # 1. HIVE MIND (Cyan Targeting)
        active_red = [u for u in red_team if u.active]
        active_cyan = [u for u in cyan_team if u.active]
        
        shared_target = None
        if active_red and active_cyan:
            # Find closest Red to the CENTER of the Phalanx
            phalanx_center = np.mean([u.pos for u in active_cyan], axis=0)
            dists = [(np.linalg.norm(phalanx_center - r.pos), r) for r in active_red]
            dists.sort(key=lambda x: x[0])
            shared_target = dists[0][1] # The unlucky victim
            
        # 2. UPDATE UNITS
        for u in cyan_team:
            u.update(1.0, cyan_team, active_red, global_target=shared_target)
            if u.hp <= 0 and u.active: # Just died
                explosions.append({'p': u.pos.copy(), 'r': 10, 'c': C_CYAN, 'a': 1.0})
                
        for u in red_team:
            u.update(1.0, red_team, active_cyan)
            if u.hp <= 0 and u.active: # Just died
                # Mark as inactive in next frame, but spawn visual now
                explosions.append({'p': u.pos.copy(), 'r': 20, 'c': C_RED, 'a': 1.0})
        
        # 3. VFX UPDATE
        active_ex = []
        for ex in explosions:
            ex['r'] += 15 # Expand fast
            ex['a'] -= 0.08
            if ex['a'] > 0: active_ex.append(ex)
        explosions = active_ex

        # 4. RENDER
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        ax.set_xlim(-540, 540)
        ax.set_ylim(0, 1920)
        ax.set_facecolor(C_BG)
        
        # Grid
        for y in range(0, 1920, 200):
            ax.axhline(y, color='#111122', linewidth=1)
            
        # DRAW BEAMS (Bottom Layer)
        # Red Lasers (Chaotic, Thin)
        for u in red_team:
            if u.active and u.laser_active > 0 and u.target:
                # Stochastic visual: Beam jitters
                jit_x = random.randint(-5, 5)
                jit_y = random.randint(-5, 5)
                ax.plot([u.pos[0], u.target.pos[0]+jit_x], [u.pos[1], u.target.pos[1]+jit_y], 
                        color=C_LASER_R, linewidth=2, alpha=0.7)
                
        # Cyan Lasers (Converging, Thick, "Raster")
        for u in cyan_team:
            if u.active and u.laser_active > 0 and u.target:
                # Perfect geometric lock
                ax.plot([u.pos[0], u.target.pos[0]], [u.pos[1], u.target.pos[1]], 
                        color=C_LASER_C, linewidth=6, alpha=0.9)
                
                # Draw "Hit Marker" on target
                ax.plot(u.target.pos[0], u.target.pos[1], marker='x', markersize=20, color=C_CYAN, markeredgewidth=3)

        # DRAW UNITS
        
        # Cyan (Squares)
        for u in cyan_team:
            if u.active:
                rect = Rectangle((u.pos[0]-40, u.pos[1]-40), 80, 80, color=C_CYAN)
                ax.add_patch(rect)
                # Structure line
                ax.plot([u.pos[0], u.pos[0]], [0, u.pos[1]], color=C_CYAN, alpha=0.2, linewidth=1)
                
                # Health Bar (Small vertical)
                h_pct = u.hp / u.max_hp
                ax.plot([u.pos[0]-50, u.pos[0]-50], [u.pos[1]-40, u.pos[1]-40+(80*h_pct)], 
                        color='white', linewidth=4)
        
        # Red (Triangles/Boids)
        for u in red_team:
            if u.active:
                # Point triangle in velocity direction
                speed = np.linalg.norm(u.vel)
                if speed > 0:
                    d = u.vel / speed
                    perp = np.array([-d[1], d[0]])
                    
                    nose = u.pos + (d * 50)
                    wing1 = u.pos - (d * 30) + (perp * 30)
                    wing2 = u.pos - (d * 30) - (perp * 30)
                    
                    poly = Polygon([nose, wing1, wing2], color=C_RED)
                    ax.add_patch(poly)
                else:
                    ax.plot(u.pos[0], u.pos[1], marker='v', color=C_RED, markersize=30)
                    
                # Health Bar
                h_pct = u.hp / u.max_hp
                ax.plot([u.pos[0]-50, u.pos[0]-50], [u.pos[1]-40, u.pos[1]-40+(80*h_pct)], 
                        color='white', linewidth=4)
                        
        # TARGET LOCK HUD
        if shared_target and shared_target.active:
            # Draw a box around the victim
            box_sz = 120 + math.sin(f*0.5)*20 # Breathing box
            rect = Rectangle((shared_target.pos[0]-box_sz/2, shared_target.pos[1]-box_sz/2), 
                             box_sz, box_sz, fill=False, edgecolor=C_CYAN, linewidth=3, linestyle='--')
            ax.add_patch(rect)
            ax.text(shared_target.pos[0], shared_target.pos[1]+100, "TARGET LOCK", 
                    color=C_CYAN, ha='center', fontsize=15, weight='bold')

        # EXPLOSIONS
        for ex in explosions:
            circ = Circle((ex['p'][0], ex['p'][1]), ex['r'], color=ex['c'], alpha=ex['a'])
            ax.add_patch(circ)
            circ2 = Circle((ex['p'][0], ex['p'][1]), ex['r']*0.7, color='white', alpha=ex['a'])
            ax.add_patch(circ2)

        # TEXT UI
        stroke = [pe.withStroke(linewidth=3, foreground="black")]
        
        # Stats
        c_alive = len(active_cyan)
        r_alive = len(active_red)
        
        ax.text(0.05, 0.95, "LANCHESTER'S SQUARE LAW", transform=ax.transAxes, color='white', fontsize=20, weight='bold', path_effects=stroke)
        ax.text(0.05, 0.05, f"PHALANX (N^2): {c_alive}", transform=ax.transAxes, color=C_CYAN, fontsize=25, weight='bold', path_effects=stroke)
        ax.text(0.95, 0.95, f"BOIDS (N): {r_alive}", transform=ax.transAxes, color=C_RED, ha='right', fontsize=25, weight='bold', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
