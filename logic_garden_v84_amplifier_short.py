"""
SOVEREIGN CODE: logic_garden_v84_amplifier_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Coagulation Cascade / Positive Feedback
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v84_short"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 84: THE AMPLIFIER")
    fig = plt.figure(figsize=(9, 16), facecolor='#000000')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#000000')
    
    particles = [{'x':0.0, 'y':14.0, 'gen':0}] # Patient Zero (Factor XII)
    mesh_active = False
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(-9, 9)
        ax.set_ylim(-16, 16)
        ax.axis('off')
        
        # SPAWN LOGIC (Cascading steps)
        # Every 40 frames, Split existing particles
        if f % 40 == 0 and f < 250 and len(particles) < 500:
            new_p = []
            for p in particles:
                # Split Logic
                offset = 6.0 / (2**p['gen']) # Spread out
                new_p.append({'x': p['x'] - offset, 'y': p['y'] - 4, 'gen': p['gen']+1})
                new_p.append({'x': p['x'] + offset, 'y': p['y'] - 4, 'gen': p['gen']+1})
            particles = new_p

        # MESH ACTIVATION (The clot)
        if f > 280:
            mesh_active = True

        # RENDER
        # Draw Connections
        if not mesh_active:
            for p in particles:
                col = '#FFFF00'
                if p['gen'] == 0: col = '#FF0000' # Trigger
                ax.scatter(p['x'], p['y'], color=col, s=100)
                
                # Draw lines up (implies hierarchy)
                # Simplified visual - just dots falling is cleaner for High Pop
        
        if mesh_active:
            # FIBRIN MESH (White Grid)
            ax.grid(color='white', linewidth=2)
            ax.set_facecolor('#330000') # Background dark red
            # Static particles trapped
            for p in particles:
                ax.scatter(p['x'], p['y'], color='#FF0000', s=150)
            ax.text(0, 0, "THROMBUS\nLOCKED", color='white', ha='center', fontsize=40, weight='bold', fontfamily='monospace')

        # HUD
        ax.text(0, 14, "POSITIVE FEEDBACK", color='white', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        if not mesh_active:
             ax.text(0, -14, f"FACTOR COUNT: {len(particles)}", color='#FFFF00', ha='center', fontsize=20, fontfamily='monospace')
        
        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#000000')
        
    plt.close(fig)

if __name__ == "__main__": run()
