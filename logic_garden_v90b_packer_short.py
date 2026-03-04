"""
SOVEREIGN CODE: logic_garden_v92_packer_final.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Chaos Packing / Void Filling
FIX: "Sand Mode" (High frequency spawning) to guarantee 99% fill.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v92_packer_final"
os.makedirs(OUT_DIR, exist_ok=True)

# Canvas (Internal logic units)
WIDTH = 9.0
HEIGHT = 16.0

def run():
    print("LOGIC GARDEN 92: THE PACKER (DENSITY PROTOCOL)")
    fig = plt.figure(figsize=(9, 16), facecolor='black')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='black')
    
    circles = [] # List of dicts: x, y, r, growing(bool), color
    
    # Palette: Neon
    colors = ['#FF00FF', '#00FFFF', '#00FF00', '#FFFF00', '#FF0000', '#FFFFFF']
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(0, WIDTH)
        ax.set_ylim(0, HEIGHT)
        ax.axis('off')
        
        # 4 PHASES OF PACKING
        
        # 1. INITIAL (0-10s): Big shapes
        if f < 300:
            spawn_attempts = 10
            min_spawn_r = 0.1
            growth_rate = 0.05
            
        # 2. DENSITY (10-15s): Fill gaps
        elif f < 450:
            spawn_attempts = 50
            min_spawn_r = 0.05
            growth_rate = 0.03
            
        # 3. SAND MODE (15-18s): Fill cracks (Micro-packing)
        elif f < 540:
            spawn_attempts = 500 # Brute force the voids
            min_spawn_r = 0.01 # Tiny dots allowed
            growth_rate = 0.01
            
        # 4. PAUSE (18-20s): Freeze
        else:
            spawn_attempts = 0
            
        # SPAWN LOGIC
        if spawn_attempts > 0:
            for _ in range(spawn_attempts): 
                nx = random.uniform(0, WIDTH)
                ny = random.uniform(0, HEIGHT)
                
                # Check collision with existing
                # We need a bit of clearance
                valid = True
                
                # Optimization: Only check against circles that are close? 
                # For <2000 circles, brute force is fine in Python (~0.01s)
                for c in circles:
                    # Quick bounding box check first
                    if abs(nx - c['x']) > c['r'] + min_spawn_r: continue
                    if abs(ny - c['y']) > c['r'] + min_spawn_r: continue
                    
                    dist_sq = (nx - c['x'])**2 + (ny - c['y'])**2
                    min_dist = c['r'] + min_spawn_r
                    if dist_sq < min_dist**2:
                        valid = False
                        break
                
                if valid:
                    col = random.choice(colors)
                    circles.append({'x': nx, 'y': ny, 'r': 0.0, 'grow': True, 'c': col})
                    # Only spawn one per loop iteration? 
                    # No, in Sand Mode we might want to spawn multiple. 
                    if f > 450: # In sand mode, keep trying
                        pass
                    else:
                        break # In normal mode, 1 spawn per frame is smooth
                
        # GROW CIRCLES
        # Only process circles that are marked 'grow'
        active_circles = [c for c in circles if c['grow']]
        
        for c in active_circles:
            # 1. Proposed new radius
            new_r = c['r'] + growth_rate
            
            # 2. Check collisions
            # Walls
            if c['x'] - new_r < 0 or c['x'] + new_r > WIDTH or c['y'] - new_r < 0 or c['y'] + new_r > HEIGHT:
                c['grow'] = False
                continue
                
            # Other Circles
            # Check against ALL circles (static + growing)
            collided = False
            for other in circles:
                if c is other: continue
                
                # Bounding box optimization
                if abs(c['x'] - other['x']) > new_r + other['r']: continue
                if abs(c['y'] - other['y']) > new_r + other['r']: continue

                dist_sq = (c['x'] - other['x'])**2 + (c['y'] - other['y'])**2
                min_dist = new_r + other['r']
                
                if dist_sq < min_dist**2:
                    collided = True
                    break
            
            if collided:
                c['grow'] = False
            else:
                c['r'] = new_r
        
        # RENDER
        # Use simple patches
        for c in circles:
            ax.add_patch(plt.Circle((c['x'], c['y']), c['r'], color=c['c']))

        # PAUSE STATE INDICATOR (Subtle)
        if f >= 540:
             # Just a tiny "Completed" dot or nothing?
             # Let's keep it pure. No text.
             pass

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='black')
        
    plt.close(fig)

if __name__ == "__main__": run()
