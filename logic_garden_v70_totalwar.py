"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v70_totalwar.py
MODE:   Retro (VIC-II Emulation)
TARGET: 10-Tank Battle Royale
STYLE:  "Total War" | 30s | C64 Palette | Sprite Multiplexing

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
    [1.00, 1.00, 1.00], # 1: White (Explosions)
    [0.53, 0.00, 0.00], # 2: Red (Team Horde)
    [0.45, 0.75, 0.79], # 3: Cyan (Team Alliance)
    [0.55, 0.17, 0.55], # 4: Purple
    [0.37, 0.65, 0.29], # 5: Green
    [0.21, 0.16, 0.47], # 6: Blue
    [0.93, 0.94, 0.46], # 7: Yellow (Fire)
    [0.55, 0.31, 0.08], # 8: Orange (Burning)
    [0.28, 0.20, 0.00], # 9: Brown (Dirt)
    [0.75, 0.42, 0.43], # 10: Light Red
    [0.33, 0.33, 0.33], # 11: Dark Grey (Tracks)
    [0.47, 0.47, 0.47], # 12: Grey (Debris)
    [0.63, 0.95, 0.61], # 13: Light Green
    [0.42, 0.37, 0.71], # 14: Light Blue
    [0.70, 0.70, 0.70]  # 15: Light Grey
])

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 30
TOTAL_FRAMES = FPS * DURATION
W, H = 320, 200

# ENTITY CONSTANTS
TANK_SIZE = 8
SPEED_MOVE = 1.5
SPEED_ROT = 0.15
BULLET_SPEED = 4.0
RELOAD_TIME = 30 # Frames

class Tank:
    def __init__(self, uid, team, x, y):
        self.uid = uid
        self.team = team # 0=Cyan, 1=Red
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 6.28) # Body angle
        self.turret_angle = self.angle
        
        self.alive = True
        self.hp = 3
        self.cooldown = random.randint(0, reload_time_var := 20)
        
        # State
        self.target = None
        self.move_timer = 0
        self.move_state = "IDLE" # IDLE, MOVE, TURN
        
    def update(self, tanks, walls):
        if not self.alive: return
        
        # 1. AI: Find Target
        if not self.target or not self.target.alive:
            # Find nearest enemy
            nearest = None
            min_dist = 9999
            for t in tanks:
                if t.alive and t.team != self.team:
                    d = (t.x - self.x)**2 + (t.y - self.y)**2
                    if d < min_dist:
                        min_dist = d
                        nearest = t
            self.target = nearest
            
        # 2. MOVEMENT (Boids-lite / Random Walk)
        # Avoid walls/friends logic is primitive (C64 AI)
        self.move_timer -= 1
        if self.move_timer <= 0:
            self.move_timer = random.randint(20, 60)
            # Pick a direction: Towards enemy or random?
            if self.target and random.random() < 0.7:
                # Flank? No, just drive at them roughly
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                desired = np.arctan2(dy, dx) + random.uniform(-0.5, 0.5)
            else:
                desired = random.uniform(0, 6.28)
            
            # Snap to 8-way for C64 feel? No, float is fine
            self.move_angle = desired
        
        # Execute Move
        # Turn Body
        diff = (self.move_angle - self.angle + np.pi) % (2*np.pi) - np.pi
        self.angle += np.clip(diff, -SPEED_ROT, SPEED_ROT)
        
        # Drive forward collision check
        nx = self.x + np.cos(self.angle) * SPEED_MOVE
        ny = self.y + np.sin(self.angle) * SPEED_MOVE
        
        # Map Boundaries
        if 10 < nx < W-10 and 10 < ny < H-10:
            self.x = nx
            self.y = ny
            
        # 3. TURRET & FIRING
        if self.target:
            # Aim
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            aim = np.arctan2(dy, dx)
            
            diff = (aim - self.turret_angle + np.pi) % (2*np.pi) - np.pi
            self.turret_angle += np.clip(diff, -0.2, 0.2)
            
            # Fire?
            if abs(diff) < 0.3 and self.cooldown <= 0:
                # Shoot
                self.cooldown = RELOAD_TIME + random.randint(0, 10)
                return True # Request Bullet Spawn
                
        self.cooldown -= 1
        return False

class Bullet:
    def __init__(self, x, y, angle, team):
        self.x = x
        self.y = y
        self.dx = np.cos(angle) * BULLET_SPEED
        self.dy = np.sin(angle) * BULLET_SPEED
        self.team = team
        self.alive = True
        self.life = 60 # Range limit

class Particle:
    def __init__(self, x, y, color, life, type_):
        self.x = x
        self.y = y
        self.color = color
        self.life = float(life)
        self.max_life = float(life)
        self.type = type_ # "SMOKE", "FIRE", "DEBRIS"
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

def draw_sprite(buffer, cx, cy, angle, turret, team, is_dead):
    # Draw Tank Sprite 8x8
    cx, cy = int(cx), int(cy)
    
    col = C64[11] if is_dead else (C64[3] if team == 0 else C64[2])
    
    # Body (Box rotated)
    # Simple raster box for performance/style
    # 8x8 block
    for y in range(cy-4, cy+5):
        for x in range(cx-4, cx+5):
            if 0 <= x < W and 0 <= y < H:
                 buffer[y, x] = col
    
    if not is_dead:
        # Turret (Line)
        tx = cx + np.cos(turret) * 6
        ty = cy + np.sin(turret) * 6
        
        # Draw line
        pts = 6
        for i in range(pts):
            lp_x = int(cx + (tx-cx)*i/pts)
            lp_y = int(cy + (ty-cy)*i/pts)
            if 0 <= lp_x < W and 0 <= lp_y < H:
                buffer[lp_y, lp_x] = C64[1] # White barrel

