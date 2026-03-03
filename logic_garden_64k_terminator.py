"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v71_terminator_final.py
MODE:   Retro (VIC-II Emulation)
TARGET: T3 Crane Chase (T-850 vs T-X)
STYLE:  "The Intercept" | Orientation Corrected
STATUS: PATCHED (Origin Flip)

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
    [0.53, 0.00, 0.00], # 2: Red
    [0.45, 0.75, 0.79], # 3: Cyan
    [0.55, 0.17, 0.55], # 4: Purple
    [0.37, 0.65, 0.29], # 5: Green
    [0.21, 0.16, 0.47], # 6: Blue
    [0.93, 0.94, 0.46], # 7: Yellow (Crane Body)
    [0.55, 0.31, 0.08], # 8: Orange (Rust/Boom)
    [0.28, 0.20, 0.00], # 9: Brown
    [0.75, 0.42, 0.43], # 10: Light Red
    [0.33, 0.33, 0.33], # 11: Dark Grey (Tires)
    [0.47, 0.47, 0.47], # 12: Grey (Road)
    [0.63, 0.95, 0.61], # 13: Light Green
    [0.42, 0.37, 0.71], # 14: Light Blue (Sky)
    [0.70, 0.70, 0.70]  # 15: Light Grey (Concrete)
])

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 25
TOTAL_FRAMES = FPS * DURATION
W, H = 320, 200

# ENTITIES
# Ground is at Y=160 (0 is Top, 200 is Bottom)
GROUND_Y = 160 

class Crane:
    def __init__(self):
        self.x = 180.0
        self.bp_x = 0.0 # Bump offset
        self.frame_anim = 0
        self.boom_angle = 0.0
        
    def update(self):
        # Bounce slightly
        self.frame_anim += 1
        self.bp_x = np.sin(self.frame_anim * 0.2) * 2.0
        # Swing Boom
        self.boom_angle = np.sin(self.frame_anim * 0.05) * 0.1

class Bike:
    def __init__(self):
        self.x = -50.0 # Starts off screen
        self.y = GROUND_Y
        self.target_x = 100.0
        self.state = "APPROACH"
        self.gun_cooldown = 0
        self.wheelshot = False
        
    def update(self, crane_x, anim_frame):
        # AI Logic
        if self.state == "APPROACH":
            self.x += 1.5 # Catch up
            if self.x >= self.target_x:
                self.state = "ATTACK"
                
        elif self.state == "ATTACK":
            # Match speed (relative 0) plus bobbing
            self.x = self.target_x + np.sin(anim_frame * 0.1) * 5
            
            if self.gun_cooldown <= 0:
                self.wheelshot = True
                self.gun_cooldown = 45 
            else:
                self.wheelshot = False
                self.gun_cooldown -= 1

class Debris:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-8, -4) 
        self.vy = random.uniform(-5, -2) 
        self.life = 60
        self.color = random.choice([11, 12, 1, 2, 7]) 

def draw_circle(buffer, cx, cy, r, c):
    # Safety bounds check
    for y in range(int(cy-r), int(cy+r+1)):
        for x in range(int(cx-r), int(cx+r+1)):
            if 0 <= x < W and 0 <= y < H:
                if (x-cx)**2 + (y-cy)**2 <= r**2:
                    buffer[y, x] = C64[c]

