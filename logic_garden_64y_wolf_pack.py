"""
SOVEREIGN CODE: logic_garden_64y_wolf_pack.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: ASW Triangulation (The Wolf Pack)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import math
import random

COLORS = {
    0:  [0, 0, 0],       # Black
    1:  [255, 255, 255], # White
    2:  [136, 0, 0],     # Red
    3:  [170, 255, 238], # Cyan
    5:  [0, 204, 85],    # Green
    6:  [0, 0, 170],     # Blue
    7:  [238, 238, 119], # Yellow
    11: [51, 51, 51],    # Dark Grey
    14: [0, 136, 255]    # Light Blue
}

W, H = 110, 196
OUT_DIR = "frames_64y_wolf"
os.makedirs(OUT_DIR, exist_ok=True)
GRID = np.zeros((H, W, 3), dtype=np.uint8)

def draw_pixel(canvas, x, y, c):
    if 0 <= x < W and 0 <= y < H: canvas[int(y), int(x)] = COLORS[c]

def draw_rect(canvas, x, y, w, h, c):
    x, y, w, h = int(x), int(y), int(w), int(h)
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(W, x+w), min(H, y+h)
    if x1 < x2 and y1 < y2: canvas[y1:y2, x1:x2] = COLORS[c]

def draw_line(canvas, x0, y0, x1, y1, c):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx = abs(x1 - x0); dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        draw_rect(canvas, x0, y0, 1, 1, c)
        if x0 == x1 and y0 == y1: break
        e2 = 2 * err
        if e2 > -dy: err -= dy; x0 += sx
        if e2 < dx: err += dx; y0 += sy

def run():
    print("LOGIC GARDEN 64y: THE WOLF PACK")
    
    # ENTITIES
    ships = [
        {'x': 20, 'y': 30, 'ping_t': 0},
        {'x': 55, 'y': 25, 'ping_t': 10},
        {'x': 90, 'y': 30, 'ping_t': 20}
    ]
    
    # Submarine (Invisible moving target)
    sub = {'x': 20, 'y': 140, 'vx': 0.5, 'vy': -0.1, 'revealed': False, 'hp': 100}
    
    pings = [] # {x, y, r, owner_idx}
    contacts = [] # {x, y, life}
    
    lock_timer = 0
    depth_charges = []
    
    for f in range(300):
        GRID[:, :] = COLORS[0] # BLACK OCEAN
        
        # 1. DRAW SURFACE
        draw_rect(GRID, 0, 0, W, 35, 6) # Blue surface water
        draw_line(GRID, 0, 35, W, 35, 14) # Water line
        
        # 2. UPDATE SHIPS & PINGS
        for idx, s in enumerate(ships):
            # Draw Ship
            draw_rect(GRID, s['x']-6, s['y'], 12, 5, 11) # Hull
            draw_rect(GRID, s['x']-2, s['y']-4, 4, 4, 11) # Tower
            
            # Emit Ping Logic
            if f % 40 == s['ping_t']:
                pings.append({'x': s['x'], 'y': s['y']+5, 'r': 1, 'id': idx})
                # Visual Flash on ship
                draw_rect(GRID, s['x'], s['y']-8, 1, 10, 5) # Antenna Scan
        
        # 3. MOVE SUB
        if sub['hp'] > 0:
            sub['x'] += sub['vx']
            sub['y'] += sub['vy']
            # Bounds
            if sub['x'] > W-10: sub['vx'] *= -1
            if sub['y'] < 50: sub['vy'] *= -1
            
            # Draw Sub (GHOST MODE - Only visible if 'revealed' is high)
            # We draw it faintly (Dark Grey) to show it exists to the viewer
            draw_rect(GRID, sub['x']-8, sub['y'], 16, 6, 11) # Body
            draw_rect(GRID, sub['x']-2, sub['y']-4, 4, 4, 11) # Conning tower
        else:
            # Wreckage
            draw_rect(GRID, sub['x']-8, sub['y'], 16, 6, 2)
        
        # 4. UPDATE PINGS & DETECT
        active_pings = []
        is_pinged_this_frame = [False, False, False] # Track which ship sees sub
        
        for p in pings:
            p['r'] += 1.5 # Sound speed
            
            # DRAW RING (Only the rim)
            # Optimization: Bresenham Circle or just sparse dots
            # We use sparse dots for "Sonar" feel
            for theta in range(0, 360, 10):
                rad = math.radians(theta)
                px = p['x'] + math.cos(rad) * p['r']
                py = p['y'] + math.sin(rad) * p['r']
                
                # Check bounds
                if py > 35 and 0 <= px < W and py < H:
                    # Draw Green Dot
                    draw_pixel(GRID, px, py, 5)
                    
                    # COLLISION WITH SUB
                    dx = px - sub['x']
                    dy = py - sub['y']
                    if abs(dx) < 8 and abs(dy) < 4:
                        # CONTACT!
                        contacts.append({'x': px, 'y': py, 'life': 5})
                        is_pinged_this_frame[p['id']] = True
            
            if p['r'] < 150:
                active_pings.append(p)
        pings = active_pings
        
        # 5. RENDER CONTACTS (The Reveal)
        hit_count = sum(is_pinged_this_frame)
        
        draw_contacts = []
        for c in contacts:
            draw_rect(GRID, c['x'], c['y'], 2, 2, 2) # Red Blip
            c['life'] -= 1
            if c['life'] > 0: draw_contacts.append(c)
        contacts = draw_contacts
        
        # 6. TRIANGULATION LOGIC
        # If we have recent contacts from multiple angles...
        # Simplified: If 3 ships pinged recently?
        # Actually, let's trigger the "KILL" if the sub is hit by specific pings
        
        if hit_count >= 1:
            draw_rect(GRID, sub['x']-8, sub['y'], 16, 6, 2) # Flash Red
        
        if f > 100 and f % 100 < 20: 
             # Simulate LOCK
             lock_timer = 1
        
        if hit_count >= 2: # 2 Ships have contact
             lock_timer = 20 # Lock window
             
        if lock_timer > 0:
            # DRAW FIRING SOLUTION LINES
            draw_line(GRID, ships[0]['x'], ships[0]['y'], sub['x'], sub['y'], 5)
            draw_line(GRID, ships[1]['x'], ships[1]['y'], sub['x'], sub['y'], 5)
            draw_line(GRID, ships[2]['x'], ships[2]['y'], sub['x'], sub['y'], 5)
            draw_rect(GRID, sub['x']-10, sub['y']-10, 20, 20, 1) # White Box
            
            # DROP CHARGE
            if f % 5 == 0:
                depth_charges.append({'x': sub['x'] + random.randint(-5,5), 'y': 50, 'ty': sub['y']})
            lock_timer -= 1

        # 7. DEPTH CHARGES
        active_dc = []
        for dc in depth_charges:
            dc['y'] += 4 # Fall speed
            draw_rect(GRID, dc['x'], dc['y'], 2, 4, 1) # White canister
            
            if dc['y'] >= dc['ty']:
                # EXPLODE
                sub['hp'] -= 20
                # Draw Shockwave
                r = 10
                for y in range(int(dc['y']-r), int(dc['y']+r)):
                    for x in range(int(dc['x']-r), int(dc['x']+r)):
                        if (x-dc['x'])**2 + (y-dc['y'])**2 < r**2:
                            draw_pixel(GRID, x, y, 1) # White foam
            else:
                active_dc.append(dc)
        depth_charges = active_dc

        # RENDER
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