def generate_totalwar():
    out_dir = "logic_garden_totalwar_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[C64] LOADING 'TOTAL WAR'...")
    
    tanks = []
    # Spawn Team Cyan (Left)
    for i in range(5):
        tanks.append(Tank(i, 0, random.randint(20, 50), random.randint(20, H-20)))
    
    # Spawn Team Red (Right)
    for i in range(5):
        tanks.append(Tank(i+5, 1, random.randint(W-50, W-20), random.randint(20, H-20)))
        
    bullets = []
    particles = []
    
    # Arena Scars (Permanent debris)
    scars = []
    
    for f in range(TOTAL_FRAMES):
        # 1. UPDATE
        # Tanks
        for t in tanks:
            if t.update(tanks, []):
                # Fire!
                bx = t.x + np.cos(t.turret_angle)*8
                by = t.y + np.sin(t.turret_angle)*8
                bullets.append(Bullet(bx, by, t.turret_angle + random.uniform(-0.1, 0.1), t.team))
                
        # Bullets
        for b in bullets:
            if not b.alive: continue
            b.x += b.dx; b.y += b.dy
            b.life -= 1
            if b.life <= 0: b.alive = False; continue
            
            if not (0 < b.x < W and 0 < b.y < H):
                b.alive = False; continue
                
            # Hit Check
            for t in tanks:
                if t.alive and t.team != b.team:
                    if (b.x - t.x)**2 + (b.y - t.y)**2 < 81: # Hit radius 9
                        b.alive = False
                        t.hp -= 1
                        # Sparks
                        for _ in range(3):
                            particles.append(Particle(b.x, b.y, 7, 10, "FIRE"))
                        
                        if t.hp <= 0:
                            t.alive = False
                            # BIG EXPLOSION
                            for _ in range(15):
                                particles.append(Particle(t.x, t.y, 7, 30, "FIRE"))
                                particles.append(Particle(t.x, t.y, 1, 15, "SMOKE"))
                            scars.append((int(t.x), int(t.y))) # Crater
                        break
        
        # Cleanup Bullets
        bullets = [b for b in bullets if b.alive]
        
        # Particles
        for p in particles:
            p.x += p.vx; p.y += p.vy
            p.life -= 1
            if p.life < 0: continue
            
        particles = [p for p in particles if p.life > 0]
        
        # 2. RENDER
        buffer = np.zeros((H, W, 3))
        
        # Ground (Black Void)
        buffer[:] = C64[0]
        
        # Dirt/Grid (Sparse)
        # Maybe random specks for texture
        # for _ in range(50):
        #    rx, ry = random.randint(0,W-1), random.randint(0,H-1)
        #    buffer[ry, rx] = C64[9] * 0.5
        
        # Scars (Dead Tanks/Craters)
        for sx, sy in scars:
            if 0 <= sx < W and 0 <= sy < H:
                buffer[sy-2:sy+3, sx-2:sx+3] = C64[11] # Grey Mark
                
        # Scars (Dead Tank Hulls - Persistent)
        for t in tanks:
            if not t.alive:
                draw_sprite(buffer, t.x, t.y, t.angle, t.turret_angle, t.team, True)
                
        # Live Tanks
        for t in tanks:
            if t.alive:
                draw_sprite(buffer, t.x, t.y, t.angle, t.turret_angle, t.team, False)
                
        # Bullets (White/Yellow pixels)
        for b in bullets:
            if 0 <= int(b.x) < W and 0 <= int(b.y) < H:
                buffer[int(b.y), int(b.x)] = C64[1]
                
        # Particles
        for p in particles:
            if 0 <= int(p.x) < W and 0 <= int(p.y) < H:
                # Color based on type/life
                c = C64[p.color]
                if p.type == "FIRE" and p.life < 10: c = C64[2] # Fade to red
                if p.type == "SMOKE": c = C64[12]
                buffer[int(p.y), int(p.x)] = c

        # 3. OVERLAY
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        ax.imshow(buffer, interpolation='nearest', aspect='auto', origin='lower')
        
        # HUD
        c_alive = sum(1 for t in tanks if t.team == 0 and t.alive)
        r_alive = sum(1 for t in tanks if t.team == 1 and t.alive)
        
        ax.text(10, H-15, f"CYAN: {c_alive}", color="#73bfe9", fontfamily='monospace', fontweight='bold', fontsize=15)
        ax.text(W-10, H-15, f"RED: {r_alive}", color="#880000", ha='right', fontfamily='monospace', fontweight='bold', fontsize=15)
        
        if c_alive == 0 and r_alive > 0:
            ax.text(W/2, H/2, "RED SURVIVES", color="red", ha='center', fontfamily='monospace', fontweight='bold', fontsize=25)
        elif r_alive == 0 and c_alive > 0:
            ax.text(W/2, H/2, "CYAN SURVIVES", color="cyan", ha='center', fontfamily='monospace', fontweight='bold', fontsize=25)
        elif r_alive == 0 and c_alive == 0:
            ax.text(W/2, H/2, "MUTUAL DESTRUCTION", color="grey", ha='center', fontfamily='monospace', fontweight='bold', fontsize=20)
            
        filename = os.path.join(out_dir, f"totalwar_{f:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if f % 60 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES} | C:{c_alive} R:{r_alive}")

if __name__ == "__main__":
    generate_totalwar()