def generate_intercept():
    out_dir = "logic_garden_terminator_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[T-850] GRAVITY RE-ALIGNED. EXECUTING CHASE...")
    
    c = Crane()
    b = Bike()
    debris_list = []
    
    road_stripes = [i * 60 for i in range(10)]
    obstacles = [] 
    next_obstacle = 30
    
    for f in range(TOTAL_FRAMES):
        
        # 1. UPDATE PHYSICS
        c.update()
        b.update(c.x, c.frame_anim)
        
        speed = 8 
        for i in range(len(road_stripes)):
            road_stripes[i] -= speed
            if road_stripes[i] < -50:
                road_stripes[i] = W + 50
        
        next_obstacle -= 1
        if next_obstacle <= 0:
            obstacles.append({'x': W + 50, 'y': GROUND_Y - 10, 'crushed': False})
            next_obstacle = random.randint(40, 90)
            
        for obs in obstacles:
            obs['x'] -= speed
            front_bumper = c.x + 80
            if not obs['crushed'] and obs['x'] < front_bumper:
                obs['crushed'] = True
                for _ in range(10):
                    debris_list.append(Debris(obs['x'], obs['y']))
                    
        obstacles = [o for o in obstacles if o['x'] > -50 and not o['crushed']]
        
        for d in debris_list:
            d.x += d.vx
            d.y += d.vy
            d.vy += 0.4 # Gravity (Positive is Down now)
            d.life -= 1
        debris_list = [d for d in debris_list if d.life > 0]
        
        # 2. RENDER
        buffer = np.zeros((H, W, 3))
        
        # Sky (Top part of buffer is index 0)
        buffer[0:GROUND_Y-20, :] = C64[14] 
        
        # Road (Bottom part of buffer)
        buffer[GROUND_Y-20:H, :] = C64[12]
        
        # Stripes
        for rx in road_stripes:
            if 0 <= rx < W:
                y_stripe = GROUND_Y + 20
                if 0 <= y_stripe < H:
                    start_x = int(np.clip(rx, 0, W))
                    end_x = int(np.clip(rx+40, 0, W))
                    buffer[y_stripe:y_stripe+4, start_x:end_x] = C64[1]
        
        # Draw Obstacles (Cars)
        for obs in obstacles:
            ox, oy = int(obs['x']), int(obs['y'])
            # Car Body
            if 0 < ox < W:
                # With Y=0 at top, y-15 is HIGHER up the screen. Correct.
                buffer[oy-15:oy, ox-20:ox+20] = C64[6] 
                draw_circle(buffer, ox-12, oy, 6, 0)
                draw_circle(buffer, ox+12, oy, 6, 0)

        # Draw Crane
        cx, cy = int(c.x), int(GROUND_Y)
        bounce = int(c.bp_x)
        
        # Wheels
        for off in [-40, 0, 40]:
            draw_circle(buffer, cx+off, cy-15+bounce, 18, 11)
            draw_circle(buffer, cx+off, cy-15+bounce, 8, 12)
            
        # Chassis
        buffer[cy-50+bounce:cy-25+bounce, cx-60:cx+90] = C64[7]
        # Cab
        buffer[cy-60+bounce:cy-25+bounce, cx+60:cx+90] = C64[7]
        buffer[cy-55+bounce:cy-40+bounce, cx+70:cx+85] = C64[3]
        
        # Boom
        bx, by = cx-20, cy-50+bounce
        boom_len = 100
        angle = -0.1 + c.boom_angle
        # Boom Angle pointing LEFT-UP
        # In Y-Down coords, UP is NEGATIVE Y.
        # Angle -0.1 is slightly up. Correct.
        ex = bx + np.cos(angle)*boom_len
        ey = by + np.sin(angle)*boom_len
        
        for k in range(20):
            for t in np.linspace(0, 1, 100):
                px = int(bx*(1-t) + ex*t)
                py = int((by-k)*(1-t) + (ey-k)*t)
                if 0 <= px < W and 0 <= py < H:
                    buffer[py, px] = C64[8]
                    
        # Hook
        hx, hy = int(ex), int(ey-10) # ey-10 is HIGHER
        # Actually Hook hangs DOWN. Down is +Y.
        # So Hook should be ey + 10.
        hx, hy = int(ex), int(ey+10) 
        
        if 0 <= hx < W:
            # Wire down
            buffer[hy:hy+40, hx] = C64[0]
            buffer[hy+40:hy+50, hx-5:hx+5] = C64[0]
            
        # Draw Arnie
        bx, by = int(b.x), int(b.y)
        if bx > -20 and bx < W+20:
            bb = int(np.random.randint(0, 2))
            
            draw_circle(buffer, bx-15, by-10+bb, 9, 0)
            draw_circle(buffer, bx+15, by-10+bb, 9, 0)
            draw_circle(buffer, bx-15, by-10+bb, 4, 15) 
            draw_circle(buffer, bx+15, by-10+bb, 4, 15)
            
            buffer[by-25+bb:by-10+bb, bx-10:bx+10] = C64[11]
            buffer[by-40+bb:by-20+bb, bx-5:bx+10] = C64[0]
            
            draw_circle(buffer, bx+5, by-42+bb, 4, 10) 
            buffer[by-43+bb:by-41+bb, bx+5:bx+9] = C64[0] 
            
            if b.wheelshot:
                draw_circle(buffer, bx+25, by-30+bb, 8, 1) 
                buffer[by-31+bb:by-29+bb, bx:bx+25] = C64[11]
            elif b.gun_cooldown > 30:
                # Gun UP (Vertical)
                buffer[by-45+bb:by-25+bb, bx:bx+4] = C64[11]
            else:
                buffer[by-30+bb:by-28+bb, bx:bx+20] = C64[11]

        # Debris
        for d in debris_list:
            if 0 <= int(d.x) < W and 0 <= int(d.y) < H:
                size = 3
                buffer[int(d.y):int(d.y)+size, int(d.x):int(d.x)+size] = C64[d.color]

        # 3. OVERLAY
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        # FIX: Origin UPPER (0,0 is Top Left)
        ax.imshow(buffer, interpolation='nearest', aspect='auto', origin='upper')
        
        # HUD Data - Y Coordinates Adjusted
        # Top of Screen
        ax.text(W/2, 20, "LOGIC GARDEN 71: THE INTERCEPT", color="#aaaaaa", ha='center', fontfamily='monospace', fontweight='bold', fontsize=15)
        
        # Bottom of Screen
        ax.text(10, H-20, "OBJ: NEUTRALIZE T-X", color="red", fontfamily='monospace', fontweight='bold', fontsize=12)
        dist = abs(c.x - b.x)
        col_dist = "white" if dist > 60 else "red"
        ax.text(10, H-35, f"RANGE: {dist:.1f} M", color=col_dist, fontfamily='monospace', fontweight='bold', fontsize=12)
        
        ax.text(W-10, H-20, "VEL: 120 KPH", color="cyan", ha='right', fontfamily='monospace', fontweight='bold', fontsize=12)
        
        if b.wheelshot:
             ax.text(b.x + 30, b.y - 40, "BANG", color="white", fontfamily='monospace', fontweight='bold', fontsize=14)

        filename = os.path.join(out_dir, f"terminator_{f:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if f % 60 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES}")

if __name__ == "__main__":
    generate_intercept()
