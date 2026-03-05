"""
SOVEREIGN CODE: logic_garden_v96_search_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: The Dark Forest / King Tut / Signal Detection
VISUAL: Radar Sweep & Discovery
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
OUT_DIR = "frames_v96_search"
os.makedirs(OUT_DIR, exist_ok=True)

# Canvas
W, H = 9, 16 

def run():
    print("LOGIC GARDEN 96: THE GREAT SEARCH")
    fig = plt.figure(figsize=(9, 16), facecolor='black')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='black')
    
    # THE HIDDEN TRUTH
    # A single point in the dark
    target_x = 4.5
    target_y = 6.0 # Lower middle
    
    # SCANNER POSITION (Moves Top to Bottom)
    scan_y = 16.0
    scan_speed = 0.15 
    
    found = False
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 16)
        ax.axis('off')
        
        # SCANNER LOGIC
        # Moves down. Resets if misses.
        scan_y -= scan_speed
        
        if scan_y < 0:
            scan_y = 16.0 # Reset sweep
            
        # Draw Scanner Line
        # Green Laser
        ax.plot([0, 9], [scan_y, scan_y], color='#00FF00', linewidth=2, alpha=0.8)
        # Trailing fade?
        ax.fill_between([0, 9], [scan_y, scan_y], [scan_y+1, scan_y+1], color='#00FF00', alpha=0.1)
        
        # NOISE (The distraction)
        # Random grey dots that appear and disappear
        np.random.seed(f) 
        noise_x = np.random.uniform(0, 9, 20)
        noise_y = np.random.uniform(0, 16, 20)
        ax.scatter(noise_x, noise_y, c='#222222', s=10)
        
        # THE TARGET
        # It's hidden unless scan hits it AND we are in the final phase
        
        # TIMING:
        # 0-12s: Miss Phase. We sweep past it.
        # 12-14s: "CALIBRATING..." Text
        # 14s+: Hit Phase.
        
        if f > 420: # 14 seconds
            # DETECTION LOGIC
            # If scan line is close to target_y
            if abs(scan_y - target_y) < 0.2:
                found = True
                
        # VISUALIZING THE TARGET
        if found:
            # EXPLOSION
            # Gold Radial Burst
            
            # Draw the Source
            ax.scatter(target_x, target_y, c='#FFD700', s=300, marker='*', zorder=20)
            
            # Rings
            idx = (f % 20) * 0.5
            c1 = plt.Circle((target_x, target_y), idx, color='#FFD700', fill=False, linewidth=2)
            c2 = plt.Circle((target_x, target_y), idx*2, color='#FFD700', fill=False, linewidth=1)
            ax.add_patch(c1)
            ax.add_patch(c2)
            
            # Text
            ax.text(W/2, H/2 + 2, "SIGNAL LOCK", color='#FFD700', ha='center', fontsize=40, weight='bold', fontfamily='monospace',
                   bbox=dict(facecolor='black', edgecolor='#FFD700'))
                   
            # Freeze scanner on target?
            scan_y = target_y 
            
        else:
            # Just hidden faint dot? 
            # Hint at it
            if f % 60 < 10: # Blinking very faintly
                ax.scatter(target_x, target_y, c='#111111', s=50) # Barely visible
                
        # HUD STATUS
        status = "SCANNING..."
        col = "#00FF00"
        
        if f > 360 and f < 420:
             status = "CALIBRATING FILTER..."
             col = "#FFFF00"
        elif found:
             status = "TARGET ACQUIRED"
             col = "#FFD700"
             
        ax.text(W/2, 1, status, color=col, ha='center', fontsize=20, fontfamily='monospace')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='black')
        
    plt.close(fig)

if __name__ == "__main__": run()
