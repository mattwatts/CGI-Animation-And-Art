"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v70_totalwar_swarm.py
MODE:   Retro (VIC-II Emulation)
TARGET: 10-Tank Battle Royale
STYLE:  "Hive Mind" | Blue Swarm vs Red Skirmishers
STATUS: CYAN VICTORY PROBABILITY > 95%

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

# --- 1. THE VIC-II PALETTE ---
C64 = np.array([
    [0.00, 0.00, 0.00], # 0: Black
    [1.00, 1.00, 1.00], # 1: White
    [0.53, 0.00, 0.00], # 2: Red (Horde)
    [0.45, 0.75, 0.79], # 3: Cyan (The Swarm)
    [0.55, 0.17, 0.55], # 4: Purple
    [0.37, 0.65, 0.29], # 5: Green
    [0.21, 0.16, 0.47], # 6: Blue
    [0.93, 0.94, 0.46], # 7: Yellow
    [0.55, 0.31, 0.08], # 8: Orange
    [0.28, 0.20, 0.00], # 9: Brown
    [0.75, 0.42, 0.43], # 10: Light Red
    [0.33, 0.33, 0.33], # 11: Dark Grey
    [0.47, 0.47, 0.47], # 12: Grey
    [0.63, 0.95, 0.61], # 13: Light Green
    [0.42, 0.37, 0.71], # 14: Light Blue
    [0.70, 0.70, 0.70]  # 15: Light Grey
])

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 25
TOTAL_FRAMES = FPS * DURATION
W, H = 320, 200

SPEED_MOVE = 1.8
SPEED_ROT = 0.2
BULLET_SPEED = 5.0
RELOAD_TIME = 25

class Tank:
    def __init__(self, uid, team, x, y):
        self.uid = uid
        self.team = team # 0=Cyan (Swarm), 1=Red (Solo)
        self.x = float(x)
        self.y = float(y)
        self.angle = random.uniform(0, 6.28)
        self.turret_angle = self.angle
        
        self.alive = True
        self.hp = 3
        self.cooldown = random.randint(0, 20)
        self.target = None
        
        # Swarm/Move logic
        self.move_angle = self.angle
        self.timer = 0
        
    def update(self, all_tanks, blue_centroid, primary_target):
        if not self.alive: return False
        
        target_entity = None
        
        # --- TEAM LOGIC SPLIT ---
        
        if self.team == 0:
            # === CYAN HIVE MIND ===
            # 1. Target: Everyone focuses on the PRIMARY TARGET designated by the Hive
            if primary_target and primary_target.alive:
                target_entity = primary_target
            
            # 2. Movement: Boids Logic (Cohesion + Separation + Attack)
            
            # Vector to Target
            tx, ty = (target_entity.x, target_entity.y) if target_entity else (W/2, H/2)
            att_vec = np.array([tx - self.x, ty - self.y])
            norm = np.linalg.norm(att_vec)
            if norm > 0: att_vec /= norm
            
            # Separation (Don't crash into friends)
            sep_vec = np.array([0.0, 0.0])
            count = 0
            for t in all_tanks:
                if t.alive and t.uid != self.uid and t.team == 0:
                    d = np.sqrt((t.x - self.x)**2 + (t.y - self.y)**2)
                    if d < 20: # Personal bubble
                        diff = np.array([self.x - t.x, self.y - t.y])
                        sep_vec += diff / d
                        count += 1
            if count > 0: sep_vec /= count
            
            # Combine Vectors
            # Aggression heavily weighted
            final_vec = att_vec * 1.5 + sep_vec * 2.0
            self.move_angle = np.arctan2(final_vec[1], final_vec[0])
            
        else:
            # === RED SKIRMISH MODE ===
            # Standard "Nearest Neighbor" individual logic
            min_d = 9999
            for t in all_tanks:
                if t.alive and t.team == 0:
                    d = (t.x - self.x)**2 + (t.y - self.y)**2
                    if d < min_d:
                        min_d = d
                        target_entity = t
            
            # Dumb Random Movement / Weak Pursuit
            self.timer -= 1
            if self.timer <= 0:
                self.timer = random.randint(10, 40)
                if target_entity and random.random() < 0.6:
                     self.move_angle = np.arctan2(target_entity.y - self.y, target_entity.x - self.x) + random.uniform(-0.5, 0.5)
                else:
                     self.move_angle += random.uniform(-1.5, 1.5)

        # --- PHYSICS EXECUTION ---
        
        # Turn Body
        diff = (self.move_angle - self.angle + np.pi) % (2*np.pi) - np.pi
        self.angle += np.clip(diff, -SPEED_ROT, SPEED_ROT)
        
        # Move
        nx = self.x + np.cos(self.angle) * SPEED_MOVE
        ny = self.y + np.sin(self.angle) * SPEED_MOVE
        if 5 < nx < W-5 and 5 < ny < H-5:
            self.x = nx; self.y = ny

        # Turret
        will_fire = False
        if target_entity:
            # Aim at Target
            dx = target_entity.x - self.x
            dy = target_entity.y - self.y
            aim = np.arctan2(dy, dx)
            
            diff = (aim - self.turret_angle + np.pi) % (2*np.pi) - np.pi
            self.turret_angle += np.clip(diff, -0.3, 0.3) # Fast turret
            
            # Fire Check
            if abs(diff) < 0.2 and self.cooldown <= 0:
                if self.team == 0: 
                    # Cyan fires faster if locked on
                    self.cooldown = RELOAD_TIME - 5 
                else:
                    self.cooldown = RELOAD_TIME + random.randint(0, 10)
                will_fire = True
        
        self.cooldown -= 1
        return will_fire

