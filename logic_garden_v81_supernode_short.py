"""
SOVEREIGN CODE: logic_garden_v71_supernode_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Medical School / Information Overload
VISUAL: The Sage filters the Rain.
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
OUT_DIR = "frames_v71_short"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 71: SUPER-NODE (SHORT FORMAT)")
    fig = plt.figure(figsize=(9, 16), facecolor='#050505')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#050505')

    # DATA RAIN
    # x, y, type (0=Noise, 1=Signal)
    raindrops = []
    
    # THE SAGE
    sage_pos = (0, -12)
    sage_radius = 1.5
    field_radius = 6.0
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(-9, 9)
        ax.set_ylim(-16, 16)
        ax.axis('off')
        
        # 1. SPAWN RAIN (Top)
        if f < TOTAL_FRAMES - 60: # Stop rain at end
            for _ in range(3):
                x = random.uniform(-8, 8)
                y = 18
                is_signal = random.random() < 0.1 # 10% Signal (Rare)
                raindrops.append({'x':x, 'y':y, 's':is_signal, 'active':True})
        
        # 2. PHYSICS
        for r in raindrops:
            if not r['active']: continue
            
            # Gravity
            r['y'] -= 0.4 
            
            # Distance to Sage
            dx = r['x'] - sage_pos[0]
            dy = r['y'] - sage_pos[1]
            dist = np.sqrt(dx*dx + dy*dy)
            
            # FIELD INTERACTION (The Filter)
            if dist < field_radius and r['y'] > sage_pos[1]:
                if r['s']:
                    # Signal: Pulled in (Gold)
                    r['x'] -= dx * 0.1
                    r['y'] -= dy * 0.1
                    if dist < sage_radius:
                        r['active'] = False # Absorbed
                else:
                    # Noise: Deflected (Grey)
                    r['x'] += dx * 0.1 # Push away
                    
            if r['y'] < -18: r['active'] = False

        # 3. RENDER RAIN
        for r in raindrops:
            if not r['active']: continue
            
            if r['s']:
                # Gold Signal
                color = '#FFD700'
                size = 0.4
                alpha = 1.0
            else:
                # Grey Noise
                color = '#444444'
                size = 0.2
                alpha = 0.5
                
            circle = plt.Circle((r['x'], r['y']), size, color=color, alpha=alpha)
            ax.add_patch(circle)

        # 4. RENDER SAGE (The Exocortex)
        # The Filter Ring
        filter_ring = plt.Circle(sage_pos, field_radius, color='#00FFFF', fill=False, linestyle='--', alpha=0.3)
        ax.add_patch(filter_ring)
        
        # The Core
        core = plt.Circle(sage_pos, sage_radius, color='#FFD700', zorder=10)
        ax.add_patch(core)
        
        # HUD TEXT
        ax.text(0, 14, "INPUT: NOISE (90%)", color='#888888', ha='center', fontsize=20, fontfamily='monospace')
        ax.text(0, -15, "OUTPUT: WISDOM", color='#FFD700', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        
        # Label the Field
        ax.text(4, -8, "EXOCORTEX\nFILTER", color='#00FFFF', ha='left', fontsize=12, fontfamily='monospace')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#050505')
        
    plt.close(fig)

if __name__ == "__main__": run()
