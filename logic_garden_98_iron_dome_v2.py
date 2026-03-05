"""
SOVEREIGN CODE: logic_garden_102_iron_dome_v2.py
FORMAT: True HD 1080x1920
SCENE: Saturation Defense (Typo Fixed)
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
DURATION = 35
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_102_dome_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# WORLD PHYSICS
G = 30.0             # Gravity (Slightly higher for faster drops)
INTERCEPT_RADIUS = 80 # Generous kill zone for visual clarity
INTERCEPTOR_SPEED = 600
ROCKET_SPEED = 300   # The variable that was typoed

# RENDER
RES_W = 1080
RES_H = 1920
ASPECT = RES_H / RES_W

# PALETTE
C_BG    = '#050510'
C_GROUND= '#111111'
C_CITY  = '#00FF44' # Green Zone
C_RED   = '#FF0044' # Threat
C_BLUE  = '#00AAFF' # Defense
C_EXPL  = '#FFDD00' # Explosion
C_SMOKE = '#555555' 

class Payload:
    def __init__(self, x, y, vx, vy, kind="RED"):
        self.pos = np.array([float(x), float(y)])
        self.vel = np.array([float(vx), float(vy)])
        self.kind = kind
        self.active = True
        self.history = []
        self.target_id = None # For Blue missiles tracking a specific Red
        self.fuel = 300 # Lifetime for blue
        self.steer_lim = 200.0 # Maneuverability limit

    def update(self, dt, threats=None):
        if not self.active: return "DEAD"
        
        acc = np.array([0.0, 0.0])

        # 1. PHYSICS
        if self.kind == "RED":
            # Ballistic Trajectory (Gravity only)
            acc = np.array([0.0, -G])
            
        elif self.kind == "BLUE":
            # GUIDANCE LOGIC (Proportional Navigation)
            self.fuel -= 1
            if self.fuel <= 0:
                self.active = False
                return "FIZZLE"
                
            # Find my target
            target = None
            if threats and self.target_id is not None:
                # Find the object with matching ID
                for t in threats:
                    if id(t) == self.target_id and t.active:
                        target = t
                        break
            
            if target:
                # LEAD CALCULATION
                to_target = target.pos - self.pos
                dist = np.linalg.norm(to_target)
                
                # Check interception before physics update to catch fast movers
                if dist < INTERCEPT_RADIUS:
                    return "INTERCEPT"

                # Time to intercept
                closing_speed = INTERCEPTOR_SPEED + np.linalg.norm(target.vel)
                tti = dist / closing_speed
                
                # Predicted Position (PIP)
                pip = target.pos + (target.vel * tti)
                
                # Desired Velocity Vector
                desired_vec = pip - self.pos
                desired_dir = desired_vec / np.linalg.norm(desired_vec)
                
                # Steering Force
                desired_vel = desired_dir * INTERCEPTOR_SPEED
                steering = desired_vel - self.vel
                
                # Limit steering (G-Limit)
                steer_mag = np.linalg.norm(steering)
                if steer_mag > self.steer_lim:
                    steering = (steering / steer_mag) * self.steer_lim
                
                acc = steering
            else:
                # No target, self destruct if high up
                if self.pos[1] > 3000: self.active = False
                acc = np.array([0.0, 0.0]) # Coast

            # Apply Acc
            self.vel += acc * dt
            
            # Clamp Speed
            speed = np.linalg.norm(self.vel)
            if speed > INTERCEPTOR_SPEED:
                self.vel = (self.vel / speed) * INTERCEPTOR_SPEED
        
        else:
            # Gravity for Red
             self.vel += np.array([0.0, -G]) * dt

        # INTEGRATE
        self.pos += self.vel * dt
        
        # HISTORY
        self.history.append(self.pos.copy())
        if len(self.history) > 30: self.history.pop(0)

        # FLOOR CHECK
        if self.pos[1] <= 0:
            self.pos[1] = 0
            self.active = False
            return "IMPACT_GROUND"
            
        return "ALIVE"

def run():
    print(f"LOGIC GARDEN 102: IRON DOME V2 ({TOTAL_FRAMES} frames)")
    
    # ENTITIES
    red_rockets = []
    blue_missiles = []
    explosions = []
    
    # TRACKING
    assigned_targets = set() 
    
    # SETUP
    CITY_X = [-800, 800] 
    DOME_POS = np.array([0.0, 10.0]) 
    
    # ATTACK WAVE SCHEDULE
    WAVES = {
        30: 2,   
        90: 5,   
        150: 35, # SATURATION EVENT
        220: 10
    }
    
    for f in range(TOTAL_FRAMES):
        
        # --- 1. THREAT GENERATION ---
        if f in WAVES:
            count = WAVES[f]
            for _ in range(count):
                # Spawn incoming from TOP margins
                start_x = random.randint(-1500, 1500)
                start_y = random.randint(3500, 4500)
                
                # Aim at city
                target_x = random.randint(CITY_X[0], CITY_X[1])
                
                vec = np.array([float(target_x), 0.0]) - np.array([float(start_x), float(start_y)])
                vecdir = vec / np.linalg.norm(vec)
                
                # INITIAL VELOCITY
                vel = vecdir * ROCKET_SPEED 
                
                # Add "Lob" (Arc)
                vel[1] += random.randint(50, 150) 
                
                r = Payload(start_x, start_y, vel[0], vel[1], "RED")
                red_rockets.append(r)

        # --- 2. DEFENSE LOGIC ---
        # Scan every few frames
        if f % 4 == 0:
            # Identify active threats above ground
            threats = [r for r in red_rockets if r.active and r.pos[1] > 100]
            # Priorities: Lowest altitude first
            threats.sort(key=lambda x: x.pos[1])
            
            shots_this_frame = 0
            
            for t in threats:
                if shots_this_frame > 2: break # Battery fire rate limit
                
                t_id = id(t)
                if t_id in assigned_targets: continue
                
                # Engagement Envelope: Falling towards city
                if t.vel[1] < 0 and t.pos[1] < 3500:
                    
                    # LAUNCH
                    b = Payload(DOME_POS[0], DOME_POS[1], 0, 0, "BLUE")
                    b.target_id = t_id
                    
                    # Initial Kick
                    # Aim slightly ahead
                    lead = t.pos + (t.vel * 1.0)
                    aim_vec = lead - b.pos
                    aim_dir = aim_vec / np.linalg.norm(aim_vec)
                    b.vel = aim_dir * INTERCEPTOR_SPEED
                    
                    blue_missiles.append(b)
                    assigned_targets.add(t_id)
                    shots_this_frame += 1

        # --- 3. PHYSICS UPDATE ---
        
        # Update Red
        active_red = []
        for r in red_rockets:
            res = r.update(0.1)
            if res == "IMPACT_GROUND":
                explosions.append({'p': r.pos.copy(), 'r': 60, 'a': 1.0, 'c': C_RED})
            elif r.active:
                active_red.append(r)
        red_rockets = active_red
        
        # Update Blue (and check kills)
        active_blue = []
        for b in blue_missiles:
            res = b.update(0.1, threats=red_rockets)
            
            hit = False
            
            # Check proximity to assigned target manually if update didn't catch it
            if b.active and b.target_id:
                tgt = next((x for x in red_rockets if id(x) == b.target_id), None)
                if tgt and tgt.active:
                    dist = np.linalg.norm(b.pos - tgt.pos)
                    if dist < INTERCEPT_RADIUS:
                        res = "INTERCEPT"

            if res == "INTERCEPT":
                # Boom
                hit = True
                b.active = False
                # Find target to kill it
                tgt = next((x for x in red_rockets if id(x) == b.target_id), None)
                if tgt:
                    tgt.active = False # Kill Red
                    midpoint = (b.pos + tgt.pos) / 2
                    explosions.append({'p': midpoint, 'r': 140, 'a': 1.0, 'c': C_EXPL})
            
            elif res == "FIZZLE":
                b.active = False
                
            if b.active:
                active_blue.append(b)
                
        blue_missiles = active_blue

        # Explosions
        active_ex = []
        for ex in explosions:
            ex['r'] += 5 
            ex['a'] -= 0.05 
            if ex['a'] > 0: active_ex.append(ex)
        explosions = active_ex

        # --- 4. RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # Camera
        ax.set_xlim(-1500, 1500)
        ax.set_ylim(0, 4000)
        ax.set_facecolor(C_BG)
        
        # City visual
        rect_city = Rectangle((CITY_X[0], 0), 1600, 100, color=C_CITY, alpha=0.3)
        ax.add_patch(rect_city)
        ax.axhline(0, color=C_GROUND, linewidth=10) # Ground line
        
        # Dome Unit
        ax.plot(DOME_POS[0], DOME_POS[1], marker='^', color=C_BLUE, markersize=20, markeredgecolor='white')
        
        # Red Trails
        for r in red_rockets:
            if len(r.history) > 1:
                hx = [h[0] for h in r.history]
                hy = [h[1] for h in r.history]
                ax.plot(hx, hy, color=C_RED, linewidth=2, alpha=0.8)
            ax.plot(r.pos[0], r.pos[1], marker='v', color=C_RED, markersize=6)
            
        # Blue Trails
        for b in blue_missiles:
            if len(b.history) > 1:
                hx = [h[0] for h in b.history]
                hy = [h[1] for h in b.history]
                ax.plot(hx, hy, color=C_BLUE, linewidth=3, alpha=0.9)
            ax.plot(b.pos[0], b.pos[1], marker='o', color='white', markersize=4)

        # Explosions
        for ex in explosions:
            circ = Circle((ex['p'][0], ex['p'][1]), ex['r'], color=ex['c'], alpha=ex['a'])
            ax.add_patch(circ)
            
            if ex['c'] == C_EXPL:
                # Flash ring
                circ2 = Circle((ex['p'][0], ex['p'][1]), ex['r']*1.3, color='white', fill=False, linewidth=3, alpha=ex['a'])
                ax.add_patch(circ2)

        # HUD
        txt_col = 'white'
        stroke = [pe.withStroke(linewidth=3, foreground="black")]
        
        ax.text(0.05, 0.95, "IRON DOME SIMULATION", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', weight='bold', path_effects=stroke)
        ax.text(0.05, 0.92, f"INBOUND: {len(red_rockets)}", transform=ax.transAxes, color=C_RED, fontsize=15, fontname='monospace', path_effects=stroke)
        ax.text(0.05, 0.89, f"INTERCEPTORS: {len(blue_missiles)}", transform=ax.transAxes, color=C_BLUE, fontsize=15, fontname='monospace', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