class Bullet:
    def __init__(self, x, y, angle, team):
        self.x = float(x); self.y = float(y)
        self.vx = np.cos(angle) * BULLET_SPEED
        self.vy = np.sin(angle) * BULLET_SPEED
        self.team = team
        self.alive = True
        self.life = 50

class Particle:
    def __init__(self, x, y, color, life):
        self.x = x; self.y = y
        self.color = color
        self.life = float(life)
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-1.5, 1.5)

def draw_tank(buffer, t, is_corpse):
    cx, cy = int(t.x), int(t.y)
    col = C64[11] if is_corpse else (C64[3] if t.team == 0 else C64[2])
    
    # Body 8x8
    for y in range(cy-4, cy+5):
        for x in range(cx-4, cx+5):
            if 0 <= x < W and 0 <= y < H: buffer[y, x] = col
            
    if not is_corpse:
        # Turret Vector
        tx = cx + np.cos(t.turret_angle) * 7
        ty = cy + np.sin(t.turret_angle) * 7
        # Line
        for i in range(8):
            lx = int(cx + (tx-cx)*i/8)
            ly = int(cy + (ty-cy)*i/8)
            if 0 <= lx < W and 0 <= ly < H: buffer[ly, lx] = C64[1]

def generate_swarm():
    out_dir = "logic_garden_swarm_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[C64] HIVE MIND ACTIVATED...")
    
    tanks = []
    # Team Cyan (Left, grouped)
    for i in range(5):
        tanks.append(Tank(i, 0, 50, 60 + i*20)) # Line formation start
        
    # Team Red (Right, scattered)
    for i in range(5):
        tanks.append(Tank(i+5, 1, random.randint(W-80, W-20), random.randint(20, H-20)))
        
    bullets = []
    particles = []
    corpses = []
    
    for f in range(TOTAL_FRAMES):
        # 1. HIVE CALCULATION (Strategos Node)
        blue_alive = [t for t in tanks if t.team == 0 and t.alive]
        red_alive = [t for t in tanks if t.team == 1 and t.alive]
        
        blue_centroid = (W/2, H/2)
        priority_target = None
        
        if blue_alive:
            # Calc Center
            avg_x = sum(t.x for t in blue_alive) / len(blue_alive)
            avg_y = sum(t.y for t in blue_alive) / len(blue_alive)
            blue_centroid = (avg_x, avg_y)
            
            # Pick Priority Target (Closest to Swarm Center)
            if red_alive:
                min_d = 99999
                for r in red_alive:
                    d = (r.x - avg_x)**2 + (r.y - avg_y)**2
                    if d < min_d:
                        min_d = d
                        priority_target = r
        
        # 2. UPDATE TANKS
        for t in tanks:
            fired = t.update(tanks, blue_centroid, priority_target)
            if fired:
                # Muzzle flash
                particles.append(Particle(t.x + np.cos(t.turret_angle)*8, t.y + np.sin(t.turret_angle)*8, 1, 5))
                # Spawn Bullet
                bullets.append(Bullet(t.x + np.cos(t.turret_angle)*6, t.y + np.sin(t.turret_angle)*6, t.turret_angle + random.uniform(-0.05,0.05), t.team))

        # 3. UPDATE PROJECTILES
        for b in bullets:
            if not b.alive: continue
            b.x += b.vx; b.y += b.vy
            b.life -= 1
            if b.life < 0 or not (0 < b.x < W and 0 < b.y < H):
                b.alive = False; continue
                
            # Hit Reg
            for t in tanks:
                if t.alive and t.team != b.team:
                    if (b.x - t.x)**2 + (b.y - t.y)**2 < 80:
                        b.alive = False
                        t.hp -= 1
                        particles.append(Particle(b.x, b.y, 7, 10))
                        
                        if t.hp <= 0:
                            t.alive = False
                            corpses.append(t)
                            # Boom
                            for _ in range(20):
                                particles.append(Particle(t.x, t.y, 7, 25)) # Yellow
                                particles.append(Particle(t.x, t.y, 2, 20)) # Red explosion
                            for _ in range(5):
                                particles.append(Particle(t.x, t.y, 11, 40)) # Smoke
                        break
        
        bullets = [b for b in bullets if b.alive]
        
        # Particles
        for p in particles:
            p.x += p.vx; p.y += p.vy
            p.life -= 1
            
        particles = [p for p in particles if p.life > 0]
        
        # 4. RENDER
        buffer = np.zeros((H, W, 3))
        buffer[:] = C64[0] # Black Void
        
        # Corpses
        for c in corpses:
            draw_tank(buffer, c, True)
            
        # Live Tanks
        for t in tanks:
            if t.alive: draw_tank(buffer, t, False)
            
        # Bullets
        for b in bullets:
            if 0 <= int(b.x) < W and 0 <= int(b.y) < H:
                 buffer[int(b.y), int(b.x)] = C64[1]
                 
        # Particles
        for p in particles:
            if 0 <= int(p.x) < W and 0 <= int(p.y) < H:
                c_idx = p.color
                if c_idx == 7 and p.life < 10: c_idx = 2
                buffer[int(p.y), int(p.x)] = C64[c_idx]

        # 5. OVERLAY (Battle Net)
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        ax.imshow(buffer, interpolation='nearest', aspect='auto', origin='lower')
        
        # Target Reticle on Priority Target
        if priority_target and priority_target.alive:
             tx, ty = priority_target.x, priority_target.y
             # Draw bracket
             rect = matplotlib.patches.Rectangle((tx-6, ty-6), 12, 12, linewidth=1, edgecolor='cyan', facecolor='none')
             ax.add_patch(rect)
             ax.text(tx, ty+12, "PRIORITY", color="cyan", ha='center', fontsize=8, fontfamily='monospace', fontweight='bold')

        # Score
        c_count = len([t for t in tanks if t.team == 0 and t.alive])
        r_count = len([t for t in tanks if t.team == 1 and t.alive])
        
        ax.text(10, H-15, f"HIVE: {c_count}", color="cyan", fontfamily='monospace', fontweight='bold', fontsize=15)
        ax.text(W-10, H-15, f"ROGUE: {r_count}", color="red", ha='right', fontfamily='monospace', fontweight='bold', fontsize=15)
        
        if r_count == 0:
            ax.text(W/2, H/2, "SWARM VICTORY", color="cyan", ha='center', fontfamily='monospace', fontweight='bold', fontsize=25)

        filename = os.path.join(out_dir, f"swarm_{f:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if f % 60 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES} | C:{c_count} R:{r_count}")

if __name__ == "__main__":
    generate_swarm()
