"""
SOVEREIGN CODE: logic_garden_v90_packer_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Chaos Packing / Void Filling
ALGO: Circle Packing 
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
OUT_DIR = "frames_v92_packer"
os.makedirs(OUT_DIR, exist_ok=True)

WIDTH = 9
HEIGHT = 16
MAX_R = 3.0

def run():
    print("LOGIC GARDEN 92: THE PACKER")
    fig = plt.figure(figsize=(9, 16), facecolor='black')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='black')
    
    circles = [] # List of dicts: x, y, r, growing(bool), color
    
    # Palette: Neon
    colors = ['#FF00FF', '#00FFFF', '#00FF00', '#FFFF00', '#FF0000']
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(0, WIDTH)
        ax.set_ylim(0, HEIGHT)
        ax.axis('off')
        
        # 1. SPAWN NEW SEEDS (If room)
        # Try N times to find a valid spot
        for _ in range(10): 
            nx = random.uniform(0, WIDTH)
            ny = random.uniform(0, HEIGHT)
            
            valid = True
            for c in circles:
                dist = np.sqrt((nx - c['x'])**2 + (ny - c['y'])**2)
                if dist < c['r'] + 0.05: # Too close / Inside (buffer 0.05)
                    valid = False
                    break
            
            if valid:
                col = random.choice(colors)
                circles.append({'x': nx, 'y': ny, 'r': 0.0, 'grow': True, 'c': col})
                break # Only spawn 1 per cycle? Or more?
                
        # 2. GROW CIRCLES
        for c in circles:
            if c['grow']:
                # Growth step
                if c['r'] < MAX_R:
                    c['r'] += 0.05
                else:
                    c['grow'] = False
                    
                # Collision Check
                # 1. Walls
                if c['x'] - c['r'] < 0 or c['x'] + c['r'] > WIDTH or c['y'] - c['r'] < 0 or c['y'] + c['r'] > HEIGHT:
                    c['grow'] = False
                
                # 2. Other Circles
                if c['grow']:
                    for other in circles:
                        if c == other: continue
                        dist = np.sqrt((c['x'] - other['x'])**2 + (c['y'] - other['y'])**2)
                        if dist < c['r'] + other['r']: # TOUCH!
                            c['grow'] = False
                            other['grow'] = False # Stop both? Usually just the growing one.
                            break
        
        # RENDER
        for c in circles:
            # Filled circle
            ax.add_patch(plt.Circle((c['x'], c['y']), c['r'], color=c['c']))
            # Outline for "Pop"
            # ax.add_patch(plt.Circle((c['x'], c['y']), c['r'], fill=False, edgecolor='white', linewidth=1, alpha=0.5))

        # HUD
        count = len(circles)
        if f % 30 == 0:
             stats = f"OBJECTS: {count}"
        else:
             stats = f"OBJECTS: {count}"
             
        ax.text(WIDTH/2, HEIGHT-1, stats, color='white', ha='center', fontsize=20, fontfamily='monospace',
               bbox=dict(facecolor='black', alpha=0.5))
               
        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='black')
        
    plt.close(fig)

if __name__ == "__main__": run()
