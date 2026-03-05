"""
SOVEREIGN CODE: logic_garden_64w_hk_swarm_v3.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: HK Swarm (Retaliation Protocol)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import math
import random

# C64 PALETTE
COLORS = {
    0:[0,0,0], 1:[255,255,255], 2:[136,0,0], 3:[170,255,238], 
    7:[238,238,119], 8:[221,136,85], 10:[255,119,119], 14:[0,136,255]
}

W, H = 110, 196
OUT_DIR = "frames_64w_hk"
os.makedirs(OUT_DIR, exist_ok=True)
GRID = np.zeros((H, W, 3), dtype=np.uint8)

def draw_rect(canvas, x, y, w, h, c):
    x, y, w, h = int(x), int(y), int(w), int(h)
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(W, x+w), min(H, y+h)
    if x1 < x2 and y1 < y2: canvas[y1:y2, x1:x2] = COLORS[c]

class Boid:
    def __init__(self, x, y):
        self.pos = np.array([float(x), float(y)])
        self.vel = np.array([0.0, 0.0])
        self.acc = np.array([0.0, 0.0])
    
    def apply_force(self, force):
        self.acc += force

    def update(self):
        self.vel += self.acc
        speed = np.linalg.norm(self.vel)
        if speed > 3.0: self.vel = (self.vel / speed) * 3.0
        self.pos += self.vel
        self.acc *= 0 
        
        # Walls
        if self.pos[0] < 0: self.vel[0] *= -1; self.pos[0]=0
        if self.pos[0] > W: self.vel[0] *= -1; self.pos[0]=W
        if self.pos[1] < 0: self.vel[1] *= -1; self.pos[1]=0
        if self.pos[1] > 140: self.vel[1] -= 0.5 # Ceil above turrets

def run():
    print("LOGIC GARDEN 64w: HK SWARM V3 (FIRE ENABLED)")
    
    flock = [Boid(random.randint(10,90), random.randint(10,50)) for _ in range(15)]
    
    # ENTITIES
    turrets = [{'x': 30, 'y': 180, 'hp': 100}, {'x': 80, 'y': 180, 'hp': 100}]
    red_bullets = []
    cyan_plasma = []
    explosions = []
    
    for f in range(250):
        GRID[:, :] = COLORS[0]
        
        # 1. TURRETS (Red Team)
        for t in turrets:
            if t['hp'] > 0:
                # Draw Base
                draw_rect(GRID, t['x']-6, t['y'], 12, 10, 2)
                # Draw Barrel (Recoil animation)
                by = t['y']-5
                if f % 10 == 0: by += 2 
                draw_rect(GRID, t['x']-2, by, 4, 6, 2)
                
                # FIRE FLAK (Upward)
                if f % 12 == 0 and random.random() > 0.4:
                     # Spread shot
                     vx = random.uniform(-1, 1)
                     red_bullets.append({'x': t['x'], 'y': by, 'vx': vx, 'vy': -3})
            else:
                # Dead Turret (Ruins)
                draw_rect(GRID, t['x']-6, t['y']+5, 12, 5, 8) # Smoldering Orange

        # 2. RED FLAK UPDATE
        active_rb = []
        for b in red_bullets:
            b['x'] += b['vx']
            b['y'] += b['vy']
            draw_rect(GRID, b['x'], b['y'], 2, 4, 10) # Light Red
            if b['y'] > 0: active_rb.append(b)
        red_bullets = active_rb

        # 3. SWARM LOGIC (Cyan Team)
        # Hive target moves L/R
        hive_target = np.array([W/2 + math.sin(f*0.05)*40, 50 + math.sin(f*0.1)*20])
        
        for b in flock:
            # A. FLOCKING
            force_seek = (hive_target - b.pos) * 0.02
            b.apply_force(force_seek)
            
            for other in flock:
                if other == b: continue
                dist = np.linalg.norm(b.pos - other.pos)
                if dist < 10: # Separation
                    push = (b.pos - other.pos) / (dist*dist + 0.1)
                    b.apply_force(push * 2.5)

            # B. EVASION (Dodge Red Flak)
            for rb in red_bullets:
                bul_pos = np.array([rb['x'], rb['y']])
                dist = np.linalg.norm(b.pos - bul_pos)
                if dist < 20: 
                    evade = (b.pos - bul_pos) / (dist + 0.1)
                    b.apply_force(evade * 2.0)
            
            b.update()
            
            # DRAW HK
            px, py = int(b.pos[0]), int(b.pos[1])
            draw_rect(GRID, px, py, 6, 4, 3) # Cyan Body
            draw_rect(GRID, px+2, py+4, 2, 2, 14) # Engine Glow
            
            # C. ATTACK PROTOCOL (Frame 60+)
            if f > 60 and random.random() < 0.08:
                # Fire Plasma Down
                cyan_plasma.append({'x': px+2, 'y': py+4, 'vy': 6}) # Fast!

        # 4. CYAN PLASMA UPDATE
        active_cp = []
        for p in cyan_plasma:
            p['y'] += p['vy']
            draw_rect(GRID, p['x'], p['y'], 2, 6, 1) # White Core
            draw_rect(GRID, p['x']-1, p['y'], 4, 6, 3) # Cyan Glow
            
            hit = False
            # Check Collision with Turrets
            for t in turrets:
                if t['hp'] > 0:
                    dx = abs(p['x'] - t['x'])
                    dy = abs(p['y'] - t['y'])
                    if dx < 8 and dy < 8:
                        t['hp'] -= 20
                        hit = True
                        # Trigger Explosion Visual
                        explosions.append({'x': t['x'], 'y': t['y'], 'r': 2, 'c': 1})
                        if t['hp'] <= 0:
                             # BIG EXPLOSION
                             explosions.append({'x': t['x'], 'y': t['y'], 'r': 5, 'c': 7})
            
            if p['y'] < H and not hit:
                active_cp.append(p)
        cyan_plasma = active_cp

        # 5. EXPLOSIONS
        active_ex = []
        for ex in explosions:
            ex['r'] += 2 # Expand
            # Draw Circle
            for y in range(H):
                for x in range(W):
                    d = math.sqrt((x-ex['x'])**2 + (y-ex['y'])**2)
                    if abs(d - ex['r']) < 3:
                        draw_rect(GRID, x, y, 1, 1, ex['c'])
            
            # Color Shift White -> Yellow -> Red
            if ex['r'] > 5: ex['c'] = 7
            if ex['r'] > 10: ex['c'] = 2
            
            if ex['r'] < 20: active_ex.append(ex)
        explosions = active_ex

        # RENDER
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
